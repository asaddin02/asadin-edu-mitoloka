import json,sys,pathlib,shutil,hashlib,datetime
from PIL import Image
ROOT=pathlib.Path('/home/asadin/Portfolio/asadin-edu/asadin-edu-mitoloka')
mode=sys.argv[1]
specpath=ROOT/sys.argv[2]
s=json.loads(specpath.read_text())
base=ROOT/f'data/artwork-generated/batch-{s["batch"]}'
if mode=='copy':
 source=sys.argv[3]
 out=base/'originals'/f'{s["slug"]}.png';out.parent.mkdir(parents=True,exist_ok=True)
 if out.exists():raise Exception('Do not overwrite existing output')
 shutil.copyfile(source,out)
 im=Image.open(out);im.thumbnail((200,200));im.save(specpath.parent/f'{s["slug"]}-200.png')
 s.update(generated_file=source,generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),original_file=str(out.relative_to(ROOT)),native_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),width=Image.open(out).width,height=Image.open(out).height)
 specpath.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
 print(str(out));print(str(specpath.parent/f'{s["slug"]}-200.png'))
elif mode=='receipt':
 ledger=json.loads((ROOT/f'data/artwork-batch-{s["batch"]}.json').read_text());item=next(x for x in ledger['items'] if x['slug']==s['slug'])
 s.update(worker='codex',worker_agent='images_a',subagent_model='gpt-6.1-sol',subagent_reasoning_effort='high',tool='OpenAI built-in image_gen',image_model='tidak dilaporkan alat',status='awaiting-independent-review',review_path=item['review_path'],rationale=ledger['user_policy']['intent'],generation_failures=s.get('generation_failures',[]),rejected_attempts=s.get('rejected_attempts',[]))
 s['visual_review']={'reviewer':'codex','verdict':'pass','notes':sys.argv[3], 'limitations':[], 'native_sha256':s['native_sha256'],'reviewed_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 (base/f'{s["slug"]}.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n');print(base/f'{s["slug"]}.json')
