import json, sys, hashlib, shutil, pathlib, datetime
from PIL import Image

root = pathlib.Path('/home/asadin/Portfolio/asadin-edu/asadin-edu-mitoloka')
batch, slug, raw, outcome, notes = sys.argv[1:6]
folder = root / 'data/artwork-generated' / ('batch-' + batch)
spec = json.loads((folder / 'drafts/session100-C' / (slug + '-spec.json')).read_text())
ledger = json.loads((root / ('data/artwork-batch-' + batch + '.json')).read_text())
item = next(x for x in ledger['items'] if x['slug'] == slug)
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
source = pathlib.Path(raw)
digest = hashlib.sha256(source.read_bytes()).hexdigest()
width, height = Image.open(source).size
history = folder / 'drafts/session100-C' / (slug + '-history.json')
rejects = json.loads(history.read_text()) if history.exists() else []
if outcome == 'reject':
    destdir = folder / 'rejected'
    destdir.mkdir(parents=True, exist_ok=True)
    n = 1
    while (destdir / f'{slug}-attempt-{n:02}.json').exists():
        n += 1
    dest = destdir / f'{slug}-attempt-{n:02}.png'
    receipt = dest.with_suffix('.json')
    shutil.copy2(source, dest)
    r = dict(original_file=str(dest.relative_to(root)), receipt_file=str(receipt.relative_to(root)), native_sha256=digest, reason=notes)
    receipt.write_text(json.dumps(dict(r, generated_file=raw, generated_at=now, prompt=spec['prompt'], tool='OpenAI built-in image_gen', image_model='tidak dilaporkan alat', width=width, height=height), ensure_ascii=False, indent=2)+'\n')
    rejects.append(r)
    history.write_text(json.dumps(rejects, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(r))
else:
    dest = folder / 'originals' / (slug + '.png')
    if dest.exists():
        old_hash = hashlib.sha256(dest.read_bytes()).hexdigest()
        safely_archived = any(x['native_sha256'] == old_hash and (root / x['original_file']).exists() and hashlib.sha256((root / x['original_file']).read_bytes()).hexdigest() == old_hash for x in rejects)
        if outcome != 'pass-replace' or not safely_archived:
            raise SystemExit('Refusing unarchived overwrite: '+str(dest))
        dest.unlink()
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, dest)
    r = dict(spec, worker='codex', worker_agent='resume100_c', subagent_model='gpt-6.1-sol', subagent_reasoning_effort='high', tool='OpenAI built-in image_gen', image_model='tidak dilaporkan alat', status='awaiting-independent-review', review_path=item['review_path'], rationale=ledger['user_policy']['intent'], generated_file=raw, generated_at=now, original_file=str(dest.relative_to(root)), native_sha256=digest, width=width, height=height, generation_failures=[], rejected_attempts=rejects, visual_review=dict(reviewer='codex', verdict='pass', notes=notes, limitations=[], native_sha256=digest, reviewed_at=now))
    r.pop('referenced_image_paths',None)
    (folder / (slug + '.json')).write_text(json.dumps(r, ensure_ascii=False, indent=2)+'\n')
    print(str(folder / (slug + '.json')))
    thumb = folder / 'drafts/session100-C' / (slug + '-200.png')
    im = Image.open(dest)
    im.thumbnail((200,200))
    im.save(thumb)
    print('THUMB',thumb)
