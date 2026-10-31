"""Soundtrack for the reel -> audio.wav (stereo, 48 kHz). No voice anywhere.
Music, ringtone, whooshes, risers and impacts are synthesised here; UI cues are real
recordings from uisfx (CC0, see sfx/LICENSE-AUDIO). All cue times come from timeline.js."""
import json, re, subprocess, wave
from pathlib import Path
import numpy as np

HERE = Path(__file__).parent
T = json.loads(re.sub(r'(\w+):', r'"\1":', re.search(r'\{.*\}', (HERE / 'timeline.js').read_text(), re.S).group(0)))
SR, DUR = 48000, T['DUR']
N = int(SR * DUR)
L, R = np.zeros(N), np.zeros(N)
rng = np.random.default_rng(11)
hz = lambda m: 440 * 2 ** ((m - 69) / 12)  # midi -> Hz
tt = lambda d: np.arange(int(SR * d)) / SR


def add(sig, start, gain=1.0, pan=0.0):
    i = int(start * SR)
    if i < 0: sig, i = sig[-i:], 0
    if i >= N: return
    sig = sig[:N - i] * gain
    L[i:i + len(sig)] += sig * np.sqrt(.5 * (1 - pan)); R[i:i + len(sig)] += sig * np.sqrt(.5 * (1 + pan))


def sample(name):
    pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(HERE / 'sfx' / f'{name}.mp3'), '-f', 's16le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    return np.frombuffer(pcm, np.int16) / 32768.0


def lowpass(x, fc):
    sp = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); sp *= 1 / np.sqrt(1 + (f / fc) ** 4); return np.fft.irfft(sp, len(x))


def noise_band(d, lo, hi):
    n = rng.standard_normal(int(SR * d)); sp = np.fft.rfft(n); f = np.fft.rfftfreq(len(n), 1 / SR)
    sp *= ((f > lo) & (f < hi)); s = np.fft.irfft(sp, len(n)); return s / (np.abs(s).max() + 1e-9)


def whoosh(d=.7, lo=300, hi=6000):
    t = tt(d); k = t / d; return noise_band(d, lo, hi) * np.sin(np.pi * k) ** 3


def riser(d, f0=120, f1=900):
    t = tt(d); k = t / d; f = f0 * (f1 / f0) ** k; ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) * .5 + noise_band(d, 2000, 9000) * .35 * k) * k ** 2


def impact(d=2.2):
    t = tt(d); f = 38 + 90 * np.exp(-t * 18)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.2)
    crack = noise_band(d, 80, 5000) * np.exp(-t * 14)
    return body * .9 + crack * .45


def tick(f=2600, d=.04):
    t = tt(d); return np.sin(2 * np.pi * f * t) * np.exp(-t * 120)


def glitch(d=.35):
    t = tt(d); sq = np.sign(np.sin(2 * np.pi * (180 + 900 * rng.random()) * t)); gate = (np.floor(t * 60) % 2)
    return (sq * .3 + noise_band(d, 500, 8000) * .5) * gate * np.exp(-t * 4)


def ring(d=.85):  # original two-tone marimba ringtone
    out = np.zeros(int(SR * d))
    for j, m in enumerate([79, 84, 79, 84]):
        t = tt(.32); s = (np.sin(2 * np.pi * hz(m) * t) + .3 * np.sin(2 * np.pi * hz(m) * 4 * t)) * np.exp(-t * 9)
        i = int(j * .18 * SR); out[i:i + len(s)] += s[:len(out) - i]
    return out


def pad(notes, start, end, vel=.05, fade=1.2, cutoff=1400):
    d = end - start + fade; t = tt(d); env = np.minimum(1, t / fade) * np.minimum(1, (d - t) / fade); out = np.zeros_like(t)
    for m in notes:
        for det in (-.15, 0, .16):
            out += np.sign(np.sin(2 * np.pi * (hz(m) + det) * t + rng.random() * 6)) * .5 + np.sin(2 * np.pi * (hz(m) + det) * t)
    add(lowpass(out * env, cutoff) * vel / len(notes), start - fade / 2, pan=0)


def pulse(start, end, bpm, midi, vel=.25):  # sub-bass heartbeat
    step = 60 / bpm; t0 = start
    while t0 < end:
        t = tt(.35); f = hz(midi); add(np.sin(2 * np.pi * f * t) * np.exp(-t * 9) * vel, t0); t0 += step


