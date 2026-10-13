from pathlib import Path
from PIL import Image
from datetime import datetime,timezone
import sys,json,hashlib,shutil
R=Path('/home/asadin/Portfolio/asadin-edu/asadin-mythological-creatures');mode,batch,s,n=sys.argv[1:5];B=R/f'data/artwork-generated/batch-{batch}';D=B/'drafts/lane-B';n=int(n);p=D/f'{s}-correction-{n:02}-request.json';x=json.load(open(p));mfile=D/f'{s}-correction-{n:02}-metadata.json'
if mode=='capture':
 src=Path(sys.argv[5]);im=Image.open(src);w,h=im.size;assert im.format=='PNG' and w==h and w>=1024
 m={'tool':'OpenAI built-in image_gen','image_model':'tidak dilaporkan alat','generated_file':str(src),'native_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'width':w,'height':h,'generated_at':datetime.fromtimestamp(src.stat().st_mtime,timezone.utc).isoformat()};mfile.write_text(json.dumps(m,indent=2)+'\n');im.thumbnail((200,200));im.save(D/f'{s}-correction-{n:02}-200.png');print(json.dumps(m))
elif mode=='final':
 m=json.load(open(mfile));assert m['native_sha256']!=x['correction_cycle']['prior_selected_native_sha256'];dst=B/'originals'/f'{s}.png';oldsha=hashlib.sha256(dst.read_bytes()).hexdigest();assert any(r['native_sha256']==oldsha for r in x['rejected_attempts']);shutil.copy2(m['generated_file'],dst);x.update(m,status='awaiting-independent-review',original_file=str(dst.relative_to(R)));x['visual_review']={'reviewer':'codex','verdict':'pass','notes':sys.argv[5],'limitations':[],'native_sha256':m['native_sha256'],'reviewed_at':datetime.now(timezone.utc).isoformat()};(B/f'{s}.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');print(s,m['native_sha256'])
