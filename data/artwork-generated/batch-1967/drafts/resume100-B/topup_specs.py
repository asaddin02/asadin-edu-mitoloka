import json,pathlib
ledger=json.load(open('data/artwork-batch-1977.json')); folder=pathlib.Path('data/artwork-generated/batch-1977/drafts/resume100-B');folder.mkdir(parents=True,exist_ok=True)
def make(slug,variant,an,eff,setting,moment,surface,light,anids,effids,setids,dis,choices):
 ids=lambda a:[f'{slug}-c{x:02}' for x in a]; item=next(i for i in ledger['items'] if i['slug']==slug)
 prompt=f'''ONE original square premium painterly cinematic Mitoloka illustration of {item['canonical_name']}, {variant}.
ANATOMY: {an} [{', '.join(ids(anids))}]
MOMENT: {moment}
POWER: {eff} [{', '.join(ids(effids))}]
SCALE & CAMERA: extreme low angle, close foreshortened framing; {('documented gigantic size, subject fills the square' if slug in ['ao','apalpador'] else 'normal human size, dominance through close framing only, no giant scale')}.
LIGHT & WEATHER: {light}, sharp rim light, deep shadows, dark walnut and antique gold with one strong accent.
SURFACE: {surface}.
SETTING: {setting} [{', '.join(ids(setids))}]
MOOD: benevolent and awe-inspiring, imposing supernatural presence, never evil, cute, calm or decorative.
HARD CONSTRAINTS: no text, writing, lettering, glyphs, inscriptions, pseudoinscriptions, symbols, logo, border, frame or watermark; no extra heads, eyes or limbs; no design borrowed from film, game, anime or comic; no nudity or explicit gore; no generic glow aura, neon outline, floating runes or energy ribbons.'''
 d=dict(slug=slug,worker='codex',worker_agent='resume100_b',subagent_model='gpt-6.1-sol',subagent_reasoning_effort='high',tool='OpenAI built-in image_gen',image_model='tidak dilaporkan alat',status='draft',review_path=item['review_path'],batch=1977,rationale=ledger['user_policy']['intent'],prompt=prompt,depicted_variant=variant,basis_claim_ids=list(dict.fromkeys(ids(anids+effids+setids))),visual_requirements=[dict(kind='anatomy',description=an,claim_ids=ids(anids)),dict(kind='effect',description=eff,claim_ids=ids(effids)),dict(kind='setting',description=setting,claim_ids=ids(setids))],claim_classification=dict(anatomy=ids(anids),power_domain_deeds=ids(effids),setting=ids(setids),disposition=ids(dis)),aura=eff+' '+','.join(ids(effids)),artistic_choices=choices,generation_failures=[],rejected_attempts=[])
 (folder/f'{slug}-spec.json').write_text(json.dumps(d,ensure_ascii=False,indent=2))
make('amilamia','golden-haired benevolent cave spirit with inexhaustible flour sieve',
'One woman with long golden-blond hair reaching the ground, one head two eyes two arms two legs under fully opaque plain earth-brown long wool dress; one golden comb in one hand and one EMPTY wooden sieve held high in other hand; no horns wings animal feet or invented anatomy',
'A thick continuous waterfall of FLOUR pours from an visibly EMPTY sieve, flour lands in a large real powder heap at bottom foreground; dry white flour powder with falling grains, no water or light beams. Her documented inexhaustible flour-giving sieve supports the poor',
'Lezao cave beside a dark reflecting pool; hair touches cave floor',
'Raise the empty sieve toward viewer while combing long hair with golden comb, face grave and compassionate, falling flour crosses lower foreground, hair sweeps downward to ground. Empty upper mesh of sieve visible, nothing inside it although flour pours beneath',
'real long golden hair, rough opaque wool, plain wood and open sieve mesh, dry flour dust and damp limestone',
'one low warm shaft from cave mouth',[2],[4,5],[1,2],[1,5],['No unsupported lamia animal legs. Opaque wool dress editorial modest clothing. Flour is specific c04 physical manifestation, not generic magical light; normal human scale.'])
make('ao','gigantic marine turtle bearing exactly three islands on its back in Bohai Sea',
'One GIGANTIC marine turtle, one turtle head two eyes one beaked mouth, exactly FOUR sea-turtle flippers and one short turtle tail. Normal sea-turtle anatomy, no dragon horns whiskers fangs or human limbs. On broad upper shell are exactly THREE distinct rocky forested island peaks, countable and separated by deep valleys',
'Carry three rocky islands on its back while driving four flippers through dark sea, head and front flippers forcing a bow wave toward viewer; water physically crashes over immense shell edges, no other magic',
'Bohai Sea, tiny ocean boat near massive turtle jaw gives documented gigantic scale, three distinct islands visibly rooted on shell',
'Surge toward viewer from beneath sea surface, enormous turtle head fills lower center and eyes command viewer, front flippers sweep outward and rear flippers visible farther back. High shell arches behind with exactly three separate small islands on it, subject turtle takes at least 75 percent of image',
'ancient dark wet turtle scutes, leathery sea-turtle skin, seawater foam, rough island rock and tiny trees',
'one low amber sun through deep sea cloud',[1,4,6],[4],[4],[1],['Choose Bohai three-island account c04 exclusively; no severed legs or Nüwa scene. Giant scale supported c06. No dragon-turtle Bixi anatomy.'])
make('apalpador','ragged giant charcoal-burner bringing chestnuts from Galician mountains',
'One GIANT adult male charcoal-burner in fully opaque ragged plain brown wool shirt, long trousers and worn boots, one head two eyes two arms two legs, soot-dark hands and weathered human face; no horns weapon crown or Santa costume',
'Offer a generous handful of real chestnuts toward foreground as he enters a house on winter festival night; he brings food and good wishes, no magical effect or destruction',
'Rural house in eastern Galician mountains at night; low human-size wooden doorway behind his bent shoulders and tiny empty child-size bed in foreground establish giant size, distant mountain slopes seen through doorway',
'Bend an enormous shoulder through low doorway while extending one huge palm full of chestnuts down toward viewer; other hand braces doorway carefully without breaking it, solemn kind face looms close. Huge figure fills square from bent head to boot, empty bed stays tiny',
'coarse tattered opaque wool, soot, cracked boots, real brown chestnut shells and rough timber',
'one low hearth fire inside house',[2,5,10],[2,6],[2,5],[6],['Documented giant c05/c10 gives scale. Soot occupational editorial detail, no invented magic. No children depicted; food offering keeps benevolence. No red Santa outfit or modern gifts.'])
