import fs from 'node:fs';
import path from 'node:path';
import {read,write,hash} from './resume-tools.mjs';
const base='data/artwork-generated/session-2000-2026-10-16',s=read(base+'/session.json');
const records=[],declines=[],prompts={},errors=[];
for(const batch of s.batches){
 const ledger=read(`data/artwork-batch-${batch}.json`),folder=`data/artwork-generated/batch-${batch}`;
 const registry=fs.existsSync(folder+'/drafts/root/codex-native-reviews.json')?read(folder+'/drafts/root/codex-native-reviews.json'):{};
 for(const item of ledger.items){
  const receipt=folder+'/'+item.slug+'.json';if(!fs.existsSync(receipt))continue;
  const r=read(receipt);
  if(r.status==='tidak-digambar'){declines.push({batch,slug:r.slug,reason:r.reason,receipt});continue;}
  if(!r.original_file||!fs.existsSync(r.original_file)){errors.push(r.slug+':missing PNG');continue;}
  const sha=hash(r.original_file),codex=registry[r.slug],claude=r.root_visual_review;
  if(sha!==r.native_sha256)errors.push(r.slug+':hash');
  const rootPass=codex?.verdict==='pass'&&codex.native_sha256===sha&&codex.native_reviewed&&codex.thumbnail_200_reviewed;
  const approved=claude?.reviewer==='claude'&&claude.verdict==='pass'&&claude.native_sha256===sha;
  records.push({batch,slug:r.slug,name:item.canonical_name,status:r.status,receipt,original_file:r.original_file,native_sha256:sha,rootPass,approved});
  prompts[r.slug]={batch,prompt:r.prompt,basis_claim_ids:r.basis_claim_ids,visual_requirements:r.visual_requirements,generated_file:r.generated_file,original_file:r.original_file,native_sha256:sha};
 }
}
const esc=x=>String(x??'').replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const approved=records.filter(r=>r.approved).length;
const gallery='docs/artwork-session-2000-2026-10-16.html';
const html=`<!doctype html><html lang="id"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Mitoloka — menuju 2000 ilustrasi</title><style>body{margin:0;background:#17130f;color:#eee4d4;font:16px/1.6 system-ui}main{max-width:1450px;margin:auto;padding:24px}a{color:#eac885}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));gap:24px}article{padding:18px;background:#251f18;border-radius:10px;min-width:0}img{display:block;width:100%;height:auto}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:13px}details{margin-top:12px}</style><main><h1>Mitoloka — menuju 2.000 ilustrasi</h1><p>Baseline 1.887 ilustrasi aktif. Target tambahan tepat113 PNG baru yang disetujui independen Claude. Snapshot: ${records.length} PNG baru, ${approved} lolos Claude, ${records.filter(r=>r.rootPass).length} lolos pemeriksaan native dan200px Codex. Integrasi dilakukan sesi Claude; jumlah aktif tidak bertambah hanya karena generasi/review.</p><p>${s.batches.map(b=>`<a href="artwork-batch-${b}.html">Batch${b}</a>`).join(' · ')}</p><section class="grid">${records.map(r=>{const receipt=read(r.receipt);return `<article><h2>${esc(r.name)}</h2><p>Batch${r.batch} · ${r.approved?'Disetujui Claude':esc(r.status)}</p><a href="../${esc(r.original_file)}"><img loading="lazy" src="../${esc(r.original_file)}" alt="${esc(r.name)}"></a><p>${esc(receipt.depicted_variant)}</p><a href="../${esc(r.receipt)}">Receipt, klaim dan riwayat</a><details><summary>Prompt persis</summary><pre>${esc(receipt.prompt)}</pre></details></article>`}).join('')}</section><h2>Entri ditunda (${declines.length})</h2><ul>${declines.map(r=>`<li><a href="../${esc(r.receipt)}">${esc(r.slug)}</a>: ${esc(r.reason)}</li>`).join('')}</ul></main></html>`;
fs.writeFileSync(gallery,html);
const links=[...html.matchAll(/(?:href|src)="([^"#]+)"/g)].map(m=>m[1]);
const missing=links.filter(p=>!fs.existsSync(path.resolve('docs',p)));
if(missing.length)errors.push('missing gallerylinks:'+missing.join(','));
const summary={updated_at:new Date().toISOString(),baseline_active:s.baseline_active,target_new_approved:113,selected_pngs:records.length,root_pass:records.filter(r=>r.rootPass).length,approved_by_claude:approved,unique_hashes:new Set(records.map(r=>r.native_sha256)).size,declines:declines.length,remaining_approval:113-approved,gallery,gallery_link_checks:links.length,errors,records,declined_entries:declines};
write(base+'/codex-prompts.json',prompts);write(base+'/codex-generation-summary.json',summary);console.log(JSON.stringify({...summary,records:undefined,declined_entries:undefined},null,2));
if(errors.length)process.exitCode=1;
