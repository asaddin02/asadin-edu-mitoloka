import json,os,shutil,hashlib,datetime
from PIL import Image
ROOT='/home/asadin/Portfolio/asadin-edu/asadin-edu-mitoloka'
def path(batch,slug):return f'{ROOT}/data/artwork-generated/batch-{batch}/drafts/correction1817-B/{slug}-spec.json'
def finish(batch,slug,native,notes):
 d=json.load(open(path(batch,slug)));b=f'data/artwork-generated/batch-{batch}';dest=ROOT+'/'+d['original_file'];tmp=dest+'.correction1817-b.tmp';shutil.copy2(native,tmp);os.replace(tmp,dest)
 sha=hashlib.sha256(open(dest,'rb').read()).hexdigest();assert sha not in d['historical_native_sha256'];assert os.stat(dest).st_ino!=os.stat(native).st_ino;im=Image.open(dest);now=datetime.datetime.now(datetime.timezone.utc).isoformat();d.pop('correction_target',None)
 d.update(status='awaiting-independent-review',generated_file=native,generated_at=now,native_sha256=sha,width=im.width,height=im.height,visual_review={'reviewer':'codex','verdict':'pass','notes':notes,'limitations':[],'native_sha256':sha,'reviewed_at':now})
 d.pop('root_visual_review',None);d.pop('correction_notes',None);json.dump(d,open(f'{ROOT}/{b}/{slug}.json','w'),indent=2,ensure_ascii=False);im.resize((200,200)).save(f'{ROOT}/{b}/drafts/correction1817-B/{slug}-200.png')
 print(json.dumps({'slug':slug,'receipt':f'{b}/{slug}.json','native_sha256':sha,'original_file':d['original_file'],'dimensions':im.size}))
def reject(batch,slug,native,reason):
 d=json.load(open(path(batch,slug)));b=f'data/artwork-generated/batch-{batch}';n=1
 while os.path.exists(f'{ROOT}/{b}/rejected/{slug}-attempt-{n:02d}.png') or os.path.exists(f'{ROOT}/{b}/rejected/{slug}-attempt-{n:02d}.json'):n+=1
 base=f'{b}/rejected/{slug}-attempt-{n:02d}';dest=f'{ROOT}/{base}.png';shutil.copy2(native,dest);sha=hashlib.sha256(open(dest,'rb').read()).hexdigest();r={'original_file':base+'.png','receipt_file':base+'.json','native_sha256':sha,'reason':reason}
 json.dump({**d,**r,'generated_file':native,'prompt':d['prompt']},open(f'{ROOT}/{base}.json','w'),indent=2,ensure_ascii=False);d['rejected_attempts'].append(r);json.dump(d,open(path(batch,slug),'w'),indent=2,ensure_ascii=False)
