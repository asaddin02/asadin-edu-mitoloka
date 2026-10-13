import json
from pathlib import Path
ROOT=Path('/home/asadin/Portfolio/asadin-edu/asadin-mythological-creatures')
B=ROOT/'data/artwork-generated/batch-1456';D=B/'drafts/lane-B'
L=json.loads((ROOT/'data/artwork-batch-1456.json').read_text());items={x['slug']:x for x in L['items'][17:34]}
def make(slug,identity,anatomy,moment,power,setting,requirements,variant,choices,aura,surface,lighting='one low warm sunset shaft; deep walnut shadows and strong rim light',camera='extreme low angle; close foreshortened framing creates dominance, no invented gigantic size'):
 x=items[slug];req=[dict(kind=k,description=d,claim_ids=[slug+'-'+c for c in cs.split(',')]) for k,d,cs in requirements];ids=list(dict.fromkeys(c for r in req for c in r['claim_ids']));assert set(ids)<=set(c['id'] for c in x['research']['claims'])
 p=f'''ONE original square premium painterly cinematic Mythics illustration of {x['canonical_name']}, {identity}. Native square PNG at least 1024 by 1024 pixels.
ANATOMY: {anatomy}
MOMENT: {moment}
POWER: {power}
SCALE & CAMERA: {camera}
LIGHT & WEATHER: {lighting}
SURFACE: {surface}
SETTING: {setting}
MOOD: imposing and awe-inspiring or menacing according to documented character; never cute, calm, tame or decorative. Being dominates and is striking at200px.
HARD CONSTRAINTS: no text, lettering, glyphs, logos, border, frame or watermark; no extra heads, eyes, limbs or fingers; no designs from films, games, anime or comics; no nudity, gore or visible wounds; no generic luminous aura, neon outline, energy ribbons or coloured magical fog. Bracketed claimIDs are instructions, never visible text.'''
 r=dict(slug=slug,worker='codex',worker_agent='lane-B',subagent_model='gpt-6.1-sol',subagent_reasoning_effort='high',tool='OpenAI built-in image_gen',image_model='tidak dilaporkan alat',status='draft-before-generation',review_path=x['review_path'],batch=1456,rationale=L['user_policy']['intent'],prompt=p,depicted_variant=variant,basis_claim_ids=ids,visual_requirements=req,aura=aura,artistic_choices=choices,generation_failures=[],rejected_attempts=[])
 pth=D/(slug+'-request.json');assert not pth.exists();pth.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');(D/(slug+'-exact-tool-request-attempt-01.json')).write_text(json.dumps({'prompt':p,'transparent_background':False},ensure_ascii=False,indent=2)+'\n')
make('hudson-river-monster','Kipsy in the alleged1886 huge-headed sea-serpent account',
 'one huge serpent head with two eyes, one long limbless serpentine body; no horns, ears, wings, fins or invented dinosaur anatomy [hudson-river-monster-c01, hudson-river-monster-c06]',
 'REAR from dark river water toward the low viewer, great head rising ten feet above surface and body turning behind, jaws parting without exaggerated fangs',
 'no documented supernatural power; only physical river splash from the reported rearing movement [hudson-river-monster-c06]',
 'Hudson River with distant banks kept minimal, no Statue of Liberty or named building [hudson-river-monster-c01, hudson-river-monster-c06]',
 [('anatomy','Reported100-foot sea serpent with huge head','c01,c06'),('effect','Rearing up to ten feet from river, physical splashes','c06'),('setting','Hudson River','c01,c06')],
 'Alleged1886 hundred-foot sea serpent account; not2006 manatee and not claimed real species.',
 ['Reports are depicted as folklore, not zoological confirmation. Brown wet scales and dusk are editorial. No supernatural power or copied mural; serpent anatomy kept minimal.'],
 'Threat comes from the reported huge head and rearing serpent body (hudson-river-monster-c06).','wet slate-brown scales and dark river spray',camera='extreme low waterline angle; documented100-foot body trails behind head, near splashes give scale')
