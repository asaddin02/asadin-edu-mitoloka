import sys,json,hashlib,datetime,struct,pathlib,shutil
slug,generated,notes=sys.argv[1:]
root=pathlib.Path('/home/asadin/Portfolio/asadin-edu/asadin-mythological-creatures')
base=root/'data/artwork-generated/batch-1327'
p=json.loads((base/'drafts/lane-B'/f'{slug}-visual.json').read_text())
ledger=json.loads((root/'data/artwork-batch-1327.json').read_text())
item=next(x for x in ledger['items'] if x['slug']==slug)
dest=base/'originals'/f'{slug}.png'
shutil.copyfile(generated,dest)
raw=dest.read_bytes(); width,height=struct.unpack('>II',raw[16:24]); sha=hashlib.sha256(raw).hexdigest()
assert width>=1024 and height>=1024
assert set(p['basis_claim_ids'])<=set(x['id'] for x in item['research']['claims'])
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
r={**p,'worker':'codex','worker_agent':'lane-B','subagent_model':'gpt-6.1-sol','subagent_reasoning_effort':'high','tool':'OpenAI built-in image_gen','image_model':'tidak dilaporkan alat','status':'awaiting-independent-review','review_path':item['review_path'],'batch':1327,'rationale':ledger['user_policy']['intent'],'generated_file':generated,'generated_at':now,'original_file':str(dest.relative_to(root)),'native_sha256':sha,'width':width,'height':height,'generation_failures':[],'rejected_attempts':[],'visual_review':{'reviewer':'codex','verdict':'pass','notes':notes,'limitations':[],'native_sha256':sha,'reviewed_at':now}}
for q in sorted((base/'rejected').glob(slug+'-attempt-*.json')):
    j=json.loads(q.read_text())
    r['rejected_attempts'].append({'original_file':j['original_file'],'receipt_file':str(q.relative_to(root)),'native_sha256':j['native_sha256'],'reason':j['reason']})
(base/f'{slug}.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'slug':slug,'sha256':sha,'width':width,'height':height,'receipt':str(base/f'{slug}.json')}))
