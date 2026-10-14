import html
import json
import shutil
from pathlib import Path

ROOT = Path.cwd()
esc = lambda value: html.escape(str(value), quote=True)

def card(item, receipt, receipt_path):
    name = item.get('canonical_name', item['slug'])
    image = ''
    if receipt.get('original_file'):
        image = f'<a href="../{esc(receipt["original_file"])}"><img loading="lazy" src="../{esc(receipt["original_file"])}" alt="{esc(name)}"></a>'
    claims = {c['id']: c for c in item['research']['claims']}
    source_rows = []
    for cid in receipt.get('basis_claim_ids', []):
        statement = claims[cid]['statement']
        if isinstance(statement, dict):
            statement = statement.get('id', statement.get('en', ''))
        source_rows.append(f'<li><code>{esc(cid)}</code>: {esc(statement)}</li>')
    rejected = ''.join(f'<li><a href="../{esc(a["original_file"])}">PNG ditolak</a> · <a href="../{esc(a["receipt_file"])}">Receipt percobaan</a>: {esc(a["reason"])}</li>' for a in receipt.get('rejected_attempts', []))
    variants = ''.join(f'<li><a href="../{esc(v["original_file"])}">Varian {esc(v.get("variant", "historis"))}</a> · <a href="../{esc(v["receipt_file"])}">Receipt varian</a> — arsip komposisi; status pilihan mengikuti receipt final.</li>' for v in receipt.get('generated_variants', []))
    choices = ''.join(f'<li>{esc(c)}</li>' for c in receipt.get('artistic_choices', []))
    return f'''<article><h2>{esc(name)}</h2><p class="status">{esc(receipt['status'])}</p>{image}
<p>{esc(receipt.get('reason') or receipt.get('depicted_variant', ''))}</p>
<p><a href="../{esc(receipt_path)}">Receipt lengkap</a> · {esc(receipt.get('image_model', 'tidak dilaporkan alat'))}</p>
<details><summary>Prompt persis PNG final</summary><pre>{esc(receipt.get('prompt') or 'Tidak ada PNG yang diterima; prompt percobaan tersedia dalam arsip penolakan.')}</pre></details>
<details><summary>Klaim sumber dan pilihan artistik</summary><ul>{''.join(source_rows)}</ul><ul>{choices}</ul></details>
<details><summary>Percobaan ditolak ({len(receipt.get('rejected_attempts', []))})</summary><ul>{rejected or '<li>Tidak ada.</li>'}</ul></details>
<details><summary>Varian historis</summary><ul>{variants or '<li>Tidak ada.</li>'}</ul></details></article>'''

def document(title, intro, cards):
    return f'''<!doctype html><html lang="id"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title>
<style>body{{margin:0;background:#17130f;color:#eee4d4;font:16px/1.6 system-ui}}main{{max-width:1450px;margin:auto;padding:24px}}a{{color:#eac885}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,340px),1fr));gap:24px}}article{{padding:20px;background:#251f18;border-radius:10px;min-width:0}}img{{display:block;width:100%;height:auto}}pre{{white-space:pre-wrap;overflow-wrap:anywhere;font-size:13px}}details{{margin-top:12px}}li{{margin-bottom:12px}}h2{{font-size:22px}}.status{{color:#ddbf87}}</style>
<main><h1>{esc(title)}</h1><p>{esc(intro)}</p><section class="grid">{''.join(cards)}</section></main></html>'''

ledger = json.loads((ROOT / 'data/artwork-batch-1717.json').read_text())
cards, counts, prompts = [], {}, {}
for item in ledger['items']:
    rp = f'data/artwork-generated/batch-1717/{item["slug"]}.json'
    if not (ROOT / rp).exists():
        continue
    r = json.loads((ROOT / rp).read_text())
    counts[r['status']] = counts.get(r['status'], 0) + 1
    cards.append(card(item, r, rp))
    if r.get('original_file'): prompts[item['slug']] = {'prompt':r['prompt'], 'original_file':r['original_file'], 'native_sha256':r['native_sha256']}
intro = ', '.join(f'{number} {status}' for status, number in counts.items()) + '. PNG yang diterima diperiksa Codex pada ukuran asli dan thumbnail 200px; menunggu tinjauan independen Claude. Setiap ciri anatomi dan efek merujuk klaim sumber.'
(ROOT / 'docs/artwork-batch-1717.html').write_text(document('Mitoloka · Batch 1717', intro, cards))
(ROOT / 'data/artwork-generated/batch-1717/codex-prompts.json').write_text(json.dumps(prompts,ensure_ascii=False,indent=2)+'\n')
print(counts)
