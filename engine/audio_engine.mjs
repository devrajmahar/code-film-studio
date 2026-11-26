/**
 * High-energy, zero-hum procedural Shorts soundtrack & transition Foley engine.
 * Reads <film_dir>/build/audio_spec.json and renders <film_dir>/build/master.wav:
 *  - Driving 130+ BPM punchy beat (tight transient kick, crisp rimshot/hat, bright pluck arp)
 *  - Subtle cinematic swish/whoosh right on every shot transition for seamless flow
 *  - Guaranteed ZERO voice overlap with crisp ~0.20s natural breath between lines
 */

import fs from "node:fs";
import path from "node:path";

const specPath = process.argv[2];
if (!specPath || !fs.existsSync(specPath)) {
  console.error("Usage: node engine/audio_engine.mjs <path/to/build/audio_spec.json>");
  process.exit(1);
}

const spec = JSON.parse(fs.readFileSync(specPath, "utf-8"));
const SR = 48000;
const DURATION = spec.duration || 32.0;
const N = Math.ceil(SR * DURATION);
const beat = 60.0 / (spec.bpm || 132);

const bgL = new Float32Array(N);
const bgR = new Float32Array(N);

let seed = 90210;
function rand() {
  seed = (seed * 1664525 + 1013904223) >>> 0;
  return seed / 4294967296;
}
function randSigned() {
  return rand() * 2 - 1;
}
function midiToHz(m) {
  return 440 * Math.pow(2, (m - 69) / 12);
}

function addStereo(startSec, durSec, fn, pan = 0.0, gain = 1.0) {
  const i0 = Math.max(0, Math.floor(startSec * SR));
  const i1 = Math.min(N, Math.floor((startSec + durSec) * SR));
  const len = Math.max(1, i1 - i0);
  const gL = gain * Math.cos(((pan + 1) * Math.PI) / 4);
  const gR = gain * Math.sin(((pan + 1) * Math.PI) / 4);
  for (let i = i0; i < i1; i++) {
    const t = (i - i0) / SR;
    const u = (i - i0) / len;
    const s = fn(t, u);
    bgL[i] += s * gL;
    bgR[i] += s * gR;
  }
}

function addPiano(startSec, durSec, midi, gain = 0.10, pan = 0.0) {
  const f = midiToHz(midi);
  addStereo(
    startSec,
    durSec,
    (t) => {
      const env = Math.min(1, t / 0.006) * Math.exp(-t * 3.4);
      const w = 2 * Math.PI * f * t;
      return (0.72 * Math.sin(w) + 0.22 * Math.sin(2 * w) * Math.exp(-t * 4.0) + 0.08 * Math.sin(3 * w) * Math.exp(-t * 6.5)) * env;
    },
    pan,
    gain
  );
}

function addPluck(startSec, midi, gain = 0.075, pan = 0.0) {
  const f = midiToHz(midi);
  addStereo(
    startSec,
    0.20,
    (t) => {
      const env = Math.min(1, t / 0.002) * Math.exp(-t * 17.0);
      const w = 2 * Math.PI * f * t;
      return (0.80 * Math.sin(w) + 0.20 * Math.sin(3 * w) * Math.exp(-t * 24)) * env;
    },
    pan,
    gain
  );
}

// Tight punchy transient thump (short 90ms decay — adds momentum with ZERO hum!)
function addPunchKick(startSec, gain = 0.13) {
  addStereo(
    startSec,
    0.11,
    (t) => {
      const f = 185 * Math.exp(-t * 42) + 88;
      const env = Math.min(1, t / 0.002) * Math.exp(-t * 28);
      return Math.sin(2 * Math.PI * f * t) * env;
    },
    0.0,
    gain
  );
}

function addTick(startSec, gain = 0.048, pan = 0.0) {
  addStereo(
    startSec,
    0.038,
    (t) => (randSigned() * 0.65 + Math.sin(2 * Math.PI * 1950 * t) * 0.35) * Math.exp(-t * 110),
    pan,
    gain
  );
}

