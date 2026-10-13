import html
import json
from datetime import datetime, timezone
from pathlib import Path

base = Path('data/artwork-generated/batch-1617')
ledger_path = Path('data/artwork-batch-1617.json')
ledger = json.loads(ledger_path.read_text())
reviews = json.loads((base / 'drafts/root/codex-variant-reviews.json').read_text())
esc = lambda text: html.escape(str(text), quote=True)
cards, declined = [], []
for item in ledger['items']:
    slug = item['slug']
    receipt_path = base / f'{slug}.json'
    receipt = json.loads(receipt_path.read_text())
    item['receipt_path'] = str(receipt_path)
    item['status'] = receipt['status']
    if receipt['status'] == 'tidak-digambar':
        item['reason'] = receipt['reason']
        declined.append(f'<li><strong>{esc(item["canonical_name"])}</strong>: {esc(receipt["reason"])} <a href="../{receipt_path}">Receipt</a></li>')
        continue
    for key in ['original_file','native_sha256']:
        item[key] = receipt[key]
    assert reviews[slug]['selected_native_sha256'] == receipt['native_sha256']
    claims = {c['id']: c for c in item['research']['claims']}
    rows = []
    for cid in receipt['basis_claim_ids']:
        statement = claims[cid]['statement']
        if isinstance(statement, dict):
            statement = statement.get('id', statement.get('en', ''))
        rows.append(f'<li><code>{esc(cid)}</code>: {esc(statement)}</li>')
    variants = []
    for variant, info in reviews[slug]['variants'].items():
        vr = json.loads(Path(info['receipt_file']).read_text())
        choice = 'Terpilih' if variant == reviews[slug]['selected_variant'] else 'Varian alternatif'
        variants.append(f'<div><a href="../{esc(info["original_file"])}"><img loading="lazy" src="../{esc(info["original_file"])}" width="200" height="200" alt="{esc(item["canonical_name"])} varian {variant}"></a><p>{choice} {variant} · <a href="../{esc(info["receipt_file"])}">Receipt varian</a></p><details><summary>Prompt persis {variant}</summary><pre>{esc(vr["prompt"])}</pre></details></div>')
    archives = ''.join(f'<li><a href="../{esc(a["original_file"])}">PNG ditolak</a> · <a href="../{esc(a["receipt_file"])}">catatan</a>: {esc(a["reason"])}</li>' for a in receipt['rejected_attempts'])
    cards.append(f'''<article><h2>{esc(item['canonical_name'])}</h2><p>{esc(receipt['depicted_variant'])}</p>
<div class="variants">{''.join(variants)}</div>
<p><strong>Pilihan Codex:</strong> {esc(reviews[slug]['selection_reason'])}</p>
<p><a href="../{esc(receipt['original_file'])}">PNG final</a> · <a href="../{receipt_path}">Receipt final</a> · {receipt['width']}×{receipt['height']} · {esc(receipt['worker_agent'])}</p>
<details><summary>Klaim sumber</summary><ul>{''.join(rows)}</ul></details>
<details><summary>Percobaan ditolak</summary><ul>{archives or '<li>Tidak ada.</li>'}</ul></details></article>''')
ledger['generation_complete'] = True
ledger['generation_completed_at'] = datetime.now(timezone.utc).isoformat()
ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2)+'\n')
document = f'''<!doctype html><html lang="id"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Mitoloka · Batch 1617</title>
<style>body{{margin:0;background:#17130f;color:#eee4d4;font:16px/1.55 system-ui}}main{{max-width:1450px;margin:auto;padding:28px}}a{{color:#eac885}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(440px,1fr));gap:24px}}article{{padding:22px;background:#251f18;border-radius:10px;min-width:0}}.variants{{display:flex;flex-wrap:wrap;gap:20px}}img{{display:block;max-width:100%;height:auto}}pre{{white-space:pre-wrap;overflow-wrap:anywhere}}details{{font-size:14px}}li{{margin-bottom:14px}}h2{{font-size:22px}}@media(max-width:500px){{main{{padding:16px}}.grid{{grid-template-columns:1fr}}}}</style>
<main><h1>Mitoloka · Batch 1617</h1><p>{len(cards)} ilustrasi terpilih, masing-masing dua varian diperiksa pada PNG asli dan200piksel. Menunggu tinjauan independen Claude. {len(declined)} entri tidak digambar dengan alasan sumber/kualitas.</p>
<p><a href="../data/artwork-batch-1617.json">Ledger</a> · <a href="../{base}/drafts/root/validation.json">Validasi</a> · <a href="../{base}/codex-generation-summary.json">Serah terima</a></p>
<section class="grid">{''.join(cards)}</section><h2>Entri tidak digambar</h2><ul>{''.join(declined)}</ul></main></html>'''
Path('docs/artwork-batch-1617.html').write_text(document)
print(f'Batch1617: {len(cards)} selected, {len(declined)} declined; gallery built')
