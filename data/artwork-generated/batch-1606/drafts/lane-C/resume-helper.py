import json,os,glob,shutil,hashlib,sys,datetime
from PIL import Image
base='data/artwork-generated/batch-1606';out=base+'/drafts/lane-C';b=json.load(open('data/artwork-batch-1606.json'))
def load(s):
 p=out+'/'+s+'-resume-request.json'
 if os.path.exists(p):return json.load(open(p))
 files=sorted(set(glob.glob(base+'/drafts/**/*'+s+'*request.json',recursive=True)+glob.glob(base+'/drafts/**/*'+s+'*.request.json',recursive=True)))
 return json.load(open(files[0]))
def write(p,d):open(p,'w').write(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def meta(s,path,n):
 im=Image.open(path);h=hashlib.sha256(open(path,'rb').read()).hexdigest();d={'tool':'OpenAI built-in image_gen','image_model':'tidak dilaporkan alat','generated_file':path,'generated_at':datetime.datetime.fromtimestamp(os.path.getmtime(path),datetime.timezone.utc).isoformat(),'native_sha256':h,'width':im.width,'height':im.height};write(out+'/'+s+'-resume-'+n+'-tool-metadata.json',d);im.thumbnail((200,200));im.save(out+'/'+s+'-resume-'+n+'-200.png');return d
mode,s=sys.argv[1:3]
if mode=='prepare':
 d=load(s);d['worker_agent']='lane-C';write(out+'/'+s+'-resume-request.json',d);print('Prepared',s)
elif mode=='meta':print(json.dumps(meta(s,sys.argv[3],sys.argv[4])))
elif mode=='accept':
 path,n,notes=sys.argv[3:6];d=load(s);m=meta(s,path,n);i=next(x for x in b['items'] if x['slug']==s);os.makedirs(base+'/originals',exist_ok=True);orig=base+'/originals/'+s+'.png';shutil.copyfile(path,orig);d.update(m);d.update({'slug':s,'worker':'codex','worker_agent':'lane-C','subagent_model':'gpt-6.1-sol','subagent_reasoning_effort':'high','status':'awaiting-independent-review','review_path':i['review_path'],'batch':1606,'rationale':b['user_policy']['intent'],'original_file':orig,'visual_review':{'reviewer':'codex','verdict':'pass','notes':notes,'limitations':[],'native_sha256':m['native_sha256'],'reviewed_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}});d.pop('request',None);write(base+'/'+s+'.json',d);print('Accepted',s,m['native_sha256'])
elif mode=='reject':
 path,n,reason=sys.argv[3:6];d=load(s);m=meta(s,path,n);os.makedirs(base+'/rejected',exist_ok=True);p=base+'/rejected/'+s+'-attempt-'+n+'.png';j=p[:-4]+'.json';shutil.copyfile(path,p);r=dict(m,prompt=d['prompt'],original_file=p,reason=reason);write(j,r);d.setdefault('rejected_attempts',[]).append({'original_file':p,'receipt_file':j,'native_sha256':m['native_sha256'],'reason':reason});write(out+'/'+s+'-resume-request.json',d);print('Rejected',s)
