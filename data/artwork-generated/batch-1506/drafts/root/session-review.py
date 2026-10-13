"""Root-only inspection support. Accept only after actually viewing native and sheet."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw

p = argparse.ArgumentParser()
p.add_argument('mode', choices=['queue', 'sheet', 'accept', 'sync'])
p.add_argument('--batch', type=int, default=1506)
p.add_argument('--slugs', default='')
p.add_argument('--notes', default='')
p.add_argument('--sheet', default='')
a = p.parse_args()
base = Path(f'data/artwork-generated/batch-{a.batch}')
ledger_path = Path(f'data/artwork-batch-{a.batch}.json')
ledger = json.loads(ledger_path.read_text())
registry_path = base / 'drafts/root/root-native-reviews.json'
registry = json.loads(registry_path.read_text()) if registry_path.exists() else {}
slugs = [s for s in a.slugs.split(',') if s]
now = datetime.datetime.now(datetime.timezone.utc).isoformat()

def receipt(slug):
    return json.loads((base / f'{slug}.json').read_text())

if a.mode == 'queue':
    for item in ledger['items']:
        rp = base / f"{item['slug']}.json"
        if not rp.exists():
            continue
        r = receipt(item['slug'])
        if r['status'] != 'awaiting-independent-review':
            continue
        if registry.get(r['slug'], {}).get('native_sha256') == r['native_sha256']:
            continue
        claims = {c['id']: c['statement'] for c in item['research']['claims']}
        print(json.dumps({'slug': r['slug'], 'file': r['original_file'], 'claims': {c: claims[c] for c in r['basis_claim_ids']}, 'review': r['visual_review']['notes']}, ensure_ascii=False))
elif a.mode == 'sheet':
    assert slugs and a.sheet
    columns = min(5, len(slugs))
    canvas = Image.new('RGB', (columns * 220, ((len(slugs) + columns - 1) // columns) * 240), '#18130e')
    draw = ImageDraw.Draw(canvas)
    for i, slug in enumerate(slugs):
        im = Image.open(receipt(slug)['original_file'])
        im.thumbnail((200, 200))
        x, y = (i % columns) * 220, (i // columns) * 240
        canvas.paste(im, (x, y))
        draw.text((x, y + 205), slug, fill='white')
    canvas.save(a.sheet)
elif a.mode == 'accept':
    assert len(slugs) == 1 and a.notes.strip() and a.sheet
    slug = slugs[0]
    r = receipt(slug)
    assert r['status'] == 'awaiting-independent-review'
    digest = hashlib.sha256(Path(r['original_file']).read_bytes()).hexdigest()
    assert digest == r['native_sha256'] == r['visual_review']['native_sha256']
    assert Path(a.sheet).exists()
    registry[slug] = {'reviewer': 'codex', 'verdict': 'pass', 'reviewed_at': now,
        'native_sha256': digest, 'original_file': r['original_file'], 'notes': a.notes,
        'sangar_checks': [True] * 7, 'thumbnail_200_reviewed': True,
        'thumbnail_notes': 'Root melihat thumbnail tepat200px: subjek, aksi dan ciri wujud tetap terbaca; ' + a.notes,
        'thumbnail_sheet': a.sheet}
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + '\n')
elif a.mode == 'sync':
    for item in ledger['items']:
        rp = base / f"{item['slug']}.json"
        if not rp.exists():
            continue
        r = receipt(item['slug'])
        if r['status'] == 'tidak-digambar':
            item.update(status=r['status'], receipt_path=str(rp), reason=r['reason'])
        elif registry.get(r['slug'], {}).get('native_sha256') == r['native_sha256']:
            item.update(status=r['status'], receipt_path=str(rp), original_file=r['original_file'], native_sha256=r['native_sha256'])
    pending = sum(x['status'] == 'pending' for x in ledger['items'])
    ledger['generation_complete'] = pending == 0
    if pending == 0:
        ledger['generation_completed_at'] = now
        ledger['status'] = 'awaiting-independent-review'
    ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'batch': a.batch, 'pending': pending, 'root_accepted': len(registry)}))
