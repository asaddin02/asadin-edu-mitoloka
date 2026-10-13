import json,sys,pathlib,os,hashlib,datetime
from PIL import Image
ROOT=pathlib.Path('/home/asadin/Portfolio/asadin-edu/asadin-edu-mitoloka')
BASE=ROOT/'data/artwork-generated/batch-1667'
DRAFT=BASE/'drafts/lane1667-C'
ledger=json.loads((ROOT/'data/artwork-batch-1667.json').read_text())
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
if sys.argv[1]=='draft':
 s=json.load(sys.stdin); item=next(i for i in ledger['items'] if i['slug']==s['slug'])
 d=dict(slug=s['slug'],worker='codex',worker_agent='lane1667-C',subagent_model='gpt-6.1-sol',subagent_reasoning_effort='high',tool='OpenAI built-in image_gen',image_model='tidak dilaporkan alat',review_path=item['review_path'],batch=1667,rationale=ledger['user_policy']['intent'],generation_failures=[],rejected_attempts=[])
 d.update(s); d['basis_claim_ids']=list(dict.fromkeys(c for r in s['visual_requirements'] for c in r['claim_ids']))
 for ids in s['claim_classification'].values(): d['basis_claim_ids']+= [c for c in ids if c not in d['basis_claim_ids']]
 valid={c['id'] for c in item['research']['claims']}; assert set(d['basis_claim_ids'])<=valid
 write(DRAFT/(s['slug']+'-attempt-'+s.get('attempt','01')+'.json'),d)
elif sys.argv[1]=='finish':
 slug,native,notes=sys.argv[2:5]; attempt=sys.argv[5] if len(sys.argv)>5 else '01'
 d=json.loads((DRAFT/(slug+'-attempt-'+attempt+'.json')).read_text()); dest=BASE/'originals'/f'{slug}.png'
 os.link(native,dest); sha=hashlib.sha256(dest.read_bytes()).hexdigest(); w,h=Image.open(dest).size
 d.update(status='awaiting-independent-review',generated_file=native,generated_at=now(),original_file=str(dest.relative_to(ROOT)),native_sha256=sha,width=w,height=h)
 d['visual_review']=dict(reviewer='codex',verdict='pass',notes=notes,limitations=[],native_sha256=sha,reviewed_at=now())
 write(BASE/(slug+'.json'),d)
 print(slug,sha,w,h)
elif sys.argv[1]=='decline':
 s=json.load(sys.stdin); item=next(i for i in ledger['items'] if i['slug']==s['slug'])
 d=dict(slug=s['slug'],worker='codex',worker_agent='lane1667-C',subagent_model='gpt-6.1-sol',subagent_reasoning_effort='high',tool='OpenAI built-in image_gen',image_model='tidak dilaporkan alat',status='tidak-digambar',review_path=item['review_path'],batch=1667,rationale=ledger['user_policy']['intent'],generated_file=None,generated_at=None,original_file=None,native_sha256=None,width=None,height=None,prompt=None,depicted_variant=None,visual_requirements=[],aura=None,artistic_choices=[],generation_failures=[],rejected_attempts=[],visual_review=None)
 d.update(s);write(BASE/(s['slug']+'.json'),d)