make('huoshu','the large fire-dwelling white-haired mouse of the Shenyijing account',
 'one natural mouse head with two eyes and two round ears, four rodent legs and one long rodent tail; exceedingly long fine WHITE silklike hairs, no horns or reptile parts [huoshu-c04, huoshu-c07]',
 'EMERGE toward viewer from fire between inexhaustible tree trunks, white hair streaming, forepaws climbing over a glowing ember while head peers down directly',
 'animal lives within real fire; fur shows red firelight in fire and white outside, not a magic energy outline or flame breath; trees withstand the fire [huoshu-c02, huoshu-c07, huoshu-c09]',
 'southern Fire Mountain amid inexhaustible trees, as Shenyijing account [huoshu-c09]',
 [('anatomy','Mouse with long fine white hair, thousand-jin weight in selected Shenyijing version','c04,c07'),('effect','Dwells in fire/red while inside, white fur when outside','c02,c07'),('setting','Fire Mountain/inexhaustible trees','c09')],
 'Shenyijing thousand-jin long white-haired mouse, not rat-sized Yan-island variant.',
 ['Fire is documented habitat, not projected fire attack. Large apparent mass grounded thousand-jin source; do not add human victim. Pink rodent nose and fine tail are editorial natural mouse rendering.'],
 'Awe comes from the great white-haired mouse emerging unhurt from fire in inexhaustible trees (huoshu-c07, huoshu-c09).','singed-looking white silky strands lit by real flames, mouse skin, ember and unconsumed bark',
 'real habitat fire is only dominant orange-red light; deep black tree shadows, sparks physically from fire',
 'extreme low angle, large documented thousand-jin mouse fills frame, ordinary small embers and tree base for scale')
make('jackalope','the dangerous horned jackrabbit of North American tall tales',
 'one jackrabbit head, two eyes, two long hare ears, exactly two pointed ANTELOPE horns, four hare legs and short hare tail; horns pointed and modestly forked like antelope, NOT deer antlers; natural hare incisors only, no carnivore fangs [jackalope-c05]',
 'CHARGE low toward viewer with horns thrust forward, long ears swept backward, forepaws airborne and hindlegs launching; sharp intent eyes',
 'documented goring danger conveyed by the thrust horns, no invented magic or lightning power [jackalope-c14]',
 'dark ground at an Old West campfire setting of its tale, small fire edge only, no cowboys or signs [jackalope-c15]',
 [('anatomy','Jackrabbit with antelope horns','c05'),('effect','Danger of goring expressed in low charge','c14'),('setting','Old West campfire setting','c15')],
 'Living jackrabbit with antelope horns, not taxidermy deer-antler variant or Persian unicorn rabbit.',
 ['Fur colour and ground are editorial. No supernatural effect; charge and goring risk from c14. Close framing rather than invented giant size; no cartoon eyes or fangs.'],
 'Danger comes from horn-first motion and source goring warning (jackalope-c05, jackalope-c14).','coarse dusty hare fur, ridged keratin horns, rough earth',
 'single campfire side light, deep brown night shadows, ordinary dust kicked by feet')
make('jiaotu','the frog-like door-ring guardian among Chinese dragon sons',
 'one living FROG-LIKE head, two eyes and broad amphibian mouth holding one plain heavy iron door ring; head and throat only, lower body/limbs outside crop; no dragon horns, beard, whiskers or snail shell combined [jiaotu-c02, jiaotu-c04]',
 'CLAMP its broad mouth around door ring and TURN directly toward approaching viewer at the closed doorway, muscles tensing; determined living guardian not a metal carving',
 'no documented power; physical clamp and wary gaze express dislike of strangers entering, no magically slamming doors [jiaotu-c03, jiaotu-c04]',
 'closed door with ring, close cropped and uninscribed [jiaotu-c04]',
 [('anatomy','Selected frog-like form, mouth holding door ring','c02,c04'),('setting','Closed door ring association/aversion to strangers','c03,c04')],
 'Frog-like living guardian and door-ring account, not mixed with primary-text snail form.',
 ['Natural amphibian skin and ring size are editorial. Macro framing supplies awe without enormous bodily scale. No supernatural effect invented. No lower-body or horn count invented; live flesh, not statue.'],
 'Awe comes from the unusual live frog-like door-ring guardian confronting an entrant (jiaotu-c02, jiaotu-c03, jiaotu-c04).','wet pebbled amphibian skin, worn iron ring and old door wood')
