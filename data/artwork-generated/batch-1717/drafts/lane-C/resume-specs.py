import sys
sys.path.insert(0,'data/artwork-generated/batch-1717/drafts/lane-C')
from helpers import spec,decline
H='\nHARD CONSTRAINTS: no text, lettering, logo, border, frame or watermark; no extra heads or limbs; no design from films, games, anime or comics; no nudity, no explicit gore; no generic glow aura, neon outlines, floating symbols or energy ribbons.'
def make(s,g,r,p,v,c,a):
 return spec(s,g,[dict(kind=k,description=d,claim_ids=[s+'-'+i for i in ids]) for k,d,ids in r],p+H,v,c,a)
s='kamappa'
make(s,dict(wujud=['kamappa-c02','kamappa-c08','kamappa-c10','kamappa-c13'],kekuatan=['kamappa-c02'],tempat=['kamappa-c14'],sifat=['kamappa-c07']),[('anatomy','Huge shapeless monster with frightful jaws and multiple sharp tongues; no invented eyes, wings, legs or horns.',['c02','c08','c10','c13']),('effect','Swollen bulk wedges at narrow valley pass; tongues thrust as weapons.',['c02','c14']),('setting','Narrow valley entrance.',['c14'])],'''ONE original square premium painterly cinematic Mitoloka illustration of Kamappa, the immense shapeless Basotho devourer.
ANATOMY: an immense shapeless continuous irregular fleshy mass, no recognizable animal skeleton, no eyes, no horns, no wings, no limbs. One frightful open jaw emerges from the front of the mass, multiple long sharp tongues thrust outward as weapons [kamappa-c02,c08,c10,c13].
MOMENT: surge toward the viewer with tongues stabbing the air, swollen bulk physically wedged in a narrow mountain pass [kamappa-c02,c14].
POWER: engulfing immense expanding mass, no magical energy, no victims or gore [kamappa-c02].
SCALE & CAMERA: very low near-ground camera; mouth and three visible sharp tongues dominate; vast irregular bulk trails out of view between tiny high cliff walls.
LIGHT & WEATHER: one low copper sunset from the side, deep walnut shadows, natural dust from heavy bulk pressing against earth.
SURFACE: coarse wrinkled dark organic skin, saliva and mud, realistic rock.
SETTING: narrow pass at a Basotho valley entrance [kamappa-c14].
MOOD: overwhelming menace, vast and horrible, never cute or decorative.''','Shapeless swollen devourer with multiple sharp tongues at the valley pass.',['Skin texture, three tongues (unspecified multiple), light and perspective editorial.','No imported python shape, eyes, wings or gore.'],'Vast body and weapon tongues c02/c08, wedged pass c14.')
s='kamohoali-i'
make(s,dict(wujud=['kamohoali-i-c07','kamohoali-i-c08'],kekuatan=['kamohoali-i-c03'],tempat=['kamohoali-i-c02'],sifat=['kamohoali-i-c04','kamohoali-i-c05']),[('anatomy','Shark incarnation, one head and normal shark fins and tail.',['c07','c08']),('effect','Tail motion guides lost sailors home; natural wake only.',['c03']),('setting','Waters near Maui and Kahoolawe.',['c02'])],'''ONE original square premium painterly cinematic Mitoloka illustration of Kamohoalii, protective Hawaiian shark god guiding lost sailors.
ANATOMY: one living shark incarnation with one head, two eyes, normal shark fins and one powerful tail; no human parts or crown [kamohoali-i-c07,c08].
MOMENT: swim directly past the low water-level viewer, sharply shake the tail to lead a small distant voyaging canoe toward the island shore [kamohoali-i-c03]. Mouth closed; guardian expression steady and authoritative.
POWER: a real curved wake and scattering water physically follow the guiding tail, no fire, steam magic or supernatural beams [kamohoali-i-c03].
SCALE & CAMERA: extreme close split-water side-front view, head dominates front, entire continuous body and tail readable; canoe distant by perspective, NOT a giant shark.
LIGHT & WEATHER: one amber low sun beneath deep storm clouds, crisp side-light on wet skin, ocean spray.
SURFACE: natural rough gray-brown shark skin, wet specular water, deep sea green.
SETTING: waters around Maui and Kahoolawe, distant dark Hawaiian island [kamohoali-i-c02].
MOOD: awe-inspiring sacred benevolent guardian, protecting sailors; no attacking victims or evil horror.''','Protective shark incarnation turning to guide a distant canoe.',['Species-neutral shark anatomy and cinematic split-water camera editorial.','No unsupported giant size, flame, steam effect or crown; normal sea spray only.'],'Shark king c04 embodied as protective shark c07/c08; guiding tail c03.')
s='kanedama'
make(s,dict(wujud=['kanedama-c06','kanedama-c10'],kekuatan=['kanedama-c06'],tempat=['kanedama-c06'],sifat=['kanedama-c01','kanedama-c04']),[('anatomy','Unworked natural object kept in its natural state.',['c06']),('effect','Rolls at feet at night giving off red light.',['c06','c10']),('setting','Night interior before tokonoma.',['c06'])],'''ONE original square premium painterly cinematic Mitoloka illustration of Kanedama, the auspicious Japanese money spirit appearing as an unworked natural object with red light.
ANATOMY: ONE rough irregular unworked rounded natural stone, no face, eyes, limbs, engraving or coin design [kanedama-c06]; natural state maintained.
MOMENT: roll right toward the viewer's feet at night, stone tipped onto one edge, scraping fine real dust across old wooden floor [kanedama-c06].
POWER: the stone itself gives off deep red light, directly illuminating nearby wood grain and ordinary opaque cloth feet at frame edge; light confined to object and surfaces, no aura cloud [kanedama-c06,c10].
SCALE & CAMERA: extreme floor-level macro, stone occupies most of image, small incidental human cloth foot at far edge demonstrates close camera not gigantic object.
LIGHT & WEATHER: dominant natural-looking red light from the stone itself, deep walnut night shadows.
SURFACE: rough porous dark rusty stone, unpolished irregular surface; aged wood and dust.
SETTING: Japanese room with dim tokonoma recess behind, night [kanedama-c06].
MOOD: uncanny and awe-inspiring auspicious presence, never evil; powerful object rather than mundane still life.''','Numazu account of natural-state red-light object rolling at night.',['Natural stone material editorial for unworked object; not claiming meteorite interpretation as fact.','Avoid modern10yen coin variant and lettering; red light expressly documented c06/c10.'],'Red-light rolling presence c06/c10, auspicious household c01/c04.')
s='kangla-sha'
make(s,dict(wujud=['kangla-sha-c01'],kekuatan=[],tempat=['kangla-sha-c06'],sifat=['kangla-sha-c01','kangla-sha-c02']),[('anatomy','Living guardian lion body with one dragon head and exactly two horns.',['c01']),('setting','Royal palace entrance, sacred royal association.',['c06'])],'''ONE original square premium painterly cinematic Mitoloka illustration of Kangla Sha, sacred Meitei guardian dragon lion.
ANATOMY: ONE living lion body with four muscular feline legs, one lion tail, ONE dragon head bearing EXACTLY TWO prominent horns, two eyes; no wings, no extra horns [kangla-sha-c01]. Living warm skin, fur, muscles, not stone or sculpture.
MOMENT: stride protectively out of the shadowed royal palace entrance toward the viewer, front paw raised and reaching into foreground, head lowered with sovereign vigilance.
POWER: no documented magical effect; grandeur comes only from anatomy, movement, texture and light.
SCALE & CAMERA: extreme low close three-quarter angle; horned dragon head and lion chest fill upper frame, four legs legible, no invented giant body size.
LIGHT & WEATHER: one low warm sun cuts across courtyard, deep brown palace shadows, fine dust from paw contact.
SURFACE: tawny dark lion fur, real dragon scales on head, two ivory-brown horns, rough courtyard earth.
SETTING: entrance of Meitei royal palace, distant understated architecture [kangla-sha-c06].
MOOD: sacred awe-inspiring benevolent guardian and royal dignity, never evil, cute or decorative.''','Living two-horned dragon-headed lion guardian at palace entrance.',['Color, fur/scales texture and stride editorial; no magical effect.','Do not depict historical statue or claim statue sizes as living size.'],'Lion-dragon anatomy c01 and sacred royal guardianship c01/c02/c06.')
s='kaupe'
make(s,dict(wujud=['kaupe-c03'],kekuatan=['kaupe-c01','kaupe-c05'],tempat=['kaupe-c04'],sifat=['kaupe-c01','kaupe-c02']),[('anatomy','Enormous man with canine head and sharp claws.',['c03']),('effect','Calling lure rendered as mouth mid-call, no visible magic sound.',['c01','c05']),('setting','Beneath Kipapa Bridge.',['c04'])],'''ONE original square premium painterly cinematic Mitoloka illustration of Kaupe, the enormous canine-headed calling spirit of Hawaii.
ANATOMY: one enormous male human body, ONE canine head, two eyes, two arms, two human legs, sharply clawed hands [kaupe-c03]. Fully opaque dark rough cloth garment from waist to ankles editorial; no nudity, no quadruped body.
MOMENT: lunge out from under the bridge toward the viewer, one clawed hand reaching foreground, canine mouth open mid deceptive cry [kaupe-c01,c05].
POWER: mimic a distressed human cry through open mouth; no magical sound rings or beams [kaupe-c05].
SCALE & CAMERA: low close three-quarter view; enormous body almost fills bridge clearance; one tiny distant clothed adult on bridge gives documented enormous scale [kaupe-c03].
LIGHT & WEATHER: one amber moon through dark clouds, deep damp walnut shadows, disturbed mud under foot.
SURFACE: coarse canine fur, sharp claws, wet human skin on arms, rough opaque fabric, damp bridge masonry.
SETTING: beneath Kipapa Bridge [kaupe-c04].
MOOD: dangerous malevolent predator, no victims or gore.''','Enormous dog-headed male spirit calling beneath Kipapa Bridge.',['Garment, moon and bridge materials editorial.','No Poki spotted coat/longdogbody conflation c09; no magic sound effect.'],'Enormous canine head/claws c03 and calling lure c05.')
s='kawaakago'
make(s,dict(wujud=['kawaakago-c01','kawaakago-c02','kawaakago-c03'],kekuatan=['kawaakago-c04','kawaakago-c05'],tempat=['kawaakago-c02'],sifat=['kawaakago-c05']),[('anatomy','Small red-skinned baby, upper body beside reeds, covered opaque clothing.',['c01','c02','c03']),('effect','Mouth mimicking infant cry to attract passerby; no magic effect.',['c04']),('setting','Riverside reeds.',['c02'])],'''ONE original square premium painterly cinematic Mitoloka illustration of Kawaakago, the small red-skinned baby-shaped Japanese yokai beside river reeds.
ANATOMY: ONE small baby with red skin, one head, two eyes, two arms; fully opaque dark ochre wrapped cloth covers entire torso and lower body; thick reeds additionally conceal lower body [kawaakago-c01,c02,c03]. No nudity, horns, fangs or claws.
MOMENT: lean forward between wet reeds toward the low close viewer, mouth open while imitating an infant's cry to attract a passerby, one small hand reaching out [kawaakago-c04].
POWER: no visible magic; the prank cry near deep water is the danger, no victim shown [kawaakago-c04,c05].
SCALE & CAMERA: extreme close riverbank view at infant eye level, small red face dominates image, large normal reeds prove small size, not a giant baby.
LIGHT & WEATHER: one low amber moon side-lights red cheek and wet reeds; deep walnut water shadows, ripples only from natural river movement.
SURFACE: natural red skin, rough opaque wrapped textile, wet brown-green reeds.
SETTING: dark riverside reeds [kawaakago-c02].
MOOD: strange unsettling mischievous yokai with risky prank, solemn and uncanny, not cute or a demonic evil child.''','Small red-skinned crying yokai in opaque cloth among riverside reeds.',['Opaque garment is editorial modesty; reeds corroborated c02.','No extra evil powers; infant prank c04/c05 only.'],'Uncanny red infant c03 and lure cry beside deep water c04/c05.')
s='kitovras'
make(s,dict(wujud=['kitovras-c01','kitovras-c02'],kekuatan=['kitovras-c04'],tempat=['kitovras-c04'],sifat=['kitovras-c03','kitovras-c04']),[('anatomy','Centaur-like half man half horse, unwinged variant.',['c01','c02']),('setting','Lukorye city associated with reign.',['c04'])],'''ONE original square premium painterly cinematic Mitoloka illustration of Kitovras, the wise centaur-like king of Russian apocrypha.
ANATOMY: one centaur-like being: ONE male human torso and head, two human arms seamlessly rising from ONE horse body, exactly four horse legs, ONE horse tail; unwinged variant [kitovras-c01,c02]. Fully opaque dark antique ceremonial robe covers human torso and waist; horse body natural coat.
MOMENT: advance with one front hoof striking stone toward the low viewer, one hand raised in emphatic wise declaration, face stern and commanding [kitovras-c04].
POWER: no visible prophecy effect; wisdom through speaking gesture only [kitovras-c04].
SCALE & CAMERA: extreme low side three-quarter view, imposing hybrid dominates, horse-human junction and all four legs clearly separated, head turned toward viewer; no invented giant size.
LIGHT & WEATHER: one low copper evening sun, deep walnut shadows, real hoof dust.
SURFACE: rough horse coat, coarse opaque robe, stone paving.
SETTING: understated old city of Lukorye, dim city walls behind [kitovras-c04].
MOOD: awe-inspiring royal wisdom and power, never ordinary rider, cute or decorative.''','Unwinged centaur variant proclaiming wisdom in Lukorye.',['Robes, human face/hair, architecture and twilight editorial.','Prophecy not depicted as glow; no weapon or crown imported.'],'Centaur anatomy c01/c02 and authoritative wisdom/reign c04.')
s='kayberen'
make(s,dict(wujud=['kayberen-c07','kayberen-c09','kayberen-c12'],kekuatan=['kayberen-c01','kayberen-c13'],tempat=['kayberen-c04','kayberen-c12'],sifat=['kayberen-c01']),[('anatomy','Invisible holy mountain spirits; human guise Anatolian variant lacks specific features.',['c07','c09','c12']),('setting','Mountains and rocks.',['c04','c12'])],'Not generated: invisible protectors; no identifiable active visible manifestation.','No visible body invented.',['Human guise alone lacks distinct sourced iconography; not importing40children as spirits.'],'Invisible mountain protection c12/c13.')
decline(s,'Roh pelindung gunung terutama tidak terlihat (c09/c12/c14). Varian manusia c07 tidak mempunyai ciri pembeda. Perlindungan hewan c01/c13 tidak menetapkan manifestasi fisik aktif; lanskap/hewan saja mengulang subjek absen. Tidak mengarang tubuh atau40sosok.')
s='king-goldemar'
make(s,dict(wujud=['king-goldemar-c01','king-goldemar-c04'],kekuatan=['king-goldemar-c04','king-goldemar-c05'],tempat=['king-goldemar-c03'],sifat=['king-goldemar-c05']),[('anatomy','Dwarf/kobold refuses to be seen; frog-like hands known by touch.',['c01','c04']),('setting','Castle Hardenstein on Ruhr.',['c03'])],'Not generated: refuses to be seen, touch-described frog hands not permission for visible body.','No visible king or frog hands invented.',['Harp-playing alone not visible active manifestation; violent act not used as gore.'],'Unseen kobold c04.')
decline(s,'Goldemar menolak terlihat dan hanya dapat diraba (c04); tangan mirip katak adalah deskripsi rabaan, bukan izin menampilkan tubuh. C03 pemainharpa tidak memberikan manifestasi terlihat yang mendominasi; ruangan/harpa saja subjekabsen. Tidak mengarang sosok dwarf terlihat atau memakai gore c05.')
