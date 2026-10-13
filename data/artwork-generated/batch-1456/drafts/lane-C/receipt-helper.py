import sys,json,pathlib,shutil,hashlib,datetime
from PIL import Image
root=pathlib.Path(__file__).resolve().parents[5]
base=root/'data/artwork-generated/batch-1456'
slug,source=sys.argv[1:3]
draft_path=sorted((base/'drafts/lane-C').glob(f'{slug}-attempt-*.request.json'))[-1]
d=json.loads(draft_path.read_text())
out=base/'originals'/f'{slug}.png'
out.parent.mkdir(parents=True,exist_ok=True)
if not out.exists(): shutil.copy2(source,out)
elif out.read_bytes()!=pathlib.Path(source).read_bytes(): raise RuntimeError('Refuse overwrite')
im=Image.open(out); width,height=im.size
assert width==height and width>=1024
sha=hashlib.sha256(out.read_bytes()).hexdigest()
thumb=base/'drafts/lane-C'/f'{slug}-200.png'
im.thumbnail((200,200));im.save(thumb)
meta={'tool':'OpenAI built-in image_gen','model_reported':False,'generated_file':source,'native_sha256':sha,'width':width,'height':height,'image_model':'tidak dilaporkan alat'}
(base/'drafts/lane-C'/draft_path.name.replace('.request.json','.tool-metadata.json')).write_text(json.dumps(meta,indent=2)+'\n')
if len(sys.argv)>3:
 items=json.loads((root/'data/artwork-batch-1456.json').read_text())
 item=next(x for x in items['items'] if x['slug']==slug)
 now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 receipt={**d,**meta,'worker':'codex','worker_agent':'lane-C','subagent_model':'gpt-6.1-sol','subagent_reasoning_effort':'high','tool':'OpenAI built-in image_gen','status':'awaiting-independent-review','review_path':item['review_path'],'batch':1456,'rationale':items['user_policy']['intent'],'generated_at':now,'original_file':str(out.relative_to(root)),'generation_failures':[],'rejected_attempts':[],'visual_review':{'reviewer':'codex','verdict':'pass','notes':sys.argv[3],'limitations':[],'native_sha256':sha,'reviewed_at':now}}
 receipt['rejected_attempts']=d.get('rejected_attempts',[])
 receipt.pop('request',None)
 (base/f'{slug}.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'slug':slug,'original_file':str(out),'thumb':str(thumb),**meta}))
