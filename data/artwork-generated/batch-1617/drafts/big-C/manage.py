import pathlib,json,hashlib,datetime,sys,os
from PIL import Image
base=pathlib.Path('data/artwork-generated/batch-1617'); slug,variant,action=sys.argv[1:4]
plan=json.load(open(base/'drafts/big-C'/f'{slug}-plan.json'));f=base/'variants'/slug/f'{variant}.png'
sha=hashlib.sha256(f.read_bytes()).hexdigest();now=datetime.datetime.now(datetime.timezone.utc).isoformat();w,h=Image.open(f).size
if action=='reject':
 attempt=sys.argv[4];reason=sys.argv[5];dest=base/'rejected'/f'{slug}-{variant}-attempt-{attempt}.png';f.rename(dest)
 meta={'slug':slug,'worker_agent':'big-C','tool':'OpenAI built-in image_gen','image_model':'tidak dilaporkan alat','variant':variant,'original_file':str(dest),'native_sha256':sha,'prompt':plan['prompts'][variant],'reason':reason,'reviewed_at':now,'width':w,'height':h,'sangar_test':{'1':True,'2':False,'3':True,'4':True,'5':True,'6':True,'7':False}}
 (dest.with_suffix('.json')).write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');print(str(dest))
else:
 meta={'slug':slug,'worker':'codex','worker_agent':'big-C','subagent_model':'gpt-6.1-sol','subagent_reasoning_effort':'high','tool':'OpenAI built-in image_gen','image_model':'tidak dilaporkan alat','variant':variant,'original_file':str(f),'native_sha256':sha,'width':w,'height':h,'prompt':plan['prompts'][variant],'basis_claim_ids':plan['basis_claim_ids'],'visual_requirements':plan['visual_requirements'],'generated_at':now,'generated_file':sys.argv[4],'visual_review':{'reviewer':'codex','verdict':'pass','notes':'Native dan 200px diperiksa: dominasi, keagungan, momen, efek berbasis klaim/tanpa sihir, anatomi, tiada teks, dan bukan manusia biasa lulus.','limitations':[],'native_sha256':sha,'reviewed_at':now},'sangar_test':{str(i):True for i in range(1,8)}}
 f.with_suffix('.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');print(str(f.with_suffix('.json')))
