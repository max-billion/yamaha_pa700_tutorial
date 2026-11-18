// Korg Pa700 Trainer — Real-Time Web Audio Synthesizer & Auto-Arranger Sound Engine
// Synthesizes all 9 Pa700 instrument families, Drum Kit, Bass, Comping, Intros/Fills/Breaks/Endings, Pads & Metronome.

(function () {
  "use strict";

  const SEMI = Math.pow(2, 1 / 12);

  function midiToFreq(midiFloat) {
    return 440 * Math.pow(2, (midiFloat - 69) / 12);
  }

  const NOTE_PC = {
    "C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
    "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
    "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11
  };

  function parseChordToMidi(chordStr) {
    if (!chordStr) return null;
    const m = String(chordStr).trim().match(/^([A-G][#b]?)\s*(.*)$/i);
    if (!m) return null;
    const rootName = m[1].charAt(0).toUpperCase() + (m[1].slice(1) || "");
    const qual = (m[2] || "").toLowerCase();
    const pc = NOTE_PC[rootName];
    if (pc === undefined) return null;

    let intervals = [0, 4, 7];
    if (qual.includes("min") || qual === "m") intervals = [0, 3, 7];
    else if (qual.includes("7")) intervals = [0, 4, 7, 10];
    else if (qual.includes("dim")) intervals = [0, 3, 6];

    const bassRoot = 36 + pc; // C2..B2 range
    const compRoot = 48 + pc; // C3..B3 range
    return {
      pc,
      isMinor: intervals[1] === 3,
      bassRoot,
      intervals,
      compNotes: intervals.map(iv => compRoot + iv)
    };
  }

  // Classify any Pa700 Sound name into a synthesis patch archetype
  function classifyPatch(soundName) {
    const s = String(soundName || "").toLowerCase();
    if (s.includes("honky")) return "honky_piano";
    if (s.includes("m1")) return "m1_piano";
    if (s.includes("tine") || s.includes("suitcase") || s.includes("ep") || s.includes("dyno") || s.includes("rhodes")) return "epiano";
    if (s.includes("grand") || s.includes("piano")) return "piano";
    if (s.includes("pipe") || s.includes("cathedral")) return "pipe_organ";
    if (s.includes("rock organ") || s.includes("overdriven")) return "rock_organ";
    if (s.includes("organ") || s.includes("drawbar") || s.includes("bx3") || s.includes("jimmy")) return "jazz_organ";
    if (s.includes("overdrive") || s.includes("tube")) return "lead_guitar";
    if (s.includes("clean") || s.includes("strat") || s.includes("funk")) return "clean_guitar";
    if (s.includes("steel") || s.includes("12-string") || s.includes("folk")) return "steel_guitar";
    if (s.includes("nylon") || s.includes("guitar")) return "nylon_guitar";
    if (s.includes("violin")) return "solo_violin";
    if (s.includes("string") || s.includes("orchestra") || s.includes("cello") || s.includes("chamber")) return "strings";
    if (s.includes("mute") && s.includes("trumpet")) return "mute_trumpet";
    if (s.includes("flugel")) return "flugelhorn";
    if (s.includes("trumpet") || s.includes("cornet") || s.includes("mariachi")) return "trumpet";
    if (s.includes("brass") || s.includes("horn") || s.includes("trombone")) return "brass";
    if (s.includes("flute") || s.includes("nay") || s.includes("pan")) return "flute";
    if (s.includes("clarinet")) return "clarinet";
    if (s.includes("sax") || s.includes("oboe") || s.includes("reed")) return "sax";
    if (s.includes("accordion") || s.includes("musette")) return "accordion";
    if (s.includes("harmonica") || s.includes("harp")) return "harmonica";
    if (s.includes("oud") || s.includes("kanun") || s.includes("qanun") || s.includes("bouzouki")) return "oud";
    if (s.includes("bass")) return "bass";
    if (s.includes("pad") || s.includes("choir") || s.includes("heaven")) return "pad";
    if (s.includes("lead") || s.includes("saw") || s.includes("jump") || s.includes("synth")) return "synth_lead";
    return "piano";
  }

  class Pa700AudioEngine {
    constructor() {
      this.ctx = null;
      this.muted = false;
      this.noiseBuffer = null;
      this.masterGain = null;
      this.kbdBus = null;
      this.kbdFilter = null;
      this.reverbSend = null;
      this.accBus = null;
      this.analyser = null;
      this.meterArray = null;

      this.activeVoices = [];
      this.pitchBendSemis = 0;
      this.modDepth = 0;

      // Lookahead 16th-note scheduler state
      this.schedulerTimer = null;
      this.nextSubStepTime = 0;
      this.subStepIndex = 0; // 0..(beatsPerBar * 4 - 1)
      this.getStateFn = null;
      this.onStepCallback = null;
    }

    init() {
      if (this.ctx) {
        if (this.ctx.state === "suspended") this.ctx.resume();
        return;
      }
      const AC = window.AudioContext || window.webkitAudioContext;
      if (!AC) return;
      this.ctx = new AC();

      // Master chain with soft limiter + level analyser
      const comp = this.ctx.createDynamicsCompressor();
      comp.threshold.value = -10;
      comp.knee.value = 12;
      comp.ratio.value = 4;
      comp.attack.value = 0.005;
      comp.release.value = 0.15;

      this.masterGain = this.ctx.createGain();
      this.masterGain.gain.value = 0.82;

      this.analyser = this.ctx.createAnalyser();
      this.analyser.fftSize = 256;
      this.meterArray = new Uint8Array(this.analyser.frequencyBinCount);

      this.masterGain.connect(comp);
      comp.connect(this.analyser);
      this.analyser.connect(this.ctx.destination);

      // Keyboard Bus -> Assignable Knob 1 Filter -> Master & Reverb
      this.kbdBus = this.ctx.createGain();
      this.kbdBus.gain.value = 0.85;

      this.kbdFilter = this.ctx.createBiquadFilter();
      this.kbdFilter.type = "lowpass";
      this.kbdFilter.frequency.value = 6500;
      this.kbdFilter.Q.value = 0.7;

      // Synthetic stereo hall impulse response for Assignable Knob 2 Reverb
      const revConvolver = this.ctx.createConvolver();
      revConvolver.buffer = this._createReverbImpulse(1.65, 2.6);
      this.reverbSend = this.ctx.createGain();
      this.reverbSend.gain.value = 0.24;

      this.kbdBus.connect(this.kbdFilter);
      this.kbdFilter.connect(this.masterGain);
      this.kbdFilter.connect(this.reverbSend);

      // Accompaniment / Arranger Bus
      this.accBus = this.ctx.createGain();
      this.accBus.gain.value = 0.80;
      this.accBus.connect(this.masterGain);
      this.accBus.connect(this.reverbSend);

      this.reverbSend.connect(revConvolver);
      revConvolver.connect(this.masterGain);

      // Shared white noise buffer for drums, breath chiff, and brush swirls
      this.noiseBuffer = this._createNoiseBuffer(2.0);
    }

    _createNoiseBuffer(seconds) {
      const len = Math.floor(this.ctx.sampleRate * seconds);
      const buf = this.ctx.createBuffer(1, len, this.ctx.sampleRate);
      const data = buf.getChannelData(0);
      for (let i = 0; i < len; i++) {
        data[i] = Math.random() * 2 - 1;
      }
      return buf;
    }

    _createReverbImpulse(seconds, decay) {
      const rate = this.ctx.sampleRate;
      const len = Math.floor(rate * seconds);
      const buf = this.ctx.createBuffer(2, len, rate);
      for (let ch = 0; ch < 2; ch++) {
        const d = buf.getChannelData(ch);
        for (let i = 0; i < len; i++) {
          const env = Math.pow(1 - i / len, decay);
          d[i] = (Math.random() * 2 - 1) * env * 0.45;
        }
      }
      return buf;
    }

    setMuted(flag) {
      this.muted = Boolean(flag);
      if (this.ctx && this.masterGain) {
        const st = this.getStateFn ? this.getStateFn() : null;
        const vol = st ? st.knobs.master_volume : 0.82;
        this.masterGain.gain.setTargetAtTime(this.muted ? 0 : vol, this.ctx.currentTime, 0.02);
      }
    }

    syncPanelControls(st) {
      if (!this.ctx || !st) return;
      const now = this.ctx.currentTime;
      const master = (!st.powerOn || this.muted) ? 0 : st.knobs.master_volume * 0.95;
      this.masterGain.gain.setTargetAtTime(master, now, 0.02);

      // BALANCE knob: 0.0 = full ACC/SONG, 0.5 = equal, 1.0 = full KBD
      const bal = st.knobs.balance;
      const kbdGain = bal >= 0.5 ? 0.88 : 0.88 * (bal / 0.5);
      const accBase = bal <= 0.5 ? 0.82 : 0.82 * ((1 - bal) / 0.5);
      const fadeMul = (st.fadeLevel !== undefined ? st.fadeLevel : 100) / 100;

      this.kbdBus.gain.setTargetAtTime(kbdGain, now, 0.03);
      this.accBus.gain.setTargetAtTime(accBase * fadeMul, now, 0.04);

      // Assignable Knob 1 = Filter Cutoff (400 Hz .. 13000 Hz)
      const cutoff = 380 * Math.pow(34, st.knobs.assign_knob_1);
      this.kbdFilter.frequency.setTargetAtTime(cutoff, now, 0.03);

      // Assignable Knob 2 = Reverb Send (0.0 .. 0.65)
      this.reverbSend.gain.setTargetAtTime(st.knobs.assign_knob_2 * 0.65, now, 0.03);
    }

    setJoystick(normX, normY) {
      // normX in [-1..1] -> +-2 semitones pitch bend; normY in [-1..1] -> vibrato depth
      this.pitchBendSemis = normX * 2.0;
      this.modDepth = Math.abs(normY) * 28;
      if (!this.ctx) return;
      const now = this.ctx.currentTime;
      const cents = this.pitchBendSemis * 100;
      this.activeVoices.forEach(v => {
        v.oscs.forEach(o => {
          try {
            o.detune.setTargetAtTime((o._baseDetune || 0) + cents, now, 0.02);
          } catch (_) {}
        });
        if (v.vibGain) {
          v.vibGain.gain.setTargetAtTime((v._baseVib || 0) + this.modDepth, now, 0.03);
        }
      });
    }

    getMeterLevel() {
      if (!this.analyser || this.muted) return 0;
      this.analyser.getByteTimeDomainData(this.meterArray);
      let maxDev = 0;
      for (let i = 0; i < this.meterArray.length; i++) {
        const dev = Math.abs(this.meterArray[i] - 128);
        if (dev > maxDev) maxDev = dev;
      }
      return Math.min(1, maxDev / 64);
    }

    // =======================================================================
    // LIVE KEYBOARD NOTE-ON / NOTE-OFF (RESPECTS SPLIT, LAYERS, SUB-SCALE)
    // =======================================================================
    playKeyboardNotes(midiNotes, st) {
      this.init();
      if (!this.ctx || !st || !st.powerOn || this.muted) return;
      this.syncPanelControls(st);
      this.releaseAllKeyboardVoices();

      const splitMidi = (!st.useGlobalSplit && st.localSplitPoint !== null)
        ? st.localSplitPoint
        : st.globalSplitPoint;

      const scalePoly = 1 / Math.sqrt(Math.max(1, midiNotes.length));

      midiNotes.forEach((rawMidi, idx) => {
        // Quarter-tone Sub-Scale detuning (-0.5 semitones = -50 cents!)
        const pc = ((rawMidi % 12) + 12) % 12;
        const quarterOffset = st.subScaleNotes.includes(pc) ? -0.5 : 0;
        const transposedMidi = rawMidi + st.masterTranspose + quarterOffset;

        const isLower = st.splitOn && rawMidi < splitMidi;

        if (isLower) {
          if (st.manualBass) {
            this._spawnSynthVoice("bass", transposedMidi - 12, 0.44 * scalePoly, this.kbdBus, st);
          } else if (!st.arrangerRunning && st.tracks.low.backing && idx === 0) {
            // Manual Bass & Lower Backing when Arranger is stopped (Manual p. 56!)
            this._spawnSynthVoice("bass", transposedMidi - 12, 0.36, this.kbdBus, st);
            if (!st.tracks.low.muted) {
              const lowPatch = classifyPatch(st.tracks.low.sound);
              this._spawnSynthVoice(lowPatch, transposedMidi + (st.tracks.low.octave || 0) * 12, 0.22 * scalePoly, this.kbdBus, st);
            }
          } else if (!st.tracks.low.muted && !st.arrangerRunning) {
            const lowPatch = classifyPatch(st.tracks.low.sound);
            this._spawnSynthVoice(lowPatch, transposedMidi + (st.tracks.low.octave || 0) * 12, 0.25 * scalePoly, this.kbdBus, st);
          }
        } else {
          // Upper 1, Upper 2, Upper 3 layered voices!
          const activeUpperKeys = ["up1", "up2", "up3"].filter(k => !st.tracks[k].muted);
          const layerScale = 1 / Math.sqrt(Math.max(1, activeUpperKeys.length));
          activeUpperKeys.forEach(tk => {
            const trk = st.tracks[tk];
            const patch = classifyPatch(trk.sound);
            const octShift = ((trk.octave || 0) + st.upperOctave) * 12;
            const trkVol = ((trk.volume || 90) / 100) * 0.34 * scalePoly * layerScale;
            this._spawnSynthVoice(patch, transposedMidi + octShift, trkVol, this.kbdBus, st);

            // Ensemble Harmony (adds chord-tone harmony below Upper 1 melody!)
            if (st.ensembleOn && tk === "up1" && idx === 0) {
              const harmOffset = st.ensembleType === "Octave" ? -12 : -4;
              this._spawnSynthVoice(patch, transposedMidi + octShift + harmOffset, trkVol * 0.62, this.kbdBus, st);
            }
          });
        }
      });
    }

    releaseAllKeyboardVoices() {
      if (!this.ctx) return;
      const now = this.ctx.currentTime;
      while (this.activeVoices.length > 0) {
        const v = this.activeVoices.pop();
        try {
          const rel = v.releaseTime || 0.18;
          v.env.gain.cancelScheduledValues(now);
          v.env.gain.setValueAtTime(Math.max(0.0001, v.env.gain.value), now);
          v.env.gain.exponentialRampToValueAtTime(0.0001, now + rel);
          v.oscs.forEach(o => o.stop(now + rel + 0.03));
          if (v.vibOsc) v.vibOsc.stop(now + rel + 0.03);
        } catch (_) {}
      }
    }

    // =======================================================================
    // INSTRUMENT PATCH SYNTHESIZER (SUSTAINED KEYBOARD & ONE-SHOT ARRANGER)
    // =======================================================================
    _spawnSynthVoice(patch, midiNote, peakGain, destBus, st, fixedDurationSec) {
      const now = this.ctx.currentTime;
      const freq = midiToFreq(midiNote);
      if (!isFinite(freq) || freq < 22 || freq > 14000) return;

      const env = this.ctx.createGain();
      env.gain.setValueAtTime(0.0001, now);

      const voiceFilter = this.ctx.createBiquadFilter();
      voiceFilter.type = "lowpass";
      voiceFilter.frequency.setValueAtTime(8000, now);
      voiceFilter.connect(env);
      env.connect(destBus);

      const oscs = [];
      let vibOsc = null;
      let vibGain = null;
      let baseVib = 0;
      let releaseTime = 0.20;
      let sustainLevel = 0.7;

      const addOsc = (type, ratio, detuneCents, gainLevel) => {
        const o = this.ctx.createOscillator();
        const g = this.ctx.createGain();
        o.type = type;
        o.frequency.setValueAtTime(freq * ratio, now);
        o._baseDetune = detuneCents;
        o.detune.setValueAtTime(detuneCents + this.pitchBendSemis * 100, now);
        g.gain.setValueAtTime(gainLevel, now);
        o.connect(g);
        g.connect(voiceFilter);
        o.start(now);
        oscs.push(o);
        return { o, g };
      };

      const addHammerTransient = (brightFreq, amt) => {
        const src = this.ctx.createBufferSource();
        src.buffer = this.noiseBuffer;
        const bp = this.ctx.createBiquadFilter();
        bp.type = "bandpass";
        bp.frequency.setValueAtTime(brightFreq, now);
        bp.Q.value = 1.8;
        const tg = this.ctx.createGain();
        tg.gain.setValueAtTime(amt * peakGain, now);
        tg.gain.exponentialRampToValueAtTime(0.0001, now + 0.025);
        src.connect(bp);
        bp.connect(tg);
        tg.connect(destBus);
        src.start(now);
        src.stop(now + 0.03);
      };

      switch (patch) {
        case "piano":
        case "honky_piano":
        case "m1_piano": {
          const det = patch === "honky_piano" ? 11 : (patch === "m1_piano" ? 4 : 1.5);
          addOsc("triangle", 1, -det, 0.75);
          addOsc("sawtooth", 1, det, patch === "m1_piano" ? 0.42 : 0.24);
          addOsc("sine", 2, 0, 0.22);
          voiceFilter.frequency.setValueAtTime(patch === "m1_piano" ? 5200 : 3800, now);
          voiceFilter.frequency.exponentialRampToValueAtTime(1100, now + 0.9);
          addHammerTransient(2600, 0.45);
          env.gain.linearRampToValueAtTime(peakGain, now + 0.006);
          env.gain.exponentialRampToValueAtTime(peakGain * 0.22, now + 1.45);
          releaseTime = 0.22;
          break;
        }

        case "epiano": {
          addOsc("sine", 1, 0, 0.85);
          addOsc("triangle", 2, 2, 0.22);
          const tine = addOsc("sine", 6, 0, 0.26);
          tine.g.gain.exponentialRampToValueAtTime(0.01, now + 0.22);
          voiceFilter.frequency.setValueAtTime(4200, now);
          env.gain.linearRampToValueAtTime(peakGain, now + 0.008);
          env.gain.exponentialRampToValueAtTime(peakGain * 0.38, now + 1.2);
          releaseTime = 0.24;
          break;
        }

        case "jazz_organ":
        case "rock_organ":
        case "pipe_organ": {
          const rotaryFast = st && st.assignableSwitches && st.assignableSwitches[3];
          addOsc("sine", 0.5, 0, 0.42);
          addOsc("sine", 1, 0, 0.75);
          addOsc(patch === "rock_organ" ? "sawtooth" : "sine", 2, 2, 0.42);
          addOsc("sine", 3, 0, 0.28);
          addOsc("sine", 4, -2, patch === "pipe_organ" ? 0.35 : 0.20);
          if (patch === "jazz_organ") {
            const perc = addOsc("sine", 3, 0, 0.45);
            perc.g.gain.exponentialRampToValueAtTime(0.001, now + 0.11);
          }
          voiceFilter.frequency.setValueAtTime(patch === "rock_organ" ? 3600 : 5400, now);
          baseVib = rotaryFast ? 18 : 5;
          env.gain.linearRampToValueAtTime(peakGain * 0.85, now + 0.012);
          releaseTime = 0.07;
          break;
        }

        case "nylon_guitar":
        case "steel_guitar":
        case "clean_guitar":
        case "lead_guitar": {
          const isLead = patch === "lead_guitar";
          addOsc(isLead ? "sawtooth" : "triangle", 1, -2, 0.65);
          addOsc("sawtooth", 1, 3, patch === "nylon_guitar" ? 0.28 : 0.48);
          voiceFilter.frequency.setValueAtTime(patch === "nylon_guitar" ? 2900 : 5200, now);
          voiceFilter.frequency.exponentialRampToValueAtTime(patch === "nylon_guitar" ? 850 : 1500, now + 0.38);
          addHammerTransient(3400, 0.35);
          env.gain.linearRampToValueAtTime(peakGain, now + 0.005);
          env.gain.exponentialRampToValueAtTime(peakGain * (isLead ? 0.62 : 0.18), now + 0.85);
          releaseTime = 0.18;
          break;
        }

        case "strings":
        case "solo_violin": {
          addOsc("sawtooth", 1, -9, 0.44);
          addOsc("sawtooth", 1, 0, 0.48);
          addOsc("sawtooth", 1, 9, 0.44);
          voiceFilter.frequency.setValueAtTime(2600, now);
          baseVib = patch === "solo_violin" ? 14 : 6;
          env.gain.linearRampToValueAtTime(peakGain * 0.88, now + (patch === "solo_violin" ? 0.06 : 0.11));
          releaseTime = 0.36;
          break;
        }

        case "brass":
        case "trumpet":
        case "mute_trumpet":
        case "flugelhorn": {
          addOsc("sawtooth", 1, -5, 0.55);
          addOsc("sawtooth", 1, 5, 0.55);
          if (patch === "mute_trumpet") {
            voiceFilter.type = "bandpass";
            voiceFilter.frequency.setValueAtTime(1950, now);
            voiceFilter.Q.value = 3.2;
          } else {
            const topF = patch === "flugelhorn" ? 1700 : 3800;
            voiceFilter.frequency.setValueAtTime(450, now);
            voiceFilter.frequency.exponentialRampToValueAtTime(topF, now + 0.055);
            voiceFilter.frequency.exponentialRampToValueAtTime(topF * 0.65, now + 0.25);
          }
          baseVib = 9;
          env.gain.linearRampToValueAtTime(peakGain * 0.92, now + 0.032);
          env.gain.exponentialRampToValueAtTime(peakGain * 0.72, now + 0.25);
          releaseTime = 0.14;
          break;
        }

        case "sax":
        case "clarinet":
        case "flute": {
          if (patch === "flute") {
            addOsc("sine", 1, 0, 0.85);
            addOsc("triangle", 2, 0, 0.18);
            addHammerTransient(4800, 0.22); // Flute breath chiff
            voiceFilter.frequency.setValueAtTime(3600, now);
            baseVib = 12;
          } else if (patch === "clarinet") {
            addOsc("square", 1, 0, 0.65);
            voiceFilter.frequency.setValueAtTime(1850, now);
            baseVib = 6;
          } else {
            addOsc("sawtooth", 1, -3, 0.58);
            addOsc("square", 1, 3, 0.32);
            voiceFilter.frequency.setValueAtTime(700, now);
            voiceFilter.frequency.exponentialRampToValueAtTime(2500, now + 0.05);
            baseVib = (st && st.assignableSwitches && st.assignableSwitches[1]) ? 32 : 13;
          }
          env.gain.linearRampToValueAtTime(peakGain * 0.88, now + 0.035);
          releaseTime = 0.14;
          break;
        }

        case "accordion":
        case "harmonica": {
          // Authentic wet musette twin-reed detuning!
          addOsc("sawtooth", 1, 0, 0.48);
          addOsc("square", 1, patch === "accordion" ? 14 : 6, 0.42);
          voiceFilter.frequency.setValueAtTime(2700, now);
          baseVib = patch === "harmonica" ? 14 : 4;
          env.gain.linearRampToValueAtTime(peakGain * 0.85, now + 0.03);
          releaseTime = 0.12;
          break;
        }

        case "oud": {
          addOsc("sawtooth", 1, -3, 0.62);
          addOsc("triangle", 1, 3, 0.52);
          voiceFilter.frequency.setValueAtTime(3800, now);
          voiceFilter.frequency.exponentialRampToValueAtTime(950, now + 0.32);
          addHammerTransient(2800, 0.5);
          env.gain.linearRampToValueAtTime(peakGain, now + 0.004);
          env.gain.exponentialRampToValueAtTime(peakGain * 0.14, now + 0.65);
          releaseTime = 0.16;
          break;
        }

        case "bass": {
          addOsc("triangle", 1, 0, 0.85);
          addOsc("sawtooth", 1, 2, 0.42);
          voiceFilter.frequency.setValueAtTime(1400, now);
          voiceFilter.frequency.exponentialRampToValueAtTime(380, now + 0.22);
          env.gain.linearRampToValueAtTime(peakGain, now + 0.006);
          env.gain.exponentialRampToValueAtTime(peakGain * 0.45, now + 0.45);
          releaseTime = 0.12;
          break;
        }

        case "pad": {
          addOsc("triangle", 1, -7, 0.55);
          addOsc("sawtooth", 1, 7, 0.38);
          addOsc("sine", 2, 0, 0.22);
          voiceFilter.frequency.setValueAtTime(1350, now);
          env.gain.linearRampToValueAtTime(peakGain * 0.82, now + 0.18);
          releaseTime = 0.45;
          break;
        }

        default: { // synth_lead
          addOsc("sawtooth", 1, -10, 0.48);
          addOsc("sawtooth", 1, 0, 0.50);
          addOsc("sawtooth", 1, 10, 0.48);
          voiceFilter.frequency.setValueAtTime(900, now);
          voiceFilter.frequency.exponentialRampToValueAtTime(5200, now + 0.08);
          voiceFilter.Q.value = 2.4;
          baseVib = 8;
          env.gain.linearRampToValueAtTime(peakGain * 0.88, now + 0.015);
          releaseTime = 0.18;
          break;
        }
      }

      if (baseVib > 0 || this.modDepth > 0) {
        vibOsc = this.ctx.createOscillator();
        vibGain = this.ctx.createGain();
        vibOsc.frequency.setValueAtTime(5.6, now);
        vibGain.gain.setValueAtTime(baseVib + this.modDepth, now);
        vibOsc.connect(vibGain);
        oscs.forEach(o => vibGain.connect(o.detune));
        vibOsc.start(now);
      }

      if (fixedDurationSec) {
        const stopAt = now + fixedDurationSec;
        env.gain.setValueAtTime(peakGain * sustainLevel, Math.max(now + 0.04, stopAt - 0.05));
        env.gain.exponentialRampToValueAtTime(0.0001, stopAt + releaseTime);
        oscs.forEach(o => o.stop(stopAt + releaseTime + 0.03));
        if (vibOsc) vibOsc.stop(stopAt + releaseTime + 0.03);
      } else {
        this.activeVoices.push({
          oscs,
          env,
          vibOsc,
          vibGain,
          _baseVib: baseVib,
          releaseTime
        });
      }
    }

    // Scheduled note helper for the lookahead Arranger sequencer
    _scheduleBandNote(time, patch, midiNote, durSec, gainAmt) {
      if (!this.ctx || this.muted) return;
      const freq = midiToFreq(midiNote);
      if (!isFinite(freq) || freq < 24 || freq > 12000) return;

      const env = this.ctx.createGain();
      const flt = this.ctx.createBiquadFilter();
      flt.type = "lowpass";
      env.gain.setValueAtTime(0.0001, time);
      flt.connect(env);
      env.connect(this.accBus);

      if (patch === "bass") {
        const o1 = this.ctx.createOscillator();
        const o2 = this.ctx.createOscillator();
        o1.type = "triangle";
        o2.type = "sawtooth";
        o1.frequency.setValueAtTime(freq, time);
        o2.frequency.setValueAtTime(freq, time);
        const g2 = this.ctx.createGain();
        g2.gain.value = 0.38;
        o1.connect(flt);
        o2.connect(g2);
        g2.connect(flt);
        flt.frequency.setValueAtTime(1150, time);
        flt.frequency.exponentialRampToValueAtTime(320, time + Math.min(0.22, durSec));
        env.gain.linearRampToValueAtTime(gainAmt, time + 0.006);
        env.gain.exponentialRampToValueAtTime(0.0001, time + durSec + 0.04);
        o1.start(time);
        o2.start(time);
        o1.stop(time + durSec + 0.06);
        o2.stop(time + durSec + 0.06);
      } else if (patch === "comp_ep" || patch === "comp_gtr") {
        const o1 = this.ctx.createOscillator();
        o1.type = patch === "comp_gtr" ? "sawtooth" : "triangle";
        o1.frequency.setValueAtTime(freq, time);
        flt.frequency.setValueAtTime(patch === "comp_gtr" ? 2800 : 2200, time);
        flt.frequency.exponentialRampToValueAtTime(750, time + durSec);
        env.gain.linearRampToValueAtTime(gainAmt, time + 0.008);
        env.gain.exponentialRampToValueAtTime(0.0001, time + durSec + 0.05);
        o1.start(time);
        o1.stop(time + durSec + 0.07);
      } else if (patch === "comp_strings" || patch === "lead_motif") {
        const o1 = this.ctx.createOscillator();
        const o2 = this.ctx.createOscillator();
        o1.type = "sawtooth";
        o2.type = "sawtooth";
        o1.frequency.setValueAtTime(freq, time);
        o2.frequency.setValueAtTime(freq, time);
        o1.detune.setValueAtTime(-7, time);
        o2.detune.setValueAtTime(7, time);
        flt.frequency.setValueAtTime(patch === "lead_motif" ? 3200 : 1700, time);
        const atk = patch === "lead_motif" ? 0.018 : 0.07;
        env.gain.linearRampToValueAtTime(gainAmt, time + atk);
        env.gain.setValueAtTime(gainAmt * 0.8, time + Math.max(atk, durSec - 0.04));
        env.gain.exponentialRampToValueAtTime(0.0001, time + durSec + 0.10);
        o1.start(time);
        o2.start(time);
        o1.stop(time + durSec + 0.12);
        o2.stop(time + durSec + 0.12);
      }
    }

    // =======================================================================
    // DRUM KIT & METRONOME SYNTHESIS
    // =======================================================================
    _playKick(time, vel = 0.72) {
      const o = this.ctx.createOscillator();
      const g = this.ctx.createGain();
      o.type = "sine";
      o.frequency.setValueAtTime(148, time);
      o.frequency.exponentialRampToValueAtTime(42, time + 0.11);
      g.gain.setValueAtTime(vel, time);
      g.gain.exponentialRampToValueAtTime(0.0001, time + 0.24);
      o.connect(g);
      g.connect(this.accBus);
      o.start(time);
      o.stop(time + 0.26);
    }

    _playSnare(time, vel = 0.45, rimOnly = false) {
      if (rimOnly) {
        const o = this.ctx.createOscillator();
        const g = this.ctx.createGain();
        o.type = "triangle";
        o.frequency.setValueAtTime(460, time);
        g.gain.setValueAtTime(vel * 0.55, time);
        g.gain.exponentialRampToValueAtTime(0.0001, time + 0.045);
        o.connect(g);
        g.connect(this.accBus);
        o.start(time);
        o.stop(time + 0.05);
        return;
      }
      // Snare body + crisp snare wires
      const body = this.ctx.createOscillator();
      const bg = this.ctx.createGain();
      body.type = "triangle";
      body.frequency.setValueAtTime(195, time);
      body.frequency.exponentialRampToValueAtTime(110, time + 0.08);
      bg.gain.setValueAtTime(vel * 0.55, time);
      bg.gain.exponentialRampToValueAtTime(0.0001, time + 0.10);
      body.connect(bg);
      bg.connect(this.accBus);
      body.start(time);
      body.stop(time + 0.11);

      const n = this.ctx.createBufferSource();
      n.buffer = this.noiseBuffer;
      const hp = this.ctx.createBiquadFilter();
      hp.type = "highpass";
      hp.frequency.setValueAtTime(1200, time);
      const ng = this.ctx.createGain();
      ng.gain.setValueAtTime(vel * 0.65, time);
      ng.gain.exponentialRampToValueAtTime(0.0001, time + 0.16);
      n.connect(hp);
      hp.connect(ng);
      ng.connect(this.accBus);
      n.start(time);
      n.stop(time + 0.18);
    }

    _playHat(time, open = false, vel = 0.22) {
      const n = this.ctx.createBufferSource();
      n.buffer = this.noiseBuffer;
      const hp = this.ctx.createBiquadFilter();
      hp.type = "highpass";
      hp.frequency.setValueAtTime(open ? 5500 : 7200, time);
      const g = this.ctx.createGain();
      const dur = open ? 0.24 : 0.048;
      g.gain.setValueAtTime(vel, time);
      g.gain.exponentialRampToValueAtTime(0.0001, time + dur);
      n.connect(hp);
      hp.connect(g);
      g.connect(this.accBus);
      n.start(time);
      n.stop(time + dur + 0.02);
    }

    _playCrash(time, vel = 0.34) {
      const n = this.ctx.createBufferSource();
      n.buffer = this.noiseBuffer;
      const bp = this.ctx.createBiquadFilter();
      bp.type = "bandpass";
      bp.frequency.setValueAtTime(4800, time);
      bp.Q.value = 0.6;
      const g = this.ctx.createGain();
      g.gain.setValueAtTime(vel, time);
      g.gain.exponentialRampToValueAtTime(0.0001, time + 0.85);
      n.connect(bp);
      bp.connect(g);
      g.connect(this.accBus);
      n.start(time);
      n.stop(time + 0.9);
    }

    _playTom(time, freqHz, vel = 0.5) {
      const o = this.ctx.createOscillator();
      const g = this.ctx.createGain();
      o.type = "sine";
      o.frequency.setValueAtTime(freqHz * 1.35, time);
      o.frequency.exponentialRampToValueAtTime(freqHz * 0.72, time + 0.14);
      g.gain.setValueAtTime(vel, time);
      g.gain.exponentialRampToValueAtTime(0.0001, time + 0.18);
      o.connect(g);
      g.connect(this.accBus);
      o.start(time);
      o.stop(time + 0.2);
    }

    _playMetronomeClick(time, accent) {
      const o = this.ctx.createOscillator();
      const g = this.ctx.createGain();
      o.type = "triangle";
      o.frequency.setValueAtTime(accent ? 1560 : 1046, time);
      g.gain.setValueAtTime(accent ? 0.32 : 0.18, time);
      g.gain.exponentialRampToValueAtTime(0.0001, time + 0.04);
      o.connect(g);
      g.connect(this.masterGain);
      o.start(time);
      o.stop(time + 0.05);
    }

    triggerPadHit(padIndex, padObj, st) {
      this.init();
      if (!this.ctx || this.muted) return;
      const now = this.ctx.currentTime;
      const ch = parseChordToMidi(st.recognizedChord) || parseChordToMidi("C Major");
      if (padObj.type === "OneShot") {
        this._playCrash(now, 0.35);
        ch.compNotes.forEach((m, i) => {
          this._scheduleBandNote(now + i * 0.03, "lead_motif", m + 12 + st.masterTranspose, 0.45, 0.20);
        });
      } else {
        this._playHat(now, true, 0.25);
      }
    }

    // =======================================================================
    // REAL-TIME LOOKAHEAD ARRANGER SEQUENCER (DRIVES CLOCK + BAND SOUND)
    // =======================================================================
    startEngineLoop(getStateFn, onBeatAdvanceFn) {
      this.getStateFn = getStateFn;
      this.onStepCallback = onBeatAdvanceFn;
      if (this.schedulerTimer) clearInterval(this.schedulerTimer);
      this.schedulerTimer = setInterval(() => this._schedulerTick(), 25);
    }

    resetGroovePosition() {
      if (this.ctx) {
        this.nextSubStepTime = this.ctx.currentTime + 0.01;
      }
      this.subStepIndex = 0;
    }

    _schedulerTick() {
      const st = this.getStateFn ? this.getStateFn() : null;
      if (!st || !st.powerOn) return;
      if (!this.ctx) return;

      this.syncPanelControls(st);

      const runningAnything = st.arrangerRunning || st.metronomeOn || st.playerRunning;
      if (!runningAnything) {
        this.nextSubStepTime = this.ctx.currentTime + 0.05;
        this.subStepIndex = 0;
        return;
      }

      if (this.nextSubStepTime < this.ctx.currentTime - 0.15) {
        this.nextSubStepTime = this.ctx.currentTime + 0.01;
      }

      const styleObj = window.PA700_DATA.styles[st.currentStyleIdx] || window.PA700_DATA.styles[0];
      const beatsPerBar = styleObj.beatsPerBar || 4;
      const subPerBeat = styleObj.meter === "6/8" ? 2 : 4;
      const totalSubSteps = beatsPerBar * subPerBeat;
      const subStepDur = (60 / Math.max(30, st.tempo)) / subPerBeat;

      while (this.nextSubStepTime < this.ctx.currentTime + 0.09) {
        const stepInBar = this.subStepIndex % totalSubSteps;
        const isQuarterBeat = (stepInBar % subPerBeat) === 0;
        const beatNumber1Based = Math.floor(stepInBar / subPerBeat) + 1;

        // Notify UI beat clock on exact beat boundaries (after step 0 initial beat)
        if (isQuarterBeat && this.subStepIndex > 0 && this.onStepCallback) {
          this.onStepCallback();
        }

        // Re-check if ending just stopped the arranger on bar boundary!
        if (st.metronomeOn && isQuarterBeat) {
          this._playMetronomeClick(this.nextSubStepTime, beatNumber1Based === 1);
        }

        if (st.arrangerRunning) {
          this._scheduleArrangerSubStep(
            this.nextSubStepTime,
            stepInBar,
            subPerBeat,
            beatsPerBar,
            subStepDur,
            styleObj,
            st
          );
        } else if (st.playerRunning && isQuarterBeat) {
          // Pleasant demo backing progression for Song Player
          const demoChords = ["A min", "D min", "G7", "C Major"];
          const cObj = parseChordToMidi(demoChords[Math.floor(st.playerBar / 4) % 4]);
          if (beatNumber1Based === 1) {
            this._playKick(this.nextSubStepTime, 0.5);
            this._scheduleBandNote(this.nextSubStepTime, "bass", cObj.bassRoot, subStepDur * 3, 0.28);
          } else if (beatNumber1Based === 3) {
            this._playSnare(this.nextSubStepTime, 0.35, true);
            cObj.compNotes.forEach(n => this._scheduleBandNote(this.nextSubStepTime, "comp_ep", n, subStepDur * 2.5, 0.13));
          }
          this._playHat(this.nextSubStepTime, false, 0.16);
        }

        this.nextSubStepTime += subStepDur;
        this.subStepIndex += 1;
      }
    }

    _scheduleArrangerSubStep(t, step, subPerBeat, beatsPerBar, subDur, styleObj, st) {
      const totalSteps = beatsPerBar * subPerBeat;
      const tr = st.masterTranspose || 0;
      const baseChord = parseChordToMidi(st.recognizedChord);
      const pitchedAllowed = st.accompOn && !st.manualBass && Boolean(baseChord);

      // 1. INTRO 3 / COUNT-IN: crisp 1-bar rimshot count-in!
      if (st.activeSection === "intro" && st.activeIntro === 3) {
        if (step % subPerBeat === 0) {
          this._playSnare(t, 0.55, true);
          this._playHat(t, false, 0.25);
        }
        return;
      }

      // 2. 1-BAR BREAK: Dramatic Stop-Time Hit on Step 0, then suspenseful silence!
      if (st.activeSection === "break") {
        if (step === 0) {
          this._playKick(t, 0.85);
          this._playCrash(t, 0.42);
          if (pitchedAllowed) {
            this._scheduleBandNote(t, "bass", baseChord.bassRoot + tr, subDur * 2.5, 0.42);
            baseChord.compNotes.forEach(n =>
              this._scheduleBandNote(t, "lead_motif", n + tr, subDur * 2.5, 0.20)
            );
          }
        } else if (step === totalSteps - 2) {
          // Pickup snare into next measure!
          this._playSnare(t, 0.48, false);
        }
        return;
      }

      // 3. 1-BAR AUTO-FILL (Tom/Snare Roll Building Energy into Next Variation!)
      if (st.activeSection === "fill") {
        const density = st.activeFill || 2;
        if (step === 0) this._playKick(t, 0.72);
        if (step < totalSteps / 2) {
          if (step % 2 === 0) this._playHat(t, false, 0.20);
          if (step === subPerBeat && pitchedAllowed) {
            this._scheduleBandNote(t, "bass", baseChord.bassRoot + tr, subDur * 2, 0.32);
          }
        } else {
          // Descending tom-tom + snare roll across second half of bar!
          const progress = (step - totalSteps / 2) / (totalSteps / 2);
          const tomFreq = 210 - progress * 105;
          if (density >= 3 || step % 2 === 0) {
            this._playTom(t, tomFreq, 0.42 + progress * 0.22);
          }
          if (step >= totalSteps - 2) {
            this._playSnare(t, 0.58, false);
          }
        }
        return;
      }

      // 4. ENDINGS 1, 2, 3 (2-Measure Musical Endings!)
      if (st.activeSection === "ending") {
        const bar = st.currentBar; // 1 or 2
        if (bar === 1) {
          // Cadential buildup (Ending 1 shifts to V7 on beat 3!)
          if (step === 0) {
            this._playKick(t, 0.72);
            this._playCrash(t, 0.28);
          }
          if (step % subPerBeat === 0) this._playHat(t, false, 0.20);
          if (st.activeEnding === 3 && (step === 0 || step === 3 || step === 6 || step === 10)) {
            // Syncopated Ending 3 band punches!
            this._playKick(t, 0.70);
            this._playSnare(t, 0.45, false);
            if (pitchedAllowed) {
              baseChord.compNotes.forEach(n =>
                this._scheduleBandNote(t, "lead_motif", n + tr, subDur * 1.8, 0.18)
              );
            }
          } else if (pitchedAllowed && (step === 0 || step === Math.floor(totalSteps / 2))) {
            const fifthShift = (st.activeEnding === 1 && step > 0) ? 7 : 0;
            this._scheduleBandNote(t, "bass", baseChord.bassRoot + fifthShift + tr, subDur * 4, 0.35);
            baseChord.compNotes.forEach(n =>
              this._scheduleBandNote(t, "comp_ep", n + fifthShift + tr, subDur * 4, 0.16)
            );
          }
        } else if (bar === 2 && step === 0) {
          // Final Bar Downbeat Resolution Hit & Sustained Chord!
          this._playKick(t, 0.85);
          this._playCrash(t, 0.45);
          if (pitchedAllowed) {
            this._scheduleBandNote(t, "bass", baseChord.bassRoot + tr, subDur * (totalSteps - 2), 0.42);
            baseChord.compNotes.forEach((n, idx) => {
              this._scheduleBandNote(t + idx * 0.025, "comp_strings", n + tr, subDur * (totalSteps - 2), 0.18);
              this._scheduleBandNote(t + idx * 0.025, "comp_ep", n + 12 + tr, subDur * (totalSteps - 3), 0.15);
            });
          }
        }
        return;
      }

      // 5. INTROS 1 & 2 vs VARIATIONS 1..4
      let chord = baseChord;
      const intensity = st.activeSection === "intro" ? 3 : st.activeVariation;

      // Intro 1 plays an actual prerecorded turnaround progression (IV -> V -> I) + melody!
      if (st.activeSection === "intro" && st.activeIntro === 1 && baseChord) {
        const shift = st.currentBar === 1 ? 5 : 7; // IV in bar 1, V in bar 2 -> resolves to I on Var!
        chord = {
          ...baseChord,
          bassRoot: baseChord.bassRoot + shift,
          compNotes: baseChord.compNotes.map(n => n + shift)
        };
        if (step % subPerBeat === 0 && pitchedAllowed) {
          const melNote = chord.compNotes[step % chord.compNotes.length] + 12 + tr;
          this._scheduleBandNote(t, "lead_motif", melNote, subDur * (subPerBeat * 0.85), 0.19);
        }
      }

      // Crash on Bar 1 Beat 1 for Variation 3/4 or Intro start
      if (st.currentBar === 1 && step === 0 && intensity >= 3) {
        this._playCrash(t, 0.28);
      }

      // Groove Archetype by Meter & Category
      if (styleObj.meter === "6/8") {
        // 6/8 Ballad (12 eighth-substeps per bar)
        if (step === 0 || step === 5) this._playKick(t, 0.62);
        if (step === 6) this._playSnare(t, 0.42, intensity === 1);
        if (step % 2 === 0 || intensity >= 2) this._playHat(t, step === 10 && intensity >= 3, 0.16);
        if (pitchedAllowed) {
          if (step === 0 || step === 6) {
            const bNote = step === 0 ? chord.bassRoot : chord.bassRoot + 7;
            this._scheduleBandNote(t, "bass", bNote + tr, subDur * 4.5, 0.34);
          }
          if (step === 0 || step === 4 || step === 6 || step === 10) {
            const arpNote = chord.compNotes[(step / 2) % chord.compNotes.length] + tr;
            this._scheduleBandNote(t, "comp_ep", arpNote, subDur * 3, 0.15);
          }
          if (intensity >= 3 && step === 0) {
            chord.compNotes.forEach(n => this._scheduleBandNote(t, "comp_strings", n + tr, subDur * 10, 0.11));
          }
        }
      } else if (styleObj.meter === "3/4") {
        // 3/4 Waltz (12 sixteenth-substeps per bar: beats at 0, 4, 8)
        if (step === 0) this._playKick(t, 0.68);
        if (step === 4 || step === 8) this._playSnare(t, 0.34, intensity === 1);
        if (step % 2 === 0) this._playHat(t, false, 0.16);
        if (pitchedAllowed) {
          if (step === 0) this._scheduleBandNote(t, "bass", chord.bassRoot + tr, subDur * 3.5, 0.38);
          if (step === 4 || step === 8) {
            chord.compNotes.forEach(n => this._scheduleBandNote(t, "comp_ep", n + tr, subDur * 2.5, 0.15));
          }
        }
      } else {
        // 4/4 Pop / Rock / Jazz / Soul / Dance / Oriental (16 sixteenth-substeps: 0..15)
        const isJazz = styleObj.category === "Jazz";
        const isDance = styleObj.category === "Dance";
        const isOriental = styleObj.id === "arabic_maqsoum";

        // Kick pattern
        if (isDance) {
          if (step % 4 === 0) this._playKick(t, 0.74); // 4-on-the-floor!
        } else if (isOriental) {
          if (step === 0 || step === 3 || step === 8) this._playKick(t, 0.72); // Dum-Tak-Dum Maqsoum!
        } else {
          if (step === 0 || step === 8 || (intensity >= 2 && step === 10) || (intensity === 4 && step === 6)) {
            this._playKick(t, 0.68);
          }
        }

        // Snare / Rim pattern
        if (step === 4 || step === 12 || (isOriental && (step === 6 || step === 14))) {
          this._playSnare(t, intensity === 1 ? 0.36 : 0.48, intensity === 1 && !isDance);
        }

        // Hi-Hat / Swing Ride pattern
        if (isJazz) {
          if (step % 4 === 0 || step === 7 || step === 15) {
            this._playHat(t, step === 7, 0.20);
          }
        } else if (intensity === 1) {
          if (step % 4 === 0) this._playHat(t, false, 0.16);
        } else if (intensity === 2) {
          if (step % 2 === 0) this._playHat(t, false, 0.18);
        } else {
          // Intensity 3 & 4: energetic 16th hats + offbeat open hat!
          if (step % 2 === 0 || intensity === 4) {
            this._playHat(t, isDance && (step === 2 || step === 6 || step === 10 || step === 14), 0.17);
          }
        }

        // Bass + Band Comping (when ACCOMP is ON and Chord recognized!)
        if (pitchedAllowed) {
          // Walking bass for Jazz, Octave bass for Dance, Root-5th groove for Pop/Rock
          if (isJazz && step % 4 === 0) {
            const walkOffsets = [0, chord.intervals[1], 7, chord.intervals[2] === 6 ? 6 : 9];
            const bNote = chord.bassRoot + walkOffsets[(step / 4) % 4] + tr;
            this._scheduleBandNote(t, "bass", bNote, subDur * 3.4, 0.35);
          } else if (isDance && step % 2 === 0) {
            const oct = (step % 4 === 2) ? 12 : 0;
            this._scheduleBandNote(t, "bass", chord.bassRoot + oct + tr, subDur * 1.6, 0.34);
          } else if (step === 0 || step === 6 || step === 8 || (intensity >= 2 && step === 14)) {
            const iv = (step === 6 || step === 14) ? 7 : 0;
            this._scheduleBandNote(t, "bass", chord.bassRoot + iv + tr, subDur * 3.0, 0.36);
          }

          // Chord comping rhythm
          const compHits = intensity === 1
            ? [0, 8]
            : intensity === 2
              ? [0, 6, 10, 12]
              : [0, 3, 6, 10, 12, 14];
          if (compHits.includes(step)) {
            const compPatch = (intensity >= 4 || isDance) ? "comp_gtr" : "comp_ep";
            chord.compNotes.forEach(n =>
              this._scheduleBandNote(t, compPatch, n + tr, subDur * 2.2, intensity >= 3 ? 0.15 : 0.12)
            );
          }

          // Lush background strings / brass layer in Variations 3 & 4
          if (intensity >= 3 && step === 0) {
            chord.compNotes.forEach(n =>
              this._scheduleBandNote(t, "comp_strings", n + 12 + tr, subDur * 14, 0.10)
            );
          }
        }
      }

      // 6. Active Looping PADS (1..4)
      st.padsActive.forEach((isOn, pIdx) => {
        if (!isOn) return;
        if (pIdx === 0 && step % 2 === 1) {
          this._playHat(t, false, 0.22); // Pad 1: Percussion/Tambourine groove
        } else if (pIdx === 1 && pitchedAllowed && step % 2 === 0) {
          const arp = chord.compNotes[(step / 2) % chord.compNotes.length] + 12 + tr;
          this._scheduleBandNote(t, "comp_gtr", arp, subDur * 1.5, 0.14); // Pad 2: Guitar/Arp sequence
        } else if (pIdx === 3 && pitchedAllowed && (step === 0 || step === 8)) {
          chord.compNotes.forEach(n =>
            this._scheduleBandNote(t, "comp_ep", n + 12 + tr, subDur * 5, 0.11)
          );
        }
      });
    }
  }

  window.pa700Audio = new Pa700AudioEngine();
})();
