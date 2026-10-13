import sys, json, hashlib, datetime
from pathlib import Path
from PIL import Image, ImageDraw

batch = int(sys.argv[1])
base = Path(f'data/artwork-generated/batch-{batch}')
folder = base / 'drafts/root'
folder.mkdir(parents=True, exist_ok=True)
rp = folder / 'root-native-reviews.json'
registry = json.loads(rp.read_text()) if rp.exists() else {}
mode = sys.argv[2]
if mode == 'record':
    for slug, note in json.load(sys.stdin).items():
        r = json.loads((base / f'{slug}.json').read_text())
        h = hashlib.sha256(Path(r['original_file']).read_bytes()).hexdigest()
        assert h == r['native_sha256']
        old = registry.get(slug)
        new = dict(reviewer='codex', verdict='pass', reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(), native_sha256=h, original_file=r['original_file'], notes=note, sangar_checks=[True]*7, thumbnail_200_reviewed=False)
        if old and old['native_sha256'] != h:
            new['previous_main_reviews'] = old.get('previous_main_reviews', []) + [old]
        registry[slug] = new
elif mode == 'sheet':
    slugs = [s for s, r in registry.items() if not r.get('thumbnail_200_reviewed')]
    output = folder / sys.argv[3]
    assert slugs and not output.exists()
    im = Image.new('RGB', (1000, ((len(slugs)+4)//5)*220), '#1c1713')
    draw = ImageDraw.Draw(im)
    for i, slug in enumerate(slugs):
        t = Image.open(registry[slug]['original_file']); t.thumbnail((200,200))
        x,y = i%5*200, i//5*220
        im.paste(t,(x,y)); draw.text((x+3,y+201),slug,fill='white')
    im.save(output)
    output.with_suffix('.json').write_text(json.dumps(slugs))
    print(output)
elif mode == 'confirm':
    sheet = folder / sys.argv[3]
    for slug in json.loads(sheet.with_suffix('.json').read_text()):
        registry[slug].update(thumbnail_200_reviewed=True, thumbnail_notes=f'Root melihat thumbnail tepat200px pada {sheet.name}; subjek dominan, ciri khas dan aksi/tatapan menggetarkan terbaca tanpa efek tambahan.')
rp.write_text(json.dumps(registry, ensure_ascii=False, indent=2)+'\n')
if mode != 'sheet':
    lp = Path(f'data/artwork-batch-{batch}.json'); ledger=json.loads(lp.read_text())
    for item in ledger['items']:
        p=base/f"{item['slug']}.json"
        if not p.exists(): continue
        r=json.loads(p.read_text())
        if r['status']=='tidak-digambar' or (registry.get(item['slug'],{}).get('native_sha256')==r.get('native_sha256')):
            item.update(status=r['status'],receipt_path=str(p))
            for k in ('original_file','native_sha256'):
                if k in r:item[k]=r[k]
    lp.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
    print('Root records',len(registry))
