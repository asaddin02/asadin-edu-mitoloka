from pathlib import Path
import json, hashlib, datetime, collections
base=Path(__file__).parent
s=json.loads((base/'session.json').read_text())
records=[]
for batch in s['batches']:
    ledger=json.loads(Path(f'data/artwork-batch-{batch}.json').read_text())
    for item in ledger['items']:
        path=Path(f'data/artwork-generated/batch-{batch}/{item["slug"]}.json')
        if not path.exists():
            records.append({'batch':batch,'slug':item['slug'],'status':'pending'});continue
        r=json.loads(path.read_text()); rev=r.get('root_visual_review') or {}
        native=Path(r.get('original_file') or '-')
        valid_native=native.is_file() and hashlib.sha256(native.read_bytes()).hexdigest()==r.get('native_sha256')
        approved=valid_native and rev.get('reviewer','').lower()=='claude' and rev.get('verdict')=='pass' and rev.get('native_sha256')==r.get('native_sha256')
        records.append({'batch':batch,'slug':item['slug'],'status':r['status'],'selected_png':bool(valid_native and r['status']!='tidak-digambar'),'approved_by_claude':approved,'native_sha256':r.get('native_sha256'),'receipt':str(path)})
counts=dict(collections.Counter(r['status'] for r in records))
approved=sum(bool(r.get('approved_by_claude')) for r in records)
manifest=json.loads(Path('assets/art/verified-manifest.json').read_text())['artworks']
summary={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseline_active':s['baseline_active'],'target_active':s['target_approved_active'],'required_new_approved':s['target_new_approved'],'active_now':len(manifest),'new_selected_pngs':sum(bool(r.get('selected_png')) for r in records),'new_independently_approved_by_claude':approved,'remaining_new_approval':max(0,s['target_new_approved']-approved),'status_counts':counts,'records':records,'note':'Baseline is active count, not an assertion that every historic approval was by Claude. New approvals require Claude reviewer, pass and matching actual PNG hash. Held historical entries excluded.'}
(base/'approval-progress.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='records'},indent=2))
