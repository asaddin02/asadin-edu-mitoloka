from pathlib import Path
import collections
import datetime
import hashlib
import json

base = Path(__file__).parent
read = lambda path: json.loads(Path(path).read_text())
digest = lambda path: hashlib.sha256(Path(path).read_bytes()).hexdigest()
session = read(base / 'session.json')
errors, records, declines, checks = [], [], [], []
claude_passes = {}
for report_path in base.glob('claude-review-*-r*.json'):
    report = read(report_path)
    for result in report.get('results', []):
        if result.get('verdict') == 'pass':
            claude_passes[(result['slug'], result['native_sha256'])] = str(report_path)

for batch in session['batches']:
    folder = Path(f'data/artwork-generated/batch-{batch}')
    ledger = read(f'data/artwork-batch-{batch}.json')
    root_reviews = read(folder / 'drafts/root/codex-native-reviews.json')
    validation = read(folder / 'drafts/root/resume-validation.json')
    checks.append({'batch':batch, 'checks':validation['checks'], 'errors':validation['errors']})
    if not validation['final'] or validation['errors']:
        errors.append(f'{batch}: validation did not pass')
    for item in ledger['items']:
        receipt_path = folder / f'{item["slug"]}.json'
        receipt = read(receipt_path)
        if receipt['status'] == 'tidak-digambar':
            declines.append({'batch':batch, 'slug':item['slug'], 'reason':receipt['reason'], 'receipt':str(receipt_path)})
            continue
        actual = digest(receipt['original_file'])
        root = root_reviews[item['slug']]
        review = receipt.get('root_visual_review', {})
        evidence = claude_passes.get((item['slug'], actual))
        valid = (receipt['status'] == 'reviewed'
                 and item['status'] == 'reviewed'
                 and actual == receipt['native_sha256'] == review.get('native_sha256') == root['native_sha256']
                 and review.get('reviewer') == 'claude' and review.get('verdict') == 'pass'
                 and root['verdict'] == 'pass' and root['native_reviewed'] and root['thumbnail_200_reviewed']
                 and bool(evidence))
        if not valid:
            errors.append(f'{item["slug"]}: missing final approval or matching evidence')
        records.append({'batch':batch, 'slug':item['slug'], 'native_sha256':actual,
                        'original_file':receipt['original_file'], 'receipt':str(receipt_path),
                        'claude_report':evidence, 'approved':valid})

manifest = read('assets/art/verified-manifest.json')['artworks']
if set(record['slug'] for record in records) & set(manifest):
    errors.append('A new selected slug was already active')
if len(records) != session['target_new_approved'] or len({record['native_sha256'] for record in records}) != len(records):
    errors.append('Final selected count or unique hash count differs from target')

before = read(base / 'resume-1425-protected-before.json')
current = {}
for directory in ['data/gemini','data/power','js','assets/art','backups']:
    root = Path(directory)
    if root.exists():
        for file in root.rglob('*'):
            if file.is_file():
                current[str(file)] = digest(file)
for name in ['data/creatures.json','data/artwork-nama-besar.json']:
    if Path(name).exists():
        current[name] = digest(name)
protected = {'baseline_files':len(before), 'current_files':len(current),
             'changed':[name for name in before if name in current and before[name] != current[name]],
             'missing':sorted(set(before) - set(current)), 'added':sorted(set(current) - set(before))}
if protected['changed'] or protected['missing'] or protected['added']:
    errors.append('Protected files changed during resume; see explicit comparison')

result = {'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'baseline_active':session['baseline_active'], 'active_installed':len(manifest),
          'target_new_approved':session['target_new_approved'], 'new_approved':sum(record['approved'] for record in records),
          'baseline_plus_new_approved':session['baseline_active'] + sum(record['approved'] for record in records),
          'selected_pngs':len(records), 'unique_hashes':len({record['native_sha256'] for record in records}),
          'declined':len(declines), 'technical_checks':sum(check['checks'] for check in checks),
          'batch_validation':checks, 'protected_files':protected, 'errors':errors,
          'integration_performed_by_codex':False, 'records':records, 'declined_entries':declines,
          'scope_note':'New approvals have Claude pass, matching actual PNG hash and matching independent Claude report. Historical baseline is active count; held historical approvals are excluded.'}
(base / 'final-validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({key:value for key,value in result.items() if key not in ['records','declined_entries']},indent=2))
raise SystemExit(bool(errors))
