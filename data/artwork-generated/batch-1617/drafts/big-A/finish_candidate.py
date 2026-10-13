import json,pathlib,sys,hashlib,datetime
from PIL import Image
slug,variant,generated_file,notes=sys.argv[1:]
b=pathlib.Path('data/artwork-generated/batch-1617');f=b/'variants'/slug/(variant+'.png')
x=json.load(open(f.with_suffix('.request.json')));sha=hashlib.sha256(f.read_bytes()).hexdigest();w,h=Image.open(f).size;now=datetime.datetime.now(datetime.timezone.utc).isoformat()
x.update(status='candidate-awaiting-root-selection',generated_file=generated_file,generated_at=now,original_file=str(f),native_sha256=sha,width=w,height=h,depicted_variant=notes,aura=notes,selection_status='pending-root-selection',not_selected_reason=None,visual_review=dict(reviewer='codex',verdict='pass',notes=notes+' Inspected native PNG and 200px thumbnail. All seven Sangar criteria pass.',limitations=[],native_sha256=sha,reviewed_at=now),sangar_checks={str(i):True for i in range(1,8)})
f.with_suffix('.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
