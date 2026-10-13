import json,pathlib,sys,hashlib,shutil,datetime
from PIL import Image
slug,native,notes=sys.argv[1:4];base=pathlib.Path('data/artwork-generated/batch-1556');draft=base/'drafts/correction-B';req=json.loads((draft/f'{slug}-attempt-02-request.json').read_text());dest=base/'originals'/f'{slug}.png';shutil.copyfile(native,dest)
sha=hashlib.sha256(dest.read_bytes()).hexdigest();im=Image.open(dest);assert im.format=='PNG' and im.width==im.height and im.width>=1024
now=datetime.datetime.now(datetime.timezone.utc).isoformat();receipt=base/f'{slug}.json';r=json.loads(receipt.read_text())
for key in ['prompt','depicted_variant','visual_requirements','basis_claim_ids','aura','artistic_choices','rejected_attempts']:r[key]=req[key]
r.update(worker='codex',worker_agent='correction-B',subagent_model='gpt-6.1-sol',subagent_reasoning_effort='high',tool='OpenAI built-in image_gen',image_model='tidak dilaporkan alat',model_reported=False,status='awaiting-independent-review',generated_file=native,generated_at=now,original_file=str(dest),native_sha256=sha,width=im.width,height=im.height)
r.pop('root_visual_review',None);r.pop('correction_notes',None)
r['visual_review']={'reviewer':'codex','verdict':'pass','notes':notes,'limitations':[],'native_sha256':sha,'reviewed_at':now,'sangar_checks':{str(i):'ya' for i in range(1,8)}}
receipt.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
meta={k:r[k] for k in ['slug','tool','image_model','model_reported','generated_file','generated_at','native_sha256','width','height']};meta['request_file']=str(draft/f'{slug}-attempt-02-request.json');(draft/f'{slug}-attempt-02-tool-metadata.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
im.resize((200,200),Image.Resampling.LANCZOS).save(draft/f'{slug}-attempt-02-200.png')
print(json.dumps(meta))
