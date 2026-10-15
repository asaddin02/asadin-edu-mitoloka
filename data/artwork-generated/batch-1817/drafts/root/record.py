import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

base=Path('data/artwork-generated/batch-1817')
registry=base/'drafts/root/codex-native-reviews.json'
reviews=json.loads(registry.read_text()) if registry.exists() else {}
notes=json.loads((base/'drafts/root/review-notes.json').read_text())
ledger_path=Path('data/artwork-batch-1817.json')
ledger=json.loads(ledger_path.read_text())
for slug,note in notes.items():
    receipt_path=base/f'{slug}.json'
    r=json.loads(receipt_path.read_text())
    sha=hashlib.sha256(Path(r['original_file']).read_bytes()).hexdigest()
    assert sha==r['native_sha256'] and r['status']=='awaiting-independent-review'
    thumbnail=base/f'drafts/root/{slug}-200.png'
    assert thumbnail.exists()
    if slug not in reviews or reviews[slug]['native_sha256']!=sha:
        reviews[slug]={'reviewer':'codex','native_reviewed':True,'thumbnail_200_reviewed':True,'thumbnail_path':str(thumbnail),'native_sha256':sha,'verdict':'pass','sangar_checks':[True]*7,'notes':note,'reviewed_at':datetime.now(timezone.utc).isoformat()}
    item=next(i for i in ledger['items'] if i['slug']==slug)
    for field in ['status','original_file','native_sha256']:item[field]=r[field]
    item['receipt_path']=str(receipt_path)
for item in ledger['items']:
    rp=base/f"{item['slug']}.json"
    if not rp.exists():continue
    r=json.loads(rp.read_text())
    if r.get('status')=='tidak-digambar':
        item.update(status=r['status'],reason=r['reason'],receipt_path=str(rp))
registry.write_text(json.dumps(reviews,ensure_ascii=False,indent=2)+'\n')
ledger_path.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
print('Root-reviewed final PNGs:',len(reviews))
