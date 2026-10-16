import json,os,hashlib,datetime,shutil
from PIL import Image
R='/home/asadin/Portfolio/asadin-edu/asadin-edu-mitoloka'
A=json.load(open(R+'/data/artwork-generated/session-100-2026-10-15/assignment-B.json'))
def paths(slug):
 a=next(x for x in A if x['slug']==slug);b=a['batch'];base=f'data/artwork-generated/batch-{b}';scratch=base+'/drafts/session100-B'
 for p in [scratch,base+'/originals',base+'/rejected']:os.makedirs(R+'/'+p,exist_ok=True)
 return b,base,scratch

def spec(slug,anatomy,effect,setting,traits,moment,variant,choices,light='one moon behind storm clouds',surface='rough natural textures'):
 b,base,scratch=paths(slug);d=json.load(open(f'{R}/data/artwork-batch-{b}.json'));i=next(x for x in d['items'] if x['slug']==slug)
 req=[]
 for kind,pair in [('anatomy',anatomy),('effect',effect),('setting',setting)]:
  if pair[1]:req.append(dict(kind=kind,description=pair[0],claim_ids=[slug+'-'+c for c in pair[1]]))
 ids=list(dict.fromkeys(c for r in req for c in r['claim_ids']))
 valid={x['id'] for x in i['research']['claims']};assert all(c in valid for c in ids),ids
 prompt=f'''ONE original square premium painterly cinematic Mitoloka illustration of {i['canonical_name']}, {variant}.
ANATOMY: {anatomy[0]} [{', '.join(anatomy[1])}]
MOMENT: {moment}
POWER: {effect[0]} [{', '.join(effect[1])}]
SCALE & CAMERA: extreme low angle; close foreshortened framing with subject filling most of the square, no invented giant size unless explicitly stated above.
LIGHT & WEATHER: {light}, sharp rim light, deep shadows; dark walnut and antique gold palette with one strong accent.
SURFACE: {surface}.
SETTING: {setting[0]} [{', '.join(setting[1])}]
MOOD: {traits[0]}; dangerous or awe-inspiring and imposing, never cute, calm or decorative.
HARD CONSTRAINTS: no text, writing, lettering, inscriptions, pseudoinscriptions, symbols, logo, border, frame or watermark; no extra heads, limbs or fingers; no design borrowed from any film, game, anime or comic; no nudity or explicit gore; no generic glow aura, neon outline or energy ribbons. Entirely original living creature; no statue or toy.'''
 out=dict(slug=slug,worker='codex',worker_agent='images_b',subagent_model='gpt-6.1-sol',subagent_reasoning_effort='high',tool='OpenAI built-in image_gen',image_model='tidak dilaporkan alat',status='draft',review_path=i['review_path'],batch=b,rationale=d['user_policy']['intent'],prompt=prompt,depicted_variant=variant,basis_claim_ids=ids,visual_requirements=req,claim_classification={k:[slug+'-'+c for c in p[1]] for k,p in [('anatomy',anatomy),('power_domain_deeds',effect),('setting',setting),('disposition',traits)]},aura=effect[0]+' '+','.join(slug+'-'+c for c in effect[1]),artistic_choices=choices,generation_failures=[],rejected_attempts=[])
 path=R+'/'+scratch+'/'+slug+'-spec.json'
 if os.path.exists(path):
  old=json.load(open(path));out['generation_failures']=old.get('generation_failures',[]);out['rejected_attempts']=old.get('rejected_attempts',[])
 json.dump(out,open(path,'w'),ensure_ascii=False,indent=2);print(prompt)

def load(slug):
 b,base,scratch=paths(slug);return b,base,scratch,json.load(open(R+'/'+scratch+'/'+slug+'-spec.json'))
def failure(slug,error):
 b,base,scratch,d=load(slug);d['generation_failures'].append(dict(error=error,at=datetime.datetime.now(datetime.timezone.utc).isoformat(),prompt=d['prompt']));json.dump(d,open(R+'/'+scratch+'/'+slug+'-spec.json','w'),ensure_ascii=False,indent=2)
def preview(slug,native):
 b,base,scratch=paths(slug);im=Image.open(native);im.resize((200,200)).save(R+'/'+scratch+'/'+slug+'-200.png');print(R+'/'+scratch+'/'+slug+'-200.png')
def finish(slug,native,notes,metadata=None):
 b,base,scratch,d=load(slug);dest=base+'/originals/'+slug+'.png';assert not os.path.exists(R+'/'+dest);shutil.copy2(native,R+'/'+dest);im=Image.open(R+'/'+dest);sha=hashlib.sha256(open(R+'/'+dest,'rb').read()).hexdigest();now=datetime.datetime.now(datetime.timezone.utc).isoformat();d.update(status='awaiting-independent-review',generated_file=native,generated_at=now,original_file=dest,native_sha256=sha,width=im.width,height=im.height,generation_metadata=metadata or {'image_model':'tidak dilaporkan alat'},visual_review=dict(reviewer='codex',verdict='pass',notes=notes,limitations=[],native_sha256=sha,reviewed_at=now));json.dump(d,open(R+'/'+base+'/'+slug+'.json','w'),ensure_ascii=False,indent=2);print(dest,sha,im.size)
def reject(slug,native,reason):
 b,base,scratch,d=load(slug);n=len(d['rejected_attempts'])+1;stem=f'{base}/rejected/{slug}-attempt-{n:02d}';dest=stem+'.png';shutil.copy2(native,R+'/'+dest);sha=hashlib.sha256(open(R+'/'+dest,'rb').read()).hexdigest();r=dict(original_file=dest,receipt_file=stem+'.json',native_sha256=sha,reason=reason);json.dump(dict(**r,prompt=d['prompt'],generated_file=native,tool=d['tool'],image_model=d['image_model'],generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat()),open(R+'/'+stem+'.json','w'),indent=2);d['rejected_attempts'].append(r);json.dump(d,open(R+'/'+scratch+'/'+slug+'-spec.json','w'),ensure_ascii=False,indent=2)
def decline(slug,reason):
 b,base,scratch,d=load(slug);d.update(status='tidak-digambar',reason=reason,generated_file=None,generated_at=None,original_file=None,native_sha256=None,width=None,height=None,visual_review=None);json.dump(d,open(R+'/'+base+'/'+slug+'.json','w'),ensure_ascii=False,indent=2);print(slug,reason)
