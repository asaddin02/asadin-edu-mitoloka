import json,hashlib,shutil,sys
from pathlib import Path
from datetime import datetime,timezone
from PIL import Image
R=Path('/home/asadin/Portfolio/asadin-edu/asadin-mythological-creatures'); B=R/'data/artwork-generated/batch-1506';D=B/'drafts/lane-B'
def finish(slug,src,draft,notes):
 d=json.loads((D/draft).read_text());src=Path(src);dst=B/'originals'/f'{slug}.png';assert not dst.exists();shutil.copy2(src,dst);im=Image.open(dst);w,h=im.size;sha=hashlib.sha256(dst.read_bytes()).hexdigest();assert im.format=='PNG' and w==h and w>=1024
 now=datetime.now(timezone.utc).isoformat();d.update(status='awaiting-independent-review',generated_file=str(src),generated_at=datetime.fromtimestamp(src.stat().st_mtime,timezone.utc).isoformat(),original_file=str(dst.relative_to(R)),native_sha256=sha,width=w,height=h);d['visual_review']={'reviewer':'codex','verdict':'pass','notes':notes,'limitations':[],'native_sha256':sha,'reviewed_at':now};assert not (B/f'{slug}.json').exists();(B/f'{slug}.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');(D/f'{slug}-resume-tool-metadata.json').write_text(json.dumps({'tool':d['tool'],'image_model':d['image_model'],'generated_file':str(src),'native_sha256':sha,'width':w,'height':h},indent=2)+'\n');print(sha)
if __name__=='__main__':finish(*sys.argv[1:])
