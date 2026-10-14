import sys,json,os
sys.path.insert(0,os.path.dirname(__file__))
from helpers import spec,finish,reject,decline
C={}
def add(slug,name,anatomy,moment,power,setting,ids_a,ids_e,ids_s,ids_t=[],variant='',choices=[]):
 ids=lambda ns:[slug+'-c'+str(n).zfill(2) for n in ns]
 groups={'wujud':ids(ids_a),'kekuatan_ranah_perbuatan':ids(ids_e),'tempat':ids(ids_s),'sifat':ids(ids_t)}
 req=[{'kind':'anatomy','description':anatomy,'claim_ids':ids(ids_a)}]
 if ids_e:req.append({'kind':'effect','description':power,'claim_ids':ids(ids_e)})
 if ids_s:req.append({'kind':'setting','description':setting,'claim_ids':ids(ids_s)})
 prompt=f'''ONE original square premium painterly cinematic Mitoloka illustration of {name}.
ANATOMY: {anatomy} [{', '.join(ids(ids_a))}]
MOMENT: {moment}
POWER: {power} [{', '.join(ids(ids_e))}]
SCALE & CAMERA: close low camera, subject occupies most of the square, sharp diagnostic anatomy, no unclaimed gigantic size; all required countable features separated and visible.
LIGHT & WEATHER: one dominant warm raking dusk light, deep walnut shadows and antique-gold highlights, high contrast, atmospheric depth without magical glow.
SURFACE: tactile natural skin, fur, feathers, scales or cloth as appropriate, painterly material detail, never plastic.
SETTING: {setting} [{', '.join(ids(ids_s))}]
MOOD: imposing and awe-inspiring or threatening according to documented character, never cute, calm or decorative.
HARD CONSTRAINTS: no text, lettering, pseudo-writing, rune, logo, border, frame or watermark; no extra heads, limbs or fingers; no design borrowed from any film, game, anime or comic; no nudity or explicit gore; no generic glow aura, neon outline or energy ribbons. No decorative symbols or inscriptions.''' 
 C[slug]=dict(groups=groups,req=req,prompt=prompt,variant=variant or anatomy,choices=['Framing, dusk light, walnut/antique-gold palette and surface treatment are editorial choices, not source facts.','No generic supernatural effects; visible physical movement only follows cited anatomy, habitat or deed.']+choices,aura=power+' '+', '.join(ids(ids_e) or ids(ids_a)))
add('qianlima','Qianlima, the exceptional thousand-li horse','One horse head, two eyes, four horse legs, one mane and one tail; powerful normal horse anatomy, no horns or wings','Gallops directly past the ground-level viewer, body pitching into a racing stride, nostrils flared, flying mane; all four hooves distinct','Its thousand-li travel ability is suggested only by extreme running momentum: hooves fling dirt backward; no magical trails','A simple earth route, unspecified editorial setting; no invented named place',[1],[1],[],choices=['Coat colour and unlocated earthen route are editorial; the horse is not made a giant.'])
add('tahoe-tessie','Tahoe Tessie, choosing the 1865 massive serpent-like sighting','One massive serpent-like aquatic body, one serpent head, two eyes and one tapering tail; no legs, wings, horns or plesiosaur design','Bursts toward the close waterline viewer, neck coiling out of the lake and jaw opening; most body fills the square','No documented supernatural power; large serpent movement displaces Lake Tahoe water into broad heavy splashes','Lake Tahoe at the California–Nevada border',[3],[3,1],[1],variant='1865 massive serpent-like account, not later friendly mascot or headless hump report.',choices=['Alternative sightings without head/tail are not combined with the chosen 1865 serpent account.'])
add('wd-q22100555','Quru, the human-faced three-footed bird of Mount Daoguo','One small duck-like bird body with two wings, white feathered head bearing one HUMAN FACE with two eyes and a human mouth, exactly THREE small avian legs and three feet near the tail, one bird tail; no beak on the human face','Pushes off a bare rock toward the viewer, wings raised and human mouth open in a cry, all THREE feet stretched apart below body in clear silhouette','The open human mouth suggests its self-naming call; no written sound and no supernatural effects','Mount Daoguo, rocky mountainside',[1,2,6],[3],[4],variant='White-headed human-faced Quru with three feet, not the alternate three hands.')
if __name__=='__main__':
 slug=sys.argv[1];d=C[slug];spec(slug,**d);print(d['prompt'])
