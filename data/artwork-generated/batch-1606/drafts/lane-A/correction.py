import json,pathlib,hashlib,shutil,datetime,sys,re
from PIL import Image
R=pathlib.Path('/home/asadin/Portfolio/asadin-edu/asadin-mythological-creatures'); MAP={'panhu':1406,'rep-un-kamuy':1406,'tangaroa':1406,'dirawong':1456}
def base(s):return R/f'data/artwork-generated/batch-{MAP[s]}'
def draft(s):return base(s)/'drafts/lane-A-user-correction'
def read(s):return json.load(open(draft(s)/f'{s}-request.json'))
def save(s,o):p=draft(s);p.mkdir(exist_ok=True,parents=True);(p/f'{s}-request.json').write_text(json.dumps(o,ensure_ascii=False,indent=2))
def archive(s,reason):
 b=base(s);o=json.load(open(b/f'{s}.json'));p=R/o['original_file'];assert hashlib.sha256(p.read_bytes()).hexdigest()==o['native_sha256'];r=b/'rejected';r.mkdir(exist_ok=True);n=1
 while (r/f'{s}-attempt-{n:02d}.png').exists()or(r/f'{s}-attempt-{n:02d}.json').exists():n+=1
 dest=r/f'{s}-attempt-{n:02d}.png';j=dest.with_suffix('.json');(r/f'{s}-attempt-{n:02d}-old-receipt.json').write_text(json.dumps(o,ensure_ascii=False,indent=2));shutil.move(p,dest);j.write_text(json.dumps({'original_file':str(dest.relative_to(R)),'native_sha256':o['native_sha256'],'prompt':o['prompt'],'generated_file':o['generated_file'],'reason':reason,'prior_receipt_file':str((r/f'{s}-attempt-{n:02d}-old-receipt.json').relative_to(R))},ensure_ascii=False,indent=2));o.setdefault('rejected_attempts',[]).append({'original_file':str(dest.relative_to(R)),'receipt_file':str(j.relative_to(R)),'native_sha256':o['native_sha256'],'reason':reason});o['historical_native_sha256']=list(dict.fromkeys(o.get('historical_native_sha256',[])+[o['native_sha256']]));o['user_correction_cycle']={'authorized_at':'2026-10-13','reason':reason,'new_attempt_limit':3,'previous_history_preserved':True};save(s,o);print('archived',s,n)
def start(s,n):
 o=read(s);(draft(s)/f'{s}-new-attempt-{n:02d}.request.json').write_text(json.dumps(o,ensure_ascii=False,indent=2));print(json.dumps(o.get('request',{'prompt':o['prompt'],'transparent_background':False})))
def persist(s,n,raw):
 d=draft(s);p=d/f'{s}-new-native-{n:02d}.png';assert not p.exists();shutil.copyfile(raw,p);im=Image.open(p);assert im.format=='PNG'and im.width==im.height and im.width>=1024;im.resize((200,200)).save(d/f'{s}-new-200-{n:02d}.png');m={'tool':'OpenAI built-in image_gen','image_model':'tidak dilaporkan alat','generated_file':raw,'generated_at':datetime.datetime.fromtimestamp(pathlib.Path(raw).stat().st_mtime,datetime.timezone.utc).isoformat(),'native_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'width':im.width,'height':im.height};(d/f'{s}-new-attempt-{n:02d}.metadata.json').write_text(json.dumps(m,indent=2));print(p)
def finish(s,n,notes):
 o=read(s);m=json.load(open(draft(s)/f'{s}-new-attempt-{n:02d}.metadata.json'));assert m['native_sha256']not in o['historical_native_sha256'];p=base(s)/'originals'/f'{s}.png';assert not p.exists();shutil.copyfile(draft(s)/f'{s}-new-native-{n:02d}.png',p);o.pop('request',None)
 for k in ['root_visual_review','independent_visual_review','correction_notes']:o.pop(k,None)
 o.update(**{k:m[k]for k in ['tool','image_model','generated_file','generated_at','native_sha256','width','height']},status='awaiting-independent-review',original_file=str(p.relative_to(R)),worker_agent='lane-A',subagent_model='gpt-6.1-sol',subagent_reasoning_effort='high',visual_review={'reviewer':'codex','verdict':'pass','notes':notes,'limitations':[],'native_sha256':m['native_sha256'],'reviewed_at':datetime.datetime.now(datetime.timezone.utc).isoformat()});(base(s)/f'{s}.json').write_text(json.dumps(o,ensure_ascii=False,indent=2));print(s,m['native_sha256'])
def reject(s,n,reason):
 o=read(s);m=json.load(open(draft(s)/f'{s}-new-attempt-{n:02d}.metadata.json'));r=base(s)/'rejected';ix=1
 while(r/f'{s}-attempt-{ix:02d}.png').exists()or(r/f'{s}-attempt-{ix:02d}.json').exists():ix+=1
 p=r/f'{s}-attempt-{ix:02d}.png';j=p.with_suffix('.json');shutil.copyfile(draft(s)/f'{s}-new-native-{n:02d}.png',p);j.write_text(json.dumps({'original_file':str(p.relative_to(R)),'native_sha256':m['native_sha256'],'generated_file':m['generated_file'],'prompt':o['prompt'],'reason':reason,'user_correction_new_attempt':n},indent=2));o['rejected_attempts'].append({'original_file':str(p.relative_to(R)),'receipt_file':str(j.relative_to(R)),'native_sha256':m['native_sha256'],'reason':reason});save(s,o)
if __name__=='__main__':
 fn=sys.argv[1];a=sys.argv[2:];globals()[fn](a[0],int(a[1]),*a[2:])if fn!='archive'else archive(*a)
