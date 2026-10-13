import sys,json,pathlib,hashlib,shutil
slug,attempt,src,reason=sys.argv[1:]
base=pathlib.Path('/home/asadin/Portfolio/asadin-edu/asadin-mythological-creatures/data/artwork-generated/batch-1356')
p=base/'rejected'/f'{slug}-attempt-{int(attempt):02d}.png'
assert not p.exists()
shutil.copyfile(src,p)
req=json.loads((base/'requests/lane-B'/f'{slug}-attempt-{int(attempt):02d}.json').read_text())
r={'slug':slug,'original_file':str(p.relative_to(base.parents[2])),'generated_file':src,'native_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'prompt':req['prompt'],'reason':reason}
p.with_suffix('.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(str(p))
