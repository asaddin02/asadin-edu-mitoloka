import sys,json,pathlib,shutil,hashlib
base=pathlib.Path(__file__).resolve().parents[2]
slug,reason,addition=sys.argv[1:4]
drafts=base/'drafts/lane-C-resume'
path=sorted(drafts.glob(f'{slug}-attempt-*.request.json'))[-1]
attempt=int(path.name.split('-attempt-')[1][:2]);d=json.loads(path.read_text())
src=base/'originals'/f'{slug}.png'
dst=base/'rejected'/f'{slug}-attempt-{attempt:02}.png';dst.parent.mkdir(exist_ok=True)
shutil.move(src,dst)
root=base.parents[2]
sha=hashlib.sha256(dst.read_bytes()).hexdigest()
meta=json.loads(path.with_name(path.name.replace('.request.json','.tool-metadata.json')).read_text())
rp=dst.with_suffix('.json')
rp.write_text(json.dumps({'slug':slug,'attempt':attempt,'original_file':str(dst.relative_to(root)),'native_sha256':sha,'prompt':d['prompt'],'reason':reason,'generated_file':meta['generated_file']},ensure_ascii=False,indent=2)+'\n')
d.setdefault('rejected_attempts',[]).append({'original_file':str(dst.relative_to(root)),'receipt_file':str(rp.relative_to(root)),'native_sha256':sha,'reason':reason})
assert attempt<3,'Maximum3attempts'
d['prompt']+='\nTARGETED CORRECTION: '+addition
d['request']['prompt']=d['prompt']
(drafts/f'{slug}-attempt-{attempt+1:02}.request.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('Rejected',slug,attempt,'and wrote next visual requirements before generating.')