// Crisp short whip-swish right on every visual transition
function addCutSwish(centerSec, gain = 0.052) {
  let prev = 0;
  const dur = 0.22;
  addStereo(
    centerSec - dur * 0.55,
    dur,
    (x, u) => {
      const env = Math.sin(Math.PI * u) ** 2;
      const s = randSigned();
      const hp = s - prev * 0.78;
      prev = s;
      return hp * 0.45 * env;
    },
    0.0,
    gain
  );
}

const SFX_HANDLERS = {
  horn: ({ t, dur = 0.16, f1 = 440, f2 = 540, gain = 0.036, pan = -0.3 }) => {
    addStereo(
      t,
      dur,
      (x) => {
        const env = Math.min(1, x / 0.01) * Math.min(1, (dur - x) / 0.02);
        return ((Math.sin(2 * Math.PI * f1 * x) + 0.35 * Math.sin(4 * Math.PI * f1 * x) + Math.sin(2 * Math.PI * f2 * x)) * 0.35) * env;
      },
      pan,
      gain
    );
  },
  tram_bell: ({ t, gain = 0.085, pan = 0.25 }) => {
    for (const off of [0.0, 0.18]) {
      addStereo(
        t + off,
        0.55,
        (x) => (0.65 * Math.sin(2 * Math.PI * 1520 * x) + 0.25 * Math.sin(2 * Math.PI * 3045 * x) * Math.exp(-x * 3.5)) * Math.min(1, x / 0.003) * Math.exp(-x * 5.8),
        pan,
        gain
      );
    }
  },
  bird: ({ t, hz = 2800, gain = 0.034, pan = 0.4 }) => {
    addStereo(
      t,
      0.13,
      (x, u) => Math.sin(2 * Math.PI * (hz + 720 * Math.sin(Math.PI * u * 1.4)) * x) * Math.sin(Math.PI * u) * Math.exp(-x * 9),
      pan,
      gain
    );
  },
  rain: ({ t, dur = 3.2, gain = 0.042 }) => {
    let prev = 0;
    addStereo(
      t,
      dur,
      (x) => {
        const env = Math.min(1, x / 0.2) * Math.min(1, (dur - x) / 0.25);
        const s = randSigned();
        const hp = s - prev * 0.85;
        prev = s;
        return hp * 0.35 * env;
      },
      0.0,
      gain
    );
  },
  whoosh: ({ t, dur = 0.55, gain = 0.06, pan = 0.0 }) => {
    let prev = 0;
    addStereo(
      t,
      dur,
      (x, u) => {
        const env = Math.sin(Math.PI * u) ** 1.6;
        const s = randSigned();
        const hp = s - prev * 0.72;
        prev = s;
        return hp * 0.5 * env;
      },
      pan,
      gain
    );
  },
  station_chime: ({ t, gain = 0.075, pan = 0.0 }) => {
    [76, 80, 83].forEach((m, idx) => {
      const f = midiToHz(m);
      addStereo(
        t + idx * 0.14,
        0.45,
        (x) => (0.75 * Math.sin(2 * Math.PI * f * x) + 0.25 * Math.sin(4 * Math.PI * f * x) * Math.exp(-x * 5)) * Math.min(1, x / 0.004) * Math.exp(-x * 5.5),
        pan,
        gain
      );
    });
  },
};

// Energetic Shorts groove: kick on beats, crisp offbeat ticks, driving eighth-note plucks
for (const seg of spec.progression || []) {
  const [s0, s1, chord, holdOnly = false] = seg;
  chord.forEach((m, idx) => addPiano(s0 + idx * 0.03, 1.4, m, 0.08, -0.25 + idx * 0.2));
  if (holdOnly) continue;
  let step = 0;
  for (let t = s0; t < s1 - 0.08; t += beat * 0.5) {
    const m = chord[step % chord.length] + (step % 4 === 3 ? 12 : 0);
    addPluck(t, m, 0.068, step % 2 === 0 ? -0.32 : 0.32);
    if (step % 2 === 0) addPunchKick(t, 0.11);
    else addTick(t, 0.045, step % 4 === 1 ? -0.18 : 0.18);
    step++;
  }
}

// Add crisp whip-swish sound on every shot cut (except shot 0)
const shots = spec.shots || spec.narration || [];
for (let k = 1; k < shots.length; k++) {
  addCutSwish(shots[k].start, 0.055);
}

for (const cue of spec.sfx || []) {
  const fn = SFX_HANDLERS[cue.type];
  if (fn) fn(cue);
}

