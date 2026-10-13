import json
from pathlib import Path
ROOT=Path('/home/asadin/Portfolio/asadin-edu/asadin-mythological-creatures')
B=ROOT/'data/artwork-generated/batch-1406'
D=B/'drafts/lane-B'
L=json.loads((ROOT/'data/artwork-batch-1406.json').read_text())
items={x['slug']:x for x in L['items'][17:34]}
def make(slug, identity, anatomy, moment, power, setting, requirements, variant, choices, aura, surface, lighting='a single slanting warm sunset shaft, deep walnut shadows, strong rim light', camera='extreme low angle, tight foreshortened framing; no invented gigantic size'):
    x=items[slug]
    req=[dict(kind=k,description=d,claim_ids=[slug+'-'+c for c in cs.split(',')]) for k,d,cs in requirements]
    ids=list(dict.fromkeys(c for r in req for c in r['claim_ids']))
    assert set(ids)<=set(c['id'] for c in x['research']['claims'])
    p=f'''ONE original square premium painterly cinematic Mythics illustration of {x['canonical_name']}, {identity}. Native square PNG at least 1024 by 1024 pixels.
ANATOMY: {anatomy}
MOMENT: {moment}
POWER: {power}
SCALE & CAMERA: {camera}
LIGHT & WEATHER: {lighting}
SURFACE: {surface}
SETTING: {setting}
MOOD: imposing and awe-inspiring or menacing as appropriate to the documented character; never cute, calm or decorative. The creature itself dominates and remains striking at 200 pixels.
HARD CONSTRAINTS: no text, lettering, glyphs, logo, border, frame or watermark; no extra heads, limbs or fingers; no design borrowed from any film, game, anime or comic; no nudity or explicit gore; no generic glow aura, neon outline, coloured magic mist or energy ribbons. Bracketed claim IDs are instructions, never visible text.'''
    r=dict(slug=slug,worker='codex',worker_agent='lane-B',subagent_model='gpt-6.1-sol',subagent_reasoning_effort='high',tool='OpenAI built-in image_gen',image_model='tidak dilaporkan alat',status='draft-before-generation',review_path=x['review_path'],batch=1406,rationale=L['user_policy']['intent'],prompt=p,depicted_variant=variant,basis_claim_ids=ids,visual_requirements=req,aura=aura,artistic_choices=choices,generation_failures=[],rejected_attempts=[])
    (D/(slug+'-request.json')).write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
make('skinfaxi','the Norse horse whose shining mane lights the sky and earth',
 'one horse head, two eyes, four hooved legs, no wings or horns; mane and tail shining like gold; simple chariot traces taut behind it, chariot only a small partial edge with no driver visible [skinfaxi-c01, skinfaxi-c02]',
 'SURGE past the low viewer through the sky, forelegs thrust forward in a powerful mid-gallop, neck bent and eye intent',
 'golden light originates in actual mane and tail hairs, illuminating cloud faces and the dark earth far below; not flame breath or magical ribbons [skinfaxi-c01, skinfaxi-c02, skinfaxi-c09]',
 'sky traversed by the horse of Day, earth visible beneath [skinfaxi-c01]',
 [('anatomy','Horse; gold-shining mane and tail; harnessed to Day chariot','c01,c02'),('effect','Mane illuminates sky and earth','c01,c02,c09'),('setting','Sky with earth below','c01')],
 'Skinfaxi drawing Day through the sky, gold-shining mane and tail account.',
 ['Chestnut coat and simple unadorned traces are editorial; no claim of canonical coat colour. Close camera creates dominance without enlarging the horse. Driver deliberately excluded because his iconography is not specified.'],
 'Awe comes from light shed by the gold-shining mane onto sky and earth (skinfaxi-c01, skinfaxi-c02, skinfaxi-c09).','coarse mane strands, short horse coat and worn harness',
 'mane itself is the sole dominant golden light, deep twilight cloud shadows, physical airborne droplets')
