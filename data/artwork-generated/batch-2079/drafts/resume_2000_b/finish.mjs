import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import sharp from 'sharp';
const [batch,slug,source,notes]=process.argv.slice(2),base=`data/artwork-generated/batch-${batch}`;
const read=p=>JSON.parse(fs.readFileSync(p)),write=(p,v)=>{fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,JSON.stringify(v,null,2)+'\n')},hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const rp=`${base}/${slug}.json`,old=fs.existsSync(rp)?read(rp):null;
const sp=batch==='2079'?`${base}/drafts/resume_2000_b/${slug}.json`:`${base}/${slug}.draft.json`;
const spec=read(sp),ledger=read(`data/artwork-batch-${batch}.json`),item=ledger.items.find(i=>i.slug===slug);
if(!item)throw new Error('not in assigned ledger');
let history=old?.rejected_attempts||[],failures=old?.generation_failures||[];
if(old){
 if(old.status!=='needs-correction')throw new Error(`existing ${old.status}`);
 if(hash(old.original_file)!==old.native_sha256)throw new Error('old hash mismatch');
 let n=1;while(fs.existsSync(`${base}/rejected/${slug}-attempt-${String(n).padStart(2,'0')}.json`))n++;
 const stem=`${base}/rejected/${slug}-attempt-${String(n).padStart(2,'0')}`;
 fs.mkdirSync(path.dirname(stem),{recursive:true});fs.copyFileSync(old.original_file,stem+'.png');
 const reason=old.correction_notes;
 const rejected={original_file:stem+'.png',receipt_file:stem+'.json',native_sha256:old.native_sha256,reason};
 write(stem+'.json',{...old,...rejected,original_source_file:old.original_file,archived_at:new Date().toISOString()});
 history=[...history,rejected];
}
const target=`${base}/originals/${slug}.png`;fs.mkdirSync(path.dirname(target),{recursive:true});fs.copyFileSync(source,target);
const sha=hash(target),meta=await sharp(target).metadata(),now=new Date().toISOString();
const r={...old,...spec,batch:Number(batch),worker:'codex',worker_agent:'resume_2000_b',subagent_model:'gpt-6.1-sol',subagent_reasoning_effort:'high',tool:'OpenAI built-in image_gen',image_model:'tidak dilaporkan alat',status:'awaiting-independent-review',review_path:item.review_path,rationale:ledger.user_policy.intent,generated_file:source,generated_at:now,original_file:target,native_sha256:sha,width:meta.width,height:meta.height,rejected_attempts:history,generation_failures:failures,visual_review:{reviewer:'codex',verdict:'pass',notes,limitations:[],native_sha256:sha,reviewed_at:now}};
for(const k of ['root_visual_review','independent_visual_review','correction_notes'])delete r[k];
write(rp,r);fs.mkdirSync(`${base}/drafts/resume_2000_b`,{recursive:true});await sharp(target).resize(200,200).png().toFile(`${base}/drafts/resume_2000_b/${slug}-200.png`);console.log(JSON.stringify({slug,receipt:rp,path:target,sha,width:meta.width,height:meta.height}));
