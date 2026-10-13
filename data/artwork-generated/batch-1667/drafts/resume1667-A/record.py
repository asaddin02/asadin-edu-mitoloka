import pathlib,json,sys,os,hashlib,datetime
from PIL import Image
ROOT=pathlib.Path('/home/asadin/Portfolio/asadin-edu/asadin-edu-mitoloka')
BASE=ROOT/'data/artwork-generated/batch-1667'
DRAFT=BASE/'drafts/resume1667-A'
def write(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
slug,attempt,native=sys.argv[1:4]
d=json.loads((DRAFT/f'{slug}-attempt-{attempt}.json').read_text())
dest=DRAFT/f'{slug}-attempt-{attempt}.png'
if not dest.exists():os.link(native,dest)
sha=hashlib.sha256(dest.read_bytes()).hexdigest()
im=Image.open(dest);w,h=im.size
im.resize((200,200)).save(DRAFT/f'{slug}-attempt-{attempt}-200.png')
d.update(generated_file=native,generated_at=datetime.datetime.fromtimestamp(os.stat(native).st_mtime,datetime.timezone.utc).isoformat(),generated_at_basis='native PNG filesystem mtime',native_sha256=sha,width=w,height=h,original_file=str(dest.relative_to(ROOT)))
write(DRAFT/f'{slug}-attempt-{attempt}.json',d)
print(json.dumps({'slug':slug,'sha256':sha,'width':w,'height':h,'draft':str(dest)}))
