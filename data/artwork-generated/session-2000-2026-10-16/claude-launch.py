from pathlib import Path
import subprocess,sys,json
base=Path(__file__).parent
batch=int(sys.argv[1]);round_name=sys.argv[2]
registry=Path(f'data/artwork-generated/batch-{batch}/drafts/root/codex-native-reviews.json')
reviews=json.loads(registry.read_text())
slugs=sys.argv[3:]
for slug in slugs:
 r=json.loads(Path(f'data/artwork-generated/batch-{batch}/{slug}.json').read_text());v=reviews.get(slug,{})
 assert v.get('verdict')=='pass' and v.get('native_sha256')==r['native_sha256'],slug
prompt=(base/'claude-review-instructions.md').read_text()+f"\nBatch {batch}, round {round_name}. Hanya tinjau slug berikut: "+','.join(slugs)+f". Laporan output: {base}/claude-review-{batch}-{round_name}.json."
(base/f'claude-request-{batch}-{round_name}.txt').write_text(prompt)
with (base/f'claude-log-{batch}-{round_name}.json').open('w') as output:
 result=subprocess.run(['claude','--safe-mode','--print','--permission-mode','dontAsk','--allowedTools','Read,Write,Edit,Bash','--output-format','json','--no-session-persistence'],input=prompt,text=True,stdout=output)
print(json.dumps({'batch':batch,'round':round_name,'requested':len(slugs),'exit_code':result.returncode,'log':str(base/f'claude-log-{batch}-{round_name}.json')}))
sys.exit(result.returncode)
