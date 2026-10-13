import json
from pathlib import Path
ROOT=Path('/home/asadin/Portfolio/asadin-edu/asadin-mythological-creatures');B=ROOT/'data/artwork-generated/batch-1506';D=B/'drafts/lane-B'
L=json.loads((ROOT/'data/artwork-batch-1506.json').read_text());items={x['slug']:x for x in L['items']}
def make(slug,identity,anatomy,moment,power,setting,requirements,variant,choices,aura,surface,lighting='one low amber sunset shaft, deep walnut shadows, sharp rimlight',camera='extreme low camera, close foreshortened framing; no undocumented giant size'):
 x=items[slug];req=[dict(kind=k,description=d,claim_ids=[slug+'-'+c for c in cs.split(',')]) for k,d,cs in requirements];ids=list(dict.fromkeys(c for r in req for c in r['claim_ids']));assert set(ids)<=set(c['id'] for c in x['research']['claims'])
 p=f'''ONE original square premium painterly cinematic Mythics illustration of {x['canonical_name']}, {identity}. Native square PNG at least1024x1024pixels.
ANATOMY: {anatomy}
MOMENT: {moment}
POWER: {power}
SCALE & CAMERA: {camera}
LIGHT & WEATHER: {lighting}
SURFACE: {surface}
SETTING: {setting}
MOOD: imposing and awe-inspiring or dangerous according to documented character; never cute, calm, tame or decorative. Subject dominates frame and remains striking at200px.
HARD CONSTRAINTS: no text, lettering, glyphs, logos, border, frame or watermark; no extra heads, eyes, limbs or fingers; no design from films, games, anime or comics; no nudity, gore or visible wounds; no generic luminous aura, neon outline, energy ribbons or coloured magical fog. Bracketed claimIDs are instructions, never visible text.'''
 r=dict(slug=slug,worker='codex',worker_agent='lane-B',subagent_model='gpt-6.1-sol',subagent_reasoning_effort='high',tool='OpenAI built-in image_gen',image_model='tidak dilaporkan alat',status='draft-before-generation',review_path=x['review_path'],batch=1506,rationale=L['user_policy']['intent'],prompt=p,depicted_variant=variant,basis_claim_ids=ids,visual_requirements=req,aura=aura,artistic_choices=choices,generation_failures=[],rejected_attempts=[])
 pth=D/(slug+'-request.json');assert not pth.exists();pth.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
def decline(slug,reason,cs):
 x=items[slug];ids=[slug+'-'+c for c in cs.split(',')];assert set(ids)<=set(c['id'] for c in x['research']['claims'])
 r=dict(slug=slug,worker='codex',worker_agent='lane-B',subagent_model='gpt-6.1-sol',subagent_reasoning_effort='high',tool='OpenAI built-in image_gen',image_model='tidak dilaporkan alat',status='tidak-digambar',review_path=x['review_path'],batch=1506,rationale=L['user_policy']['intent'],reason=reason,basis_claim_ids=ids,visual_requirements=[],generation_failures=[],rejected_attempts=[],artistic_choices=['Tidak mengarang wujud, menyalin adaptasi, atau memakai generic glow untuk memenuhi Uji Sangar.'])
 p=B/(slug+'.json');assert not p.exists();p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
