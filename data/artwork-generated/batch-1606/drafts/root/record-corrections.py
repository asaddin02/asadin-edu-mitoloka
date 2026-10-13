import json, pathlib, datetime, hashlib, shutil
p = pathlib.Path('data/artwork-generated/batch-1606')
queue_path = p / 'drafts/root/user-correction-queue.json'
queue = json.loads(queue_path.read_text())
notes = {
'hatmehit': 'Substantial opaque linen replaces sheer fabric. Fish crown, forward gesture and ordinary myrrh smoke remain clear.',
'chiwen': 'Wet soft gums, tongue, saliva and flexible scales make the short hornless fish-dragon visibly alive while it lunges over the roof.',
'carbuncle-legendary-creature': 'A mature small dog with a red head mirror snatches a belt. Narrow eyes, adult teeth and low close camera remove the cute puppy appearance.',
'namaka': 'A solid female actor steps toward the viewer while extending a five-finger palm. A tidal wall destroys houses. Female personification derives from chiefess and hand-to-hand narratives.',
'panhu': 'A dog-headed human with human hands and clothed legs climbs from a golden vessel documented in the c04 quotation. The incomplete transformation is unmistakable.',
'rep-un-kamuy': 'The young harpoon-bearing human directs an adult whale and calf toward the shore amid moving seawater. Both normal arms and opaque clothes are visible.',
'tangaroa': 'The personified atua moves between two huge tidal walls, gripping a clearly pointed spear. Water domain and human action replace the ordinary whale.',
'dirawong': 'The living goanna at headland scale physically opens a flowing river channel. Five-clawed front feet, displaced banks and creator action dominate.',
'wd-q11244093': 'A white dragon with an expressive dragon head swoops through clouds. Conventional mane, whiskers and antlers are explicitly editorial category details. The subject replaces the waterspout.',
'wd-q757989': 'A broad dragon head uncoils around a stele top with physical contact dust. Conventional dragon rendering is documented as editorial; it reads as a dragon rather than a snake.',
'yellow-dragon': 'A yellow dragon rears from soil with a dominant expressive head. Earth domain is contextual; no earthquake or beam is invented. Conventional dragon features are editorial.',
'panlong-mythology': 'An aquatic dragon rises from its tight water coil. A broad jaw, beard and whiskers distinguish its hornless editorial rendering from an ordinary snake.',
'ao-guang': 'A royal anthropomorphic dragon king greets from the palace amid torrential rain. Two normal hands and opaque robes; dragon head and crown are explicit editorial choices.',
'pincoya': 'The sea spirit rises within water and dances facing the sea. Dense fish schools show fertility; human legs, opaque dress and protective cheerfulness remain.',
'anchimayen': 'A small airborne child with a cold fixed gaze visibly dazzles an adult who shields his eyes. Opaque clothes, a solid body and sourced light replace the abstract fireball and cute first replacement.'
}
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
registry, ledgers, backed = {}, {}, set()
for row in queue:
    slug = row['slug']
    receipt = json.loads(pathlib.Path(row['receipt_path']).read_text())
    sha = hashlib.sha256(pathlib.Path(receipt['original_file']).read_bytes()).hexdigest()
    assert sha == receipt['native_sha256']
    number = '01' if slug in ['hatmehit','chiwen','carbuncle-legendary-creature','pincoya'] else '02' if slug in ['panhu','rep-un-kamuy','wd-q11244093','wd-q757989','anchimayen'] else '03'
    sheet = str(p / f'drafts/root/corrections-qc-{number}.png')
    if slug == 'namaka':
        sheet = 'data/artwork-generated/batch-1406/drafts/root-correction/namaka-correction-200.png'
    record = {'reviewer':'codex','verdict':'pass','reviewed_at':now,'native_sha256':sha,'original_file':receipt['original_file'],'notes':'Root inspected native PNG: '+notes[slug],'sangar_checks':[True]*7,'thumbnail_200_reviewed':True,'thumbnail_notes':'Root inspected exact 200px thumbnail; correction addresses the supplied Claude rejection. '+notes[slug],'thumbnail_sheet':sheet}
    registry[slug] = record
    row.update(status='awaiting-independent-review',new_native_sha256=sha,root_native_and_thumbnail_pass=True)
    ledger_path = row['ledger']
    if ledger_path not in ledgers:
        ledgers[ledger_path] = json.loads(pathlib.Path(ledger_path).read_text())
    item = next(i for i in ledgers[ledger_path]['items'] if i['slug'] == slug)
    item.update(status=receipt['status'],receipt_path=row['receipt_path'],original_file=receipt['original_file'],native_sha256=sha)
    old_registry = pathlib.Path(row['receipt_path']).parent / 'drafts/root/root-native-reviews.json'
    if old_registry.exists():
        backup = old_registry.with_name('root-native-reviews-before-corrections-20261013.json')
        if str(old_registry) not in backed:
            if not backup.exists():
                shutil.copyfile(old_registry, backup)
            backed.add(str(old_registry))
        old = json.loads(old_registry.read_text())
        old[slug] = record
        old_registry.write_text(json.dumps(old,ensure_ascii=False,indent=2)+'\n')
    print(slug, 'history',len(receipt['rejected_attempts']))
for ledger_path, ledger in ledgers.items():
    pathlib.Path(ledger_path).write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
(p / 'drafts/root/correction-native-reviews.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n')
queue_path.write_text(json.dumps(queue,ensure_ascii=False,indent=2)+'\n')
