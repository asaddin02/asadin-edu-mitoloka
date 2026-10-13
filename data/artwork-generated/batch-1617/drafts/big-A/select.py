import json,pathlib,sys,os,hashlib,datetime
slug,variant,reason=sys.argv[1:];b=pathlib.Path('data/artwork-generated/batch-1617');d=b/'variants'/slug
for v in ['A','B']:
 f=d/(v+'.json');x=json.load(open(f));x.update(selection_status='selected' if v==variant else 'not-selected',not_selected_reason=None if v==variant else reason)
 f.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
x=json.load(open(d/(variant+'.json')));orig=b/'originals'/(slug+'.png')
if orig.exists() and hashlib.sha256(orig.read_bytes()).hexdigest()!=x['native_sha256']:
 old=b/'drafts'/'big-A'/(slug+'-previous-selection-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S')+'.png');orig.rename(old)
if not orig.exists():os.link(d/(variant+'.png'),orig)
x.update(status='awaiting-independent-review',original_file=str(orig),selected_variant=variant,selected_variant_reason=reason,generated_variants=[dict(variant=v,original_file=str(d/(v+'.png')),receipt_file=str(d/(v+'.json')),selected=v==variant) for v in ['A','B']])
x['rejected_attempts']=[]
for rf in sorted((b/'rejected').glob(slug+'-*-attempt-*.json')):
 r=json.load(open(rf));x['rejected_attempts'].append(dict(original_file=r['original_file'],receipt_file=str(rf),native_sha256=r['native_sha256'],reason=r['reason']))
x['artistic_choices'].append('Root Codex selected '+variant+' after native/200px comparison: '+reason+' This is illustrator selection, not independent review.')
(b/(slug+'.json')).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
