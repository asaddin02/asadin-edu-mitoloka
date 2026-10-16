import json,sys,pathlib,hashlib,shutil,datetime
from PIL import Image
batch,slug,raw,notes=sys.argv[1:]
root=pathlib.Path.cwd();folder=root/f'data/artwork-generated/batch-{batch}';draft=folder/'drafts/resume100-B'/f'{slug}-spec.json';d=json.load(open(draft));dest=folder/'originals'/f'{slug}.png';dest.parent.mkdir(exist_ok=True);assert not dest.exists();shutil.copy2(raw,dest);sha=hashlib.sha256(dest.read_bytes()).hexdigest();now=datetime.datetime.now(datetime.timezone.utc).isoformat();im=Image.open(dest)
d.update(status='awaiting-independent-review',worker_agent='resume100_b',generated_file=raw,generated_at=now,original_file=str(dest.relative_to(root)),native_sha256=sha,width=im.width,height=im.height,visual_review=dict(reviewer='codex',verdict='pass',notes=notes,limitations=[],native_sha256=sha,reviewed_at=now))
(folder/f'{slug}.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print(str(dest.relative_to(root)),sha)
