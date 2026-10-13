import sys,json,pathlib,importlib.util,datetime
D=pathlib.Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('w',D/'worker.py');w=importlib.util.module_from_spec(sp);sp.loader.exec_module(w)
s=sys.argv[2];o=json.load(open(D/(s+'-request.json')));n=len(o['rejected_attempts'])+1
if sys.argv[1]=='start':
 (D/f'{s}-request-attempt-{n:02d}.json').write_text(json.dumps(o,ensure_ascii=False,indent=2));(D/'outstanding-call.json').write_text(json.dumps({'slug':s,'attempt':n,'state':'running','started_at':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2));print(json.dumps(o['request']))
else:
 w.persist(s,sys.argv[3]);(D/f'{s}-tool-attempt-{n:02d}.json').write_text(json.dumps({'tool':'OpenAI built-in image_gen','image_model':'tidak dilaporkan alat','generated_file':sys.argv[3]},indent=2));(D/'outstanding-call.json').write_text(json.dumps({'slug':s,'attempt':n,'state':'completed','generated_file':sys.argv[3]},indent=2))
