import html
import json
from pathlib import Path

base = Path('data/artwork-generated/batch-1406')
ledger = json.loads(Path('data/artwork-batch-1406.json').read_text())
esc = lambda s: html.escape(str(s), quote=True)
cards, deferred = [], []
for item in ledger['items']:
    receipt = json.loads((base / f"{item['slug']}.json").read_text())
    if receipt['status'] == 'tidak-digambar':
        deferred.append(f"<li><strong>{esc(item['canonical_name'])}</strong>: {esc(receipt['reason'])}</li>")
        continue
    claims = {c['id']: c for c in item['research']['claims']}
    claim_rows = []
    for cid in receipt['basis_claim_ids']:
        statement = claims[cid]['statement']
        if isinstance(statement, dict):
            statement = statement.get('id', statement.get('en', ''))
        claim_rows.append(f'<li><code>{esc(cid)}</code>: {esc(statement)}</li>')
    cards.append(f'''<article data-search="{esc(item['canonical_name'] + ' ' + item['slug'])}">
<a href="../{esc(receipt['original_file'])}" target="_blank" rel="noopener"><img src="../{esc(receipt['original_file'])}" width="200" height="200" loading="lazy" alt="{esc(item['canonical_name'])}"></a>
<h2>{esc(item['canonical_name'])}</h2><p class="slug">{esc(item['slug'])}</p>
<p>{esc(receipt['depicted_variant'])}</p><p><a href="../{base}/{esc(item['slug'])}.json">Receipt JSON</a> · {receipt['width']}×{receipt['height']} · {esc(receipt['worker_agent'])}</p>
<details><summary>Klaim dan prompt</summary><ul>{''.join(claim_rows)}</ul><pre>{esc(receipt['prompt'])}</pre></details></article>''')
style = '''body{margin:0;background:#17130f;color:#eee4d4;font:16px/1.5 system-ui,sans-serif}main{max-width:1400px;margin:auto;padding:32px}a{color:#eac885}input{box-sizing:border-box;width:100%;padding:12px;margin:16px 0 24px;border:1px solid #6b573d;border-radius:8px;background:#241e17;color:#fff;font:inherit}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:20px}article{background:#251f18;padding:16px;border-radius:10px}article img{display:block;margin:auto;width:200px;height:200px;object-fit:contain}h2{font-size:19px;margin-bottom:0}.slug{font-size:13px;color:#c4b79f;overflow-wrap:anywhere;margin-top:2px}article p{font-size:14px}details{font-size:13px}pre{white-space:pre-wrap;overflow-wrap:anywhere}li{margin-bottom:10px}article[hidden]{display:none}footer{margin-top:36px}'''
document = f'''<!doctype html><html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Mythics · Batch 1406</title><style>{style}</style></head><body><main>
<h1>Mythics · Batch 1406</h1><p>{len(cards)} ilustrasi menunggu tinjauan Claude · {len(deferred)} tidak digambar · belum dipasang ke situs.</p>
<p>Klik thumbnail 200 piksel untuk PNG asli. Pemeriksaan Codex selesai; tinjauan independen menunggu Claude.</p>
<p><a href="../data/artwork-batch-1406.json">Ledger</a> · <a href="../{base}/codex-generation-summary.json">Serah terima</a> · <a href="../{base}/drafts/root/batch-validation.json">Validasi</a></p>
<label for="search">Cari nama atau slug</label><input id="search" type="search" placeholder="Cari ilustrasi" autocomplete="off"><p id="count" aria-live="polite">{len(cards)} ilustrasi</p>
<section class="grid">{''.join(cards)}</section><h2>Entri ditunda</h2><ul>{''.join(deferred) or '<li>Tidak ada.</li>'}</ul>
<footer>PNG asli, receipt, klaim, dan prompt tersedia secara lokal. Riset serta ilustrasi aktif tetap dikelola Claude.</footer></main>
<script>const cards=[...document.querySelectorAll('article')];document.querySelector('#search').addEventListener('input',event=>{{const q=event.target.value.trim().toLocaleLowerCase();cards.forEach(c=>c.hidden=!c.dataset.search.toLocaleLowerCase().includes(q));document.querySelector('#count').textContent=cards.filter(c=>!c.hidden).length+' ilustrasi';}});</script></body></html>'''
Path('docs/artwork-batch-1406.html').write_text(document)
print(f'Gallery: {len(cards)} illustrations, {len(deferred)} deferred.')
