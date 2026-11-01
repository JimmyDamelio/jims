"""Soundtrack for the reel -> audio.wav (stereo, 48 kHz). No voice anywhere.
Music, whooshes, risers and impacts are synthesised here; UI cues are real
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
def pluck(m, v=.18):
    t = tt(1.2); return (np.sin(2 * np.pi * hz(m) * t) + .4 * np.sin(4 * np.pi * hz(m) * t)) * np.exp(-t * 5) * v


pad([50, 57, 60, 65], 0.0, T['s1'], vel=.05, cutoff=1000)                    # hook: Dm
pad([46, 53, 57, 62], T['s1'], T['s2'], vel=.055, cutoff=1300)               # facts: Bb
pulse(T['s1'], T['s2'], 100, 38, .16)
pad([43, 50, 55, 58], T['s2'], T['s3'], vel=.055, cutoff=1300)               # the file: Gm
pulse(T['s2'], T['s3'], 100, 38, .14)
pad([45, 52, 55, 60, 64], T['s3'], T['reveal'], vel=.06, cutoff=1600)         # danger: Am, building
pulse(T['s3'], T['reveal'] - .1, 126, 38, .22)
pad([38, 45, 48, 53], T['reveal'] + .3, T['s4'], vel=.055, cutoff=800)        # reveal: low Dm
pad([46, 53, 58, 62, 65], T['s4'], T['s5'], vel=.055, cutoff=2000)           # reflexes: Bbmaj
pulse(T['s4'], T['s5'], 96, 34, .12)
pad([41, 48, 53, 57, 60, 67], T['s5'], DUR, vel=.06, cutoff=2400)             # end: Fadd9
for b, m in [(T['hook3'], 74), (T['s1'] + .3, 70), (T['dangerTxt'], 72)] + [(r, m) for r, m in zip(T['r'], (70, 74, 77, 81, 82))] + [(T['end1'], 77), (T['end2'], 81), (T['logo'] + .9, 89)]:
    add(pluck(m), b, pan=.2)

# ---------------- sound design (picture-synced) ----------------
add(whoosh(.6, 400, 7000), 0.0, .25)
for j in range(7): add(sample('typing'), .3 + j * .15, .25, (-1) ** j * .2)
add(whoosh(.5, 800, 9000), T['hook1'], .14, -.3)
add(impact(1.2), T['hook3'] + .1, .4)
add(sample('warning'), T['badge'], .6)
for s in (T['s1'], T['s2'], T['s3'], T['s4'], T['s5']): add(whoosh(.8), s - .4, .45, -.2)
add(sample('connect'), T['nodes'], .45); add(sample('connect'), T['nodes'] + .25, .45, .3)
add(sample('scanning'), T['flow'], .3)
add(glitch(.3), T['intrude'], .4); add(sample('error'), T['intrude'] + .2, .55)
for j, b in enumerate((T['c1'], T['c2'], T['c3'], T['c4'])): add(sample('select' if j < 2 else 'info'), b, .5, (-.3, .3, -.3, .3)[j])
for j, b in enumerate(T['f']):
    for k in range(4): add(sample('typing'), b + k * .1, .22, rng.uniform(-.4, .4))
add(sample('lock'), T['bank'], .55)
for b in T['inject'][:3]: add(whoosh(.5, 1500, 9000), b, .3, .3); add(sample('press'), b + .55, .5)
k = T['inject'][0]
while k < T['typeEnd']: add(sample('typing'), k, .14, .2); k += .11
add(sample('receive'), T['typeEnd'], .6)
add(sample('warning'), T['tag'], .4)
add(riser(T['reveal'] - T['typeEnd']), T['typeEnd'], .3)
add(impact(), T['reveal'], .95); add(glitch(.4), T['reveal'], .4)
add(sample('error'), T['goal'], .45)
for b in T['r']: add(sample('select'), b, .5); add(whoosh(.4, 1000, 8000), b - .2, .2)
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
