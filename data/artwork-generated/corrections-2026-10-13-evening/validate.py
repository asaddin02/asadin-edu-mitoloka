import hashlib
import json
import struct
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

base = Path('data/artwork-generated/corrections-2026-10-13-evening')
reviews = json.loads((base / 'codex-native-reviews.json').read_text())
checks, errors = 0, []

def check(ok, message):
    global checks
    checks += 1
    if not ok:
        errors.append(message)

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

for batch, slug in [(1606, 'tata-duende'), (1617, 'frigg'), (1617, 'mnemosyne')]:
    ledger = json.loads(Path(f'data/artwork-batch-{batch}.json').read_text())
    item = next(i for i in ledger['items'] if i['slug'] == slug)
    rp = f'data/artwork-generated/batch-{batch}/{slug}.json'
    r = json.loads(Path(rp).read_text())
    check(r['slug'] == slug and r['batch'] == batch, f'{slug}: identity')
    check(r['status'] == 'awaiting-independent-review', f'{slug}: status')
    check(r['review_path'] == item['review_path'] and r['rationale'] == ledger['user_policy']['intent'], f'{slug}: policy/source')
    check(r['worker'] == 'codex' and r['tool'] == 'OpenAI built-in image_gen' and r['image_model'] == 'tidak dilaporkan alat', f'{slug}: provenance')
    check(r['subagent_model'] == 'gpt-6.1-sol' and r['subagent_reasoning_effort'] == 'high', f'{slug}: agent metadata')
    for field in ['root_visual_review', 'independent_visual_review', 'correction_notes']:
        check(field not in r, f'{slug}: forbidden {field}')
    for field in ['prompt', 'depicted_variant', 'aura', 'generated_at', 'original_file', 'generated_file']:
        check(bool(r.get(field)), f'{slug}: {field}')
    ids = {c['id'] for c in item['research']['claims']}
    check(bool(r['basis_claim_ids']) and set(r['basis_claim_ids']) <= ids, f'{slug}: basis claims')
    check(bool(r['visual_requirements']) and bool(r['artistic_choices']), f'{slug}: visual requirements/choices')
    for requirement in r['visual_requirements']:
        check(requirement['kind'] in ['anatomy', 'effect', 'setting'] and bool(requirement['description']) and bool(requirement['claim_ids']), f'{slug}: requirement')
        check(set(requirement['claim_ids']) <= ids and set(requirement['claim_ids']) <= set(r['basis_claim_ids']), f'{slug}: requirement source')
    png = Path(r['original_file']).read_bytes()
    sha = digest(r['original_file'])
    check(png[:8] == b'\x89PNG\r\n\x1a\n', f'{slug}: PNG')
    width, height = struct.unpack('>II', png[16:24])
    check(width == height == r['width'] == r['height'] and width >= 1024, f'{slug}: dimensions')
    check(sha == r['native_sha256'] == digest(r['generated_file']), f'{slug}: native provenance/hash')
    check(r['visual_review']['reviewer'] == 'codex' and r['visual_review']['verdict'] == 'pass' and r['visual_review']['native_sha256'] == sha and not r['visual_review']['limitations'], f'{slug}: worker review')
    rv = reviews[slug]
    check(rv['native_reviewed'] and rv['thumbnail_200_reviewed'] and Path(rv['thumbnail_path']).exists() and rv['native_sha256'] == sha and all(rv['sangar_checks']) and len(rv['sangar_checks']) == 7, f'{slug}: root review')
    check(all(item[k] == r[k] for k in ['status', 'original_file', 'native_sha256']) and item['receipt_path'] == rp, f'{slug}: ledger sync')
    check(isinstance(r['generation_failures'], list) and isinstance(r['rejected_attempts'], list), f'{slug}: history')
    for a in r['rejected_attempts']:
        ar = json.loads(Path(a['receipt_file']).read_text())
        check(digest(a['original_file']) == a['native_sha256'] == ar['native_sha256'], f'{slug}: archive hash')
        check(bool(ar['prompt']) and ar['reason'] == a['reason'], f'{slug}: archive prompt/reason')
        check(Path(ar['generated_file']).exists() and digest(ar['generated_file']) == a['native_sha256'], f'{slug}: archive tool provenance')
    check(sha not in {a['native_sha256'] for a in r['rejected_attempts']}, f'{slug}: new image differs from rejected')

snapshot = json.loads(Path('data/artwork-generated/batch-1667/drafts/root/protected-resume-2052.json').read_text())
for path, sha in snapshot.items():
    check(Path(path).exists() and digest(path) == sha, f'Protected change since resume: {path}')

class Links(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ['href', 'src'] and value:
                parsed = urlsplit(value)
                if not parsed.scheme and not parsed.netloc and parsed.path:
                    check((self.page.parent / unquote(parsed.path)).exists(), f'Broken link in {self.page}: {value}')

for path in ['docs/artwork-batch-1667.html', 'docs/artwork-batch-1606.html', 'docs/artwork-batch-1617.html', 'docs/artwork-corrections-2026-10-13-evening.html']:
    parser = Links()
    parser.page = Path(path)
    parser.feed(parser.page.read_text())

result = {'checked_at': datetime.now(timezone.utc).isoformat(), 'checks': checks, 'errors': errors, 'corrected': list(reviews), 'protected_resume_files': len(snapshot), 'integration_performed': False}
(base / 'validation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(bool(errors))
