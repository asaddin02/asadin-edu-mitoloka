import datetime
import hashlib
import json
import sys
from pathlib import Path

base = Path('data/artwork-generated/batch-1406')
registry_path = base / 'drafts/root/root-native-reviews.json'
registry = json.loads(registry_path.read_text()) if registry_path.exists() else {}
notes = json.load(sys.stdin)
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
for slug, note in notes.items():
    receipt = json.loads((base / f'{slug}.json').read_text())
    actual = hashlib.sha256(Path(receipt['original_file']).read_bytes()).hexdigest()
    assert receipt['native_sha256'] == actual
    previous = registry.get(slug)
    entry = dict(reviewer='codex', verdict='pass', reviewed_at=now,
                 native_sha256=actual, original_file=receipt['original_file'],
                 notes=note, sangar_checks=[True] * 7, thumbnail_200_reviewed=False)
    if previous and previous['native_sha256'] != actual:
        entry['previous_main_reviews'] = previous.get('previous_main_reviews', []) + [previous]
    registry[slug] = entry
registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + '\n')
ledger_path = Path('data/artwork-batch-1406.json')
ledger = json.loads(ledger_path.read_text())
for item in ledger['items']:
    rp = base / f"{item['slug']}.json"
    if not rp.exists():
        continue
    receipt = json.loads(rp.read_text())
    if receipt['status'] == 'tidak-digambar' or item['slug'] in registry:
        item.update(status=receipt['status'], receipt_path=str(rp))
        for key in ['original_file', 'native_sha256']:
            if key in receipt:
                item[key] = receipt[key]
ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + '\n')
print('Main native review recorded:', ', '.join(notes))