make('xiangliu','the Shanhaijing nine-HUMAN-faced blue-bodied serpent of Gonggong',
 'exactlyNINEdistinct HUMAN heads, eachwith2human eyes/one mouth/one nose, on nine short branching necks emergingfromONEblue snake body, no snakeheads, horns, wings, legs or arms. ALL9faces fullyvisible, laidout3rows of3, no overlap or hiddenfaces, face countliteral [xiangliu-c01, xiangliu-c08]',
 'SURGE towardviewer from the newlyflooding marsh, allNINEhuman faces lookingdownorforward, teethnaturalhuman notsnakefangs; onecoiledblue snakebody pushesahead',
 'whereitpasses, ground becomesbitter poisonousmarsh water; floodwater wellsaroundbody andfills freshchannels, no neonpoisonvapour orprojectilebreath [xiangliu-c05, xiangliu-c07, xiangliu-c09]',
 'newlywaterlogged marsh andwateryvalley, vegetation subdued [xiangliu-c07, xiangliu-c09]',
 [('anatomy','Nine human-faced heads and blue snakebody','c01,c08'),('effect','Passage turns ground into bitter marshes/wateryvalleys','c05,c07,c09'),('setting','Newlyformed marsh/flood valley','c07,c09')],
 'Shanhaijing nine human faces with blue snakebody; not ordinary nine snake heads.',
 ['Nine short separatedneckbranches editorial staging tocount9faces; humanfeatures/blue scaletexture editorial. No gore/rankblood episode, genericpoison glow or extraanatomy.'],
 'Danger comes from9human faces ononeblueserpent and passage creating bitterfloodmarsh (xiangliu-c08, xiangliu-c09).','wetbluescales, weatheredhumanfaces and muddywater',camera='extreme lowwaterline angle; closebody/headcluster dominates;9heads arranged3clearrolls of3 with gaps')
make('xiao-mythology','the dreaded long-armed ape Xiao of the Western Shanhaijing',
 'one natural MACAQUE-like head/twoeyes/tworoundears; onefurredapetorso, TWO exceptionallylong ape arms,twoapelegs,oneape tail; no humanface or4wingbirdvariant [xiao-mythology-c04, xiao-mythology-c07]',
 'HURL oneplainrock forward towardviewer withright exceptionallylongarm, leftlongarm reachingback forbalance, mouth tense and eyesfocused. Fullupperarms/forearms visible so disproportionatelength clear',
 'documented skilledthrowing only: physical rockleavinghand andordinary dust, no magic aura [xiao-mythology-c04, xiao-mythology-c07]',
 'neutral roughground, WesternShanhaijing creature without specific mountain imported [xiao-mythology-c07]',
 [('anatomy','Longarmed ape resembling macaque','c04,c07'),('effect','Skilledthrowing/depictedthrowing','c04,c07'),('setting','WesternShanhaijing account,neutralground','c07')],
 'Western long-armed macaque throwing, notNorthern4wing/oneeye/dogtailbird.',
 ['Rock is editorial concrete thingthrown; no magicpower. Longarms explicit; furcolour/ground editorial, closecamera no giantsizeinvented.'],
 'Threat comes fromdreadedlongarmedape hurling aprojectile (xiao-mythology-c07).','matted brownmacaquefur, hardstone anddrydust')
make('yahui','the animal-form Mixtec cosmological composite Yahui',
 'one reptilian head/twoeyes; tortoiseCARAPACEbody withfourreptilianclawedlegs,one reptilian tail; flint-firemotifs at NOSEtip andTAILtip rendered asdistinct nonluminous red-orangeflint-shaped plates. No humanhead,headdressor knives fromnahual variant [yahui-c06]',
 'STEP forward onto rockyground towardviewer, nearclawedforelimb stretching, noseflintand curvingtailflint bothclearlyvisible, living fleshandshell notflatcodexsymbol',
 'no documentedprojectedfire or supernaturalaction; flint-firemotif is anatomicaliconographicmotif ONLY, no flamebreath,auras or inventedblasts [yahui-c06]',
 'neutralshadowedground for documentedanimalcosmogonyform, no historicalhumanritecave imported [yahui-c06]',
 [('anatomy','Reptilianhead,tortoiseshell,clawedreptilelimbs,flintfiremotifnose/tailtips','c06'),('setting','Animalcosmogonyform onneutralground','c06')],
 'Animal reptile/tortoiseshell/flintfiretips, not humanheaded nahualpriest.',
 ['Natural scales and flint-shaped red-orange stoneplates editorial realization ofcodexmotif, no claimoffireprojection. Fourreptilelimbs are ordinary limbarrangement, no inventedextraarms. No sacrificialscene or copiedsacredpattern.'],
 'Awe comes fromdocumentedreptile/tortoise/flint-firecomposite (yahui-c06).','roughcarapace, leatheryreptilescales, chippedflintplates andstone')