make('joint-snake','the Southern American snake said to break apart and rejoin',
 'one serpent head, two eyes, one otherwise limbless continuous snake body; hard parchmentlike smooth skin; rear body split into several short clean segments, with no blood or exposed organs; no extra heads [joint-snake-c01, joint-snake-c02, joint-snake-c05]',
 'SNAP its dry separated tail segments back into alignment as the head rises toward close viewer, gaps between four or five small rear segments clearly visible before reconnection',
 'documented breaking and reassembling physically shown by separated pieces drawing into a single chain; no light ribbons, sparks or aura [joint-snake-c02, joint-snake-c05]',
 'Southern United States tale, neutral dark ground; no specific habitat invented [joint-snake-c01]',
 [('anatomy','Legendary snake, hard smooth stiff skin','c01,c05'),('effect','Breaks in short clean bloodless segments/reassembles','c02,c05'),('setting','SouthernUnitedStates, unspecified ground','c01')],
 'Legendary self-reassembling snake, not a claim that actual glass lizards can rejoin.',
 ['Dry segment boundaries are clean closed surfaces to avoid gore. Brown scale colour and plain ground are editorial. Mythic action shown without inventing actual lizard anatomy or scientific ability.'],
 'Threat comes from bloodless pieces actively drawing into a snake behind its poised head (joint-snake-c02, joint-snake-c05).','glass-smooth matte-brown snake skin, parchment-hard closed segment faces and dry ground')
make('kanas-lake-monster','the unconfirmed giant Red Fish described in the1985 report from Kanas Lake',
 'one massive RED fish, broad head reportedly over a metre wide; one head and two natural fish eyes, scaled fish neck/shoulder cropped close; do not specify taimen species or invent horns, whiskers, extra fins or predatory fangs, mouth partly open with no visible teeth [kanas-lake-monster-c01, kanas-lake-monster-c07]',
 'RISE up against the low viewer from the lake surface, broad red head and shoulder displacing a heavy wave, not a small normal fish at a distance',
 'no documented supernatural powers; displaced water from emergence only, no invented swallowing livestock scene [kanas-lake-monster-c07]',
 'Kanas Lake Xinjiang, far lake shore barely visible [kanas-lake-monster-c01]',
 [('anatomy','Reported giant red fish10–15m with head over1m wide; unconfirmed','c01,c07'),('setting','Kanas Lake Xinjiang','c01')],
 '1985 reported giant Red Fish, intentionally unconfirmed and not identifying it as taimen.',
 ['Red fish report is depicted as a reported form, not species confirmation. Scale pattern and unspeciated fish head are editorial. Only close head/shoulder shows; no invented fin counts or mammal/reptile composite. No supernatural power.'],
 'Awe comes from reported10–15m Red Fish with metre-wide head emerging close (kanas-lake-monster-c07).','wet red-brown fish scales and physically displaced lake water',camera='extreme low waterline view, documented immense head fills frame; lake wave much smaller than head')
make('kanbari-nyudo','the Japanese toilet yokai in Sekien monk-like bird-expelling form',
 'one monk-like human figure with one head/two eyes, two arms/two legs, shaved or balding scalp, fully opaque simple monk robe; one living bird emerging from open mouth, bird has one head/two wings/two legs, no blood or injury [kanbari-nyudo-c02]',
 'LEAN suddenly into dark toilet doorway toward viewer while a bird bursts from his open mouth with wings already beating; one hand grabs doorpost',
 'documented mouth-expelled bird only; no gold head, aura, magic chant glyphs or fox body mixed in [kanbari-nyudo-c02]',
 'old wooden toilet doorway at year end, no fixtures or human visitor shown [kanbari-nyudo-c01, kanbari-nyudo-c07]',
 [('anatomy','Monk-like figure, bird expelled from mouth','c02'),('effect','Physical bird exit from mouth','c02'),('setting','Toilet at year end','c01,c07')],
 'Sekien monk-like bird-expelling depiction, not severed-head or fox anecdote.',
 ['Simple opaque brown robe, bare scalp and small unspeciated bird are editorial monk/bird rendering. Close framing not invented giant scale; no gross bodily functions or toilet use. Frightening supernatural event without gore.'],
 'Uncanny threat comes from the monk-like yokai expelling a live bird from his mouth (kanbari-nyudo-c02).','aged human skin, coarse opaque robe, natural bird feathers and wooden post',
 'single low oil-lamp light outside crop, dark toilet doorway, dusty cold air')
