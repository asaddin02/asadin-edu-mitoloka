import json,sys,os,shutil,hashlib,datetime,glob
from PIL import Image
slugs={'carbuncle-legendary-creature':1356,'pincoya':1456,'anchimayen':1506}
def write(p,d):open(p,'w').write(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
mode,s=sys.argv[1:3];batch=slugs[s];base=f'data/artwork-generated/batch-{batch}';draft=base+'/drafts/lane-C-correction-20261013';os.makedirs(draft,exist_ok=True);rp=base+'/'+s+'.json';dp=draft+'/'+s+'-request.json'
if mode=='prepare':
 old=json.load(open(rp));q=next(x for x in json.load(open('data/artwork-generated/batch-1606/drafts/root/user-correction-queue.json')) if x['slug']==s);os.makedirs(base+'/rejected',exist_ok=True);n=1
 while glob.glob(base+'/rejected/'+s+f'-attempt-{n:02d}*'):n+=1
 p=base+'/rejected/'+s+f'-attempt-{n:02d}.png';j=p[:-4]+'.json';full=p[:-4]+'-old-receipt.json';shutil.copyfile(old['original_file'],p);shutil.copyfile(rp,full);write(j,{'slug':s,'original_file':p,'native_sha256':old['native_sha256'],'generated_file':old['generated_file'],'prompt':old['prompt'],'reason':q['reason'],'old_receipt_path':full,'source':q['source']});old.setdefault('rejected_attempts',[]).append({'original_file':p,'receipt_file':j,'native_sha256':old['native_sha256'],'reason':q['reason']});old.update(worker_agent='lane-C',subagent_model='gpt-6.1-sol',subagent_reasoning_effort='high',status='draft-before-generation',correction_cycle='user-authorized2026-10-13',correction_archive_receipt=full);write(dp,old);print(s,'old archived',p)
elif mode=='meta' or mode=='accept':
 path,n=sys.argv[3:5];im=Image.open(path);h=hashlib.sha256(open(path,'rb').read()).hexdigest();m={'tool':'OpenAI built-in image_gen','image_model':'tidak dilaporkan alat','generated_file':path,'generated_at':datetime.datetime.fromtimestamp(os.path.getmtime(path),datetime.timezone.utc).isoformat(),'native_sha256':h,'width':im.width,'height':im.height};write(draft+'/'+s+'-attempt-'+n+'-tool-metadata.json',m);im.thumbnail((200,200));im.save(draft+'/'+s+'-attempt-'+n+'-200.png');print(json.dumps(m))
 if mode=='accept':
  d=json.load(open(dp));d.update(m);d['status']='awaiting-independent-review';d['visual_review']={'reviewer':'codex','verdict':'pass','notes':sys.argv[5],'limitations':[],'native_sha256':h,'reviewed_at':datetime.datetime.now(datetime.timezone.utc).isoformat()};d.pop('request',None)
  for k in ['root_visual_review','independent_visual_review','correction_notes']:d.pop(k,None)
  shutil.copyfile(path,d['original_file']);write(rp,d);print('accepted',rp)