make('snallygaster','the Frederick County bird-reptile folklore chimera',
 'one reptile-bird head with exactly ONE eye centred high on its forehead and no side eyes; long pointed metallic beak opened enough to expose a row of sharp teeth; one pair enormous wings and two steel-hook-clawed legs; a few octopus-like tentacles distinctly separate from the legs [snallygaster-c04, snallygaster-c07, snallygaster-c08]',
 'SWOOP silently downward straight at the viewer with beak gaping and hook claws reaching, wing tips cropping frame',
 'no invented supernatural effect; documented silent swooping attack, movement only [snallygaster-c05]',
 'dark woods of Frederick County Maryland [snallygaster-c11]',
 [('anatomy','Bird-reptile hybrid with metallic toothed beak','c04'),('anatomy','Octopus-like tentacles','c07'),('anatomy','Huge wings, hooked claws, central forehead eye','c08'),('effect','Silent swoop toward prey','c05'),('setting','Frederick County woods','c11')],
 'Composite folklore description, central-eye enormous-wing account with metallic toothed beak and reported tentacles.',
 ['Wing and tentacle count beyond singular pair of wings is editorial staging, not asserted folklore count; only two legs shown. No blood-drinking scene or gore; no invented magic.'],
 'Threat comes from the toothed beak, hooked claws and silent swoop (snallygaster-c04, snallygaster-c05, snallygaster-c08).','weathered metal-like bill, rough scales, damp feathers and tactile tentacles', 'one cold moon shaft, deep brown forest shadows, wind-stirred leaves')
make('tangaroa','Tangaroa-whakamau-tai, the Māori sea atua depicted in whale form',
 'a living whale, one head, two eyes, two pectoral flippers and a broad horizontal tail; natural whale form with no humanoid parts, jewellery or invented tattoo motifs [tangaroa-c02]',
 'RISE from the tide toward the viewer as the tidal surge lifts around its immense close-framed head; benevolent but overwhelming, not a monster',
 'the tide forms a powerful rising wall physically curling around the whale under its documented tidal authority, water and spray only [tangaroa-c02]',
 'open sea, Tangaroa maritime realm [tangaroa-c01]',
 [('anatomy','Whale depiction of Tangaroa-whakamau-tai','c02'),('effect','Physically moving tidal surge','c02'),('setting','Sea realm','c01')],
 'Tangaroa-whakamau-tai in documented whale form, controlling tides.',
 ['Natural unspeciated whale body is editorial; no species identification asserted. Framing rather than miniature boats creates scale. Respectful awe for a living tradition; no menace toward people.'],
 'Reverent awe comes from whale manifestation amid its moving tide (tangaroa-c02).','wet slate-grey whale skin, heavy water sheets and spray',
 'single amber sunset seam lighting crest and wet whale, ocean shadows almost black')
make('teju-jagua','the enormous Guaraní lizard guardian of caves and treasures, here the documented single-dog-head version',
 'exactly ONE huge dog head on an enormous four-legged lizard body with one long lizard tail; two eyes emit actual fire; gold dust and mineral grains lie on scales; no horns, no additional heads [teju-jagua-c05, teju-jagua-c10, teju-jagua-c02, teju-jagua-c15]',
 'LIFT its great dog head out of the cavern while remaining heavily planted on four legs, jaws parting in a warning, not sprinting because mobility is limited',
 'brief real fire flickers directly from the two eyes and lights the near cave stone; scales shine with gold dust from rolling on treasure [teju-jagua-c02, teju-jagua-c15]',
 'cavern abyss of legendary Yaguarón hill, a few unworked gold grains and stones nearby [teju-jagua-c11, teju-jagua-c15]',
 [('anatomy','Single giant dog-head variant, enormous lizard body, limited mobility','c05,c10'),('effect','Fire from eyes','c02'),('effect','Gold-dust-shining skin','c15'),('setting','Cavern of Yaguarón hill','c11'),('setting','Hidden treasure of gold and precious stones','c15')],
 'Single dog-headed enormous lizard variant explicitly accepted by teju-jagua-c05/c10, with fiery gaze and gold-dusted skin.',
 ['Single-head version avoids hiding or miscounting seven heads; it is not an invented reduction. Stationary body plus raised warning head respects limited mobility. No victims: guardian presented with reverent awe.'],
 'Awe comes from enormous lizard anatomy and the feared fire-shooting gaze (teju-jagua-c02, teju-jagua-c05, teju-jagua-c10).','rough lizard scales covered with adhered gold dust, coarse dog muzzle fur, dark cave stone',
 'eye fire is the dominant warm light, deep cavern blackness, falling dust',
 'extreme low angle inside cavern mouth, huge documented body looming over small rock fragments')