make('yumboes','one benevolent two-foot-high pearly-white ancestral spirit fromtheWolof account',
 'one smalladult humanlikespirit, onehead/twoeyes,twoarms/twolegs, pearlyWHITEskin andSILVERhair; fullyopaque simpleplainrobe toankles; naturalhands5digits. ExactlyaboutTWOfeet tall, nothumansizegiant [yumboes-c02, yumboes-c03, yumboes-c09, yumboes-c11]',
 'DANCE a solemn lament step on familygrave, onefoot raisedandhands lifted withfaceinclined downwardtowardviewer; compassionate ancestralpresence, no evilattack',
 'documented lamenting/dancingongraves only, no necromanticglow,fire,giantscale or floatingrunes [yumboes-c12]',
 'a plain uninscribed familygrave inJaloffmainland facingGoree tradition, graveearth/subordinateroots clarify smallscale [yumboes-c08, yumboes-c12]',
 [('anatomy','Pearlywhite spirit/silverhair,twofeetheight,localstyleclothing','c02,c03,c09,c11'),('effect','Lamenting/dancingonfamilygraves','c12'),('setting','Jaloff mainland/Goreeaccount familygrave','c08,c12')],
 'Single benevolent pearlywhite/silverhaired miniature ancestralspirit, no disembodiedservanthandvariant.',
 ['Plainopaquecloth is editorial modestclothes without claimingexactWolofcostume. Moonreflection onpearlyskin notselfemittedlight. Macroframing notenlargedbody; respectful ancestralbelief, no stereotypes or occultmotifs.'],
 'Awe comes fromtiny pearl-white ancestralspirit dancinglamentonfamilygrave (yumboes-c02, yumboes-c09, yumboes-c12).','pearlypaleskin,silveryhair,coarseplainclothanddampgraveearth',lighting='one lowcoldmoonbeam, deepwalnutshadows andsilverrimlight; ordinarywind',camera='extreme lowmacrograveground camera; tiny2footspirit dominatescloseframe,ordinaryroot/graveearth show documented smallscale')
make('aim','the Goetia Duke with three distinctheads and a burningfirebrand, ridingaviper',
 'ONEhandsomehumanoidbody fullyclothed inopaqueplainrobe; exactlyTHREEheads arrangedseparateatshoulders: viewerLEFTserpenthead/twoeyes, CENTERhandsomehumanhead/twoeyes with exactlyTWOclearlyvisible STARshaped marksONFOREHEAD, viewerRIGHT CAThead/twoeyes. Exactlytwohumanarms/twolegs; RIGHThandholdsoneburningfirebrand; ridesONElimblessviperwithonehead/twoeyes. Noextrahorns/headsinflames [aim-c05, aim-c06]',
 'RIDE the rearingviper down towardviewer and THRUST burningfirebrand toward stonecastle, all3headsfacingviewer andall2foreheadstarsvisible',
 'real firefromfirebrand ignitescastlewoodroof nearby, source power sets cities/castles ablaze; physicalsmoke/sparks only [aim-c06]',
 'burningcastle atnight, closeforegroundviperandrider dominates, nootherpeople [aim-c06]',
 [('anatomy','Humanoidbody3heads serpent/humanwith2stars/cat','c05'),('anatomy','Viper steed/firebrand','c06'),('effect','Firebrand sets castle aflame','c06'),('setting','Castle','c06')],
 'Sloane3825 serpent/man-with2stars/catheads ridingviper, not calf-headvariant.',
 ['Opaqueplainrobe andstar-shapedflatforeheadmarks editorial material realization; no glowingglyphs. Fireeffect onlyfromdocumentedfirebrand, nolegion crowd. Threeheadseachclear andsteedheadnotconfusedwithrider.'],
 'Danger comes from3distinctheads andfirebrand burningcastle (aim-c05, aim-c06).','naturalhuman/cat/snakefaces,wetviper scales,opaquecloth,charredwood',lighting='burningfirebrand isdominantamberlight, deepnight shadows, physicalsmokeandsparks',camera='extreme lowangle; riderupperbody/headcluster fillsupperframe,viperonehead clearbelow,allthreeheadsunoccluded')
