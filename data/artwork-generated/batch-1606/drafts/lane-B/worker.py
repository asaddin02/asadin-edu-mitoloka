import json,hashlib,shutil,sys
from pathlib import Path
from datetime import datetime,timezone
from PIL import Image
R=Path('/home/asadin/Portfolio/asadin-edu/asadin-mythological-creatures');B=R/'data/artwork-generated/batch-1606';D=B/'drafts/lane-B'
def info(src):
 src=Path(src);im=Image.open(src);w,h=im.size;assert im.format=='PNG' and w==h and w>=1024;return hashlib.sha256(src.read_bytes()).hexdigest(),w,h
mode,slug,attempt=sys.argv[1:4];attempt=int(attempt);req=D/f'{slug}-attempt-{attempt:02}-request.json';d=json.loads(req.read_text())
if mode=='capture':
 src=sys.argv[4];sha,w,h=info(src);m={'tool':d['tool'],'image_model':'tidak dilaporkan alat','generated_file':src,'native_sha256':sha,'width':w,'height':h};(D/f'{slug}-attempt-{attempt:02}-tool-metadata.json').write_text(json.dumps(m,indent=2)+'\n');im=Image.open(src);im.thumbnail((200,200));im.save(D/f'{slug}-attempt-{attempt:02}-200.png');print(src,sha)
else:
 m=json.loads((D/f'{slug}-attempt-{attempt:02}-tool-metadata.json').read_text());src=Path(m['generated_file']);sha,w,h=info(src);note=sys.argv[4]
 if mode=='finalize':
  dst=B/'originals'/f'{slug}.png'
  if dst.exists():
   oldsha=hashlib.sha256(dst.read_bytes()).hexdigest();assert any(r['native_sha256']==oldsha for r in d['rejected_attempts']);oldreceipt=B/f'{slug}.json';archive=B/'rejected'/f'{slug}-attempt-{attempt-1:02}-old-receipt.json';assert not archive.exists();shutil.copy2(oldreceipt,archive)
  shutil.copy2(src,dst);now=datetime.now(timezone.utc).isoformat();d.update(status='awaiting-independent-review',generated_file=str(src),generated_at=datetime.fromtimestamp(src.stat().st_mtime,timezone.utc).isoformat(),original_file=str(dst.relative_to(R)),native_sha256=sha,width=w,height=h);d['visual_review']={'reviewer':'codex','verdict':'pass','notes':note,'limitations':[],'native_sha256':sha,'reviewed_at':now};assert not (B/f'{slug}.json').exists() or attempt>1;(B/f'{slug}.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print(slug,sha)
 elif mode=='reject':
  dst=B/'rejected'/f'{slug}-attempt-{attempt:02}.png';assert not dst.exists();shutil.copy2(src,dst);side=dst.with_suffix('.json');r={'original_file':str(dst.relative_to(R)),'native_sha256':sha,'generated_file':str(src),'prompt':d['prompt'],'reason':note};side.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');d['rejected_attempts'].append({'original_file':r['original_file'],'receipt_file':str(side.relative_to(R)),'native_sha256':sha,'reason':note});d['prompt']+='\nTARGETED CORRECTION: '+sys.argv[5];p=D/f'{slug}-attempt-{attempt+1:02}-request.json';assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print(note)
