import json, hashlib, shutil, sys
from pathlib import Path
from datetime import datetime, timezone
from PIL import Image
ROOT=Path('/home/asadin/Portfolio/asadin-edu/asadin-mythological-creatures')
B=ROOT/'data/artwork-generated/batch-1506'
D=B/'drafts/lane-B'
ledger=json.loads((ROOT/'data/artwork-batch-1506.json').read_text())
def finalize(slug, source, notes):
    draft=json.loads((D/(slug+'-request.json')).read_text())
    dest=B/'originals'/ (slug+'.png')
    assert not dest.exists(), 'Do not overwrite originals'
    shutil.copy2(source,dest)
    im=Image.open(dest); w,h=im.size
    assert w==h and w>=1024 and im.format=='PNG'
    sha=hashlib.sha256(dest.read_bytes()).hexdigest()
    draft.update(status='awaiting-independent-review',generated_file=source,generated_at=datetime.now(timezone.utc).isoformat(),original_file=str(dest.relative_to(ROOT)),native_sha256=sha,width=w,height=h)
    draft['visual_review']={'reviewer':'codex','verdict':'pass','notes':notes,'limitations':[],'native_sha256':sha,'reviewed_at':datetime.now(timezone.utc).isoformat()}
    (B/(slug+'.json')).write_text(json.dumps(draft,ensure_ascii=False,indent=2)+'\n')
    return sha
if __name__=='__main__':
    if sys.argv[1]=='reject':
        slug,source,attempt,reason,correction=sys.argv[2:7]
        p=D/(slug+'-request.json');draft=json.loads(p.read_text())
        dest=B/'rejected'/(slug+'-attempt-'+str(attempt).zfill(2)+'.png')
        assert not dest.exists()
        shutil.copy2(source,dest);sha=hashlib.sha256(dest.read_bytes()).hexdigest();side=dest.with_suffix('.json')
        r={'original_file':str(dest.relative_to(ROOT)),'native_sha256':sha,'prompt':draft['prompt'],'reason':reason}
        side.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
        draft['rejected_attempts'].append({'original_file':str(dest.relative_to(ROOT)),'receipt_file':str(side.relative_to(ROOT)),'native_sha256':sha,'reason':reason})
        draft['prompt']+='\nCORRECTION: '+correction
        (D/(slug+'-attempt-'+str(attempt).zfill(2)+'-request.json')).write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
        p.write_text(json.dumps(draft,ensure_ascii=False,indent=2)+'\n')
    elif sys.argv[1]=='thumb':
        im=Image.open(sys.argv[2]);im.thumbnail((200,200));im.save(D/(sys.argv[3]+'-200.png'))
    elif sys.argv[1]=='finalize': print(finalize(sys.argv[2],sys.argv[3],sys.argv[4]))
