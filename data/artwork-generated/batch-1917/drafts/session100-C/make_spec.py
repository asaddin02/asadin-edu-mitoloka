import json,pathlib,sys
root=pathlib.Path('.')
def spec(batch,slug,variant,req,classes,aura,choices,prompt):
 d=dict(slug=slug,batch=batch,depicted_variant=variant,basis_claim_ids=list(dict.fromkeys(c for r in req for c in r['claim_ids'])),visual_requirements=req,claim_classification=classes,aura=aura,artistic_choices=choices,prompt=prompt)
 p=root/f'data/artwork-generated/batch-{batch}/drafts/session100-C/{slug}-spec.json';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');return d
def req(k,d,*c):return dict(kind=k,description=d,claim_ids=list(c))
spec(1917,'lobisomem','Brazilian werewolf variant lunging along a moonlit road.',[req('anatomy','One werewolf, one wolf-like head, two ears, two eyes, two arms and two legs.','lobisomem-c01'),req('effect','Nighttime attack on road; no visible supernatural aura.','lobisomem-c06'),req('setting','Road at full-moon night.','lobisomem-c05','lobisomem-c06')],dict(anatomy=['lobisomem-c01'],power_or_deed=['lobisomem-c06'],setting=['lobisomem-c05','lobisomem-c06'],disposition=['lobisomem-c06']),'Threat comes from the werewolf form c01 attacking along the road c06.', ['Werewolf version selected rather than incompatible pig or fireball variants.','Framing creates dominance without claiming giant scale.','Torn opaque plain trousers are editorial modesty clothing; no invented magic.'],'''ONE original square premium painterly cinematic Mitoloka illustration of Lobisomem, the Brazilian werewolf of folklore.
ANATOMY: one wolf-man with exactly one snarling wolf head, two wolf ears, two natural eyes, two muscular arms, two digitigrade legs, dense coarse dark fur, long muzzle and visible fangs; opaque plain torn trousers conceal the waist. [lobisomem-c01]
MOMENT: lunge out of the road's darkness toward the viewer, one clawed forehand raking the earth, jaws opened in a threatening snarl, shoulders violently twisted.
POWER: no documented visible magical effect; night attack along a road is the documented action [lobisomem-c06]. Only physical dirt displaced by claws.
SCALE & CAMERA: extreme low ground-level angle, tight framing, forehand and wolf muzzle dominate; normal werewolf bodily scale, not a giant.
LIGHT & WEATHER: one dominant full moon through dark clouds, sharp pale rim light, warm deep shadows, ordinary road dust.
SURFACE: coarse matted fur, dirty claws, rough muzzle skin, worn opaque cloth.
SETTING: rural Brazilian dirt road at full-moon night [lobisomem-c05, lobisomem-c06].
MOOD: dangerous, menacing and imposing, predatory confrontation, never cute, calm or decorative.
HARD CONSTRAINTS: no text, pseudoinscriptions, lettering, logo, border, frame or watermark; no extra heads, limbs or fingers; no design borrowed from film, game, anime or comic; no nudity or explicit gore; no generic glow aura, neon outline, magic symbols or energy ribbons.''')
