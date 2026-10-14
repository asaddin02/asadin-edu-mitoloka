import json, os, hashlib, datetime
from PIL import Image
ROOT='/home/asadin/Portfolio/asadin-edu/asadin-edu-mitoloka'
B='data/artwork-generated/batch-1717'
def spec(slug,groups,req,prompt,variant,choices,aura):
 d=json.load(open(ROOT+'/data/artwork-batch-1717.json')); i=next(x for x in d['items'] if x['slug']==slug)
 ids=list(dict.fromkeys(c for r in req for c in r['claim_ids']))
 out=dict(slug=slug,worker='codex',worker_agent='resume1717-B',subagent_model='gpt-6.1-sol',subagent_reasoning_effort='high',tool='OpenAI built-in image_gen',image_model='tidak dilaporkan alat',status='draft',review_path=i['review_path'],batch=1717,rationale=d['user_policy']['intent'],prompt=prompt,depicted_variant=variant,basis_claim_ids=ids,claim_classification=groups,visual_requirements=req,aura=aura,artistic_choices=choices,generation_failures=[],rejected_attempts=[])
 assert all(c in {a['id'] for a in i['research']['claims']} for c in ids)
 path=f'{ROOT}/{B}/drafts/lane-B/{slug}-spec.json'
 if os.path.exists(path):
  old=json.load(open(path));out['rejected_attempts']=old.get('rejected_attempts',[]);out['generation_failures']=old.get('generation_failures',[])
 json.dump(out,open(path,'w'),indent=2,ensure_ascii=False)
 return out
def finish(slug,native,notes):
 p=f'{ROOT}/{B}/drafts/lane-B/{slug}-spec.json';d=json.load(open(p));dest=f'{ROOT}/{B}/originals/{slug}.png'
 try:os.link(native,dest)
 except OSError:
  import shutil;shutil.copy2(native,dest)
 sha=hashlib.sha256(open(dest,'rb').read()).hexdigest();im=Image.open(dest); now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 d.update(status='awaiting-independent-review',generated_file=native,generated_at=now,original_file=f'{B}/originals/{slug}.png',native_sha256=sha,width=im.width,height=im.height,visual_review=dict(reviewer='codex',verdict='pass',notes=notes,limitations=[],native_sha256=sha,reviewed_at=now))
 json.dump(d,open(f'{ROOT}/{B}/{slug}.json','w'),indent=2,ensure_ascii=False)
 im.resize((200,200)).save(f'{ROOT}/{B}/drafts/lane-B/{slug}-200.png')
 print(json.dumps({'slug':slug,'path':dest,'sha':sha,'dimensions':im.size}))
def reject(slug,native,attempt,reason):
 d=json.load(open(f'{ROOT}/{B}/drafts/lane-B/{slug}-spec.json'));base=f'{B}/rejected/{slug}-attempt-{attempt:02d}';dest=f'{ROOT}/{base}.png'
 try:os.link(native,dest)
 except OSError:
  import shutil;shutil.copy2(native,dest)
 sha=hashlib.sha256(open(dest,'rb').read()).hexdigest(); r=dict(original_file=base+'.png',receipt_file=base+'.json',native_sha256=sha,reason=reason)
 json.dump(dict(**r,prompt=d['prompt'],generated_file=native,tool=d['tool'],image_model=d['image_model'],worker_agent=d['worker_agent'],basis_claim_ids=d['basis_claim_ids'],visual_requirements=d['visual_requirements']),open(ROOT+'/'+base+'.json','w'),indent=2)
 d['rejected_attempts'].append(r);json.dump(d,open(f'{ROOT}/{B}/drafts/lane-B/{slug}-spec.json','w'),indent=2,ensure_ascii=False)
def decline(slug,reason):
 p=f'{ROOT}/{B}/drafts/lane-B/{slug}-spec.json';d=json.load(open(p));d.update(status='tidak-digambar',reason=reason,generated_file=None,generated_at=None,original_file=None,native_sha256=None,width=None,height=None,visual_review=None)
 json.dump(d,open(f'{ROOT}/{B}/{slug}.json','w'),indent=2,ensure_ascii=False);print(slug+' declined: '+reason)
