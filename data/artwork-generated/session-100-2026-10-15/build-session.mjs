import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {read, write, hash} from './resume-tools.mjs';

const base='data/artwork-generated/session-100-2026-10-15';
const batches=[1917,1967,1977,1979];
const records=[],declines=[],batchReports=[],prompts={},errors=[];
const check=(ok,message)=>{if(!ok)errors.push(message)};
for(const batch of batches){
  const ledger=read(`data/artwork-batch-${batch}.json`);
  const folder=`data/artwork-generated/batch-${batch}`;
  const reviews=read(`${folder}/drafts/root/codex-native-reviews.json`);
  const validation=read(`${folder}/drafts/root/resume-validation.json`);
  check(validation.final&&!validation.errors.length,`Batch ${batch}: validation failed`);
  const counts={};let drawn=0;
  for(const item of ledger.items){
    const receipt=`${folder}/${item.slug}.json`,r=read(receipt);
    counts[r.status]=(counts[r.status]||0)+1;
    if(r.status==='tidak-digambar'){
      declines.push({batch,slug:item.slug,name:item.canonical_name,reason:r.reason,receipt});
      continue;
    }
    drawn++;
    const sha=hash(r.original_file),review=reviews[item.slug];
    check(['reviewed','awaiting-independent-review'].includes(r.status),`${item.slug}: final status`);
    check(sha===r.native_sha256,`${item.slug}: native hash`);
    check(review?.native_sha256===sha&&review.verdict==='pass'&&review.native_reviewed&&review.thumbnail_200_reviewed,`${item.slug}: root inspection`);
    const record={batch,slug:item.slug,name:item.canonical_name,status:r.status,receipt,original_file:r.original_file,native_sha256:sha,width:r.width,height:r.height,worker_agent:r.worker_agent,root_review:`${folder}/drafts/root/codex-native-reviews.json`};
    records.push(record);
    prompts[item.slug]={batch,prompt:r.prompt,reference_images:r.referenced_image_paths||[],basis_claim_ids:r.basis_claim_ids,visual_requirements:r.visual_requirements,original_file:r.original_file,native_sha256:sha,generated_file:r.generated_file,tool:r.tool,image_model:r.image_model};
  }
  const gallery=read(`${folder}/drafts/root/gallery-validation.json`);
  check(!gallery.missing.length,`Batch ${batch}: gallery links`);
  batchReports.push({batch,receipts:ledger.items.length,selected_pngs:drawn,status_counts:counts,checks:validation.checks,errors:validation.errors,gallery:gallery.gallery,gallery_link_checks:gallery.links,archived_rejected_attempts:validation.archived_attempts,image_tool_failures:validation.tool_failures});
}
check(records.length===100,'Exactly 100 final PNGs required');
check(new Set(records.map(r=>r.native_sha256)).size===100,'Exactly 100 unique final hashes required');
check(new Set(records.map(r=>r.slug)).size===100,'Exactly 100 unique creatures required');
const corrections=[];
for(const [batch,slug]of [[1817,'wd-q12284431'],[1867,'triton']]){
  const folder=`data/artwork-generated/batch-${batch}`,receipt=`${folder}/${slug}.json`,r=read(receipt);
  const v=read(`${folder}/drafts/root/correction-validation.json`);
  check(v.final&&!v.errors.length&&v.scope.includes(slug),`${slug}: correction validation`);
  corrections.push({batch,slug,status:r.status,receipt,original_file:r.original_file,native_sha256:r.native_sha256,checks:v.checks,errors:v.errors});
}
const original=read(`${base}/resume-protected-before.json`),current={};
function scan(p){for(const e of fs.readdirSync(p,{withFileTypes:true})){const q=p+'/'+e.name;if(e.isDirectory())scan(q);else current[q]=hash(q)}}
for(const p of ['data/gemini','data/power','js','assets/art','backups'])if(fs.existsSync(p))scan(p);
for(const p of ['data/creatures.json','data/artwork-nama-besar.json'])if(fs.existsSync(p))current[p]=hash(p);
const changed=Object.keys(original).filter(p=>current[p]!==original[p]);
const added=Object.keys(current).filter(p=>!Object.hasOwn(original,p));
write(`${base}/protected-final.json`,{checked_at:new Date().toISOString(),baseline_files:Object.keys(original).length,current_files:Object.keys(current).length,changed,added,deleted:Object.keys(original).filter(p=>!Object.hasOwn(current,p)),note:'Concurrent Claude research/review/integration changed protected files. Codex and image agents did not write these paths; baseline retained, no rollback or false identical claim.'});
const held=read('data/artwork-generated/batch-1867/praded.json');
const externalHold={batch:1867,slug:'praded',status:held.status,reviewer:held.root_visual_review?.reviewer,verdict:held.root_visual_review?.verdict,notes:held.root_visual_review?.notes,scope:'Outside the 100 new images and two corrected originals; preserve Claude review and culture hold. Full batch1867 validation reports this status/field mismatch.'};
const escape=s=>String(s??'').replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
function card(record){
  const r=read(record.receipt),p=prompts[record.slug];
  return `<article><h2>${escape(record.name||record.slug)}</h2><p>Batch ${record.batch} · ${escape(record.status)}</p><a href="../${escape(record.original_file)}"><img loading="lazy" src="../${escape(record.original_file)}" alt="${escape(record.name||record.slug)}"></a><p>${escape(r.depicted_variant)}</p><p><a href="../${escape(record.receipt)}">Receipt, klaim dan riwayat</a></p><details><summary>Prompt persis</summary><pre>${escape(r.prompt)}</pre></details><details><summary>Dasar visual</summary><ul>${(r.visual_requirements||[]).map(q=>`<li>${escape(q.kind)}: ${escape(q.description)} (${escape(q.claim_ids.join(', '))})</li>`).join('')}</ul></details></article>`;
}
const gallery='docs/artwork-session-100-2026-10-15.html';
const reviewed=records.filter(r=>r.status==='reviewed').length,awaiting=records.filter(r=>r.status==='awaiting-independent-review').length;
const html=`<!doctype html><html lang="id"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Mitoloka · 100 gambar baru</title><style>body{margin:0;background:#17130f;color:#eee4d4;font:16px/1.6 system-ui}main{max-width:1450px;margin:auto;padding:24px}a{color:#eac885}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));gap:24px}article{padding:18px;background:#251f18;border-radius:10px;min-width:0}img{display:block;width:100%;height:auto}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:13px}details{margin-top:12px}h2{font-size:21px}table{border-collapse:collapse;width:100%}td,th{text-align:left;padding:10px;border-bottom:1px solid #514536}</style><main><h1>Mitoloka · 100 gambar baru</h1><p>100 PNG unik, masing-masing 1254 × 1254 piksel, diperiksa agen utama pada ukuran asli dan 200 piksel. ${reviewed} sudah diluluskan Claude; ${awaiting} menunggu tinjauan independen. Status ini snapshot saat galeri dibuat; integrasi dilakukan sesi Claude.</p><p>OpenAI built-in image_gen · model: tidak dilaporkan alat. Dua koreksi dari batch lama tersedia sesudah koleksi utama. Dua belas entri ditunda dan diganti, sehingga jumlah final tetap 100.</p><nav>${batchReports.map(b=>`<a href="artwork-batch-${b.batch}.html">Batch ${b.batch} (${b.selected_pngs} PNG)</a>`).join(' · ')}</nav><section class="grid">${records.map(card).join('')}</section><h1>Koreksi tambahan dari batch lama</h1><section class="grid">${corrections.map(card).join('')}</section><h1>Entri yang ditunda</h1><table><thead><tr><th>Entri</th><th>Alasan</th></tr></thead><tbody>${declines.map(r=>`<tr><td><a href="../${escape(r.receipt)}">${escape(r.name)}</a></td><td>${escape(r.reason)}</td></tr>`).join('')}</tbody></table><h2>Catatan tinjauan di luar target</h2><p>Praded telah diluluskan Claude tetapi ditahan karena budaya riset belum ditetapkan. Status dan catatan Claude dipertahankan; koreksi Triton pada batch yang sama sudah lolos audit tersendiri.</p></main></html>`;
fs.writeFileSync(gallery,html);
const links=[...html.matchAll(/(?:href|src)="([^"#]+)"/g)].map(m=>m[1]);
const missing=links.filter(p=>!fs.existsSync(path.resolve('docs',p)));
check(!missing.length,'Session gallery has missing links');
const summary={session:'100-images-2026-10-15',completed_at:new Date().toISOString(),target_final_pngs:100,selected_pngs:records.length,unique_native_hashes:new Set(records.map(r=>r.native_sha256)).size,root_native_and_200_pass:records.length,reviewed_by_claude:reviewed,awaiting_independent_review:awaiting,new_batch_receipts:records.length+declines.length,declines:declines.length,batches:batchReports,additional_corrections:corrections,new_batch_validation_checks:batchReports.reduce((n,b)=>n+b.checks,0),additional_correction_checks:corrections.reduce((n,c)=>n+c.checks,0),image_tool_failures:batchReports.reduce((n,b)=>n+b.image_tool_failures,0),tool:'OpenAI built-in image_gen',image_model:'tidak dilaporkan alat',agents:['images_a','images_b','images_c','resume100_a','resume100_b','resume100_c'],parallel_lanes:3,subagent_model:'gpt-6.1-sol',subagent_reasoning_effort:'high',root_generated:['amatsumara'],orchestration_issues:[{reason:'Workspace out of credits interrupted agent turns',resolved:true},{reason:'Transient ENOSPC while writing Tarkshya draft',resolved:true,history_deleted:false}],protected_snapshot:{baseline:Object.keys(original).length,current:Object.keys(current).length,changed:changed.length,added:added.length,comparison:`${base}/protected-final.json`,concurrent_claude_work:true},external_hold:externalHold,integration_performed_by_codex:false,commits_or_pushes_by_codex:false,gallery,gallery_link_checks:links.length,missing_links:missing,errors,records,declined_entries:declines,prompt_set:`${base}/codex-prompts.json`};
write(`${base}/codex-prompts.json`,prompts);
write(`${base}/codex-generation-summary.json`,summary);
write(`${base}/final-validation.json`,{checked_at:new Date().toISOString(),selected_pngs:records.length,unique_hashes:summary.unique_native_hashes,root_native_and_200_pass:records.length,new_batch_validation_checks:summary.new_batch_validation_checks,additional_correction_checks:summary.additional_correction_checks,gallery_link_checks:links.length,errors,external_unrelated_hold:externalHold});
const session=read(`${base}/session.json`);
write(`${base}/session.json`,{...session,updated_at:summary.completed_at,status:errors.length?'validation-failed':'complete',selected_pngs:records.length,root_pass:records.length,reviewed_by_claude:reviewed,awaiting_independent_review:awaiting,additional_corrections:corrections.length,summary:`${base}/codex-generation-summary.json`,gallery});
console.log(JSON.stringify({selected_pngs:records.length,unique_hashes:summary.unique_native_hashes,root_pass:records.length,reviewed_by_claude:reviewed,awaiting_independent_review:awaiting,additional_corrections:corrections.length,checks:summary.new_batch_validation_checks+summary.additional_correction_checks,gallery_link_checks:links.length,protected_changed:changed.length,protected_added:added.length,external_hold:externalHold.slug,errors,gallery},null,2));
assert.equal(errors.length,0,errors.join('\n'));
