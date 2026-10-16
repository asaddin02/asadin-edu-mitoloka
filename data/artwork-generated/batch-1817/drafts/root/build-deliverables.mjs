import fs from 'node:fs';
import path from 'node:path';
import {read,write} from './resume-tools.mjs';
const batch=Number(process.argv[2]);
const base=`data/artwork-generated/batch-${batch}`,ledger=read(`data/artwork-batch-${batch}.json`);
const esc=s=>String(s??'').replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const document=(title,intro,cards)=>`<!doctype html><html lang="id"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(title)}</title><style>body{margin:0;background:#17130f;color:#eee4d4;font:16px/1.6 system-ui}main{max-width:1450px;margin:auto;padding:24px}a{color:#eac885}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,340px),1fr));gap:24px}article{padding:20px;background:#251f18;border-radius:10px;min-width:0}img{display:block;width:100%;height:auto}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:13px}details{margin-top:12px}li{margin-bottom:12px}h2{font-size:22px}.status{color:#ddbf87}</style><main><h1>${esc(title)}</h1><p>${esc(intro)}</p><section class="grid">${cards.join('')}</section></main></html>`;
function card(item,r,rp){
  const claims=new Map(item.research.claims.map(c=>[c.id,c]));
  const basis=(r.basis_claim_ids||[]).map(id=>{const s=claims.get(id)?.statement;return `<li><code>${esc(id)}</code>: ${esc(typeof s==='object'?(s.id||s.en):s)}</li>`}).join('');
  const rejected=(r.rejected_attempts||[]).map(a=>`<li><a href="../${esc(a.original_file)}">PNG ditolak</a> · <a href="../${esc(a.receipt_file)}">Receipt percobaan</a>: ${esc(a.reason)}</li>`).join('');
  const image=r.original_file?`<a href="../${esc(r.original_file)}"><img loading="lazy" src="../${esc(r.original_file)}" alt="${esc(item.canonical_name)}"></a>`:'';
  return `<article><h2>${esc(item.canonical_name||item.slug)}</h2><p class="status">${esc(r.status)}</p>${image}<p>${esc(r.reason||r.depicted_variant)}</p><p><a href="../${esc(rp)}">Receipt lengkap</a> · ${esc(r.image_model)}</p><details><summary>Prompt persis PNG final</summary><pre>${esc(r.prompt||'Tidak ada PNG terpilih.')}</pre></details><details><summary>Klaim sumber dan pilihan artistik</summary><ul>${basis}</ul><ul>${(r.artistic_choices||[]).map(s=>`<li>${esc(s)}</li>`).join('')}</ul></details><details><summary>Arsip penolakan (${r.rejected_attempts?.length||0})</summary><ul>${rejected||'<li>Tidak ada.</li>'}</ul></details></article>`;
}
const cards=[],counts={},prompts={},declines=[];let attempts=0,failures=0;
for(const item of ledger.items){
  const rp=`${base}/${item.slug}.json`;if(!fs.existsSync(rp))continue;
  const r=read(rp);counts[r.status]=(counts[r.status]||0)+1;attempts+=r.rejected_attempts?.length||0;failures+=r.generation_failures?.length||0;
  cards.push(card(item,r,rp));
  if(r.original_file)prompts[item.slug]={prompt:r.prompt,original_file:r.original_file,native_sha256:r.native_sha256};
  if(r.status==='tidak-digambar')declines.push({slug:item.slug,name:item.canonical_name,reason:r.reason});
}
const title=`Mitoloka · Batch ${batch}`;
const intro=Object.entries(counts).map(([s,n])=>`${n} ${s}`).join(', ')+'. Gambar baru dan koreksi menunggu tinjauan independen Claude. Status reviewed mengikuti keputusan Claude; integrasi dilakukan sesi Claude. Prompt, klaim, pilihan editorial dan riwayat penolakan tersedia pada tiap kartu.';
const gallery=`docs/artwork-batch-${batch}.html`;
fs.writeFileSync(gallery,document(title,intro,cards));
write(`${base}/codex-prompts.json`,prompts);
const summary={batch,updated_at:new Date().toISOString(),target:ledger.target,receipts:cards.length,status_counts:counts,selected_pngs:Object.keys(prompts).length,archived_rejected_attempts:attempts,tool_failures:failures,tool:'OpenAI built-in image_gen',image_model:[...new Set(ledger.items.map(i=>{const p=`${base}/${i.slug}.json`;return fs.existsSync(p)?read(p).image_model:null}).filter(Boolean))],declines,gallery,prompt_set:`${base}/codex-prompts.json`,integration_performed_by_codex:false};
write(`${base}/codex-generation-summary.json`,summary);
const html=fs.readFileSync(gallery,'utf8'),links=[...html.matchAll(/(?:href|src)="(\.\.\/[^"#]+)"/g)].map(m=>m[1]);
const missing=links.filter(p=>!fs.existsSync(path.resolve('docs',p)));
write(`${base}/drafts/root/gallery-validation.json`,{checked_at:new Date().toISOString(),gallery,links:links.length,missing});
console.log(JSON.stringify({...summary,link_checks:links.length,missing_links:missing},null,2));
if(missing.length)process.exitCode=1;
if(process.argv.includes('--corrections')){
  const corrections=[[1767,'nandi-bear'],[1817,'wd-q12284431'],[1817,'wd-q17065939'],[1817,'wd-q12279265'],[1817,'wd-q10441691']];
  const correctionCards=[],records=[],correctionPrompts={};
  for(const [bn,slug]of corrections){
    const l=read(`data/artwork-batch-${bn}.json`),item=l.items.find(i=>i.slug===slug),rp=`data/artwork-generated/batch-${bn}/${slug}.json`,r=read(rp);
    correctionCards.push(card(item,r,rp));
    records.push({batch:bn,slug,name:item.canonical_name,status:r.status,reason:r.reason||null,receipt:rp,original_file:r.original_file||null,native_sha256:r.native_sha256||null});
    if(r.original_file)correctionPrompts[slug]={prompt:r.prompt,original_file:r.original_file,native_sha256:r.native_sha256};
  }
  const cg='docs/artwork-corrections-2026-10-15.html';
  fs.writeFileSync(cg,document('Mitoloka · Koreksi 15 Oktober 2026','Empat koreksi PNG siap ditinjau Claude; satu makhluk ditunda setelah tiga percobaan gagal. Bukti dan alasan pada receipt serta arsip penolakan. Tidak ada integrasi oleh Codex.',correctionCards));
  const cl=[...fs.readFileSync(cg,'utf8').matchAll(/(?:href|src)="(\.\.\/[^"#]+)"/g)].map(m=>m[1]),cm=cl.filter(p=>!fs.existsSync(path.resolve('docs',p)));
  write('data/artwork-generated/corrections-2026-10-15/codex-generation-summary.json',{updated_at:new Date().toISOString(),tool:'OpenAI built-in image_gen',image_model:'tidak dilaporkan alat',records,gallery:cg,link_checks:cl.length,missing_links:cm,integration_performed:false});
  write('data/artwork-generated/corrections-2026-10-15/codex-prompts.json',correctionPrompts);
  console.log(JSON.stringify({correction_gallery:cg,records,link_checks:cl.length,missing_links:cm},null,2));
  if(cm.length)process.exitCode=1;
}