make('tenghuang','the auspicious Chenghuang foxlike beast of the Shanhaijing account',
 'a foxlike animal, one head, two eyes, four paws and one fox tail; horns grow unmistakably from the BACK behind shoulders, not forehead; no wings because this selected primary-text variant does not mention wings [tenghuang-c06]',
 'SPRING forward over a low foreground ridge, forepaws extended toward viewer, back horns sharply silhouetted above its spine, alert and commanding',
 'no visible invented magic; longevity of a rider is not shown as an energy effect [tenghuang-c06]',
 'earth beneath the creature in land of Bai-min; terrain kept indistinct because source supplies no specific landscape [tenghuang-c06]',
 [('anatomy','Foxlike creature with horns on its back','c06'),('setting','Land of Bai-min, otherwise unspecified terrain','c06')],
 'Shanhaijing Chenghuang foxlike back-horned form, without wings or horse-body mixture.',
 ['Ochre fur, back horn pair and dark neutral ground are editorial. Back horns are enlarged for readability, not relocated to head. No visible supernatural effect; auspicious longevity cannot justify invented energy.'],
 'Auspicious awe comes from startling back-horned fox anatomy and forceful close framing (tenghuang-c01, tenghuang-c06); no invented magic.',
 'dense wind-ruffled fox fur, matte keratin horns, dusty ground')
make('tepegoz','the one-eyed giant ogre of the Oghuz Book of Dede Korkut',
 'one head with exactly ONE eye in forehead, no normal pair of eyes below; humanlike body with two arms and two legs; visibly tough leathery skin; torso and pelvis fully covered by heavy opaque undyed cloth, no helmet or horns [tepegoz-c01, tepegoz-c05, tepegoz-c06]',
 'LUNGE out of his cave, one empty hand reaching toward the viewer and the other braced on cave wall, single eye fixed on us',
 'no invented magical effect; hard skin shown through dense rough surface only [tepegoz-c06]',
 'his rocky cave lair [tepegoz-c05]',
 [('anatomy','One-eyed ogre with single forehead eye','c01'),('anatomy','Giant with very hard skin','c05,c06'),('setting','Cave lair','c05')],
 'Adult single-forehead-eyed giant ogre before the blinding episode.',
 ['Full opaque rough garment is editorial to avoid nudity. No victims, gore or laser eye. Giant size is grounded in c05 original quote. No attack arrows inserted.'],
 'Threat comes from the giant cave ogre and single staring eye with tough skin (tepegoz-c01, tepegoz-c05, tepegoz-c06).','hard leathery skin, heavy coarse cloth, damp rock',
 'single low dying fire outside frame lighting cave doorway, dust without magical smoke',
 'extreme low angle at cave floor, giant looms over small cave stones')
