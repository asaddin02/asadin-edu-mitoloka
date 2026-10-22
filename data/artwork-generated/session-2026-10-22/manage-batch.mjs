import fs from 'node:fs';
import path from 'node:path';
import sharp from 'sharp';
import {isDeepStrictEqual} from 'node:util';
import {computeFillStatus} from '../../../scripts/gemini/fill-lib.mjs';
import {read,write,hash} from './resume-tools.mjs';
const [command,number,...args]=process.argv.slice(2);
const batch=Number(number),base=`data/artwork-generated/batch-${batch}`;
const ledgerPath=`data/artwork-batch-${batch}.json`, ledger=read(ledgerPath);
const regPath=`${base}/drafts/root/codex-native-reviews.json`;
const reviews=fs.existsSync(regPath)?read(regPath):{};
const onlyArg=args.find(a=>a.startsWith('--only='));
const only=onlyArg?new Set(onlyArg.slice(7).split(',')):null;
const pairs=ledger.items.filter(i=>!only||only.has(i.slug)).map(item=>{const p=`${base}/${item.slug}.json`;return {item,p,r:fs.existsSync(p)?read(p):null}});
if(command==='pending-review'){
  const list=pairs.filter(({item,r})=>r?.status==='awaiting-independent-review'&&r.original_file&&fs.existsSync(r.original_file)&&reviews[item.slug]?.native_sha256!==r.native_sha256).slice(0,Number(args[0]||4));
  const tiles=[];
  for(const [{item,r},i]of list.map((p,i)=>[p,i])){
    const thumb=`${base}/drafts/root/${item.slug}-200.png`;
    fs.mkdirSync(path.dirname(thumb),{recursive:true});
    await sharp(r.original_file).resize(200,200).png().toFile(thumb);
    tiles.push({input:fs.readFileSync(thumb),left:i*200,top:0});
    const ids=new Set(r.basis_claim_ids);
    console.log(JSON.stringify({slug:item.slug,name:item.canonical_name,original:r.original_file,hash:r.native_sha256,requirements:r.visual_requirements,choices:r.artistic_choices,claims:item.research.claims.filter(c=>ids.has(c.id)).map(c=>({id:c.id,statement:c.statement.en||c.statement}))}));
  }
  write(`${base}/drafts/root/pending-review.json`,list.map(p=>p.item.slug));
  if(tiles.length)await sharp({create:{width:tiles.length*200,height:200,channels:3,background:'#17130f'}}).composite(tiles).png().toFile(`${base}/drafts/root/pending-review-200.png`);
  console.log('PENDING',list.map(p=>p.item.slug).join(','));
}
if(command==='sync'){
  const counts={};
  for(const {item,p,r}of pairs){
    if(!r)continue;
    counts[r.status]=(counts[r.status]||0)+1;
    if(['awaiting-independent-review','tidak-digambar','needs-correction'].includes(r.status)){
      item.status=r.status; item.receipt_path=p;
      if(r.status==='tidak-digambar'){
        item.reason=r.reason;
        for(const k of ['original_file','native_sha256'])delete item[k];
      } else for(const k of ['original_file','native_sha256'])item[k]=r[k];
    }
  }
  ledger.generation_complete=pairs.every(p=>p.r!==null);
  ledger.generation_completed_at=ledger.generation_complete?(ledger.generation_completed_at||new Date().toISOString()):null;
  ledger.generation_status_counts=counts;
  // Preserve integration status/completion fields owned by Claude.
  if(!ledger.items.some(i=>i.status==='complete'))ledger.status=ledger.generation_complete?'awaiting-independent-review':'in-progress';
  write(ledgerPath,ledger);
  console.log(JSON.stringify({batch,counts,pending:pairs.filter(p=>!p.r).map(p=>p.item.slug)},null,2));
}
if(command==='validate'){
  const final=args.includes('--final'),errors=[],pending=[],notReviewed=[],sourceChanges=[];let checks=0,drawn=0,declined=0,archived=0,failures=0;
  const check=(v,n)=>{checks++;if(!v)errors.push(n)};
  const {entries,status}=await computeFillStatus(read('data/creatures.json'));
  for(const {item,p,r}of pairs){
    const s=item.slug;
    if(!r){pending.push(s);continue;}
    check(r.slug===s&&r.batch===batch,`${s}: identity`);
    check(r.worker==='codex'&&r.tool==='OpenAI built-in image_gen'&&!!r.image_model,`${s}: provenance`);
    check(r.review_path===item.review_path&&r.rationale===ledger.user_policy.intent,`${s}: source and policy`);
    const claims=new Map(item.research.claims.map(c=>[c.id,c]));
    const current=new Map((entries.get(s)?.claims||[]).map(c=>[c.id,c]));
    check(['lengkap-informasi','lengkap-bergambar'].includes(status[s]?.status),`${s}: current eligible research`);
    for(const id of r.basis_claim_ids||[]){
      check(claims.has(id),`${s}: documented basis ${id}`);
      check(current.has(id)&&isDeepStrictEqual(current.get(id).statement,claims.get(id).statement),`${s}: current source statement ${id}`);
    }
    if(!isDeepStrictEqual(entries.get(s),item.research))sourceChanges.push(s);
    check(Array.isArray(r.generation_failures)&&Array.isArray(r.rejected_attempts),`${s}: history arrays`);
    failures+=(r.generation_failures||[]).length;
    for(const a of r.rejected_attempts||[]){
      archived++;
      check(fs.existsSync(a.original_file)&&fs.existsSync(a.receipt_file),`${s}: archive files`);
      if(fs.existsSync(a.original_file)&&fs.existsSync(a.receipt_file)){
        const ar=read(a.receipt_file);
        check(hash(a.original_file)===a.native_sha256&&ar.native_sha256===a.native_sha256,`${s}: rejected hash`);
        check(!!ar.prompt&&ar.reason===a.reason,`${s}: rejected prompt and reason`);
        check(!!ar.generated_file&&fs.existsSync(ar.generated_file)&&hash(ar.generated_file)===a.native_sha256,`${s}: rejected generated provenance`);
      }
    }
    if(r.status==='tidak-digambar'){declined++;check(!!r.reason&&item.status===r.status&&item.receipt_path===p,`${s}: decline`);continue;}
    drawn++;
    check(r.status==='awaiting-independent-review'||r.status==='reviewed',`${s}: final status ${r.status}`);
    check(!!r.prompt&&!!r.generated_at&&!!r.aura&&!!r.depicted_variant,`${s}: presentation metadata`);
    if(r.status==='awaiting-independent-review')for(const k of ['root_visual_review','independent_visual_review','correction_notes'])check(!Object.hasOwn(r,k),`${s}: no independent-review field ${k}`);
    check(r.visual_requirements?.length>0&&r.artistic_choices?.length>0,`${s}: visual requirements`);
    for(const req of r.visual_requirements||[]){check(['anatomy','effect','setting'].includes(req.kind)&&!!req.description&&req.claim_ids?.length>0,`${s}: requirement schema`);for(const id of req.claim_ids||[])check(claims.has(id)&&r.basis_claim_ids.includes(id),`${s}: requirement basis ${id}`);}
    check(!!r.original_file&&fs.existsSync(r.original_file),`${s}: original exists`);
    if(r.original_file&&fs.existsSync(r.original_file)){
      const sha=hash(r.original_file),m=await sharp(r.original_file).metadata();
      check(sha===r.native_sha256&&m.width===r.width&&m.height===r.height&&m.width===m.height&&m.width>=1024&&m.format==='png',`${s}: native PNG/hash/dimensions`);
      check(!!r.generated_file&&fs.existsSync(r.generated_file)&&hash(r.generated_file)===sha,`${s}: selected generated provenance`);
      check(r.visual_review?.native_sha256===sha&&r.visual_review.reviewer==='codex'&&r.visual_review.verdict==='pass',`${s}: author visual review`);
      const rev=reviews[s];
      if(!rev||rev.native_sha256!==sha)notReviewed.push(s);
      else{
        check(rev.native_reviewed&&rev.thumbnail_200_reviewed&&fs.existsSync(rev.thumbnail_path),`${s}: root native and 200px viewed`);
        if(r.status==='awaiting-independent-review')check(rev.verdict==='pass'&&rev.sangar_checks?.length===7&&rev.sangar_checks.every(Boolean),`${s}: root seven Sangar checks`);
      }
      if(r.status==='awaiting-independent-review')check(item.native_sha256===sha&&item.original_file===r.original_file&&item.receipt_path===p&&item.status===r.status,`${s}: synchronized ledger`);
    }
  }
  if(final){check(!pending.length,'All receipts exist');check(!notReviewed.length,'All selected PNGs observed by root');check(ledger.generation_complete===true,'Generation complete flag');}
  const result={checked_at:new Date().toISOString(),batch,scope:only?[...only]:'whole-batch',final,checks,errors,drawn,declined,pending,notRootReviewed:notReviewed,archived_attempts:archived,tool_failures:failures,external_research_metadata_changed:sourceChanges,integration_performed:false};
  write(`${base}/drafts/root/${only?'correction-validation':'resume-validation'}${final?'':'-progress'}.json`,result);console.log(JSON.stringify(result,null,2));process.exitCode=errors.length?1:0;
}