make('kao-bull','the great divine Meitei bull of the Khamba Thoibi epic before its taming',
 'one living great bull, one head/two eyes, two natural bull horns, four hoofed legs and one bovine tail; no wings, jewellery or invented supernatural body parts [kao-bull-c01, kao-bull-c13, kao-bull-c15]',
 'BURST from water-edge reeds toward viewer with head lowered and horns thrust forward, powerful shoulders surging and reed stems bent by bodily contact',
 'no documented magical power; imposing divine bull force conveyed by physical forward motion only, no aura [kao-bull-c13, kao-bull-c15]',
 'reeds bordering the waters of Waithou [kao-bull-c13]',
 [('anatomy','Divine great bull and natural horns','c01,c13,c15'),('setting','Waithou waters and reeds','c13')],
 'Untamed great divine bull at Waithou, before the father-name taming.',
 ['Dark bull coat is editorial. Powerful emergence and lowered horns echo dangerous pre-taming account without showing victim or gore. Respectful formidable divine animal, no demonic redesign or invented giant size beyond great bull.'],
 'Awe comes from the great horned bull forcefully emerging at Waithou (kao-bull-c13, kao-bull-c15).','wet bovine hair, thick keratin horns, mud and snapped real reeds')
make('kerakera-onna','the giant middle-aged Japanese woman yokai laughing over a wall',
 'one gigantic middle-aged woman, one head/two eyes and natural human teeth; two arms/two legs with lower legs hidden behind wall; fully opaque closed kimono, no fangs, horns or invented extra features [kerakera-onna-c03, kerakera-onna-c08, kerakera-onna-c10]',
 'LEAN towering over a much smaller wall directly toward viewer, open mouth in sudden wide cackle and shoulder shaking, hands planted on wall top',
 'documented frightening laugh conveyed by mouth, posture and shaking shoulders, NO sound-energy rings or invented terrorbeam [kerakera-onna-c04, kerakera-onna-c07]',
 'wall beside lonely street or alley [kerakera-onna-c04, kerakera-onna-c11]',
 [('anatomy','Giant middle-aged woman in kimono','c03,c08,c10'),('effect','Laughing over wall, frightening cackle','c04,c07'),('setting','Wall on lonely alley','c04,c11')],
 'Giant kimono-clad middle-aged laughing woman; not a severed head.',
 ['Opaque dark plain kimono and pinned hair are editorial. Giant scale is documented; wall as size reference. Human teeth only, not monsterfangs; cackle rendered as physical action without visible magic.'],
 'Threat comes from enormous laughing woman looming over small wall and alley (kerakera-onna-c03, kerakera-onna-c04, kerakera-onna-c07).','weathered skin, rough plain kimono, old wall plaster',
 'single low amber lantern light, deep alley shadows and ordinary wind',
 'extreme low alley-floor camera, documented giant woman dwarfs ordinary wall; head fills upper half')
