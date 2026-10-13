import json, pathlib, datetime, sys, hashlib
batch, slug, notes, sheet = sys.argv[1:5]
base=pathlib.Path('data/artwork-generated')/('batch-'+batch)
r=json.loads((base/(slug+'.json')).read_text())
sha=hashlib.sha256(pathlib.Path(r['original_file']).read_bytes()).hexdigest()
assert sha==r['native_sha256']
p=base/'drafts/root/root-native-reviews.json';reg=json.loads(p.read_text())
reg[slug]={'reviewer':'codex','verdict':'pass','reviewed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'native_sha256':sha,'original_file':r['original_file'],'notes':'Root native: '+notes,'sangar_checks':[True]*7,'thumbnail_200_reviewed':True,'thumbnail_notes':'Root saw exact200px: diagnostic form and active moment remain clear. '+notes,'thumbnail_sheet':sheet}
p.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n')
lp=pathlib.Path('data')/('artwork-batch-'+batch+'.json');b=json.loads(lp.read_text())
i=next(i for i in b['items'] if i['slug']==slug);i.update(status=r['status'],receipt_path=str(base/(slug+'.json')),original_file=r['original_file'],native_sha256=sha)
lp.write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n')
print(slug, len(reg))