make('amalanhig','the human-looking Visayan grave-risen neck-biting vampire',
 'one humanlookingadult withonehead/twoeyes,twoarms/twolegs; exactlyTWOenlargedUPPERcanines clearlyvisible, otherwisehumanmouth; fullyopaque simpledarkshirtandtrousers. Intactskin,NOrottingwounds/nudity ormoviezombiedesign [amalanhig-c01, amalanhig-c02]',
 'RISE abruptly fromdarkgraveearth towardviewer, torsoforward, onehumanhand reachingfromground, openmouth revealingtwoenlargeduppercanines; no victim or bitecontactshown',
 'documented risingfromgraveand neckbiteintent conveyed by reachingandcanines, no magicalresurrectionauraor explicitinjury [amalanhig-c01, amalanhig-c02]',
 'plain uninscribed Visayangraveearth, no namedchurch/ritualsymbols [amalanhig-c01]',
 [('anatomy','Humanlooking withenlargeduppercanines','c02'),('effect','Risesfromgrave/huntsbyneckbite','c01'),('setting','Visayangrave','c01')],
 'Human-looking grave-risen vampire withuppercanines, no corpse-rotting/naked orPedroPendukoadaptation design.',
 ['Opaqueplainclothes,skincomplexion anddarkgraveearth editorial. No actualvictim/injury orrottingflesh. Literatureclaimused astraditionalform, not franchiseadaptationvisual.'],
 'Threat comes fromgrave-rise andtwoenlargeduppercanines for neckbiting (amalanhig-c01, amalanhig-c02).','weatheredintactskin,coarseopaqueclothes,dampgraveearth',lighting='one lowcoldmoonbeam, deepwalnutshadows,earthdust')
make('ame-no-wakahiko','the valorous young heavenly envoy with the heavenlydeerbow',
 'one handsomeYOUNGADULTman,onehead/twoeyes,twoarms/twolegs; opaqueplainancientrobe,noarmour orinventedsunhalo; onebowandoneFEATHEREDarrow, nootherweapons [ame-no-wakahiko-c05, ame-no-wakahiko-c22, ame-no-wakahiko-c24]',
 'RELEASE a featheredarrow steeplyupwardtowardheaven, bowarm stretchedanddrawinghand justopened, handsomeface focusedandlookingupward, no deadpheasant/victimshown',
 'arrowflies allthewaytoHEAVEN inenvoy story; physicalarrowvisible leavingbowandclimbingintosky,no neontrail or inventedgraincontrol [ame-no-wakahiko-c07, ame-no-wakahiko-c24]',
 'earth belowheaven assourcedenvoy scene, neutralstoneledge againstdramaticopen sky, not Ajisukitakahikone destroyinghut [ame-no-wakahiko-c03, ame-no-wakahiko-c07]',
 [('anatomy','Handsomeyoung envoy,valorous','c05,c22'),('anatomy','Heavenlydeerbow/featheredarrows','c24'),('effect','Arrowfliesfromearthtoheaven','c07,c24'),('setting','Earth/heaven envoyaccount','c03,c07')],
 'Youngadult deity heavenlyarcher fromNihongi envoyepisode, notmedievalserpenthusband orAjisukitakahikone.',
 ['Opaqueplainrobe andhairstyle editorial, notcanonicalcostume. Bowmaterial simpledeer-antler-inspired tips onlysourcebowname notliteralantlerornament. No pheasantdeath, cosmicbody enlargement, sunhalo,stormcontrol orgrainpowermadeup. Lowangle andheavenboundarrowprovide reverent awe.'],
 'Awe comes fromvalorousheavenlyarcher andarrowreachingheaven (ame-no-wakahiko-c22, ame-no-wakahiko-c24, ame-no-wakahiko-c07).','naturalhumanskin,plainopaquecloth,woodbowandfeatheredarrows',camera='extreme lowcloseangle, archerdominates withforeshortenedbow/arms,skyarrowtrajectoryclearwithoutmagicaltrail')