make('kinie-ger','the quoll-headed and quoll-bodied hunter with human limbs of Southeastern Australian traditional stories',
 'one quoll head with two eyes/rounded ears, furred quoll torso and one quoll tail; exactly TWO human arms and TWO human legs, human five-finger hands and five-toe feet; fully opaque waist wrap; one plain spear firmly held in a human hand, no armour, motifs or extra limbs [kinie-ger-c01, kinie-ger-c02]',
 'PIVOT from drinking at the waterhole to face viewer, spear coming upward into readiness, one human foot pushing from muddy edge',
 'no documented supernatural power; predatory menace through human-limbed quoll anatomy and spear, no victims shown [kinie-ger-c01, kinie-ger-c02]',
 'waterhole where the ambush story places him [kinie-ger-c03]',
 [('anatomy','Quoll head/body, human limbs','c02'),('anatomy','Hunts with spear','c01'),('setting','Waterhole','c03')],
 'Quoll-headed/quoll-bodied hunter with human limbs before owl/crow ambush.',
 ['Opaque waist wrap and plain unornamented spear are editorial modesty/material choices. Quoll spotted coat is natural animal rendering; no Aboriginal sacred designs invented. No killing, blood, supernatural glow or enlarged giant scale.'],
 'Threat comes from ruthless spear hunter with human limbs on quoll body (kinie-ger-c01, kinie-ger-c02).','matted spotted quoll fur, human skin, rough opaque cloth, plain wood spear and mud')
make('klu','a Ladakh lu/naga water spirit in documented human-torso serpent-tail form',
 'one human head with two eyes, human torso with exactly two human arms, serpent lower body and one long tail instead of legs; fully opaque dark tunic/mantle over torso and opaque wrap at waist-to-tail transition; NO legs, horns, extra heads or snake hood invented [klu-c05]',
 'RISE in a slow commanding bend from spring water toward low viewer, hands held open while physical spring water arches up around the coiled lower serpent body; reverent nature spirit, not a demon',
 'water controlled physically, clear spring water curves upward and pours back over stones under documented water authority; no neon aura or illness effect [klu-c06, klu-c08]',
 'natural spring in Ladakh, plain uninscribed rock and water [klu-c07]',
 [('anatomy','Ladakh naga: human torso with serpent tail','c05'),('effect','Controls water','c06,c08'),('setting','Natural spring affinity in Ladakh','c07')],
 'Ladakh human-torso serpent-tail naga form, not Bon animal-headed composites.',
 ['Human face, fully opaque dark simple clothes and scale colour are editorial generic form, not precise canonical iconography. No jewellery/ritual symbols invented. Reverent awe for living belief, with water only; no visible disease or destructive action.'],
 'Awe comes from documented naga hybrid rising in its physically moving spring water (klu-c05, klu-c06, klu-c08).','natural human skin, rough opaque cloth, dark wet serpent scales and clear spring water')
make('koolakamba','the unconfirmed African ape described by nineteenth-century observers',
 'one ape head with very ROUND head and face, prominent cheekbones and sunken cheeks; whiskerlike black hair runs around face and below chin; two eyes, two arms/two legs, black long arm hair interrupted by partly bare arm skin; no invented gorilla crest or huge fangs [koolakamba-c01, koolakamba-c06, koolakamba-c08, koolakamba-c09, koolakamba-c10]',
 'WITHDRAW into shadow while turning its round face down toward the close viewer, one hand gripping a nearby unfeatured ground edge; alert and shy, not attacking',
 'no documented supernatural power; no attack or violence added to shy hard-to-approach animal [koolakamba-c11]',
 'interior of Gabon Ovenga River region, dim indistinct vegetation only [koolakamba-c03, koolakamba-c11]',
 [('anatomy','Ape, more bipedal/flatter face than chimp, reported male4ft3in','c01,c06,c08'),('anatomy','Round head/face, prominent cheekbones/sunken cheeks, surrounding whiskers','c09'),('anatomy','Black hair long on partly bare arms','c10'),('setting','Interior Ovenga/Gabon region; shy disposition','c03,c11')],
 'Observer-described round-faced black-haired male; unconfirmed ape identity, not proven hybrid.',
 ['Retreating alert turn respects documented shyness, not invented predator behaviour. No huge scale; close camera gives imposing encounter. Ground/vegetation texture and dusky lighting editorial. No supernatural effect or species certainty.'],
 'Awe comes from close encounter with unusually round-faced reported ape, not invented aggression (koolakamba-c06, koolakamba-c09, koolakamba-c11).','coarse black hair, partly bare arm skin, strongly modelled cheekbones and natural vegetation',
 'one warm shaft through dim vegetation, deep shadow obscures background, no visible magical effect')
