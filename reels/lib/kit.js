// Jimmy Décrypte motion kit: shared Canvas 2D helpers (extracted from reel #01). Expects <canvas id="c" width=1080 height=1920>.
const W = 1080, H = 1920, c = document.getElementById('c'), x = c.getContext('2d');
const NIGHT = '#071B3A', BLUE = '#1261D8', LIGHT = '#35A7FF', WHITE = '#FFFFFF', ICE = '#EAF4FF', DANGER = '#FF5468', OK = '#22C97A';

// ---------- maths ----------
const cl = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
const pr = (t, a, b) => cl((t - a) / (b - a));
const lerp = (a, b, k) => a + (b - a) * k;
const eo = k => 1 - Math.pow(1 - k, 4);                 // entrance (ease-out quart)
const ei = k => k * k * k;                              // exit
const eio = k => k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2;
const back = k => { const s = 1.70158; k -= 1; return k * k * ((s + 1) * k + s) + 1; };
function mulberry(a) { return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const hash = n => { const r = mulberry(n * 7919 + 13); return r(); };
const rgba = (hex, a) => { const n = parseInt(hex.slice(1), 16); return `rgba(${n >> 16},${n >> 8 & 255},${n & 255},${a})`; };
// in/out envelope: fades in over [a,a+fi], out over [b-fo,b]
const env = (t, a, b, fi = .35, fo = .3) => Math.min(eo(pr(t, a, a + fi)), 1 - ei(pr(t, b - fo, b)));

// ---------- drawing helpers (all multiply current globalAlpha) ----------
function rr(X, Y, w, h, r) { x.beginPath(); x.roundRect(X, Y, w, h, r); }
function alpha(a, fn) { x.save(); x.globalAlpha *= a; fn(); x.restore(); }
function font(size, w = 700, fam = 'SG') { x.font = `${w} ${size}px ${fam}`; }
function txt(s, X, Y, size, col = WHITE, w = 700, fam = 'SG', align = 'center', ls = 0) {
  font(size, w, fam); x.fillStyle = col; x.textAlign = align; x.textBaseline = 'middle';
  x.letterSpacing = ls + 'px'; x.fillText(s, X, Y); x.letterSpacing = '0px';
}
function wrap(s, maxW, size, w, fam) { font(size, w, fam); const out = []; let line = '';
  for (const word of s.split(' ')) { const t = line ? line + ' ' + word : word; if (x.measureText(t).width > maxW && line) { out.push(line); line = word; } else line = t; }
  out.push(line); return out; }
const GL = 'ABCDEF0123456789#$%&@*<>/\\=+';
function scramble(s, k, seed) { // decrypt effect: chars resolve left to right
  const n = s.length, done = Math.floor(k * (n + 4)); let o = '';
  for (let i = 0; i < n; i++) { if (s[i] === ' ' || i < done - 4) o += s[i]; else if (i < done) o += GL[Math.floor(hash(seed + i * 31) * GL.length)]; else o += k > 0 ? GL[Math.floor(hash(seed * 3 + i) * GL.length)] : ' '; }
  return o; }
// kinetic line: words rise + unblur with stagger
function kinetic(s, X, Y, size, t, t0, col = WHITE, opts = {}) {
  const words = s.split(' '), w = opts.w || 700, fam = opts.fam || 'SG'; font(size, w, fam);
  const sp = x.measureText(' ').width, widths = words.map(q => x.measureText(q).width);
  const total = widths.reduce((a, b) => a + b, 0) + sp * (words.length - 1);
  let cx = X - total / 2; const out = opts.out ? 1 - ei(pr(t, opts.out - .3, opts.out)) : 1;
  words.forEach((q, i) => {
    const k = eo(pr(t, t0 + i * .07, t0 + i * .07 + .45));
    if (k > 0) alpha(k * out, () => {
      x.filter = k < 1 ? `blur(${(1 - k) * 10}px)` : 'none';
      const hl = opts.hl && opts.hl.includes(i);
      txt(q, cx + widths[i] / 2, Y + (1 - k) * 46, size, hl ? LIGHT : col, w, fam);
      if (hl && opts.under) { const u = eo(pr(t, t0 + i * .07 + .3, t0 + i * .07 + .8)); x.fillStyle = LIGHT; x.fillRect(cx, Y + size * .58, widths[i] * u, 7); }
      x.filter = 'none';
    });
    cx += widths[i] + sp;
  });
}

// ---------- background: depth grid, particles, light lines ----------
const rnd = mulberry(42);
const PARTS = Array.from({ length: 90 }, () => ({ x: rnd() * W, y: rnd() * H, z: .2 + rnd() * .9, s: rnd() * 6.28, r: .8 + rnd() * 2.6 }));
function background(t, cam) {
  const g = x.createRadialGradient(W / 2, H * .45, 50, W / 2, H * .5, H * .85);
  g.addColorStop(0, '#0D2E63'); g.addColorStop(.55, NIGHT); g.addColorStop(1, '#040F22');
  x.fillStyle = g; x.fillRect(0, 0, W, H);
  // perspective floor grid (drifts toward camera)
  x.save(); x.strokeStyle = rgba(LIGHT, .09); x.lineWidth = 2;
  const hz = 1180 - cam.y * .15, vx = W / 2 - cam.x * .3;
  for (let i = -14; i <= 14; i++) { x.beginPath(); x.moveTo(vx + i * 22, hz); x.lineTo(vx + i * 260, H + 200); x.stroke(); }
  for (let j = 0; j < 14; j++) { const d = ((j + (t * .35) % 1) / 14); const y = hz + Math.pow(d, 2.2) * (H - hz + 200);
    x.globalAlpha = d; x.beginPath(); x.moveTo(0, y); x.lineTo(W, y); x.stroke(); }
  x.restore();
  const hg = x.createLinearGradient(0, hz - 260, 0, hz + 60); hg.addColorStop(0, rgba(NIGHT, 0)); hg.addColorStop(.8, rgba(NIGHT, .95)); hg.addColorStop(1, rgba(NIGHT, 0));
  x.fillStyle = hg; x.fillRect(0, hz - 260, W, 320);
  // particles with parallax
  for (const p of PARTS) {
    const px = ((p.x - cam.x * p.z * .6 + Math.sin(t * .3 + p.s) * 20) % W + W) % W;
    const py = ((p.y - cam.y * p.z * .6 - t * 18 * p.z) % H + H) % H;
    x.fillStyle = rgba(p.z > .8 ? WHITE : LIGHT, .15 + .35 * p.z * (.6 + .4 * Math.sin(t * 2 + p.s)));
    x.beginPath(); x.arc(px, py, p.r * p.z * (cam.z || 1), 0, 6.28); x.fill();
  }
}
// diagonal light streaks used as transitions
function streaks(t, t0, n = 5) {
  const k = pr(t, t0 - .35, t0 + .45); if (k <= 0 || k >= 1) return;
  x.save(); x.globalCompositeOperation = 'lighter';
  for (let i = 0; i < n; i++) {
    const off = (hash(t0 * 100 + i) - .5) * 900, w = 6 + hash(i + t0) * 40, kk = eio(cl(k * 1.3 - i * .06));
    const cx = lerp(-700, W + 700, kk) + off * .3;
    const g = x.createLinearGradient(cx - 400, 0, cx + 400, 0);
    g.addColorStop(0, rgba(LIGHT, 0)); g.addColorStop(.5, rgba(i % 2 ? WHITE : LIGHT, .55)); g.addColorStop(1, rgba(LIGHT, 0));
    x.fillStyle = g; x.translate(W / 2, H / 2); x.rotate(-.42); x.fillRect(cx - W / 2 - 400, -1600 + off, 800, w); x.setTransform(1, 0, 0, 1, 0, 0);
  }
  x.restore();
}
function flash(t, t0, d = .25, a = .5, col = WHITE) { const k = pr(t, t0, t0 + d); if (k > 0 && k < 1) { x.fillStyle = rgba(col, a * (1 - k)); x.fillRect(0, 0, W, H); } }

// ---------- icons ----------
function bankIcon(X, Y, s, col) { x.save(); x.translate(X, Y); x.scale(s, s); x.fillStyle = col;
  x.beginPath(); x.moveTo(-40, -12); x.lineTo(0, -38); x.lineTo(40, -12); x.closePath(); x.fill();
  for (let i = -3; i <= 3; i += 2) x.fillRect(i * 10 - 4, -6, 8, 34); x.fillRect(-42, 30, 84, 8); x.restore(); }
function handset(X, Y, s, col, rot = 0) { x.save(); x.translate(X, Y); x.rotate(rot); x.scale(s, s); x.strokeStyle = col; x.lineWidth = 9; x.lineCap = 'round';
  x.beginPath(); x.arc(0, 8, 22, Math.PI * 1.05, Math.PI * 1.95); x.stroke(); x.fillStyle = col; rr(-30, -2, 14, 16, 5); x.fill(); rr(16, -2, 14, 16, 5); x.fill(); x.restore(); }
function cross(X, Y, r, k, col) { x.save(); x.strokeStyle = col; x.lineWidth = 8; x.lineCap = 'round'; const a = cl(k * 2), b = cl(k * 2 - 1);
  x.beginPath(); x.moveTo(X - r, Y - r); x.lineTo(X - r + 2 * r * a, Y - r + 2 * r * a); x.stroke();
  if (b > 0) { x.beginPath(); x.moveTo(X + r, Y - r); x.lineTo(X + r - 2 * r * b, Y - r + 2 * r * b); x.stroke(); } x.restore(); }
function check(X, Y, r, k, col) { x.save(); x.strokeStyle = col; x.lineWidth = 9; x.lineCap = 'round'; x.lineJoin = 'round';
  x.beginPath(); x.moveTo(X - r, Y); const a = cl(k * 2.5); x.lineTo(X - r + r * .7 * a, Y + r * .7 * a);
  const b = cl(k * 1.6 - .5); if (b > 0) x.lineTo(X - r * .3 + r * 1.3 * b, Y + r * .7 - r * 1.5 * b); x.stroke(); x.restore(); }

// ---------- phone ----------
const PW = 480, PH = 980, PX = 540, PY = 1080;
function phone(t, screen, o = {}) {
  const s = o.s ?? 1, tilt = o.tilt ?? 0, dx = o.dx ?? 0, dy = o.dy ?? 0;
  x.save(); x.translate(PX + dx, PY + dy); x.rotate(o.rot ?? 0);
  x.transform(Math.cos(tilt), Math.sin(tilt) * .18, 0, 1, 0, 0); x.scale(s, s);
  // glow + shadow
  x.shadowColor = rgba(LIGHT, .35); x.shadowBlur = 90; x.fillStyle = '#081733'; rr(-PW / 2, -PH / 2, PW, PH, 74); x.fill(); x.shadowBlur = 0;
  const rim = x.createLinearGradient(-PW / 2, -PH / 2, PW / 2, PH / 2); rim.addColorStop(0, rgba(LIGHT, .9)); rim.addColorStop(.5, rgba(BLUE, .3)); rim.addColorStop(1, rgba(LIGHT, .7));
  x.strokeStyle = rim; x.lineWidth = 4; rr(-PW / 2, -PH / 2, PW, PH, 74); x.stroke();
  // screen
  x.save(); rr(-PW / 2 + 16, -PH / 2 + 16, PW - 32, PH - 32, 60); x.clip();
  x.translate(-PW / 2 + 16, -PH / 2 + 16); screen(t, PW - 32, PH - 32);
  x.restore();
  x.fillStyle = '#000'; rr(-70, -PH / 2 + 34, 140, 40, 20); x.fill(); // island
  // glass reflection sweep
  const gx = ((t * .25) % 1.6 - .3) * PW * 2 - PW;
  const rg = x.createLinearGradient(gx - 120, -PH / 2, gx + 120, PH / 2); rg.addColorStop(0, rgba(WHITE, 0)); rg.addColorStop(.5, rgba(WHITE, .05)); rg.addColorStop(1, rgba(WHITE, 0));
  x.fillStyle = rg; rr(-PW / 2 + 16, -PH / 2 + 16, PW - 32, PH - 32, 60); x.fill();
  x.restore();
}
function screenBg(w, h, top = '#0F3470') { const g = x.createLinearGradient(0, 0, 0, h); g.addColorStop(0, top); g.addColorStop(1, '#06162F'); x.fillStyle = g; x.fillRect(0, 0, w, h); }
function statusBar(w, clock = '21:47') { txt(clock, 64, 52, 26, WHITE, 600, 'IN'); x.fillStyle = WHITE; for (let i = 0; i < 4; i++) x.fillRect(w - 128 + i * 9, 58 - i * 5, 6, 6 + i * 5); rr(w - 82, 42, 40, 20, 5); x.fill(); }
// ---------- glitch (post) ----------
const tmp = document.createElement('canvas'); tmp.width = W; tmp.height = H; const tx = tmp.getContext('2d');
function glitch(t, amt, seed) {
  if (amt <= 0) return; tx.clearRect(0, 0, W, H); tx.drawImage(c, 0, 0);
  const r = mulberry(seed);
  for (let i = 0; i < 14; i++) { const y = r() * H, hh = 10 + r() * 120, off = (r() - .5) * 140 * amt; x.drawImage(tmp, 0, y, W, hh, off, y, W, hh); }
  x.save(); x.globalCompositeOperation = 'lighter'; x.globalAlpha = .2 * amt;
  x.drawImage(tmp, 14 * amt, 0); x.fillStyle = rgba(DANGER, .25 * amt); x.fillRect(0, 0, W, H); x.restore();
}
// film grain + vignette
const grains = Array.from({ length: 4 }, (_, k) => { const g = document.createElement('canvas'); g.width = 270; g.height = 480; const gx = g.getContext('2d'), id = gx.createImageData(270, 480), r = mulberry(k + 9);
  for (let i = 0; i < id.data.length; i += 4) { const v = r() * 255; id.data[i] = id.data[i + 1] = id.data[i + 2] = v; id.data[i + 3] = 20; } gx.putImageData(id, 0, 0); return g; });
function finish(t) {
  x.save(); x.globalCompositeOperation = 'overlay'; x.imageSmoothingEnabled = false; x.drawImage(grains[Math.floor(t * 30) % 4], 0, 0, W, H); x.restore();
  const v = x.createRadialGradient(W / 2, H / 2, H * .35, W / 2, H / 2, H * .75); v.addColorStop(0, rgba('#020814', 0)); v.addColorStop(1, rgba('#020814', .6)); x.fillStyle = v; x.fillRect(0, 0, W, H);
}

// ---------- camera ----------
function camAt(t, K) { // keyframes [t, x, y, zoom]
  let i = 0; while (i < K.length - 2 && t > K[i + 1][0]) i++;
  const [a, b] = [K[i], K[i + 1]], k = eio(pr(t, a[0], b[0]));
  return { x: lerp(a[1], b[1], k), y: lerp(a[2], b[2], k), z: lerp(a[3], b[3], k) };
}
function withCam(cam, depth, fn) { x.save(); x.translate(W / 2, H / 2); x.scale(1 + (cam.z - 1) * depth, 1 + (cam.z - 1) * depth); x.translate(-W / 2 - cam.x * depth, -H / 2 - cam.y * depth); fn(); x.restore(); }
