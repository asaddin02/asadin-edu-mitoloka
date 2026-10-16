import fs from 'node:fs';
const base='data/artwork-generated/batch-2079';
for(const slug of ['irudica','keneo']){
 const s=JSON.parse(fs.readFileSync(`${base}/${slug}.json`));
 if(slug==='irudica'){
 s.prompt=`ONE original square premium painterly cinematic Mitoloka illustration of Irudica, the fierce red-haired spirit dwelling in a whirlwind in Croatian folklore.
ANATOMY: ONE adult female spirit, one head, two eyes, two arms, two legs completely hidden under a CLOSED fully opaque ankle-length tattered black gown with opaque dark leggings beneath. Long vivid RED HAIR whipping horizontally. Fierce wild glare with bared ordinary teeth, no horns or wings. [irudica-c04,irudica-c06]
MOMENT: SURGE toward the viewer as the leading edge of a thunderstorm, twist at the waist inside a powerful spinning whirlwind. She defiantly looks toward us, fierce and dangerous, never frightened or shielding her face. Arms angled to balance, no spellcasting gesture.
POWER: A VERY VISIBLE dense funnel-shaped spinning column of saltwater spray, dust and flying pebbles circles her fully covered lower body, narrows toward the sea rocks below, and coils in broad continuous physical bands around her. The whirlwind is her dwelling [irudica-c01], she leads heavy thunderstorms [irudica-c07]. Behind and to one side, a branching thunderbolt descends FROM THE SKY chasing her, hitting a rock behind her. Lightning is God's pursuit of her, NEVER emitted from her hands/body. [irudica-c05]
SCALE & CAMERA: close full figure, slightly low camera with NO upskirt view; face, red hair and recognizable funnel together fill most of frame, no invented giant size.
LIGHT & WEATHER: single dominant distant lightning flash through black thunderclouds, deep walnut shadows and sharp rim light through spray.
SURFACE: heavy wet opaque cloth, soaked red hair strands, rough limestone, white salt spray and dark suspended grit.
SETTING: rocky Dalmatian Hvar coast under thunderclouds. [irudica-c05,irudica-c10]
MOOD: violent and uncanny storm spirit actively advancing, visibly dangerous rather than ordinary woman in weather.
HARD CONSTRAINTS: no bare thighs, knees or hips; no parted skirt or lifted hem; no aura, magic glow, text, lettering, logo, border, frame, watermark, extra limbs or fingers; no borrowed film/game/anime design; no nudity or gore.`;
 s.depicted_variant='Fierce red-haired Irudica rides visibly inside a spinning coastal whirlwind; pursuing lightning strikes behind her.';
 s.visual_requirements=[{kind:'anatomy',description:'Female spirit with long red hair; all legs hidden under closed opaque gown.',claim_ids:['irudica-c04','irudica-c06']},{kind:'effect',description:'Dense clearly visible spinning whirlwind surrounding lower body; storm front leads with spirit while external lightning pursues her from sky.',claim_ids:['irudica-c01','irudica-c05','irudica-c07']},{kind:'setting',description:'Dalmatian/Hvar rocky sea coast.',claim_ids:['irudica-c05','irudica-c10']}];
 s.artistic_choices=['Closed ankle-length dark gown and opaque leggings are editorial modest clothing, never split or lifted.','Human female presentation follows Salome identity c04; long red hair c06 is the distinctive documented trait.','Visible spray/dust vortex literalizes dwelling in whirlwind c01, not an aura; fierce expression interprets evil spirit c01.','No giant scale or invented supernatural anatomy; external lightning is pursuit c05, never her weapon.'];
 }else{
 s.prompt=`ONE original square premium painterly cinematic Mitoloka illustration of Keneo, the old ONI who judges the weight of sin by hanging souls clothing at the Sanzu River.
ANATOMY: ONE clearly demonic ONI-FORMED elderly man, ONE head, TWO eyes, TWO arms, TWO legs, glaring deep-set eyes, massive furrowed brow, coarse weathered DARK RED oni skin, bared ordinary teeth, wild long grey hair and beard, TWO SMALL blunt oni horns. He wears a CLOSED fully opaque coarse black-brown robe from neck to ankles. [keneo-c01,keneo-c02,keneo-c08]
MOMENT: Glare down toward viewer in severe judgement as he WITHDRAWS BOTH empty open five-fingered hands away from an EMPTY pale robe he has just hung. Brow lowered, mouth a stern snarl, never startled or pleading.
POWER: A thin living branch of the HUGE Eryoju tree begins high at left, stretches horizontally then BENDS IN A DEEP DOWNWARD CURVE solely from the impossible weight of ONE empty pale robe hanging freely at the tip. A CLEAR visible gap separates his hands from the branch and robe; NO HANDS pull, support or touch either. The branch is thin enough that deep sag visibly communicates weight of sin, while the trunk is massive. [keneo-c03,keneo-c05,keneo-c08]
SCALE & CAMERA: low close view, oni elder face fills upper right third, down-curved branch and empty robe occupy left third, hands between with clear gaps; great trunk and dark river behind. No invented giant size for Keneo.
LIGHT & WEATHER: one cold moon behind cloud; stark rim light on coarse red face and robe, deep walnut shadows, ordinary river mist.
SURFACE: coarse red aged skin, tangled grey hair, worn opaque cloth, deeply furrowed bark and strained thin living wood.
SETTING: great Eryoju beside Sanzu River in the folk Buddhist underworld. [keneo-c01,keneo-c08]
MOOD: sacred awe and stern terrifying judgement, unmistakable oni elder rather than ordinary old man hanging laundry.
HARD CONSTRAINTS: no people inside weighed robe, no victims/torture/skin removal, no nudity or gore; no generic aura, neon or energy ribbons; no text, logo, border or watermark; no extra limbs/fingers; no borrowed film/game/anime/comic design.`;
 s.depicted_variant='Stern red-skinned oni elder releasing an empty robe whose sin-weight bends a thin Eryoju branch deeply down beside Sanzu River.';
 s.artistic_choices=['Dark-red weathered oni skin, fierce brow, bared teeth, wild hair and two small blunt horns are editorial interpretation of documented oni-formed old man c01/c08, following explicit Claude correction.','Opaque coarse robe is modest editorial clothing. No torture or victims depicted.','Thin deeply sagging branch and hands visibly apart make the documented c05/c08 sin weighing readable.','Moonlight and close low framing are editorial, no added magic or giant scale.'];
 }
 for(const k of ['root_visual_review','correction_notes','visual_review'])delete s[k];
 fs.writeFileSync(`${base}/drafts/resume_2000_b/${slug}.json`,JSON.stringify(s,null,2)+'\n');
}