make('anchimayen','the Mapuche bright flying fireball manifestation of Anchimayen',
 'ONEbright flyingFIREBALL, nochildface/body/limbs insidefire andnoreconstructedremains; thisis documentedtransformedmanifestation [anchimayen-c01]',
 'FLY straightpastcloseviewer, compactphysicalwhite-hotfireballfillsmostframe withviolentnaturalflameedges, luminouslightfloodingforegroundground',
 'documentedbrilliantlight confuses/disorientsnearviewer; lightwashesoutnearforeground asfireballpasses, novictim,sickeyes,laserbeam,runes or genericcharacterhalo [anchimayen-c07]',
 'neutraldarkground, no specific Mapuchelandmark or inventedritualscene [anchimayen-c01, anchimayen-c07]',
 [('anatomy','Transformedbrightflyingfireballmanifestation','c01'),('effect','Brightlight disorientsupclose','c07'),('setting','Closeencounter inunspecifieddarkground','c01,c07')],
 'Active flying fireballmanifestation, not literalchildcorpse/childbody ormoon-goddessconfusion.',
 ['§6.5documentedactive manifestation chosen insteadofchildbody. Physicalbrightballnotgenericbodyaura; amberwhitefirecolourandneutralground editorial. Nochildinperil orillustratedremains.'],
 'Danger comes frombrightflyingfireball andblinding/disorientingnearencounter (anchimayen-c01, anchimayen-c07).','turbulentphysicalflameedges,scorched-lookingneutralrockbutnoinventedburndamage',lighting='fireballitselfdocumentedbrillianceonlydominantlight; deepblackshadows,strongnaturalbloom,nocolourfog',camera='extreme lowclosegroundcamera; fireballfillsframeandactivelypasses,notanemptylandscape')
decline('apukohai','Riset hanya menyebut marine monster dan pertarungan Kawelo (c01/c02/c03/c05), tanpa anatomi, warna, ukuran Apukohai, atau kuasa aktifnya. Raksasa adalah Kawelo c04, bukan Apukohai. Tiki mask/lightning c06 berasal komik Shermans Lagoon dan tidak diimpor. Tidak menggambar ular/ikan/hybrid/monster laut generik tanpa klaim wujud.','c01,c02,c03,c04,c05,c06')
make('ascapart','the thirty-foot English giant beforehisduel withBevis',
 'one intacthuman-shapedGIANT,onehead/twoeyes,twoarms/twolegs; opaqueheavyplainmedievaltunic/trousers; one massive uprootedTREEusedasCLUB graspedinrighthand,nohorns or armour invented [ascapart-c01, ascapart-c02, ascapart-c06]',
 'SWING treeclub down towardcloseviewer, bodytwistingandonefoot steppingforward, fiercechallengebeforedefeat,notkidnappingscene',
 'no supernaturalpower; documentedtreeclub andterrifyingvillages physicallyconveydanger, ordinarydustfromstride only [ascapart-c02, ascapart-c07]',
 'Southampton countryside/NewForest folklore, smallsubordinateplaincottageroofs show30footscale [ascapart-c05, ascapart-c07]',
 [('anatomy','Giant30feettall','c01,c02,c06'),('anatomy','Treeclub','c02'),('effect','Terrifieslocalvillages','c07'),('setting','Southampton/NewForest countryside','c05,c07')],
 'Intact30-foot giant withtreeclub beforedefeat, not loyal squire orkidnappingepisode.',
 ['Plainopaqueclothes,hair anduninscribedcottages editorial. Exactly30footscale approximatebyordinaryroofs, no demonparts or magic. Clubtree sourced, impactnovictimorgore.'],
 'Threat comes from30-footgiant andtreeclub terrorizingvillages (ascapart-c02, ascapart-c06, ascapart-c07).','roughhumanskin,coarseopaquecloth,rawtreebarkandroots')
