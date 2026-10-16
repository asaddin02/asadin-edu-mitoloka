import json,os,hashlib,shutil,datetime,sys
from PIL import Image
B='data/artwork-generated/batch-'+sys.argv[1]; slug=sys.argv[2]; action=sys.argv[3]
def read(p):
 with open(p) as f:return json.load(f)
def write(p,x):
 os.makedirs(os.path.dirname(p),exist_ok=True)
 with open(p,'w') as f:json.dump(x,f,indent=2);f.write('\n')
def sha(p):return hashlib.sha256(open(p,'rb').read()).hexdigest()
spec=read(B+'/drafts/resume_2000_a/'+slug+'-spec.json');rp=B+'/'+slug+'.json';old=read(rp) if os.path.exists(rp) else {}
ledger=read('data/artwork-batch-'+sys.argv[1]+'.json');item=next(i for i in ledger['items'] if i['slug']==slug)
r={**old,**spec,'slug':slug,'batch':int(sys.argv[1]),'worker':'codex','worker_agent':'resume_2000_a','subagent_model':'gpt-6.1-sol','subagent_reasoning_effort':'high','tool':'OpenAI built-in image_gen','image_model':'tidak dilaporkan alat','review_path':item['review_path'],'rationale':ledger['user_policy']['intent'],'rejected_attempts':old.get('rejected_attempts',[]),'generation_failures':old.get('generation_failures',[])}
if action=='decline':r.update(status='tidak-digambar',reason=spec['reason']);write(rp,r);print(rp);sys.exit()
generated=sys.argv[4]; notes=sys.argv[5]
if old.get('status')=='needs-correction':
 n=1
 while os.path.exists(B+'/rejected/'+slug+'-attempt-%02d.json'%n):n+=1
 ar=B+'/rejected/'+slug+'-attempt-%02d'%n
 assert sha(old['original_file'])==old['native_sha256']
 os.makedirs(os.path.dirname(ar),exist_ok=True);shutil.copyfile(old['original_file'],ar+'.png')
 entry={'original_file':ar+'.png','receipt_file':ar+'.json','native_sha256':old['native_sha256'],'reason':old['correction_notes']}
 write(ar+'.json',{**old,**entry,'previous_receipt':old,'archived_at':datetime.datetime.now(datetime.timezone.utc).isoformat()})
 r['rejected_attempts'].append(entry)
target=B+'/originals/'+slug+'.png';os.makedirs(os.path.dirname(target),exist_ok=True);shutil.copyfile(generated,target);digest=sha(target);im=Image.open(target);now=datetime.datetime.now(datetime.timezone.utc).isoformat()
r.update(status='awaiting-independent-review',generated_file=generated,generated_at=now,original_file=target,native_sha256=digest,width=im.width,height=im.height,visual_review={'reviewer':'codex','verdict':'pass','notes':notes,'limitations':[],'native_sha256':digest,'reviewed_at':now})
for k in ['root_visual_review','independent_visual_review','correction_notes','edit_reference_file']:r.pop(k,None)
write(rp,r);im.resize((200,200)).save(B+'/drafts/resume_2000_a/'+slug+'-200.png');print(rp,digest)
