import json, pathlib, hashlib, shutil, datetime, sys
from PIL import Image
R=pathlib.Path('/home/asadin/Portfolio/asadin-edu/asadin-mythological-creatures'); B=R/'data/artwork-generated/batch-1406'; D=B/'drafts/lane-A'
def draft(slug,anatomy,ids,moment,power,pids,setting,sids,variant,choices,light='one dominant warm sidelight, deep shadows, strong rim light',surface='tactile natural surfaces'):
    cid=lambda a:[slug+'-'+s for s in a.split(',') if s]
    req=[{'kind':'anatomy','description':anatomy,'claim_ids':cid(ids)}]
    if pids:req.append({'kind':'effect','description':power,'claim_ids':cid(pids)})
    if sids:req.append({'kind':'setting','description':setting,'claim_ids':cid(sids)})
    basis=list(dict.fromkeys(sum([r['claim_ids'] for r in req],[])))
    prompt=f'''ONE original square premium painterly cinematic Mythics illustration of {slug.replace('-', ' ')}, {variant}.
ANATOMY: {anatomy} [{', '.join(cid(ids))}]
MOMENT: {moment}
POWER: {power} [{', '.join(cid(pids))}]
SCALE & CAMERA: extreme low angle; tight frame and foreshortening, distinguishing anatomy clearly visible; the creature dominates 80 percent of the square; never invent colossal size beyond the documented form.
LIGHT & WEATHER: {light}; physical particles only where justified by the action.
SURFACE: {surface}.
SETTING: {setting} [{', '.join(cid(sids))}]
MOOD: imposing and awe-inspiring or menacing as appropriate to the documented disposition; never cute, calm or decorative. Living belief beings treated respectfully.
HARD CONSTRAINTS: render ONE native square PNG at least 1024x1024 pixels; no text, lettering, glyphs, logo, border, frame or watermark; no extra heads, limbs or fingers; no design borrowed from any film, game, anime or comic; no nudity or explicit gore; no generic glow aura, neon outline or energy ribbons.'''
    obj={'slug':slug,'prompt':prompt,'visual_requirements':req,'basis_claim_ids':basis,'depicted_variant':variant,'artistic_choices':choices,'aura':power+' ['+', '.join(cid(pids) or cid(ids))+']','request':{'prompt':prompt,'transparent_background':False}}
    (D/(slug+'-request.json')).write_text(json.dumps(obj,ensure_ascii=False,indent=2));return obj

def finish(slug,raw,notes):
    obj=json.load(open(D/(slug+'-request.json')));x=json.load(open(R/'data/artwork-batch-1406.json'));item=next(i for i in x['items'] if i['slug']==slug)
    dst=B/'originals'/f'{slug}.png'
    if dst.exists():raise RuntimeError('Would overwrite original')
    shutil.copyfile(raw,dst);im=Image.open(dst);w,h=im.size;assert im.format=='PNG' and w==h and w>=1024
    sha=hashlib.sha256(dst.read_bytes()).hexdigest();now=datetime.datetime.now(datetime.timezone.utc).isoformat();im.resize((200,200)).save(D/(slug+'-200.png'))
    obj.pop('request');obj.update(worker='codex',worker_agent='lane-A',subagent_model='gpt-6.1-sol',subagent_reasoning_effort='high',tool='OpenAI built-in image_gen',image_model='tidak dilaporkan alat',status='awaiting-independent-review',review_path=item['review_path'],batch=1406,rationale=x['user_policy']['intent'],generated_file=raw,generated_at=now,original_file=str(dst.relative_to(R)),native_sha256=sha,width=w,height=h,generation_failures=obj.get('generation_failures',[]),rejected_attempts=obj.get('rejected_attempts',[]),visual_review={'reviewer':'codex','verdict':'pass','notes':notes,'limitations':[],'native_sha256':sha,'reviewed_at':now})
    (B/(slug+'.json')).write_text(json.dumps(obj,ensure_ascii=False,indent=2));print(slug,str(dst),sha,w,h)
if __name__=='__main__':finish(sys.argv[1],sys.argv[2],sys.argv[3])
def reject(slug,raw,reason,new_prompt):
    obj=json.load(open(D/(slug+'-request.json')));r=B/'rejected';r.mkdir(exist_ok=True);n=len(obj.get('rejected_attempts',[]))+1;dst=r/f'{slug}-attempt-{n:02d}.png';assert not dst.exists();shutil.copyfile(raw,dst);sha=hashlib.sha256(dst.read_bytes()).hexdigest();rp=dst.with_suffix('.json');rp.write_text(json.dumps({'original_file':str(dst.relative_to(R)),'native_sha256':sha,'prompt':obj['prompt'],'reason':reason,'generated_file':raw},indent=2));shutil.copyfile(D/(slug+'-request.json'),D/f'{slug}-request-attempt-{n:02d}.json');obj.setdefault('rejected_attempts',[]).append({'original_file':str(dst.relative_to(R)),'receipt_file':str(rp.relative_to(R)),'native_sha256':sha,'reason':reason});obj['prompt']=new_prompt;obj['request']['prompt']=new_prompt;(D/(slug+'-request.json')).write_text(json.dumps(obj,indent=2))