make('tulevieja','the Costa Rican and Panamanian winged ghost woman with a tule hat',
 'one aged witchlike woman head beneath broad tule hat, two eyes, two human arms; exactly two hawk legs with talons, exactly two bat wings; torso entirely covered by opaque worn blouse and heavy wrapped skirt with lower bird legs visible; a tied bundle of firewood on her back [tulevieja-c01, tulevieja-c03, tulevieja-c07, tulevieja-c08]',
 'DROP from a low flight toward the viewer, wings thrust outward and both hawk talons brought forward, old face intent beneath the clear broad hat',
 'documented flight only; no glowing aura or invented spell [tulevieja-c09]',
 'near the Virilla river and her dilapidated shack, glimpsed behind rather than dominating [tulevieja-c07]',
 [('anatomy','Ghost woman wearing tule hat','c01,c07'),('anatomy','Hawk legs, witch face, bat wings and firewood','c03,c08'),('effect','Taking flight and descending','c09'),('setting','Virilla river near dilapidated shack','c07')],
 'MINED Costa Rican bat-winged, hawk-legged old woman account, modestly clothed editorially.',
 ['Opaque blouse and skirt deliberately replace the source bare-breast detail to satisfy no nudity. No victim or gore. Hat woven texture, worn clothing colours and evening lighting are editorial. No reversed track marks needed in airborne view.'],
 'Threat comes from the bird talons and sudden descending flight (tulevieja-c03, tulevieja-c08, tulevieja-c09).','coarse woven tule hat, aged skin, leathery bat wings, hawk scales and worn cloth')
make('u-scultone','the serpent-like reptilian Scultone of the Sardinian Golgo chasm legend',
 'one large reptilian serpent head with two eyes and a long limbless coiling serpent body; no invented wings, horns or legs; jaws parted [u-scultone-c01, u-scultone-c05, u-scultone-c08]',
 'THRUST its head toward the viewer from the black mouth of the chasm, muscular coil gripping near rocks',
 'no visible eye beam: the deadly gaze is expressed by direct stare alone; gravel dislodges through body movement only [u-scultone-c02, u-scultone-c09]',
 'Su Sterru chasm on the Golgo plateau, sparse shrub edges [u-scultone-c04, u-scultone-c08]',
 [('anatomy','Reptile-like dragon, selected serpent account','c01,c05,c08'),('effect','Deadly gaze represented without invented rays','c02,c09'),('setting','Golgo chasm with nearby shrubs','c04,c08')],
 'Su Sterru serpent account rather than the modern comic basilisk.',
 ['Limbless serpent depiction follows explicit serpent sources. Slate-brown scales and dusk are editorial. No gaze beam, petrification or victim introduced; death power remains a threatening stare.'],
 'Danger comes from lethal direct gaze and serpent emerging from its chasm (u-scultone-c02, u-scultone-c08, u-scultone-c09).','wet overlapping serpent scales, broken limestone and shrub twigs')
make('wd-q11244093','the White Dragon interpreted as a white sea waterspout in Korean tradition',
 'no invented solid dragon anatomy; the subject IS the documented white waterspout manifestation, a massive twisting column of sea water and white foam, not a humanoid or a small distant funnel [wd-q11244093-c06]',
 'REAR directly above the viewer at the base of the twisting white sea column, its spiral leaning and wrenching the surface into an overwhelming vortex',
 'active waterspout lifts ocean spray and churns a visible surface vortex; purely water and foam, no neon or dragon laser [wd-q11244093-c06]',
 'Korean sea in the waterspout interpretation [wd-q11244093-c06]',
 [('anatomy','White waterspout manifestation, deliberately no invented solid body','c06'),('effect','Active white water column and sea spray','c06'),('setting','Sea in Korean tradition','c06')],
 'Korean white-waterspout manifestation, not combined with Chinese dragon anatomy or novel powers.',
 ['Aniconic manifestation is intentional per GAMBAR 6.5 and explicitly documented by c06. The active white column is the subject and occupies almost the entire frame; not a calm seascape. No solid head, horns or claws invented.'],
 'Awe comes from the towering physical white sea waterspout regarded as White Dragon (wd-q11244093-c06).','dense white sea foam, torn spray and black-green water',
 'single amber gap in storm cloud lights spray, deep walnut-black ocean shadows',
 'extreme low sea-surface camera, white column fills frame from near foreground vortex to cropped cloud ceiling')