make('ayida-wedo','the revered cosmic rainbowserpent shapinglandforms inAyidaWedo tradition',
 'ONEimmenseRAINBOWserpent,one head/twoeyes,one longlimblesssnakebodyandtail; naturalmutedrainbowhuesinthe scales,nolegs,horns,wings,humanoidtorsoorborroweddragonanatomy [ayida-wedo-c04, ayida-wedo-c05, ayida-wedo-c15]',
 'SWEEP enormousbodythroughfreshvalley, headturningtowardcloseviewer whileitsbodycarvesariverchannel behind,benevolent worldformingpresence,notpredatorattack',
 'bodypassageleavesCANYONS,RIVERS,VALLEYS,MOUNTAINS: physicallynewrivercurlingalongserpentgroove,earthbankspushedaside, no neonrainbowribbons orbodyglow [ayida-wedo-c05]',
 'worldforminglandscape withfreshvalley/rivermountain contours, subordinatetosnakehead andbody [ayida-wedo-c02, ayida-wedo-c05]',
 [('anatomy','Rainbowserpent','c04,c05,c15'),('effect','Bodypassageformslandforms/rivers/valleys','c05'),('setting','Cosmicworldforminglandscape','c02,c05')],
 'Cosmicrainbowserpent creatinglandforms, not ritualmedium,Anyi-ewo malevariant orCatholicimage.',
 ['Rainbow colours naturaliridescentscalesnotneon; singlehead/limblessserpent minimalgenericserpentanatomy. Giantworldformingscale sourced c05. No MawuLisa seconddeitydepicted, no inventedstorms/damage/victims. ReverentlivingVodoutradition.'],
 'Reverentawe comes fromrainbowserpent whosepassagecreatesriver/canyon/valley/mountain (ayida-wedo-c05).','wet iridescentrainbowscales, freshsoilbanksandflowingriver',camera='extreme lowriverbankcamera; colossalworldformingserpenthead dominates withsmallnewvalleybehind')
make('barak','the blessed shaggydog riddenbyshamans ascendingtothesky',
 'ONEshaggylivingdog,onehead/twoeyes,twoears,fourcaninelegs,onefurry tail,no wings/horns/humanhead. ONEfullyopaqueclothedadultshaman riderwithonehead,twoarms,twolegs,seatedonback,plainunpatternedcloth,noinventedsacredmotifs [barak-c01, barak-c03, barak-c05]',
 'BOUND upwardintothesky carryingtherider, forelegsstretchedtowardlowviewer andhindlegsthrustingbehind, alertdignifieddogface notfriendlypetportrait',
 'documentedshamanascensiontothesky ridingBarak; dogmovesphysicallyaboveordinarycloudbankwithoutwings,magicribbons orneonhalo [barak-c05]',
 'skyaboveclouds, mainlandlowandindistinctfarbelow [barak-c05]',
 [('anatomy','Blessedshaggyhuntingdog','c01,c02,c03'),('anatomy','Shamanridingsacreddog','c05'),('effect','Ascensiontothesky','c05'),('setting','Sky','c05')],
 'Sacreddog asheavenwardshamanmount, notdogheadedhuman orKerkeseggscene.',
 ['Dogbreed/coatcolour andplainopaque riderclothes editorial, no ethnographicclaims/sacredsymbols. Rideronlyneeded todocumentascension; animalnotgiganticbutlargeenoughtorideassourced. No evilredesign,spiritaura orwings.'],
 'Awe comes fromblessedshaggydog carryingashamanintothesky (barak-c02, barak-c05).','coarsemattedfur,plainopaqueclothandnaturalcloudmoisture',camera='extreme lowclosecloudbankcamera,doghead/forepawsdominant;rider smalleronbackanddistantgroundgiveascension')
