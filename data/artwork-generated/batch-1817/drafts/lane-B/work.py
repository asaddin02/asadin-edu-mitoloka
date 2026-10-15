from helpers import *
def make(slug,name,identity,anatomy,moment,power,camera,light,surface,setting,groups,req,variant,choices,aura):
 prompt=f'''ONE original square premium painterly cinematic Mitoloka illustration of {name}, {identity}.
ANATOMY: {anatomy}
MOMENT: {moment}
POWER: {power}
SCALE & CAMERA: extreme low angle; {camera}
LIGHT & WEATHER: {light}
SURFACE: {surface}
SETTING: {setting}
MOOD: menacing / awe-inspiring; dangerous and imposing, never cute, calm or decorative.
HARD CONSTRAINTS: no text, lettering, logo, border, frame or watermark; no extra heads, limbs or fingers; no design borrowed from any film, game, anime or comic; no nudity or explicit gore; no generic glow aura, neon outline or energy ribbons; no tattoos, glyphs or pseudo-text.'''
 spec(slug,groups,req,prompt,variant,choices,aura)
 print(prompt)