make('kui-chinese-mythology','Kui of the Liubo mountain Shanhaijing oxlike one-footed account',
 'one OX head with two eyes/two natural ox ears and absolutely NO HORNS; blue-green oxlike body, exactly ONE single central leg ending in ONE hoof beneath belly; all sides shown so no hidden legs exist; NO other legs, arms, wings or human face; one ox tail [kui-chinese-mythology-c05]',
 'BOUND out of water toward viewer balanced on its ONE central hoof, all body limbs fully readable against spray, head held forward with radiant gaze',
 'its emergence brings WIND AND RAIN; rain driven across real spray and watersurface. Glare like sun and moon lights wet rain from the face, not generic body aura; voice thunder suggested by open ox muzzle, NO lightning beam or bolt invented [kui-chinese-mythology-c06]',
 'waters at Liubo mountain in East Sea, rock outline behind subordinate [kui-chinese-mythology-c05]',
 [('anatomy','Blue-green oxlike body, NOhorns, exactly one foot','c05'),('effect','Water emergence causes wind/rain; glare like sun/moon, voice like thunder','c06'),('setting','Liubo mountain East Sea','c05')],
 'Shanhaijing hornless blue-green one-footed ox form; no musician, red drum or human-faced ape mixture.',
 ['Central placement and broad single hoof are editorial staging of explicit one-foot anatomy. Gaze illumination tied only to c06; no lightning inferred from thunder voice. No terrifying gore; overwhelming nature-being awe.'],
 'Awe comes from single-footed hornless blue-green ox and emergence bringing wind/rain plus sun/moonlike glare (kui-chinese-mythology-c05, kui-chinese-mythology-c06).','wet blue-green ox hair, single keratin hoof, heavy rain and sea spray',
 'documented face glare is dominant warm pale light, rain rim-lit against deep sea-storm shadows',
 'extreme low shoreline camera, close whole body visibly containing exactly one central leg, no cropped/hidden legs')
make('langben-rese','the Nordic ballad giant at Skottfjället before the duel with Vidrik',
 'one living human-shaped giant, one head/two eyes, exactly two arms/two legs; fully opaque heavy tunic and trousers, no horns, fangs or invented magical attributes [langben-rese-c01, langben-rese-c03]',
 'STRIDE down toward the viewer from mountain rocks, one huge empty fist thrust forward in challenge and other arm braced behind; intact before the duel, no beheading scene',
 'no documented supernatural power; intimidating giant motion and size only [langben-rese-c01, langben-rese-c03]',
 'Skottfjället near Brattön in Bohuslän, rough mountain rocks [langben-rese-c02]',
 [('anatomy','Nordic giant, intact before duel','c01,c03'),('setting','Skottfjället near Brattön Bohuslän','c02')],
 'Living intact giant before duel, not the subsequent headless run.',
 ['Fully opaque rough tunic/trousers, beard and weathered human face are editorial, not source iconography. No invented weapons or powers. Giant size documented; small mountain rocks frame towering body without invented architecture.'],
 'Threat comes from a giant striding down into a confrontational duel moment (langben-rese-c01, langben-rese-c03).','weathered human skin, coarse dark opaque cloth and rock dust',camera='extreme low mountain-foot camera, documented giant towers over smaller rocks, full torso and charging legs visible')
