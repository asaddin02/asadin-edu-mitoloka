import pathlib,json,hashlib,datetime,sys
slug,v,n,reason=sys.argv[1:];b=pathlib.Path('data/artwork-generated/batch-1617');d=b/'variants'/slug;rej=b/'rejected';rej.mkdir(exist_ok=True)
f=d/(v+'.png');rf=rej/(slug+'-'+v+'-attempt-'+n+'.png');f.rename(rf)
p=json.load(open(d/(v+'.request.json')));sha=hashlib.sha256(rf.read_bytes()).hexdigest();p.update(status='rejected',original_file=str(rf),native_sha256=sha,reason=reason,rejected_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
rj=rf.with_suffix('.json');rj.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
(d/(v+'.request.json')).rename(d/(v+'-attempt-'+n+'.request.json'))
if (d/(v+'.json')).exists():(d/(v+'.json')).rename(d/(v+'-attempt-'+n+'.json'))
