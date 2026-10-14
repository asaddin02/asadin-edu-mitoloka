from helpers import spec,decline
D='no text, lettering, logo, border, frame or watermark; no extra heads, limbs or fingers; no film, game, anime or comic design; no nudity or explicit gore; no generic glow aura, neon outline or energy ribbons.'
def make(slug,groups,requirements,lines,variant,choices,aura):
 ids=lambda ns:[slug+'-c'+n for n in ns.split(',') if n]
 groups={k:ids(v) for k,v in groups.items()}
 req=[dict(kind=k,description=d,claim_ids=ids(c)) for k,d,c in requirements]
 prompt='ONE original square premium painterly cinematic Mitoloka illustration of '+lines[0]+'.\n'+'\n'.join(lines[1:])+'\nHARD CONSTRAINTS: '+D
 spec(slug,groups,req,prompt,variant,choices,aura)
make('four-symbols',dict(wujud='02,05,06',kekuatan_perbuatan='01,03',tempat='01',sifat='01'),[
('anatomy','Empat penjaga saja: naga biru, burung merah, harimau putih, kesatuan kura-kura hitam berbelit ular.','02,05,06'),('setting','Langit bintang sebagai konstelasi empat penjuru.','01')],[
'Four Symbols, exactly FOUR sacred directional constellation guardians',
'ANATOMY: four guardian compositions: one Azure Dragon with one head, one Vermilion Bird with one head and two wings, one White Tiger with one head and four legs, one Black Turtle-Snake composite with a turtle head and ONE snake wound continuously around its shell. The snake belongs to the turtle-snake entity and is never a separate fifth guardian. Distinct dragon/bird/tiger/turtle faces, all readable. [four-symbols-c02,c05,c06]',
'MOMENT: converge toward the low camera in coordinated guarding movement: azure dragon curves down across upper left, vermilion bird sweeps its red wings across upper right, white tiger leaps forward at lower left, black turtle pushes forward at lower right while its attached serpent tightens around its shell. Four interlocking silhouettes, no independent snake floating elsewhere.',
'POWER: no documented attack; do not depict fire, lightning, magical water or energy. Majesty through physical anatomy, directional convergence and constellation context only. [four-symbols-c01,c03]',
'SCALE & CAMERA: tight low-angle perspective, four entities together fill 90 percent square; no human or giant-size comparison.',
'LIGHT & WEATHER: single warm horizon light, deep night shadows, antique gold rim light, natural star points only.',
'SURFACE: azure dragon scales, layered vermilion feathers, coarse white tiger fur with dark stripes, black weathered turtle shell and natural dark serpent scales.',
'SETTING: dark celestial sky of their constellations, subtle natural stars; no diagram, symbols, constellations joined by lines or invented palace. [four-symbols-c01]',
'MOOD: awe-inspiring sacred protectors, energetic and imposing, never evil, cute or decorative.'],
'Empat penjaga konstelasi maju dalam satu komposisi, Xuanwu tetap satu kesatuan kura-kura-ular.',
['Gerak konvergen dan cahaya horizon editorial; tidak menafsir asosiasi unsur c03 sebagai kuasa serangan.','Detail warna/bulu/sisik mengikuti jenis hewan c02; satu ular melilit kura-kura bukan entitas kelima.'],
'Keagungan empat penjaga c01/c02 lewat konvergensi aktif tanpa efek kuasa rekaan.')
make('fuzanglong',dict(wujud='01,04',kekuatan_perbuatan='01,03,06',tempat='01,07',sifat='01'),[
('anatomy','Satu naga bawah tanah dengan satu mutiara berharga.','01,04'),('effect','Naga menerobos tanah sebagai asal gunung api dalam cerita.','03'),('setting','Tanah bawah dunia dan harta terpendam alami/buatan.','01,02,07')],[
'Fuzanglong, the underworld dragon guarding buried treasure and a treasured magical pearl',
'ANATOMY: one original Chinese dragon with a long scaled serpentine body, one head and two eyes, four conservative clawed legs, no wings; one large pearl held close beneath a foreclaw. No extra heads or pearls. Conventional dragon silhouette is restrained editorial interpretation of the word dragon, not a source-specific horn or claw count. [fuzanglong-c01,c04]',
'MOMENT: thrust its head and front body upward through a broken rock ceiling toward the viewer while sheltering its pearl, mouth open in commanding warning, visibly connected coils below.',
'POWER: a volcanic breach physically cracks earth and sends stones and dark ash upward as the dragon breaks through to report to heaven; warm molten rock visible only in the distant fissure. The pearl casts no magic beam. [fuzanglong-c03]',
'SCALE & CAMERA: extreme low-angle close view, head and body fill 85 percent square; avoid unsupported humans or size comparisons.',
'LIGHT & WEATHER: single molten-rock backlight from fissure, amber rim on scales, dark volcanic ash and falling natural rock fragments.',
'SURFACE: rugged dark umber scales, mineral dust, scratched old gold and unpolished natural gems, smooth ivory pearl.',
'SETTING: earthen underworld cavern, partially revealed buried treasure of natural minerals and old unmarked metal vessels. [fuzanglong-c01,c02,c07]',
'MOOD: imposing treasure guardian, awe and physical danger, never cute or decorative.'],
'Naga penjaga harta menerobos tanah gunung api sambil melindungi mutiara.',
['Anatomi naga konservatif bersisik/serpentine berkaki empat tanpa sayap adalah interpretasi editorial c01; bukan klaim tanduk/jari sumber.','Bukaan magma adalah visualisasi gunung api c03, tidak menambahkan kuasa napas-api. Mutiara c04 tidak diberi aura atau sinar rekaan.'],
'Terobosan vulkanik c03 dan tatapan penjaga harta c01 mendominasi.')
make('gajasimha',dict(wujud='01,07,10',kekuatan_perbuatan='08',tempat='08',sifat='08'),[
('anatomy','Tubuh singa dengan satu kepala gajah dan belalai.','01,07,10'),('setting','Pintu utama natamandapa kuil konteks penjaga.','08')],[
'Gajasimha, the sacred living elephant-headed lion guardian',
'ANATOMY: exactly one elephant head with two eyes, two elephant ears, one trunk and two natural tusks attached to one powerful lion body with four lion legs, lion mane around the neck and one lion tail. No second animal or second lion face. [gajasimha-c01,c07,c10]',
'MOMENT: bound down from the dark temple threshold toward the low viewer, one forepaw planted and one raised, trunk sweeping forward and mane blowing; all four leg attachments plausible.',
'POWER: no documented magical attack; guarding action and hybrid anatomy only. Ordinary dust stirred by paws, no shockwaves or supernatural ground cracks.',
'SCALE & CAMERA: very low close camera, elephant head and lion torso fill 85 percent square; no humans or invented giant-size comparison.',
'LIGHT & WEATHER: one warm oil lamp within the doorway, gold rim light on elephant ears and mane, deep shadows, physical disturbed dust.',
'SURFACE: thick creased elephant skin, coarse lion mane and ochre fur, weathered stone threshold.',
'SETTING: main doorway of temple natamandapa as a living dvarapala guardian rather than sculpture; restrained dark stone doorway without specific invented iconography. [gajasimha-c08]',
'MOOD: sacred and awe-inspiring guardian, solemn powerful protection, never evil or cute.'],
'Gajah berkepala satu pada tubuh singa hidup melangkah aktif dari pintu kuil.',
['Tidak mencampur motif singa menindih gajah dengan varian hybrid elephant-headed c01/c10.','Tusk/mane/detail tubuh hewan dan lampu/pintu polos editorial konservatif; tidak mengklaim ornamentasi kuil khusus. Tidak ada efek kuasa karena sumber tidak memuatnya.'],
'Anatomi hybrid c01/c10 dan tugas penjaga pintu c08 memberi keagungan aktif.')
make('gaoh',dict(wujud='01,02',kekuatan_perbuatan='04,05,07',tempat='07,08',sifat='04,10'),[
('anatomy','Raksasa berwujud pria tua soliter.','01,02'),('effect','Berjuang melepas rantai pada batu sehingga angin bertiup; badai.','04,07'),('setting','Terikat batu dalam langit utara luas.','07,08')],[
'Gaoh, the mostly benevolent giant wind spirit in the form of a solitary old man',
'ANATOMY: one giant elderly man with one head, two eyes, two arms and two legs, weathered face and long grey hair. Fully opaque plain dark mantle and layered cloth cover the whole torso, hips and legs; no invented tribal headdress or sacred motifs. Massive iron chains bind him to a natural rock. [gaoh-c01,c02,c07]',
'MOMENT: strain against the taut chains with both hands and planted feet, torso twisting toward the low viewer, eyes resolute rather than evil; hair and cloth swept strongly in one direction.',
'POWER: his attempt to break free drives actual gale wind, visible as flying cloud banks and dust ripped from the rock, a storm physically churns around the rock without magical ribbons or lightning beams. [gaoh-c04,c07]',
'SCALE & CAMERA: extreme low angle; his colossal body fills the frame against huge cloud banks, distant small mountain ridges far below establish documented giant proportions. [gaoh-c01,c08]',
'LIGHT & WEATHER: one warm break in storm clouds lights face and hands, deep storm shadows, powerful wind, natural dust.',
'SURFACE: old creased skin, grey wind-tangled hair, rough opaque fabric, tarnished iron chain and jagged rock.',
'SETTING: broad northern sky where the giant is confined, rock suspended amid ordinary cloud banks as editorial spatial staging. [gaoh-c07,c08]',
'MOOD: awe-inspiring sacred wind authority, mostly benevolent and obedient to Creator, no malicious cannibal scene, no demon face. [gaoh-c04,c10]'],
'Pria tua raksasa terikat batu berjuang dan menghasilkan angin badai.',
['Busana buram tanpa motif tribal, jenis logam rantai, tata ruang batu dan cahaya celah awan editorial.','Memilih versi terikat batu langit utara c07/c08; tidak mencampur westsky/cave atau empat hewan-windwatchers. Tidak merobek langit karena c09 adalah kondisi hipotetis bila bebas.'],
'Proporsi raksasa c01/c08 dan angin fisik saat berjuang c07 memberi keagungan, bukan evil.')
make('giant-anaconda',dict(wujud='01,02,07',kekuatan_perbuatan='07',tempat='01,07',sifat='07'),[
('anatomy','Ular anaconda raksasa lebih dari 9 meter menurut laporan legenda, bukan specimen fact.','01,02,07'),('effect','Membalik/meremukkan perahu kayu dengan tubuh.','07'),('setting','Hutan hujan Amazon.','01,07')],[
'the Giant Anaconda, the legendary immense serpent of Amazon tales, a report rather than verified zoology',
'ANATOMY: one enormous anaconda with exactly one head, two eyes, a single unbroken muscular coiling body and one tail, no legs, horns or wings. Natural olive-black blotched scales, closed powerful mouth without exaggerated fangs. [giant-anaconda-c01,c02,c07]',
'MOMENT: tighten a heavy coil around a wooden canoe, visibly buckling and tipping its hull while lifting its head directly toward the low viewer; continuous thick body loops behind the boat, no gore or people.',
'POWER: physical boat capsizing and crushing as reported in the modern account of the legend, no spell, electrical effect or invented poison. Water erupts from the rolling hull. [giant-anaconda-c07]',
'SCALE & CAMERA: waterline close wide view; huge snake fills foreground, a recognisable full-size wooden canoe in its coil supports the reported more-than-nine-meter scale without extrapolating a hundred-meter monster. [giant-anaconda-c02,c07]',
'LIGHT & WEATHER: single dusk break through rainforest canopy, warm gold rims, very dark green shadows, natural muddy splashes.',
'SURFACE: wet textured blotched scales, soaked scratched canoe planks, muddy river water, dense humid foliage.',
'SETTING: flooded Amazon rainforest river margin. [giant-anaconda-c01,c07]',
'MOOD: dangerous crushing confrontation, powerful documented legendary scale, never ordinary zoological portrait.'],
'Legenda anaconda besar membalik dan menekan kano kayu, memakai account c07.',
['Perahu kosong, air/latar Amazon editorial; ukuran menggunakan laporan c02/c07 dan tidak dipresentasikan sebagai specimen terbukti.','Efek kapal dipakai hanya dari modern-popular-culture c07, bukan atribut universal atau riset biologis.'],
'Anaconda berukuran legenda c01/c02 menekan kano c07 memberi ancaman nyata.')
make('gl-r',dict(wujud='01',kekuatan_perbuatan='01,04',tempat='01,04',sifat='01'),[],[
'Glær, the Norse horse named among the mounts of the gods',
'ANATOMY: not generated; only generic horse form is documented.','MOMENT: not generated.','POWER: no active distinguishing manifestation documented.','SCALE & CAMERA: not generated.','LIGHT & WEATHER: not generated.','SURFACE: not generated.','SETTING: Yggdrasil judging journey is narrative context [gl-r-c01,c04].','MOOD: no supported distinctive depiction.'],
'Tidak digambar: kuda tanpa ciri fisik atau manifestasi aktif pembeda.',
['Glær clear/glassy/shining c02/c06 adalah etimologi, bukan bukti tubuh kaca atau pancaran cahaya; tidak mengimpor kaki delapan Sleipnir atau pemilik dewa tertentu.'],
'Tidak ada manifestasi cukup untuk melewati penolakan hewan biasa.')
decline('gl-r','Klaim c01/c04 hanya memberi bentuk kuda dan perjalanan para dewa ke Yggdrasil, tanpa penampilan pembeda atau manifestasi aktif. Etimologi clear/glassy/shining c02/c06 bukan kuasa cahaya/tubuh kaca; membuat kuda biasa atau ciri rekaan gagal GAMBAR6.4/6.5.')
make('gol-bogalar',dict(wujud='01,04,10',kekuatan_perbuatan='02,04,10',tempat='01,03,10',sifat='04'),[
('anatomy','Satu bull air dan satu bull peternak yang bergulat.','04,10'),('effect','Bull lake muncul dari air dan bergulat bull manusia.','02,04,10'),('setting','Danau pegunungan Karçal pada cahaya pagi awal.','01,02,10')],[
'Göl Boğaları, a lake bull emerging from a mountain lake to wrestle a shepherd\'s bull',
'ANATOMY: exactly TWO bulls, one central dark lake bull and one secondary brown terrestrial bull, each with one head, two eyes, two natural horns, four hooved legs and one tail. No steel horns, aquatic fins, extra heads, fantasy eyes or invented monster anatomy. [gol-bogalar-c04,c10]',
'MOMENT: the massive-framed lake bull surges half out of the water and locks its horns with the shore bull, both necks straining and heads lowered near the viewer; the lake bull dominates, legs physically driving the surge.',
'POWER: physical emergence and wrestling at the shore, a dense sheet of water drains from the lake bull and waves crash from its movement; no magical water manipulation or curse effects. [gol-bogalar-c02,c04,c10]',
'SCALE & CAMERA: extreme low waterline camera, lake bull head and shoulders fill 65 percent square, its rival side-on at right secondary but clearly identifiable, natural bull scale, no giant comparison.',
'LIGHT & WEATHER: first dawn light from one narrow warm horizon strip, wet gold rimlight, deep mountain shadow, natural spray and cold mist. [gol-bogalar-c02]',
'SURFACE: soaked dark coarse fur, heavy wet natural horns, brown rival fur, rocky shore and dark lake water.',
'SETTING: mountain lake in Karçal mountains of Ardanuç, rocky shore at dawn. [gol-bogalar-c01,c02,c10]',
'MOOD: mythic aquatic confrontation, dangerous wrestling action, never passive ordinary grazing livestock.'],
'Bull danau Karçal muncul dan bergulat bull peternak pada fajar.',
['Bulu hitam/coklat pembeda editorial, bukan warna bersumber. Tidak menambah horn-steel karena atribut bull blacksmith versi lain c08.','Tidak memakai buffalo appearance c09 dari rumour Van Monster lain, atau darah/curses c05/c06/c13. Efek air seluruhnya kontak fisik c02/c04/c10.'],
'Muncul dari danau dan bergulat c02/c04/c10 memberi ancaman naratif tanpa anatomi rekaan.')
make('golden-kite',dict(wujud='01,02,05',kekuatan_perbuatan='02,05',tempat='05,06',sifat='01,04'),[
('anatomy','Satu burung kite emas suci bertengger ujung busur Jinmu, bukan gagak tiga kaki.','01,02,05'),('effect','Cahaya emas seperti kilat menyilaukan musuh; hujan es dan langit gelap.','02,05'),('setting','Medan pertempuran Jinmu/Tomi.','05,06')],[
'the Golden Kite, sacred golden spirit bird perched on Jinmu\'s bow and dazzling the opposing army',
'ANATOMY: exactly ONE golden kite raptor with one beaked head, two piercing eyes, two broad wings and exactly TWO taloned feet visibly gripping the TIP of a tall curved bow. No crow anatomy, no third leg. Jinmu is secondary, one fully clothed distant figure holding the bow, with opaque plain historical robes and no invented ornate imperial crown. [golden-kite-c01,c02,c05]',
'MOMENT: brace on the bowtip with talons visibly planted and sweep both wings outward toward the low viewer, golden head turned down in commanding direct gaze; opposing warriors behind recoil and shield their eyes.',
'POWER: documented bright golden lightning-like LIGHT radiates physically from golden feathers and illuminates the hail and enemy faces, dazzling the army; depict no electrical attack bolts, no floating rune or circular aura. Sudden dark sky and falling hail. [golden-kite-c02,c05]',
'SCALE & CAMERA: extreme low close viewpoint to bowtip, kite fills 80 percent square through perspective, Jinmu hand and opaque sleeve near base of bow, small warriors blurred behind; no unsupported giant bird size.',
'LIGHT & WEATHER: bird\'s documented golden light is the single dominant source, deep storm-dark background, illuminated falling hail, antique gold/umber palette. [golden-kite-c05]',
'SURFACE: highly tactile metallic-golden feather barbs, dark gold beak, rough wooden bow and translucent hailstones.',
'SETTING: dark battlefield from Jinmu narrative, opposing army reacting, no flag lettering or historical emblems. [golden-kite-c05,c06]',
'MOOD: awe-inspiring sacred beneficent omen, commanding and luminous, never evil, demonic or cute.'],
'Kite emas dua kaki pada ujung busur menyilaukan pasukan dalam hujan es.',
['Cahaya emas c02/c05 adalah pengecualian terdukung, bukan aura generik. Tidak memberi lightningattack; pola feathers golden dan busana plain editorial.','Tidak mencampur Yatagarasu c03; kaki dua, tidak gagak. Framing membuat burung dominan tanpa klaim giant.'],
'Cahaya penyilau documented c02/c05 dan wingbrace pada bowtip membuat keagungan sakral.')