make('beast-of-bodmin','the unconfirmed darkpuma-like predatory BeastofBodminMoor',
 'one naturalPUMA-like largecatwithdarkgreytoBLACKfur,onehead/twoeyes,twoears,fourcatlegs,onelongcattail; noleopardspots,mane,horns,sabreteethor supernaturalparts [beast-of-bodmin-c02, beast-of-bodmin-c05]',
 'LUNGE fromdarkmoorgrass towardcloseviewer, mouthdrawnback withnaturalcatcanines, nearforepawclaws reaching,headlowandeyesfixed, no preyinjuryshown',
 'no documentedmagic; reportedpredatory threat tiedtoallegedlivestockdeaths, no confirmedkills depicted [beast-of-bodmin-c01]',
 'BodminMoor Cornwall, darkroughgrass/stone andlowhorizon [beast-of-bodmin-c02]',
 [('anatomy','Darkgrey/blackpuma-likebigcat reported','c02,c05'),('effect','Allegedpredatorythreat blamedforlivestockdeaths','c01'),('setting','BodminMoorCornwall','c02')],
 'Reportedblackpuma-likecat, notprovenblackleopardskull orscientificexistenceclaim.',
 ['Momentoflunge editorialrendering ofallegedpredation, noassertionofconfirmedkill. Darkpumaformc05 notrugleopardc04. Closecamera ordinarybigcatscale,nomagicaleffect.'],
 'Threat comes fromallegedlargepredatorycatlunging atclosemoorlevel (beast-of-bodmin-c01, beast-of-bodmin-c05).','coarsewetblackcatfur,naturalclaws,moorgrassandroughstone',lighting='one lowcoldmoonbeam, deepwalnutshadows andcoldrimlight,ordinarymist')
make('beast-of-exmoor','the unconfirmed blackcat of Exmoor livestockpredationreports',
 'ONEblackPUMA-likecat,onehead/twoeyes,twoears,fourlegs,onelongtail,naturalcatcanines/claws; noleopardspots,mane,horns,sabreteethor magicfeatures [beast-of-exmoor-c05, beast-of-exmoor-c07]',
 'STALK towardviewer throughmoorgrass, shouldersrolling andnearforepaw reachingacrossforegroundstone, lipcurl showsnaturalcanines, musclesreadytopounce',
 'no documentedmagic; reportedlivestockpredationassociatedwithcreature butunconfirmed, novictim/blood orconfirmedkillscene [beast-of-exmoor-c03, beast-of-exmoor-c06]',
 'ruralExmoor Devon/Somerset, subordinategrassandlowstone [beast-of-exmoor-c05]',
 [('anatomy','Reportedgrey/blackleopardorpuma-likecat;selectedpuma','c05,c07'),('effect','Allegedlivestockkillreportsnotconfirmed','c03,c06'),('setting','Exmoor Devon/Somerset','c05')],
 'Reportedblackpuma variant, noassertionofspeciesorverified1983livestockkiller.',
 ['Alertstalk/menace editorialstaging ofreportedpredatoryencounter, notconfirmedattack. Naturalbigcatparts,nooversizedgiantor paranormalpowers. No deadsealhoaxshown.'],
 'Threat comes fromcloseencounterwithreportedblackpredatorycat (beast-of-exmoor-c05, beast-of-exmoor-c06, beast-of-exmoor-c07).','wetblackfur,naturalcatteeth/claws,roughmoorgrass',lighting='one lowwarm sunsetshaft,deepwalnutshadows,ordinarymistside',camera='extreme lowtightforegroundcamera,pumaheadandforepawdominant,noinventedgiantscale')