# ---------------- music ----------------
pad([50, 57, 60, 65], 0.0, T['s2'], vel=.05, cutoff=900)                     # hook: Dm(add) haze
pad([46, 53, 58, 62], T['s2'], T['s3'], vel=.06, cutoff=1100)                 # call: Bb
pulse(T['s2'], T['s3'], 96, 38, .22)
pad([43, 50, 55, 58, 61], T['s3'], T['freeze'], vel=.07, cutoff=1600)         # app: tension (G-dim colour)
pulse(T['s3'], T['freeze'] - .1, 128, 38, .26)
pad([38, 45, 48, 53], T['freeze'] + .4, T['s5'], vel=.05, cutoff=700)         # reveal: dark low
pad([50, 57, 62, 66, 69], T['s5'], T['s7'], vel=.055, cutoff=2000)           # solution: D major, clear
pulse(T['s5'], T['s7'], 92, 38, .14)
pad([50, 57, 62, 64, 69], T['s7'], DUR, vel=.06, cutoff=2400)                 # end: Dadd9
def pluck(m, v=.18):
    t = tt(1.2); return (np.sin(2 * np.pi * hz(m) * t) + .4 * np.sin(4 * np.pi * hz(m) * t)) * np.exp(-t * 5) * v
for b, m in [(T['title5'], 74), (T['quote'], 78), (T['r1'], 81), (T['r2'], 78), (T['r3'], 74), (T['end1'], 74), (T['end1'] + .12, 81), (T['logo'] + .9, 86)]:
    add(pluck(m), b, pan=.2)

# ---------------- sound design (picture-synced) ----------------
add(whoosh(.6, 400, 7000), 0.0, .25)
add(whoosh(.5, 800, 9000), T['hook1'], .18, -.3)
add(whoosh(.5, 800, 9000), T['hook2'], .18, .3)
for r in T['ring']: add(ring(), r, .32)
add(sample('press'), T['accept'], .8)
for s in (T['s2'], T['s3'], T['s5'], T['s6'], T['s7']): add(whoosh(.8), s - .4, .45, -.2)
for b in (T['b1'], T['b2'], T['b3']): add(sample('receive'), b, .55, .15)
add(sample('warning'), T['flag'], .5)
add(sample('notification'), T['notif'], .8)
add(sample('press'), T['tapNotif'], .7)
add(whoosh(.4, 1500, 9000), T['app'] - .1, .25)
k = T['count']
while k < T['countEnd']: add(tick(2400 + 900 * (k - T['count'])), k, .18); k += .06
add(sample('typing'), T['cursor'] + .2, .35)
add(riser(T['freeze'] - T['cursor']), T['cursor'], .35)
add(impact(), T['freeze'], .95)
add(glitch(.45), T['freeze'], .4)
for j in range(6): add(sample('typing'), T['scramble'] + j * .1, .3, (-1) ** j * .3)
add(glitch(.25), T['scramble'], .35)
add(sample('error'), T['scramble'] + .7, .7)
add(impact(1.4), T['valEq'], .5)
for j in range(22): add(tick(3000 + 2000 * rng.random(), .06), T['money'] + j * .07 + rng.random() * .03, .12, rng.uniform(-.7, .7))
add(sample('blocked'), T['money'] + .45, .45)
add(glitch(.2), 19.95, .25)
for b in (T['x1'], T['x2'], T['x3']): add(sample('delete'), b + .1, .5)
add(sample('info'), T['quote'], .55)
add(sample('disconnect'), T['hang'], .8)
for b in (T['r1'], T['r2'], T['r3']): add(sample('select'), b, .5)
add(impact(1.8), T['end1'], .55)
for j in range(9): add(sample('typing'), T['logo'] + j * .1, .28, (-1) ** j * .25)
add(sample('success'), T['logo'] + .95, .6)


# ---------------- reverb, master ----------------
def reverb(x, seed, secs=1.8, mix=.22):
    r = np.random.default_rng(seed); n = int(SR * secs); t = np.arange(n) / SR
    ir = r.standard_normal(n) * np.exp(-t * 4); ir[:int(.01 * SR)] = 0; ir /= np.sqrt((ir ** 2).sum())
    m = 1 << int(np.ceil(np.log2(len(x) + n))); wet = np.fft.irfft(np.fft.rfft(x, m) * np.fft.rfft(ir, m), m)[:len(x)]
    return x * (1 - mix) + wet * mix * 1.4


L, R = reverb(L, 1), reverb(R, 2)
t = np.arange(N) / SR
master = np.minimum(1, t / .05) * np.minimum(1, (DUR - t) / .6)
L, R = np.tanh(L * master * 1.4), np.tanh(R * master * 1.4)  # soft clip
peak = max(np.abs(L).max(), np.abs(R).max()); L, R = L / peak * .9, R / peak * .9
pcm = (np.stack([L, R], 1) * 32767).astype(np.int16)
with wave.open(str(HERE / 'audio.wav'), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('audio.wav', pcm.shape[0] / SR, 's')