make('wd-q757989','Fuxi, the dragon-shaped son associated with literature and coiling around stone steles',
 'a single living dragon-shaped coiling creature, one head with two eyes; one continuous flexible coiled body encircling the top of a stone stele; deliberately no wings, jewellery or invented magical features, feet out of crop [wd-q757989-c02, wd-q757989-c07]',
 'UNCOIL its head down around the stele top toward the low viewer, throat bending forward and gaze alert, unmistakably living rather than a stone ornament',
 'no documented magic; no visible energy effects [wd-q757989-c01, wd-q757989-c02]',
 'top of a weathered stone stele, broad face plain and devoid of all text or carved symbols [wd-q757989-c02]',
 [('anatomy','Dragon-shaped literary son','c07'),('anatomy','Coiling around stele top','c02'),('setting','Stone stele with no visible lettering','c02')],
 'Fuxi as a living coiling dragon-shaped being at top of a stele, rather than Bixi turtle pedestal.',
 ['Scales and plain stone are editorial dragon-shape render details. Horns and feet remain unseen because source does not count them. Stele blank for no-text rule; no magical writing or animated glyphs. No invented powers.'],
 'Awe comes from the live dragon-shaped being uncoiling around the stele (wd-q757989-c02, wd-q757989-c07).','tactile dark bronze-brown scales and rough weathered stone')
make('wd-q9602528','Jiguang, the auspicious patterned white horse with a red mane',
 'one horse head, two eyes, four hooved legs, one tail; white body with dark natural irregular coat patterning, rich RED mane in real hair strands, no horns, wings or jewellery [wd-q9602528-c02, wd-q9602528-c05]',
 'BURST forward from marsh water, forelegs thrusting up toward viewer and red mane whipped backward, intent gaze, commanding auspicious presence',
 'no documented visual magic: only physical water splashes from motion; longevity and fireproof coat story are not converted into powers [wd-q9602528-c02, wd-q9602528-c05]',
 'great marsh from which this horse is born, reeds at margins only [wd-q9602528-c02]',
 [('anatomy','Patterned white horse with red mane','c02,c05'),('setting','Great marsh','c02')],
 'Patterned white, red-maned marsh horse form; not yellow Tenghuang alias.',
 ['Dark pattern arrangement, lighting and red mane shade are editorial. No visible magic; fire-resistant garment account c08 not treated as living horse ability. Framing and forceful movement provide awe without giant size.'],
 'Awe comes from the unusual patterned white coat and scarlet mane in vigorous marsh emergence (wd-q9602528-c02, wd-q9602528-c05).','wet white horse hair, rich red mane strands, dark marsh water',
 'single low amber sunset shaft, deep marsh shadows, heavy physical splashes')
make('xiaotian-quan','the black celestial dog accompanying Erlang Shen, using its powerful bite and howl',
 'one BLACK thin hunting dog with one head, two eyes, four legs and one tail, natural canine muzzle and teeth, no wings, horns, armour or anthropomorphic body [xiaotian-quan-c01, xiaotian-quan-c02, xiaotian-quan-c11]',
 'LEAP forward snarling in a forceful bark at the viewer, forepaws reaching and hindquarters propelling, loyal celestial guardian rather than evil beast',
 'documented powerful bite and howl expressed in open jaws and air from barking; no visual sound rings or invented magic [xiaotian-quan-c02]',
 'near the Southern Heavenly Gate of the loyal-dog legend, only a dark unlettered gate edge seen [xiaotian-quan-c08]',
 [('anatomy','Black dog','c01,c02'),('anatomy','Thin hunting dog appearance','c11'),('effect','Bite and howl used to subdue demons','c02'),('setting','Southern Heavenly Gate in loyal dog legend','c08')],
 'Loyal black thin celestial hunting dog, not the wicked-woman variant.',
 ['No demon victim, blood or invented sound energy. Unornamented heavenly gate is editorial; no religious symbols invented. Close framing keeps dog extraordinary through confrontational celestial guardianship without colossal size.'],
 'Awe comes from the loyal dog violent forward movement and documented battle bite/howl (xiaotian-quan-c01, xiaotian-quan-c02).','coarse black fur, sinewy limbs, wet black nose and stone gate')
