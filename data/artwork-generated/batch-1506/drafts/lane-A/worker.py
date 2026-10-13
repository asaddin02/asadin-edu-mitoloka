import json,pathlib,hashlib,shutil,datetime,sys
from PIL import Image
R=pathlib.Path('/home/asadin/Portfolio/asadin-edu/asadin-mythological-creatures');B=R/'data/artwork-generated/batch-1506';D=B/'drafts/lane-A'
def draft(s,anatomy,ids,moment,power,pids,setting,sids,variant,choices,light='one dominant warm sidelight, deep shadows and strong rim light',surface='tactile natural surfaces'):
 cid=lambda a:[s+'-'+t for t in a.split(',')if t];req=[{'kind':'anatomy','description':anatomy,'claim_ids':cid(ids)}]
 if pids:req.append({'kind':'effect','description':power,'claim_ids':cid(pids)})
 if sids:req.append({'kind':'setting','description':setting,'claim_ids':cid(sids)})
 p=f'''ONE original square premium painterly cinematic Mythics illustration of {s.replace('-',' ')}, {variant}.
ANATOMY: {anatomy} [{', '.join(cid(ids))}]
MOMENT: {moment}
POWER: {power} [{', '.join(cid(pids))}]
SCALE & CAMERA: extreme low angle; tight framing and foreshortening, distinguishing anatomy fully readable; being fills most of square; no invented gigantic size.
LIGHT & WEATHER: {light}; only physical particles justified by action.
SURFACE: {surface}.
SETTING: {setting} [{', '.join(cid(sids))}]
MOOD: imposing awe or menace appropriate to documented disposition, never cute, calm or decorative. Living religious traditions treated reverently.
HARD CONSTRAINTS: ONE native square PNG minimum1024x1024; no text, lettering, glyphs, logo, border, frame or watermark; no extra heads, limbs or fingers; no design from film, game, anime or comic; no nudity or explicit gore; no generic glow aura, neon outline or energy ribbons.'''
 o={'slug':s,'prompt':p,'request':{'prompt':p,'transparent_background':False},'visual_requirements':req,'basis_claim_ids':list(dict.fromkeys(sum([v['claim_ids']for v in req],[]))),'depicted_variant':variant,'artistic_choices':choices,'aura':power+' ['+', '.join(cid(pids)or cid(ids))+']','generation_failures':[],'rejected_attempts':[]};(D/(s+'-request.json')).write_text(json.dumps(o,ensure_ascii=False,indent=2));return o

def persist(s,raw):
 o=json.load(open(D/(s+'-request.json')));n=len(o['rejected_attempts'])+1;dest=D/f'{s}-native-attempt-{n:02d}.png';assert not dest.exists();shutil.copyfile(raw,dest);im=Image.open(dest);assert im.format=='PNG'and im.width==im.height and im.width>=1024;im.resize((200,200)).save(D/f'{s}-200-attempt-{n:02d}.png');(D/f'{s}-raw-attempt-{n:02d}.json').write_text(json.dumps({'generated_file':raw,'native_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'width':im.width,'height':im.height},indent=2));print(dest)

def finish(s,n,notes):
 o=json.load(open(D/(s+'-request.json')));meta=json.load(open(D/f'{s}-raw-attempt-{n:02d}.json'));i=next(j for j in json.load(open(R/'data/artwork-batch-1506.json'))['items']if j['slug']==s);x=json.load(open(R/'data/artwork-batch-1506.json'));src=D/f'{s}-native-attempt-{n:02d}.png';dst=B/'originals'/f'{s}.png';shutil.copyfile(src,dst);now=datetime.datetime.now(datetime.timezone.utc).isoformat();o.pop('request');o.update(worker='codex',worker_agent='lane-A',subagent_model='gpt-6.1-sol',subagent_reasoning_effort='high',tool='OpenAI built-in image_gen',image_model='tidak dilaporkan alat',status='awaiting-independent-review',review_path=i['review_path'],batch=1506,rationale=x['user_policy']['intent'],generated_file=meta['generated_file'],generated_at=now,original_file=str(dst.relative_to(R)),native_sha256=meta['native_sha256'],width=meta['width'],height=meta['height'],visual_review={'reviewer':'codex','verdict':'pass','notes':notes,'limitations':[],'native_sha256':meta['native_sha256'],'reviewed_at':now});(B/(s+'.json')).write_text(json.dumps(o,ensure_ascii=False,indent=2));print(s,meta['native_sha256'])

def reject(s,n,reason,newprompt):
 o=json.load(open(D/(s+'-request.json')));meta=json.load(open(D/f'{s}-raw-attempt-{n:02d}.json'));r=B/'rejected';r.mkdir(exist_ok=True);dst=r/f'{s}-attempt-{n:02d}.png';assert not dst.exists();shutil.copyfile(D/f'{s}-native-attempt-{n:02d}.png',dst);rp=dst.with_suffix('.json');rp.write_text(json.dumps({'original_file':str(dst.relative_to(R)),'native_sha256':meta['native_sha256'],'generated_file':meta['generated_file'],'prompt':o['prompt'],'reason':reason},indent=2));shutil.copyfile(D/(s+'-request.json'),D/f'{s}-request-attempt-{n:02d}.json');o['rejected_attempts'].append({'original_file':str(dst.relative_to(R)),'receipt_file':str(rp.relative_to(R)),'native_sha256':meta['native_sha256'],'reason':reason});o['prompt']=newprompt;o['request']['prompt']=newprompt;(D/(s+'-request.json')).write_text(json.dumps(o,indent=2))

def decline(s,reason):
 x=json.load(open(R/'data/artwork-batch-1506.json'));i=next(j for j in x['items']if j['slug']==s);o=json.load(open(D/(s+'-request.json')))if(D/(s+'-request.json')).exists()else{'slug':s,'basis_claim_ids':[],'visual_requirements':[],'generation_failures':[],'rejected_attempts':[]};o.pop('request',None);o.update(worker='codex',worker_agent='lane-A',subagent_model='gpt-6.1-sol',subagent_reasoning_effort='high',tool='OpenAI built-in image_gen',image_model='tidak dilaporkan alat',status='tidak-digambar',reason=reason,review_path=i['review_path'],batch=1506,rationale=x['user_policy']['intent']);(B/(s+'.json')).write_text(json.dumps(o,ensure_ascii=False,indent=2))
if __name__=='__main__':
 if sys.argv[1]=='persist':persist(sys.argv[2],sys.argv[3])
 elif sys.argv[1]=='finish':finish(sys.argv[2],int(sys.argv[3]),sys.argv[4])