make('luduan','the auspicious lion-headed composite Luduan, not the similar Jiaoduan deer account',
 'one LION head with two eyes, exactly ONE RHINO horn on nose; dragonlike long scaled body, exactly four BEAR paws with bear claws, wet overlapping FISH scales; one OX tail with terminal hair tuft. No antlers, deer head, horse tail, wings, extra horns or extra heads [luduan-c01, luduan-c02]',
 'SWEEP forward in a bounding stride toward viewer, lion head lowered commandingly and bear forepaws reaching; powerful auspicious presence, not evil monster',
 'documented swift travel conveyed through physical bounding movement and ordinary dust, no energy trails or language glyphs [luduan-c03]',
 'near an enlightened ruler throne setting, plain blurred architectural edge only, drawn from auspicious imperial association; no text or people [luduan-c04, luduan-c07]',
 [('anatomy','Lionhead/rhinohorn','c01'),('anatomy','Dragonbody, bear paws, fishscales, oxtail','c02'),('effect','Rapid travel','c03'),('setting','Imperial auspicious throne association','c04,c07')],
 'Composite lion/rhino/dragon/bear/fish/ox form from c01/c02; not conflated with Jiaoduan one-horned green deer.',
 ['Living being, not an incense burner or ornamental statue. Bronze-brown colour, scale pattern and architectural edge editorial. One nasal horn staged clearly; no supernatural aura, magic speech or cruelty.'],
 'Awe comes from unmistakable composite anatomy and very swift movement (luduan-c01, luduan-c02, luduan-c03).','rough lion fur, rhino keratin, overlapping fish scales, bear fur paws and ox-tail tuft')
make('maushop','Moshup, the benevolent Wampanoag giant provider at Aquinnah',
 'one intact human giant, one head/two eyes, two arms/two legs; fully opaque plain rough tunic and knee-length wrapped garment covers torso and pelvis; no invented headdress, feathers, warpaint, tattoos or ritual symbols [maushop-c01, maushop-c08]',
 'LOWER a huge boulder from both hands into the ocean ahead of himself to make a stepping stone, body bending protectively toward shore, benevolent provider rather than destructive fighter',
 'documented immense boulder-placement makes stepping stones, physically driving a circle of displaced seawater around boulder; no magical energy or gore [maushop-c04]',
 'Aquinnah Cliffs Martha Vineyard and ocean below, cliffs small alongside documented giant [maushop-c02, maushop-c10, maushop-c12]',
 [('anatomy','Benevolent giant human hero','c01,c08'),('effect','Places thrown boulders in ocean as steppingstones','c04'),('setting','AquinnahCliffs/Ocean/MarthaVineyard','c02,c10,c12')],
 'Benevolent Aquinnah giant making ocean stepping stones, no whale-killing episode or demonic redesign.',
 ['Human facial details and fully opaque unornamented clothing editorial, not claims of specific tribal costume. Respectful living Wampanoag tradition; no stereotypes or sacred motifs. Massive scale grounded c04/c08; no victim or gore.'],
 'Reverent awe comes from benevolent giant forming ocean stepping stones with boulders (maushop-c04, maushop-c08).','weathered human skin, coarse opaque cloth, giant boulder stone and ocean spray',
 'one golden sunset shaft silhouettes giant and illuminates water splash; deep walnut cliff shadows',
 'extreme low shore camera looking up, giant dominates, smaller AquinnahCliffs and ocean give documented scale')
x=items['khambrangchak'];r=dict(slug=x['slug'],worker='codex',worker_agent='lane-B',subagent_model='gpt-6.1-sol',subagent_reasoning_effort='high',tool='OpenAI built-in image_gen',image_model='tidak dilaporkan alat',status='tidak-digambar',review_path=x['review_path'],batch=1456,rationale=L['user_policy']['intent'],reason='Riset hanya memberi burung wagtail (identifikasi yellow/whitepied berbeda antarpeneliti, khambrangchak-c04), kebiasaan merapikan bulu/rias wajah (c05), serta mencuci kaki dan digigit kepiting di sungai (c06/c07). Tidak ada tubuh supernatural, skala besar, kuasa, atau manifestasi aktif yang bisa membuat gambar agung/berbahaya tanpa mengarang. Adegan burung biasa dan kepiting akan gagal Uji Sangar; tidak mengubahnya menjadi monster/giant.',basis_claim_ids=['khambrangchak-c04','khambrangchak-c05','khambrangchak-c06','khambrangchak-c07'],visual_requirements=[],generation_failures=[],rejected_attempts=[],artistic_choices=['Menolak menggambar daripada mengarang anatomi/power atau mengubah disposisi burung folklor.'])
pth=B/'khambrangchak.json';assert not pth.exists();pth.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
