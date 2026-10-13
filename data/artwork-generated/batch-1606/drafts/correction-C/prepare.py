import json,hashlib,shutil
from pathlib import Path
base=Path('data/artwork-generated/batch-1606')
slug='tata-duende'
r=json.loads((base/(slug+'.json')).read_text())
i=1
while (base/'rejected'/f'{slug}-attempt-{i:02}.json').exists() or (base/'rejected'/f'{slug}-attempt-{i:02}.png').exists(): i+=1
arc=base/'rejected'/f'{slug}-attempt-{i:02}.png'; ar=arc.with_suffix('.json');arc.parent.mkdir(exist_ok=True)
old=Path(r['original_file']);assert hashlib.sha256(old.read_bytes()).hexdigest()==r['native_sha256']
shutil.copy2(old,arc)
a=dict(r);a.update(original_file=str(arc),reason=r['correction_notes']);ar.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
rej=r.get('rejected_attempts',[])+[{'original_file':str(arc),'receipt_file':str(ar),'native_sha256':r['native_sha256'],'reason':r['correction_notes']}]
prompt='''ONE original square premium painterly cinematic Mitoloka illustration of TATA DUENDE, the small elderly guardian of Belize's jungle, with backward feet and hands without thumbs.
ANATOMY: Exactly ONE small elderly bearded man, ONE head, TWO eyes, TWO arms, TWO legs; tall weathered brown hat, opaque rough dark tunic and opaque cropped trousers. Each of TWO raised open palms is completely visible and has EXACTLY FOUR long separate fingers and NO THUMB, no fifth digit, no thumb stub, continuous smooth thumb-free outer palm edges. [tata-duende-c02, tata-duende-c08, tata-duende-c13]
MOMENT: Stride across the jungle path to block an intruder, turning his stern weathered face toward the viewer and lifting both thumbless palms in an authoritative warning. Both palms must face the camera, all FOUR digits on each hand visibly separated.
FOOT ORIENTATION, CRITICAL: Show BOTH bare feet clearly from the side, entirely below the cropped trousers. His chest, hips, knees and walking direction face the LEFT edge of image. But BOTH bare feet are turned 180 degrees at the ankles, pointing toward the RIGHT edge: both rounded HEELS are at the LEFT ends of the feet, and both TOE GROUPS at the RIGHT ends, behind the body. Do not paint ordinary forward feet. Each ankle joins near its left heel, with the long instep and toes extending rightward, anatomically reverse to the left-facing knees. Space the two legs so both reversed feet are visible, not overlapped. [tata-duende-c08, tata-duende-c13]
POWER: A documented good forest guardian makes a forceful physical stop gesture, with no supernatural emission, no shapeshifting, no wounds or victims. [tata-duende-c02, tata-duende-c05, tata-duende-c12, tata-duende-c14]
SCALE & CAMERA: Ground-level close full-body view, strong three-quarter SIDE view of torso oriented left, face turned to us. Small stature stays clear beside huge nearby roots and broad jungle leaves; subject dominates through close framing, NOT giant scaling. Two raised palms, full tall hat and BOTH backward bare feet all in frame.
LIGHT & WEATHER: ONE hard late sunset shaft through a dark canopy, copper rim light on beard, palms and heels, deep walnut shadows; disturbed leaf litter at his step. No colored magic fog.
SURFACE: Craggy elderly skin, coarse beard, battered woven hat, heavy rough opaque cloth, moist roots and torn leaves; solemn protective authority, tactile and believable.
SETTING: Tangled tropical jungle in Belize, dark forest path and roots. [tata-duende-c02, tata-duende-c05]
MOOD: Awe-inspiring, uncanny and imposing protective spirit, stern commanding stare; never cute, cheerful, comic, calm or decorative.
HARD CONSTRAINTS: Native square PNG minimum 1024. No text, lettering, logo, border, frame or watermark; no extra heads, limbs or fingers; FOUR fingers only on each of TWO hands, ZERO thumbs. BOTH feet point right although knees and torso point left. No design borrowed from film, game, anime or comic; no nudity or explicit gore; no generic glow aura, neon outline or energy ribbons.'''
r.update(prompt=prompt,rejected_attempts=rej,worker_agent='correction-C',subagent_model='gpt-6.1-sol',subagent_reasoning_effort='high',basis_claim_ids=['tata-duende-c02','tata-duende-c08','tata-duende-c13','tata-duende-c05','tata-duende-c12','tata-duende-c14'],visual_requirements=[{'kind':'anatomy','description':'Small elderly bearded man with tall hat; one head/two eyes/two arms/two legs, opaque tunic and cropped trousers. Both visible raised palms have exactly FOUR fingers and ZERO thumbs. In side view torso and knees point left while BOTH bare feet point right, with heels left and toes behind the ankles on right.','claim_ids':['tata-duende-c02','tata-duende-c08','tata-duende-c13']},{'kind':'effect','description':'Good guardian blocks forest path with a commanding physical warning; no emitted magic or shapeshifting.','claim_ids':['tata-duende-c02','tata-duende-c05','tata-duende-c12','tata-duende-c14']},{'kind':'setting','description':'Belize tropical jungle with nearby roots and leaves confirming small stature.','claim_ids':['tata-duende-c02','tata-duende-c05']}])
(base/'drafts'/'correction-C'/f'{slug}-correction-01.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
(base/'drafts'/'correction-C'/f'{slug}-correction-01.prompt.txt').write_text(prompt)
print('Archived',arc,ar,'; persisted requirements + prompt')
