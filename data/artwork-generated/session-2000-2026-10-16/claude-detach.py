from pathlib import Path
import subprocess,sys,json
base=Path(__file__).parent
batch=int(sys.argv[1]);round_name=sys.argv[2]
reviews=json.loads(Path(f'data/artwork-generated/batch-{batch}/drafts/root/codex-native-reviews.json').read_text())
slugs=sys.argv[3:]
for slug in slugs:
 r=json.loads(Path(f'data/artwork-generated/batch-{batch}/{slug}.json').read_text());v=reviews.get(slug,{})
 assert v.get('verdict')=='pass' and v.get('native_sha256')==r['native_sha256'],slug
prompt=(base/'claude-review-instructions.md').read_text()+f"\nBatch {batch}, round {round_name}. Hanya tinjau slug berikut: "+','.join(slugs)+f". Laporan output: {base}/claude-review-{batch}-{round_name}.json."
request=base/f'claude-request-{batch}-{round_name}.txt';request.write_text(prompt)
with request.open('r') as inp, (base/f'claude-log-{batch}-{round_name}.json').open('w') as output, (base/f'claude-stderr-{batch}-{round_name}.txt').open('w') as err:
 proc=subprocess.Popen(['claude','--safe-mode','--print','--permission-mode','dontAsk','--allowedTools','Read,Write,Edit,Bash','--output-format','json','--no-session-persistence'],stdin=inp,stdout=output,stderr=err,start_new_session=True)
record={'pid':proc.pid,'batch':batch,'round':round_name,'requested':slugs}
(base/f'claude-process-{batch}-{round_name}.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