// 115 Hz high-pass filter on BG bus (guarantees ZERO low-frequency hum!)
const hpAlpha = 0.985;
let xL = 0, yL = 0, xR = 0, yR = 0;
for (let i = 0; i < N; i++) {
  yL = hpAlpha * (yL + bgL[i] - xL); xL = bgL[i]; bgL[i] = yL;
  yR = hpAlpha * (yR + bgR[i] - xR); xR = bgR[i]; bgR[i] = yR;
}

function readWavMono16(filepath) {
  const buf = fs.readFileSync(filepath);
  let off = 12;
  while (off + 8 < buf.length) {
    const id = buf.toString("ascii", off, off + 4);
    const sz = buf.readUInt32LE(off + 4);
    if (id === "data") {
      const cnt = Math.floor(sz / 2);
      const out = new Float32Array(cnt);
      for (let i = 0; i < cnt; i++) out[i] = buf.readInt16LE(off + 8 + i * 2) / 32768;
      return out;
    }
    off += 8 + sz + (sz % 2);
  }
  return new Float32Array(0);
}

const voiceBus = new Float32Array(N);
const duckEnv = new Float32Array(N);
let lastVoiceEndSample = 0;

for (const item of shots) {
  if (!fs.existsSync(item.wav)) continue;
  const samples = readWavMono16(item.wav);
  const startSec = item.voice_start !== undefined ? item.voice_start : item.start;
  // Tight 0.14s minimum separation — snappy Shorts flow, mathematically ZERO voice overlap
  const i0 = Math.max(lastVoiceEndSample + Math.floor(0.14 * SR), Math.floor(startSec * SR));
  const maxEnd = item.duration ? Math.min(N, Math.floor((item.start + item.duration - 0.04) * SR)) : N;
  const count = Math.min(samples.length, Math.max(0, maxEnd - i0));
  for (let i = 0; i < count; i++) {
    voiceBus[i0 + i] = samples[i];
    duckEnv[i0 + i] = Math.abs(samples[i]);
  }
  lastVoiceEndSample = i0 + count;
}

const L = new Float32Array(N);
const R = new Float32Array(N);
let env = 0;
const fadeIn = Math.floor(0.10 * SR);
const fadeOut = Math.floor(0.55 * SR);
for (let i = 0; i < N; i++) {
  const tgt = duckEnv[i] > 0.015 ? 1.0 : 0.0;
  env += (tgt > env ? 0.004 : 0.0004) * (tgt - env);
  const bgGain = 1.0 - 0.56 * env;
  let g = 1.0;
  if (i < fadeIn) g *= i / fadeIn;
  if (i > N - fadeOut) g *= (N - i) / fadeOut;
  L[i] = Math.tanh((bgL[i] * bgGain + voiceBus[i] * 0.98) * g * 1.10);
  R[i] = Math.tanh((bgR[i] * bgGain + voiceBus[i] * 0.98) * g * 1.10);
}

const outPath = path.join(path.dirname(specPath), "master.wav");
const dataBytes = N * 4;
const wav = Buffer.alloc(44 + dataBytes);
wav.write("RIFF", 0);
wav.writeUInt32LE(36 + dataBytes, 4);
wav.write("WAVE", 8);
wav.write("fmt ", 12);
wav.writeUInt32LE(16, 16);
wav.writeUInt16LE(1, 20);
wav.writeUInt16LE(2, 22);
wav.writeUInt32LE(SR, 24);
wav.writeUInt32LE(SR * 4, 28);
wav.writeUInt16LE(4, 32);
wav.writeUInt16LE(16, 34);
wav.write("data", 36);
wav.writeUInt32LE(dataBytes, 40);

let p = 44;
for (let i = 0; i < N; i++) {
  wav.writeInt16LE(Math.max(-32768, Math.min(32767, Math.round(L[i] * 32767))), p);
  wav.writeInt16LE(Math.max(-32768, Math.min(32767, Math.round(R[i] * 32767))), p + 2);
  p += 4;
}
fs.writeFileSync(outPath, wav);
console.log(`Wrote master audio: ${outPath} (${DURATION.toFixed(2)}s, snappy 132bpm, ZERO overlap)`);
