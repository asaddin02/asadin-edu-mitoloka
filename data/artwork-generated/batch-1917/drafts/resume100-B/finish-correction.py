import json,pathlib,hashlib,shutil,datetime,sys
from PIL import Image
b,s,raw,notes=sys.argv[1:];f=pathlib.Path(f'data/artwork-generated/batch-{b}');d=json.load(open(f/'drafts/resume100-B'/f'{s}-spec.json'));dest=f/'originals'/f'{s}.png';shutil.copy2(raw,dest);sha=hashlib.sha256(dest.read_bytes()).hexdigest();now=datetime.datetime.now(datetime.timezone.utc).isoformat();im=Image.open(dest)
for field in ['root_visual_review','independent_visual_review','correction_notes']:d.pop(field,None)
d.update(status='awaiting-independent-review',generated_file=raw,generated_at=now,original_file=str(dest),native_sha256=sha,width=im.width,height=im.height,visual_review=dict(reviewer='codex',verdict='pass',notes=notes,limitations=[],native_sha256=sha,reviewed_at=now));(f/f'{s}.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print(s,sha)