make('xolotl','the Mexica dog-headed deity who protects the sun in its underworld journey',
 'one dog head on a male human body, two arms, two legs; two EMPTY eye sockets clearly dark and unoccupied, not glowing eyes; a large conch-like twisted wind jewel on the chest; fully opaque heavy mantle and knee-length wrapped garment cover torso and pelvis, no glyphs [xolotl-c01, xolotl-c05, xolotl-c06]',
 'STRIDE upward from the dark underworld toward the viewer, one hand held open in protective command and the other drawn forward, conch jewel and dog head prominent',
 'one fork of real lightning lights the surrounding darkness, grounded in lightning deity domain; no rays from sockets or jewel [xolotl-c01]',
 'dark threshold of Mictlan, the underworld route he guides, no invented temples or living victims [xolotl-c08]',
 [('anatomy','Dog-headed human deity','c01,c09'),('anatomy','Empty eye sockets','c06'),('anatomy','Conch-like twisted wind jewel','c05'),('effect','Lightning from documented divine domain','c01'),('setting','Mictlan underworld route','c08')],
 'Dog-headed psychopomp with empty eye sockets and conch wind jewel.',
 ['Opaque mantle and wrapped garment are editorial modesty choices; no claim that their cut is canonical. Reverent, commanding protector rather than horror caricature. Underworld rock threshold is editorial; no invented buildings or hieroglyphs.'],
 'Awe comes from lightning domain and dog-headed psychopomp protecting the sun (xolotl-c01, xolotl-c05, xolotl-c08).','matte dark canine skin, rough cloth, large ridged conch shell and underworld rock',
 'one real distant lightning fork is sole dominant light, deep walnut darkness and dusty air')
make('yara-ma-yha-who','the red, toothless tree-dwelling monster recounted in Southeastern Australian Aboriginal lore',
 'one red humanoid figure about four feet tall, snake-like oversized head, huge toothless mouth, large protruding belly, two arms and two short legs; all five fingers on each hand and all five toes on each foot end in cup-shaped suckers; two eyes, no teeth, horns or wings; fully opaque plain dark waist wrap [yara-ma-yha-who-c04, yara-ma-yha-who-c05]',
 'DROP from a low wild-fig branch toward the close viewer in an ambush, hands thrust forward so every sucker fingertip is readable, mouth opening snake-wide',
 'no invented magic or blood effects; documented dropping ambush and sucker anatomy only [yara-ma-yha-who-c06, yara-ma-yha-who-c15]',
 'dense leafy wild fig tree during DAYLIGHT, canopy shaded with a single sun shaft, never night [yara-ma-yha-who-c02, yara-ma-yha-who-c06, yara-ma-yha-who-c12]',
 [('anatomy','Small red figure with huge snake-like head, belly and toothless mouth','c04,c05'),('anatomy','Cup suckers at fingers and toes','c05'),('effect','Dropping tree ambush; no gore','c06,c15'),('setting','Wild fig tree, daytime activity','c02,c06,c12')],
 'Four-foot red toothless snake-headed humanoid with hand and foot suckers, daytime fig-tree ambush.',
 ['Opaque waist wrap is editorial to avoid nudity. Dominance through close framing, not giant scale. Strongly shaded daytime canopy permits low-key lighting without contradicting daytime-only account. No Aboriginal motifs or designs borrowed.'],
 'Threat comes from oversized toothless swallowing mouth and octopus-like fingertip/toe suckers in descending ambush (yara-ma-yha-who-c04, yara-ma-yha-who-c05, yara-ma-yha-who-c15).','matte red skin, cup-shaped sucker fingertips, rough fig bark and leaves',
 'single angled daytime sun shaft through dense canopy, deep warm leafy shadows')