make('begu-ganjang','the Batak longshadow spirit in the elongatedgrowingform reports',
 'ONElargeTHINELONGATED DARKSHADOW-likehuman-formfigure,onehead silhouette,exactlytwoarm silhouettes/twolegs, opaque continuousshadowbody withoutnudity ordiscernibleeyes/teeth/horns/claws [begu-ganjang-c13, begu-ganjang-c15, begu-ganjang-c16, begu-ganjang-c23]',
 'LENGTHEN upwardwhile STRIDING towardcloseviewer acrossfieldedge, unnaturallylongbody fillsverticalframeanddarkheadleansdown, lowerstridelarge,notstaticdecorativeghost',
 'documentedappearsgrowing tallerandbiggeraslookedat; elongatedshadowbodystretchesupward, no magicalribbons/killbeam or victimdamage [begu-ganjang-c15, begu-ganjang-c16, begu-ganjang-c23]',
 'farmlandfieldedgeassociatedwithguardiantradition, plaincrop silhouettes withoutspecificritual/house [begu-ganjang-c17, begu-ganjang-c24]',
 [('anatomy','Large thin elongated darkshadowlikefigure','c13,c15,c16,c23'),('effect','Apparentgrowthwhenlookedat','c15,c16,c23'),('setting','Fieldassociation','c17,c24')],
 'Documentedlongdarkgrowingbody/shadowform, notformlessvariant orevilowneraccusation.',
 ['Genericclosedhumanoidsilhouette editorialminimalform; nofacecountattributes/eyes invented. Shadowyopaquebodyusesactualdarknessnotneonmist. Noethniccostume, ritualor accusationsagainstpeople; aura fromheightgrowthonly.'],
 'Awe/uncannythreat comes fromthinlongshadowbody thatgrowswhenlookedat (begu-ganjang-c15, begu-ganjang-c23).','matteblackshadowoutline againstroughfieldgrass',lighting='one lowcoldmoonbeambehindfigure,silhouettingbody; deepwalnutfieldshadows,noemittedglow',camera='extreme lowfieldfloorcamera;elongatedfiguretowersovernearordinarycropstems,head/bodydominant')
make('bi-an','the living aged-tiger form of the just prison-gate guardian',
 'ONEAGEDTIGER withonehead/twoeyes,twoears,fournaturaltigerlegs/onetail; greyingwhiskers andweatheredstripedfur; nohorns,wings,dragonbody or lionmane imported [bi-an-c02, bi-an-c10]',
 'STEP protectivelyoutfromprison-gate shadowtowardviewer, nearforepawfirmlyforward, headloweredwithpiercingjudgmentalgaze andmouthslightlyopen,notcalmtamedanimalorstatue',
 'no documentedmagicaleffect; loyaltyandjustice expressedasfirmguardianconfrontation, nolaserjudgmentbeam [bi-an-c09, bi-an-c10]',
 'plainuninscribedprison gate/governmenthall threshold, guardianlivingnotornamentalcarving [bi-an-c04, bi-an-c05, bi-an-c10]',
 [('anatomy','Agedtiger/strongtigerform','c02,c10'),('effect','Loyaljusticeguardian','c09,c10'),('setting','Prisongate/governmentthreshold','c04,c05,c10')],
 'Agedtiger variant, notlionfigure fromalternateoldrecord c08.',
 ['Greywhiskers/weathering editorialagecues. Naturalcatteeth/clawsnotaddedmagicalparts. Livingguardian closeframe, ordinarytigerscale, respectfuljusticecharacter ratherthanevilattack.'],
 'Awe comes frompowerfulagedtiger guardingprisonthreshold andjudgingright/wrong (bi-an-c02, bi-an-c09, bi-an-c10).','coarseweatheredstripedtigerfur,greywhiskersandwornstone')
