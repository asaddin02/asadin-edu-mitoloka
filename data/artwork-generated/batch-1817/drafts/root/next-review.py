import pathlib,json,sys
from PIL import Image,ImageDraw
b=pathlib.Path('data/artwork-generated/batch-1817');ledger=json.loads(pathlib.Path('data/artwork-batch-1817.json').read_text());rv=json.loads((b/'drafts/root/codex-native-reviews.json').read_text());blocked=json.loads((b/'drafts/root/rejected-awaiting-correction.json').read_text()) if (b/'drafts/root/rejected-awaiting-correction.json').exists() else {};names=[]
for item in ledger['items']:
 p=b/(item['slug']+'.json')
 if not p.exists():continue
 r=json.loads(p.read_text());s=r['slug']
 if r.get('status')=='awaiting-independent-review' and rv.get(s,{}).get('native_sha256')!=r['native_sha256'] and blocked.get(s)!=r['native_sha256']:names.append(s)
names=names[:int(sys.argv[1] if len(sys.argv)>1 else 4)];out=Image.new('RGB',(max(1,len(names))*200,230),'#ddd');draw=ImageDraw.Draw(out)
for n,s in enumerate(names):
 r=json.loads((b/(s+'.json')).read_text());item=next(x for x in ledger['items'] if x['slug']==s);print(s,'REQ',json.dumps(r['visual_requirements'],ensure_ascii=False),'CHOICES',r['artistic_choices']);print('SOURCE',json.dumps({c['id']:(c['statement'].get('en',c['statement']) if isinstance(c['statement'],dict) else c['statement']) for c in item['research']['claims'] if c['id'] in r['basis_claim_ids']},ensure_ascii=False));thumb=Image.open(r['original_file']).resize((200,200));thumb.save(b/f'drafts/root/{s}-200.png');out.paste(thumb,(n*200,0));draw.text((n*200+2,200),s,fill='black')
(b/'drafts/root/next-review-slugs.json').write_text(json.dumps(names));out.save(b/'drafts/root/next-review-200.png');print('REVIEW',names)