make('yazi','the fierce wild-dog-headed dragon son associated with combat',
 'extreme close-up of exactly one WILD DOG head and upper neck, two normal eyes, snarling canine teeth, rough fur; lower body entirely outside crop because source gives no body anatomy; no horns or dragon body invented [yazi-c02]',
 'THRUST its snarling head toward viewer in a sudden confrontational turn, eye corners fiercely narrowed, not a neutral animal portrait [yazi-c03]',
 'no documented supernatural power; ferocity through jaw motion and physical glare only [yazi-c03]',
 'indistinct dark backdrop with a small unlettered sword hilt at bottom edge as the documented weapon association, not a throne or invented battlefield [yazi-c04, yazi-c05]',
 [('anatomy','Wild dog head','c02'),('setting','Weapons/sword-hilt association, background otherwise unspecified','c04,c05')],
 'Wild-dog-headed living Yazi in head-and-neck crop without invented lower-body anatomy.',
 ['Crop deliberately avoids unsupported body. Fur colours, scarless muzzle and lighting are editorial. Sword-hilt corner signals documented association without turning being into sculpture. No power effects or invented battlefield.'],
 'Threat comes from fierce combat character and snarling wild-dog head (yazi-c02, yazi-c03).','matted dark wild-dog fur, wet canine nose, worn plain steel hilt')
make('yellow-dragon','the Yellow Emperor animal manifestation embodying earth in Chinese tradition',
 'one yellow dragon head, two eyes, close cropped coiling dragon neck; body and limbs remain outside image; no invented horns, wings, armour, additional faces or jewels; yellow scales are editorial rendering of named dragon form [yellow-dragon-c01, yellow-dragon-c03]',
 'RISE from the dark earth into the close viewer plane, head bending down in overwhelming reverent presence, not an evil monster',
 'no earthquake, earth-splitting, breath weapon or supernatural glow is asserted; earth domain represented by soil held against yellow neck, displaced ordinary dust from emergence only [yellow-dragon-c02, yellow-dragon-c03]',
 'earth-coloured ground at Chengji, location of recorded appearance, no invented palace [yellow-dragon-c06]',
 [('anatomy','Yellow dragon manifestation of Yellow Emperor','c01,c03'),('setting','Earth domain and ground at Chengji','c02,c03,c06')],
 'Yellow dragon manifestation, head and neck crop to avoid inventing undocumented limb or horn counts.',
 ['Scaly head and long neck are editorial minimal dragon-form rendering, not a claim of exact iconography. Yellow colour follows name; no unsupported powers derived from earth affiliation. Awe through close angle and emergence; no giant comparison or evil expression.'],
 'Reverent awe comes from the Yellow Emperor dragon manifestation and earth association (yellow-dragon-c01, yellow-dragon-c02, yellow-dragon-c03).','matte yellow-ochre scale texture and dry dark soil')
# Abdu is deliberately declined: species and stable anatomy are not identified.
x=items['abdu-fisch']
r=dict(slug=x['slug'],worker='codex',worker_agent='lane-B',subagent_model='gpt-6.1-sol',subagent_reasoning_effort='high',tool='OpenAI built-in image_gen',image_model='tidak dilaporkan alat',status='tidak-digambar',review_path=x['review_path'],batch=1406,rationale=L['user_policy']['intent'],reason='Sumber menyebut ikan yang belum teridentifikasi (abdu-fisch-c01); bentuk Oxyrhynchos hanya hipotesis Bonnet (abdu-fisch-c05), bukan wujud pasti. Menghasilkan ikan rinci akan mengarang spesies/anatomi, sedangkan bahtera matahari tanpa subjek tidak lolos Uji Sangar. Tidak ada manifestasi aktif abstrak yang terdokumentasi untuk menggantikan tubuh.',basis_claim_ids=['abdu-fisch-c01','abdu-fisch-c05','abdu-fisch-c06'],visual_requirements=[],generation_failures=[],rejected_attempts=[],artistic_choices=['Menolak menggambar daripada mengubah hipotesis bentuk menjadi ikonografi pasti.'])
(B/'abdu-fisch.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
