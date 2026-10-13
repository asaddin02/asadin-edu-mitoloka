import html
import json
import re
from pathlib import Path

base = Path('data/artwork-generated/corrections-2026-10-13-afternoon')
old = json.loads((base / 'receipts-before.json').read_text())
reviews = json.loads((base / 'codex-native-reviews.json').read_text())
ledgers = {}
cards = []
esc = lambda s: html.escape(str(s), quote=True)
for slug, row in old.items():
    r = json.loads(Path(row['receipt']).read_text())
    assert r['status'] == 'awaiting-independent-review'
    assert reviews[slug]['native_sha256'] == r['native_sha256']
    assert all(reviews[slug]['sangar_checks'])
    ledger_path = f'data/artwork-batch-{r["batch"]}.json'
    if ledger_path not in ledgers:
        ledgers[ledger_path] = json.loads(Path(ledger_path).read_text())
    item = next(i for i in ledgers[ledger_path]['items'] if i['slug'] == slug)
    for field in ['status','original_file','native_sha256']:
        item[field] = r[field]
    item['receipt_path'] = row['receipt']
    gallery = Path(f'docs/artwork-batch-{r["batch"]}.html')
    if gallery.exists():
        document = gallery.read_text()
        previous = html.escape(row['data']['prompt'], quote=True)
        if previous in document:
            backup = base / f'gallery-batch-{r["batch"]}-before.html'
            if not backup.exists():
                backup.write_text(document)
            gallery.write_text(document.replace(previous, html.escape(r['prompt'], quote=True)))
    claims = {c['id']: c for c in item['research']['claims']}
    claim_html = []
    for cid in r['basis_claim_ids']:
        statement = claims[cid]['statement']
        if isinstance(statement, dict):
            statement = statement.get('id', statement.get('en',''))
        claim_html.append(f'<li><code>{esc(cid)}</code>: {esc(statement)}</li>')
    archives = ''.join(f'<li><a href="../{esc(a["original_file"])}">PNG ditolak</a> · <a href="../{esc(a["receipt_file"])}">catatan</a>: {esc(a["reason"])}</li>' for a in r['rejected_attempts'])
    cards.append(f'''<article id="{esc(slug)}"><h2>{esc(item['canonical_name'])}</h2>
<a href="../{esc(r['original_file'])}"><img src="../{esc(r['original_file'])}" width="200" height="200" alt="{esc(item['canonical_name'])}"></a>
<p>Batch {r['batch']} · {r['width']}×{r['height']} · <a href="../{esc(row['receipt'])}">Receipt</a></p>
<p>Gambar pengganti menunggu tinjauan independen Claude.</p>
<p><strong>Koreksi Claude:</strong> {esc(row['data']['correction_notes'])}</p>
<p><strong>Pemeriksaan Codex:</strong> {esc(reviews[slug]['notes'])}</p>
<details><summary>Klaim dan prompt persis</summary><ul>{''.join(claim_html)}</ul><pre>{esc(r['prompt'])}</pre></details>
<details><summary>Riwayat percobaan</summary><ul>{archives}</ul></details></article>''')
    if gallery.exists():
        document = gallery.read_text()
        header = f'<h2>{esc(item["canonical_name"])}</h2>'
        matched = [a for a in re.findall(r'<article\b[^>]*>.*?</article>', document, re.S) if header in a]
        assert len(matched) == 1, f'{slug}: expected one gallery card'
        backup = base / f'gallery-batch-{r["batch"]}-before.html'
        if not backup.exists():
            backup.write_text(document)
        gallery.write_text(document.replace(matched[0], cards[-1], 1))
for path, ledger in ledgers.items():
    Path(path).write_text(json.dumps(ledger, ensure_ascii=False, indent=2)+'\n')
document = f'''<!doctype html><html lang="id"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Mitoloka · 7 koreksi · 13 Oktober 2026</title><style>body{{background:#17130f;color:#eee4d4;font:16px/1.55 system-ui;margin:0}}main{{max-width:1300px;margin:auto;padding:28px}}a{{color:#eac885}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:22px}}article{{padding:20px;background:#251f18;border-radius:10px;min-width:0}}img{{display:block;margin:auto}}pre{{white-space:pre-wrap;overflow-wrap:anywhere}}details{{font-size:14px}}li{{margin-bottom:10px}}h2{{font-size:21px}}</style>
<main><h1>Mitoloka · 7 koreksi · 13 Oktober 2026</h1><p>7 PNG diperiksa Codex pada ukuran asli dan thumbnail 200 piksel; menunggu tinjauan independen Claude.</p>
<p>Klik gambar untuk PNG asli. <a href="../{base}/validation.json">Validasi</a> · <a href="../{base}/codex-native-reviews.json">Pemeriksaan Codex</a></p><section class="grid">{''.join(cards)}</section></main></html>'''
Path('docs/artwork-corrections-2026-10-13-afternoon.html').write_text(document)
print('Updated ledgers:', ', '.join(ledgers), '; gallery cards:', len(cards))
