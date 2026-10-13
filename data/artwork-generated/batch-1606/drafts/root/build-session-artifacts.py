import html, json, pathlib, datetime
p = pathlib.Path('data/artwork-generated/batch-1606')
ledger = json.loads(pathlib.Path('data/artwork-batch-1606.json').read_text())
queue = json.loads((p/'drafts/root/user-correction-queue.json').read_text())
receipts = [json.loads((p/(i['slug']+'.json')).read_text()) for i in ledger['items']]
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
finals = [r for r in receipts if r['status']=='awaiting-independent-review']
declined = [r for r in receipts if r['status']=='tidak-digambar']
validation = json.loads((p/'drafts/root/batch-validation.json').read_text())
cv = json.loads((p/'drafts/root/corrections-validation.json').read_text())
summary = {'completed_at':now,'batch':1606,'generation_complete':True,'final':len(finals),'declined':len(declined),'pending':0,'resumed_receipts':27,'resumed_final':25,'resumed_declined':2,'recovered_historical_outputs':['wd-q15925032','sihuhata'],'all_native_and_200px_root_reviews':True,'tool':'OpenAI built-in image_gen','image_model':'tidak dilaporkan alat','subagents':{'model':'gpt-6.1-sol','reasoning_effort':'high','lane-A':{'batch_assigned':9,'corrections':4},'lane-B':{'batch_assigned':9,'corrections':5},'lane-C':{'batch_assigned':9,'corrections':3}},'main_agent_corrections':['hatmehit','chiwen','namaka'],'session_calls':{'total':53,'successful_pngs':52,'tool_failures':1,'new_quality_rejections':14,'new_selected_batch_pngs':23,'new_selected_correction_pngs':15},'historical_interrupted_call':{'slug':'ouni','attempt':1,'png_returned':False},'batch_archived_rejections':validation['archived_rejected_pngs'],'batch_validation':validation,'corrections_validation':cv,'corrections':queue,'declined_entries':[{'slug':r['slug'],'reason':r['reason']} for r in declined],'independent_review_pending':True,'integration_performed':False,'commit_push_deploy_performed':False,'protected_files_snapshot':str(p/'drafts/root/protected-resume-before.json'),'note':'All 15 correction verdicts were supplied in the owner message; Claude had not yet written them to repository receipts. The replacements need fresh independent review. Three root-generated corrections use null sub-agent metadata truthfully.'}
(p/'codex-generation-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
(p/'codex-prompts.json').write_text(json.dumps([{'slug':r['slug'],'prompt':r['prompt'],'original_file':r['original_file'],'native_sha256':r['native_sha256']}for r in finals],ensure_ascii=False,indent=2)+'\n')
cs={'completed_at':now,'corrections':15,'status':'awaiting-independent-review','source':'Owner message relaying Claude review, 2026-10-13','image_model':'tidak dilaporkan alat','validation':cv,'items':queue,'integration_performed':False}
(p/'codex-corrections-2026-10-13-summary.json').write_text(json.dumps(cs,ensure_ascii=False,indent=2)+'\n')
# Refresh each gallery so embedded prompts match the selected replacement PNGs.
builder=(p/'drafts/root/build-gallery.py').read_text()
for batch in [1277,1356,1406,1456,1506,1606]:
    exec(compile(builder.replace('1606',str(batch)),f'gallery-{batch}','exec'),{})
esc=lambda text: html.escape(str(text),quote=True)
cards=[]
for row in queue:
    r=json.loads(pathlib.Path(row['receipt_path']).read_text())
    archive=next((a for a in r['rejected_attempts'] if 'claude' in a['reason'].lower() or 'owner' in a['reason'].lower()),None)
    if archive is None:
        # Find the archived previous selection by matching the original correction reason.
        archive=next((a for a in r['rejected_attempts'] if row['reason'].split(';')[0].lower() in a['reason'].lower()),r['rejected_attempts'][-1])
    details=''.join(f'<li>{esc(c)}</li>'for c in r['artistic_choices'])
    old=f'<a href="../{esc(archive["original_file"])}"><img src="../{esc(archive["original_file"])}" width="200" height="200" loading="lazy" alt="Gambar ditolak"></a>'
    new=f'<a href="../{esc(r["original_file"])}"><img src="../{esc(r["original_file"])}" width="200" height="200" loading="lazy" alt="Gambar pengganti"></a>'
    cards.append(f'<article><h2>{esc(row["slug"])}</h2><p>Batch {r["batch"]} · <a href="../{esc(row["receipt_path"])}">Receipt</a></p><p>{esc(row["reason"])}</p><div class="compare"><figure>{old}<figcaption>Ditolak</figcaption></figure><figure>{new}<figcaption>Pengganti untuk ditinjau</figcaption></figure></div><p>{esc(r["depicted_variant"])}</p><details><summary>Klaim, pilihan rendering, dan prompt</summary><p>{esc(", ".join(r["basis_claim_ids"]))}</p><ul>{details}</ul><pre>{esc(r["prompt"])}</pre></details></article>')
style='body{margin:0;background:#17130f;color:#eee4d4;font:16px/1.5 system-ui}main{max-width:1200px;margin:auto;padding:28px}a{color:#eac885}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(440px,1fr));gap:20px}article{background:#251f18;padding:20px;border-radius:10px}.compare{display:flex;flex-wrap:wrap;gap:14px}figure{margin:0}img{display:block;object-fit:contain}figcaption{font-size:13px;color:#c4b79f}h2{font-size:21px;overflow-wrap:anywhere}pre{white-space:pre-wrap;overflow-wrap:anywhere}details{font-size:13px}@media(max-width:500px){.grid{grid-template-columns:1fr}main{padding:12px}}'
page=f'<!doctype html><html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Mythics · 15 koreksi 13 Oktober 2026</title><style>{style}</style></head><body><main><h1>15 gambar pengganti · 13 Oktober 2026</h1><p>Menjawab catatan penolakan Claude yang disampaikan pemilik. Seluruh pengganti diperiksa Codex pada PNG asli dan 200px; menunggu tinjauan independen Claude.</p><p><a href="../{p}/codex-corrections-2026-10-13-summary.json">Serah terima</a> · <a href="../{p}/drafts/root/corrections-validation.json">Validasi</a> · <a href="artwork-batch-1606.html">Batch 1606</a></p><section class="grid">{"".join(cards)}</section></main></body></html>'
pathlib.Path('docs/artwork-corrections-2026-10-13.html').write_text(page)
print('Session artifacts and correction gallery written.')
