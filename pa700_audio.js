/**
 * Korg Pa700 Audio Engine v2.0
 *
 * Multi-tier SoundFont & Web Audio synthesizer supporting all 1,845 Factory Sounds,
 * 379 Factory Styles, and 415 Factory Pads from Pa700 User Manual v1.5 E.
 *
 * Static-Web (GitHub Pages) & Open-Source SoundFont Stack:
 *   1. FluidR3 GM (Streaming)   - Per-instrument on-demand CORS streaming with in-memory patch caching.
 *   2. GeneralUser GS (.sf3/.sf2)- Full GM/GS SoundFont via SpessaSynth Worklet + IndexedDB cache.
 *   3. MuseScore General (.sf3)  - MS Basic / MuseScore_General via SpessaSynth + IndexedDB cache.
 *   4. FluidR3 Mono GM (.sf3)    - Single-file FluidR3Mono_GM via SpessaSynth + IndexedDB cache.
 *   5. FreePats GM (.sf2 Stack)  - Stackable local/user FreePats GM + Percussion .sf2 banks.
 *   6. Procedural WebAudio       - Zero-network 128-GM + Korg DNC synthesis fallback.
 */
(function (window) {
  "use strict";

  const FLUID_CDN_BASE = "https://cdn.jsdelivr.net/gh/gleitz/midi-js-soundfonts@gh-pages/FluidR3_GM";

  // Exact 128 GM program slugs from FluidR3_GM names.json
  const FLUIDR3_SLUGS = [
    "acoustic_grand_piano", "bright_acoustic_piano", "electric_grand_piano", "honkytonk_piano",
    "electric_piano_1", "electric_piano_2", "harpsichord", "clavinet",
    "celesta", "glockenspiel", "music_box", "vibraphone",
    "marimba", "xylophone", "tubular_bells", "dulcimer",
    "drawbar_organ", "percussive_organ", "rock_organ", "church_organ",
    "reed_organ", "accordion", "harmonica", "tango_accordion",
    "acoustic_guitar_nylon", "acoustic_guitar_steel", "electric_guitar_jazz", "electric_guitar_clean",
    "electric_guitar_muted", "overdriven_guitar", "distortion_guitar", "guitar_harmonics",
    "acoustic_bass", "electric_bass_finger", "electric_bass_pick", "fretless_bass",
    "slap_bass_1", "slap_bass_2", "synth_bass_1", "synth_bass_2",
    "violin", "viola", "cello", "contrabass",
    "tremolo_strings", "pizzicato_strings", "orchestral_harp", "timpani",
    "string_ensemble_1", "string_ensemble_2", "synth_strings_1", "synth_strings_2",
    "choir_aahs", "voice_oohs", "synth_choir", "orchestra_hit",
    "trumpet", "trombone", "tuba", "muted_trumpet",
    "french_horn", "brass_section", "synth_brass_1", "synth_brass_2",
    "soprano_sax", "alto_sax", "tenor_sax", "baritone_sax",
    "oboe", "english_horn", "bassoon", "clarinet",
    "piccolo", "flute", "recorder", "pan_flute",
    "blown_bottle", "shakuhachi", "whistle", "ocarina",
    "lead_1_square", "lead_2_sawtooth", "lead_3_calliope", "lead_4_chiff",
    "lead_5_charang", "lead_6_voice", "lead_7_fifths", "lead_8_bass__lead",
    "pad_1_new_age", "pad_2_warm", "pad_3_polysynth", "pad_4_choir",
    "pad_5_bowed", "pad_6_metallic", "pad_7_halo", "pad_8_sweep",
    "fx_1_rain", "fx_2_soundtrack", "fx_3_crystal", "fx_4_atmosphere",
    "fx_5_brightness", "fx_6_goblins", "fx_7_echoes", "fx_8_scifi",
    "sitar", "banjo", "shamisen", "koto",
    "kalimba", "bagpipe", "fiddle", "shanai",
    "tinkle_bell", "agogo", "steel_drums", "woodblock",
    "taiko_drum", "melodic_tom", "synth_drum", "reverse_cymbal",
    "guitar_fret_noise", "breath_noise", "seashore", "bird_tweet",
    "telephone_ring", "helicopter", "applause", "gunshot"
  ];

  const SOUND_LIBRARIES = {
    fluidr3_stream: {
      id: "fluidr3_stream",
      label: "FluidR3 GM (Stream)",
      mode: "stream",
      sizeLabel: "On-demand CDN",
      license: "MIT",
      description: "Streams per-instrument FluidR3 GM banks on demand from jsDelivr CDN and caches decoded notes in memory."
    },
    generaluser: {
      id: "generaluser",
      label: "GeneralUser GS (.sf3)",
      mode: "sf2",
      sizeLabel: "8.0 MB",
      license: "Permissive",
      urls: [
        "./soundfonts/generaluser/GeneralUserGS.sf3",
        "https://raw.githubusercontent.com/spessasus/SpessaSynth/master/soundfonts/GeneralUserGS.sf3"
      ]
    },
    generaluser_full: {
      id: "generaluser_full",
      label: "GeneralUser GS (.sf2)",
      mode: "sf2",
      sizeLabel: "30.8 MB",
      license: "Permissive",
      urls: [
        "./soundfonts/generaluser/GeneralUser-GS.sf2",
        "https://raw.githubusercontent.com/mrbumpy409/GeneralUser-GS/main/GeneralUser-GS.sf2"
      ]
    },
    fluidr3_full: {
      id: "fluidr3_full",
      label: "FluidR3 Mono GM (.sf3)",
      mode: "sf2",
      sizeLabel: "22.6 MB",
      license: "MIT",
      urls: [
        "./soundfonts/fluidr3/FluidR3Mono_GM.sf3",
        "https://raw.githubusercontent.com/musescore/MuseScore/main/share/sound/FluidR3Mono_GM.sf3"
      ]
    },
    musescore: {
      id: "musescore",
      label: "MuseScore General (.sf3)",
      mode: "sf2",
      sizeLabel: "48.9 MB",
      license: "MIT",
      urls: [
        "./soundfonts/musescore/MuseScore_General.sf3",
        "./soundfonts/musescore/MS_Basic.sf3",
        "https://raw.githubusercontent.com/musescore/MuseScore/main/share/sound/MS%20Basic.sf3"
      ]
    },
    freepats: {
      id: "freepats",
      label: "FreePats GM (.sf2 Stack)",
      mode: "sf2",
      sizeLabel: "Local / Upload",
      license: "CC0 / GPLv3+Exc",
      urls: [
        "./soundfonts/freepats/FreePatsGM-20221026.sf2",
        "./soundfonts/freepats/FreePatsGM-Percussion-20200822.sf2"
      ],
      stackUrls: [
        "./soundfonts/freepats/FreePatsGM-Percussion-20200822.sf2"
      ]
    },
    procedural: {
      id: "procedural",
      label: "Procedural WebAudio",
      mode: "procedural",
      sizeLabel: "0 KB (Offline)",
      license: "Built-in"
    }
  };

  const NOTE_NAMES_FLAT = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"];
  const NOTE_TO_SEMI = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };

  function midiToFlatName(midi) {
    const m = Math.max(0, Math.min(127, Math.round(midi)));
    const oct = Math.floor(m / 12) - 1;
    return `${NOTE_NAMES_FLAT[m % 12]}${oct}`;
  }

  function midiToFreq(midi) {
    return 440 * Math.pow(2, (midi - 69) / 12);
  }

  function clamp(v, lo, hi) {
    return Math.max(lo, Math.min(hi, v));
  }

  function parseChordToMidi(chordStr, transposeOffset = 0) {
    if (!chordStr || chordStr === "---" || chordStr === "N.C.") return null;
    const match = chordStr.trim().match(/^([A-G])([#b]?)(.*)$/);
    if (!match) return null;
    let semi = NOTE_TO_SEMI[match[1]];
    if (match[2] === "#") semi += 1;
    if (match[2] === "b") semi -= 1;
    semi = (((semi + transposeOffset) % 12) + 12) % 12;
    const rootMidi = 48 + semi;   // C3..B3 accompaniment root
    const bassRoot = 36 + semi;   // C2..B2 fundamental bass root
    const q = (match[3] || "").trim();

    const isMin = /^m(?!aj)/i.test(q) || q.startsWith("min");
    const isDim = q.includes("dim");
    const isAug = q.includes("aug");
    const isSus4 = q.includes("sus4");
    const isSus2 = q.includes("sus2");
    const isMaj7 = q.includes("maj7");
    const isDom7 = !isMaj7 && q.includes("7");
    const isSixth = !isDom7 && q.includes("6");

    const thirdSemi = isSus4 ? 5 : (isSus2 ? 2 : ((isMin || isDim) ? 3 : 4));
    const fifthSemi = isDim ? 6 : (isAug ? 8 : 7);
    const seventhSemi = isMaj7 ? 11 : (isSixth ? 9 : 10);

    const intervals = [0, thirdSemi, fifthSemi];
    if (isMaj7 || isDom7 || isSixth) intervals.push(seventhSemi);

    // Smooth voice-led close voicing centered around F3..F4 (53..65)
    const closeVoicing = intervals.map((iv) => {
      let m = rootMidi + iv;
      while (m < 53) m += 12;
      while (m > 66) m -= 12;
      return m;
    }).sort((a, b) => a - b);

    // Rootless Jazz/Bossa/Soul shell (3rd, 7th/6th, 9th)
    const jazzShell = [thirdSemi, seventhSemi, 14].map((iv) => {
      let m = rootMidi + iv;
      while (m < 54) m += 12;
      while (m > 69) m -= 12;
      return m;
    }).sort((a, b) => a - b);

    return {
      rootMidi,
      bassRoot,
      compNotes: intervals.map((i) => rootMidi + i),
      closeVoicing,
      jazzShell,
      thirdSemi,
      fifthSemi,
      seventhSemi,
      isMin,
      isDim,
      isAug,
      fifthMidi: rootMidi - 5
    };
  }

  // Resolve NTT Pitch Codes (0..25 single notes, 50..62 multi-note voicings/strums)
  function resolveStylePitchEvents(chordObj, code, isBass, octShift, tr) {
    const base = (isBass ? chordObj.bassRoot : chordObj.rootMidi) + (octShift || 0) * 12 + (tr || 0);
    const t3 = chordObj.thirdSemi;
    const t5 = chordObj.fifthSemi;
    const t7 = chordObj.seventhSemi;

    if (code < 50) {
      let off = 0;
      switch (code) {
        case 0:  off = 0; break;              // R
        case 1:  off = 2; break;              // D2 / 9th
        case 2:  off = t3; break;             // D3 (chord 3rd)
        case 3:  off = 5; break;              // D4 / 11th
        case 4:  off = t5; break;             // D5 (chord 5th)
        case 5:  off = 9; break;              // D6 / 13th
        case 6:  off = t7; break;             // D7 (chord 7th)
        case 7:  off = 10; break;             // B7 (Mixolydian/Blues b7)
        case 8:  off = 12; break;             // R8
        case 9:  off = t5 - 12; break;        // L5 (5th below root)
        case 10: off = -12; break;            // LR
        case 11: off = 14; break;             // U9
        case 12: off = t3 + 12; break;        // U3
        case 13: off = t5 + 12; break;        // U5
        case 14: off = 24; break;             // U8
        case 15: off = 6; break;              // B5 (#4/b5)
        case 16: off = -1; break;             // LT (leading tone below root)
        case 17: off = 1; break;              // B2 (Phrygian b2)
        case 18: off = 8; break;              // S5 (#5/b6: 007 Spy & Tango)
        case 19: off = 3; break;              // B3 (Blues minor 3rd)
        case 20: off = -3; break;             // L6 (low 6th below root)
        case 21: off = -7; break;             // L4 (low 4th below root)
        case 22: off = t5 + 1; break;         // A5
        case 23: off = t5 - 1; break;         // C5 (chromatic below 5th)
        case 24: off = 21; break;             // U6
        case 25: off = 22; break;             // UB7
        default: off = 0; break;
      }
      let m = base + off;
      if (isBass) {
        while (m < 28) m += 12;
        while (m > 55) m -= 12;
      } else {
        m = clamp(m, 36, 96);
      }
      return [{ midi: m, delaySec: 0, durScale: 1, velScale: 1 }];
    }

    const sh = (octShift || 0) * 12 + (tr || 0);
    switch (code) {
      case 50: // CLOSE voice-led chord
        return chordObj.closeVoicing.map((n) => ({ midi: n + sh, delaySec: 0, durScale: 1, velScale: 0.86 }));
      case 51: // OPEN lush piano/pad/strings voicing
        return [0, t5, 12 + t3, 12 + t5].map((iv, i) => ({
          midi: clamp(chordObj.rootMidi + iv + sh, 40, 92), delaySec: i * 0.004, durScale: 1.05, velScale: 0.82
        }));
      case 52: // HIGH_STAB brass/organ/clav punch
        return chordObj.closeVoicing.map((n) => ({ midi: clamp(n + 12 + sh, 48, 92), delaySec: 0, durScale: 0.82, velScale: 0.94 }));
      case 53: // JAZZ_SHELL rootless 3-7-9
        return chordObj.jazzShell.map((n) => ({ midi: n + sh, delaySec: 0, durScale: 1, velScale: 0.85 }));
      case 54: // POWER5 rock dyad (0, +7)
        return [0, 7].map((iv) => ({ midi: clamp(chordObj.rootMidi - 12 + iv + sh, 36, 84), delaySec: 0, durScale: 0.92, velScale: 0.96 }));
      case 55: // POWER8 stadium rock stack (0, +7, +12)
        return [0, 7, 12].map((iv) => ({ midi: clamp(chordObj.rootMidi - 12 + iv + sh, 36, 86), delaySec: 0, durScale: 0.96, velScale: 0.95 }));
      case 56: { // STRUM_DN staggered guitar downstroke
        const gtr = [0, 7, 12, 12 + t3];
        return gtr.map((iv, i) => ({
          midi: clamp(chordObj.rootMidi + iv + sh, 40, 86), delaySec: i * 0.014, durScale: 1.05, velScale: i === 0 ? 0.95 : 0.82
        }));
      }
      case 57: { // STRUM_UP staggered guitar upstroke
        const gtrUp = [12 + t5, 12 + t3, 12, 7];
        return gtrUp.map((iv, i) => ({
          midi: clamp(chordObj.rootMidi + iv + sh, 43, 88), delaySec: i * 0.011, durScale: 0.88, velScale: 0.80
        }));
      }
      case 58: // CHUCK damped percussive guitar/mandolin/pompe chop
        return chordObj.closeVoicing.map((n, i) => ({
          midi: clamp(n + sh, 48, 86), delaySec: i * 0.004, durScale: 0.22, velScale: 0.92
        }));
      case 59: // MONTUNO Cuban piano octave-shell
        return [0, t3, t5, 12].map((iv) => ({
          midi: clamp(chordObj.rootMidi + 12 + iv + sh, 48, 92), delaySec: 0, durScale: 0.88, velScale: 0.86
        }));
      case 60: // QUARTAL modern modal/house voicing (0, +5, +10)
        return [0, 5, 10].map((iv) => ({
          midi: clamp(chordObj.rootMidi + iv + sh, 45, 88), delaySec: 0, durScale: 1, velScale: 0.86
        }));
      case 61: // THIRDS harmonized dyad (Mariachi Tpts, Norteno Acc, Bouzouki, Steel)
        return [12 + t3, 12 + t5].map((iv) => ({
          midi: clamp(chordObj.rootMidi + iv + sh, 48, 92), delaySec: 0, durScale: 1, velScale: 0.92
        }));
      case 62: // FOURTHS parallel 4ths (Smoke Rock / Organ)
        return [0, 5].map((iv) => ({
          midi: clamp(chordObj.rootMidi + iv + sh, 40, 86), delaySec: 0, durScale: 0.95, velScale: 0.94
        }));
      default:
        return chordObj.closeVoicing.map((n) => ({ midi: n + sh, delaySec: 0, durScale: 1, velScale: 0.85 }));
    }
  }

  function classifyPatch(soundName) {
    const n = (soundName || "").toLowerCase();
    if (n.includes("honky")) return "honky_piano";
    if (n.includes("m1 piano") || n.includes("korg")) return "m1_piano";
    if (n.includes("tine") || n.includes("wurly") || n.includes("e.p") || n.includes("ep ") || n.includes("suitcase") || n.includes("rhodes")) return "epiano";
    if (n.includes("piano") || n.includes("grand")) return "piano";
    if (n.includes("pipe organ") || n.includes("cathedral")) return "pipe_organ";
    if (n.includes("rock org") || n.includes("bx3") || n.includes("overdriven org")) return "rock_organ";
    if (n.includes("organ") || n.includes("rotary")) return "jazz_organ";
    if (n.includes("accordion") || n.includes("musette") || n.includes("bandoneon")) return "accordion";
    if (n.includes("harmonica")) return "harmonica";
    if (n.includes("oud") || n.includes("sitar") || n.includes("kanun") || n.includes("bouzouki") || n.includes("mandolin") || n.includes("banjo")) return "oud";
    if (n.includes("nylon")) return "nylon_guitar";
    if (n.includes("12str") || n.includes("steel") || n.includes("acoustic gtr") || n.includes("folk")) return "steel_guitar";
    if (n.includes("overdrive") || n.includes("dist") || n.includes("tube") || n.includes("crunch")) return "lead_guitar";
    if (n.includes("guitar") || n.includes("gtr") || n.includes("strat")) return "clean_guitar";
    if (n.includes("bass") || n.includes("tuba")) return "bass";
    if (n.includes("violin") || n.includes("cello") || n.includes("fiddle")) return "solo_violin";
    if (n.includes("string") || n.includes("choir") || n.includes("vox")) return "strings";
    if (n.includes("mute")) return "mute_trumpet";
    if (n.includes("flugel")) return "flugelhorn";
    if (n.includes("trumpet") || n.includes("cornet")) return "trumpet";
    if (n.includes("brass") || n.includes("horn") || n.includes("trombone") || n.includes("trb")) return "brass";
    if (n.includes("sax")) return "sax";
    if (n.includes("clarinet") || n.includes("oboe")) return "clarinet";
    if (n.includes("flute") || n.includes("whistle") || n.includes("ocarina")) return "flute";
    if (n.includes("celesta") || n.includes("glock") || n.includes("bell") || n.includes("chime") || n.includes("vibe") || n.includes("marimba")) return "bell";
    if (n.includes("lead") || n.includes("saw") || n.includes("square") || n.includes("jump")) return "synth_lead";
    return "pad";
  }

  // IndexedDB cache for downloaded / user-uploaded SoundFonts
  const SF_CACHE = {
    dbName: "pa700_soundfont_cache_v1",
    storeName: "banks",
    open() {
      return new Promise((resolve, reject) => {
        if (!window.indexedDB) return reject(new Error("IndexedDB unavailable"));
        const req = window.indexedDB.open(this.dbName, 1);
        req.onupgradeneeded = () => {
          const db = req.result;
          if (!db.objectStoreNames.contains(this.storeName)) {
            db.createObjectStore(this.storeName);
          }
        };
        req.onsuccess = () => resolve(req.result);
        req.onerror = () => reject(req.error || new Error("IDB error"));
      });
    },
    async get(key) {
      try {
        const db = await this.open();
        return await new Promise((resolve, reject) => {
          const tx = db.transaction(this.storeName, "readonly");
          const getReq = tx.objectStore(this.storeName).get(key);
          getReq.onsuccess = () => resolve(getReq.result || null);
          getReq.onerror = () => reject(getReq.error);
        });
      } catch (_) {
        return null;
      }
    },
    async set(key, arrayBuffer) {
      try {
        const db = await this.open();
        return await new Promise((resolve, reject) => {
          const tx = db.transaction(this.storeName, "readwrite");
          const putReq = tx.objectStore(this.storeName).put(arrayBuffer, key);
          putReq.onsuccess = () => resolve(true);
          putReq.onerror = () => reject(putReq.error);
        });
      } catch (_) {
        return false;
      }
    },
    async clearAll() {
      try {
        const db = await this.open();
        return await new Promise((resolve, reject) => {
          const tx = db.transaction(this.storeName, "readwrite");
          const clrReq = tx.objectStore(this.storeName).clear();
          clrReq.onsuccess = () => resolve(true);
          clrReq.onerror = () => reject(clrReq.error);
        });
      } catch (_) {
        return false;
      }
    }
  };

  // -------------------------------------------------------------------------
  // Main Audio Engine
  // -------------------------------------------------------------------------
  class Pa700AudioEngine {
    constructor() {
      this.ctx = null;
      this.enabled = true;
      this.initialized = false;

      // Audio routing buses
      this.masterGain = null;
      this.analyser = null;
      this.compressor = null;
      this.kbdBus = null;
      this.arrangerBus = null;
      this.drumBus = null;
      this.reverbNode = null;
      this.reverbSend = null;
      this.sfOutputGain = null;
      this.noiseBuffer = null;

      // Real-time performance state
      this.masterVolume = 0.85;
      this.balanceVal = 0.5;
      this.joystickX = 0;
      this.joystickY = 0;
      this.pitchBendSemis = 0;
      this.activeVoices = [];
      this.activeSfNotes = [];
      this.meterArray = null;

      // Data indices built from PA700_DATA
      this.soundByName = new Map();
      this.soundById = new Map();
      this.padByName = new Map();
      this.padById = new Map();
      this._buildDataIndices();

      // Multi-tier SoundFont State
      this.activeLibId = "fluidr3_stream";
      this.libLoadState = "ready"; // 'ready' | 'loading' | 'loaded' | 'error'
      this.libProgressPct = 0;
      this.libStatusMsg = "Streaming ready";
      this.sfSynth = null;
      this.sfMode = null; // 'worklet' | 'processor' | null
      this.sfLoadedBanks = [];
      this.sfChannelProgramKey = {};
      this.scheduledSfTimers = new Set();
      this._sfInitPromise = null;

      // FluidR3_GM per-instrument on-demand cache
      this.fluidPatchCache = new Map();      // gmProg -> { C4: dataUri, ... }
      this.fluidPatchInflight = new Map();   // gmProg -> Promise
      this.fluidAudioCache = new Map();      // "prog:C4" -> AudioBuffer
      this.failedPrograms = new Map();       // gmProg -> { ms, reason } (network/offline errors only)
      this.currentPressSession = 0;
      this.isAnyKeyHeld = false;
      this.latencyMetrics = {
        limitMs: null,
        lastLoadMs: 0,
        droppedCount: 0,
        lastDropReason: "",
        loadedPatchesCount: 0
      };
      this.statusListeners = [];

      // Arranger loop scheduling
      this.loopTimerId = null;
      this.padSeqTimers = new Set();
      this.getStateFn = null;
      this.lastBeatScheduledTime = 0;
      this.subStepIndex = 0;
      this.nextSubStepTime = 0;
      this.barSubStepsSeen = 0;
      this.lastArrangerRunning = false;
      this.pendingArrangerStop = false;
    }

    _buildDataIndices() {
      const DATA = window.PA700_DATA;
      if (!DATA) return;
      if (Array.isArray(DATA.sounds)) {
        DATA.sounds.forEach((s) => {
          this.soundById.set(s.id, s);
          const low = s.name.toLowerCase();
          if (!this.soundByName.has(low) || s.type === "Factory") {
            this.soundByName.set(low, s);
          }
        });
      }
      if (Array.isArray(DATA.pads)) {
        DATA.pads.forEach((p) => {
          this.padById.set(p.id, p);
          const low = p.name.toLowerCase();
          if (!this.padByName.has(low)) this.padByName.set(low, p);
        });
      }
    }

    resolveSoundRecord(soundName) {
      if (!soundName) return null;
      if (typeof soundName === "object" && soundName.name) return soundName;
      const key = String(soundName).trim().toLowerCase();
      if (this.soundByName.has(key)) return this.soundByName.get(key);
      if (this.soundById.has(soundName)) return this.soundById.get(soundName);
      // Graceful synthesized fallback record if uncatalogued
      const patchType = classifyPatch(soundName);
      return {
        name: String(soundName),
        type: "Factory",
        group: patchType,
        category: patchType,
        isDrum: false,
        cc00: 121,
        cc32: 0,
        pc: 0,
        gmProgram: 0,
        dnc: null,
        profile: { gmProgram: 0, brightness: 1.0, detuneCents: 4, attackScale: 1, releaseScale: 1, chorusMix: 0.08, vibrato: 0, overdrive: 0, rotary: false }
      };
    }

    resolvePadRecord(padObjOrName) {
      if (!padObjOrName) return null;
      if (typeof padObjOrName === "object") {
        if (padObjOrName.id && this.padById.has(padObjOrName.id)) return this.padById.get(padObjOrName.id);
        if (padObjOrName.name && this.padByName.has(padObjOrName.name.toLowerCase())) {
          return this.padByName.get(padObjOrName.name.toLowerCase());
        }
        return padObjOrName;
      }
      const low = String(padObjOrName).toLowerCase();
      return this.padByName.get(low) || this.padById.get(padObjOrName) || { name: String(padObjOrName), type: "OneShot" };
    }

    onStatusChange(fn) {
      if (typeof fn === "function") this.statusListeners.push(fn);
    }

    _emitStatus() {
      const snap = this.getLibraryStatus();
      this.statusListeners.forEach((fn) => {
        try { fn(snap); } catch (_) {}
      });
    }

    getLibraryStatus() {
      const lib = SOUND_LIBRARIES[this.activeLibId] || SOUND_LIBRARIES.fluidr3_stream;
      return {
        activeId: this.activeLibId,
        activeLabel: lib.label,
        mode: lib.mode,
        state: this.libLoadState,
        progressPct: this.libProgressPct,
        statusMsg: this.libStatusMsg,
        loadedBanks: [...this.sfLoadedBanks],
        sfEngineReady: Boolean(this.sfSynth && this.sfLoadedBanks.length > 0),
        droppedCount: this.latencyMetrics.droppedCount,
        lastDropReason: this.latencyMetrics.lastDropReason,
        lastLoadMs: this.latencyMetrics.lastLoadMs,
        dropThresholdMs: this.latencyMetrics.limitMs,
        loadedPatchesCount: this.latencyMetrics.loadedPatchesCount,
        libraries: Object.values(SOUND_LIBRARIES).map((l) => ({
          id: l.id, label: l.label, mode: l.mode, sizeLabel: l.sizeLabel, license: l.license
        }))
      };
    }

    async init() {
      if (this.initialized) return true;
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (!AudioCtx) return false;
      this.ctx = new AudioCtx({ latencyHint: "interactive" });

      this.compressor = this.ctx.createDynamicsCompressor();
      this.compressor.threshold.setValueAtTime(-14, this.ctx.currentTime);
      this.compressor.ratio.setValueAtTime(3.2, this.ctx.currentTime);
      this.compressor.attack.setValueAtTime(0.004, this.ctx.currentTime);
      this.compressor.release.setValueAtTime(0.22, this.ctx.currentTime);

      this.masterGain = this.ctx.createGain();
      this.masterGain.gain.setValueAtTime(this.enabled ? this.masterVolume : 0, this.ctx.currentTime);

      this.analyser = this.ctx.createAnalyser();
      this.analyser.fftSize = 256;
      this.meterArray = new Uint8Array(this.analyser.frequencyBinCount);

      this.kbdBus = this.ctx.createGain();
      this.arrangerBus = this.ctx.createGain();
      this.drumBus = this.ctx.createGain();
      this.sfOutputGain = this.ctx.createGain();
      this.sfOutputGain.gain.setValueAtTime(0.95, this.ctx.currentTime);

      // Build impulse reverb + noise buffer
      this._buildNoiseAndReverb();

      this.kbdBus.connect(this.compressor);
      this.arrangerBus.connect(this.compressor);
      this.drumBus.connect(this.compressor);
      this.sfOutputGain.connect(this.compressor);
      this.kbdBus.connect(this.reverbSend);
      this.arrangerBus.connect(this.reverbSend);
      this.reverbSend.connect(this.reverbNode);
      this.reverbNode.connect(this.compressor);

      this.compressor.connect(this.masterGain);
      this.masterGain.connect(this.analyser);
      this.analyser.connect(this.ctx.destination);

      this.initialized = true;
      // Restore cached SoundFont banks seamlessly if previously stored
      this._restoreCachedBanksAsync();
      return true;
    }

    _buildNoiseAndReverb() {
      const sr = this.ctx.sampleRate;
      const nb = this.ctx.createBuffer(1, sr * 1.0, sr);
      const nd = nb.getChannelData(0);
      for (let i = 0; i < nd.length; i++) nd[i] = Math.random() * 2 - 1;
      this.noiseBuffer = nb;

      const revLen = Math.floor(sr * 1.45);
      const revBuf = this.ctx.createBuffer(2, revLen, sr);
      for (let c = 0; c < 2; c++) {
        const ch = revBuf.getChannelData(c);
        for (let i = 0; i < revLen; i++) {
          ch[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / revLen, 2.7);
        }
      }
      this.reverbNode = this.ctx.createConvolver();
      this.reverbNode.buffer = revBuf;
      this.reverbSend = this.ctx.createGain();
      this.reverbSend.gain.setValueAtTime(0.16, this.ctx.currentTime);
    }

    async resume() {
      if (!this.initialized) await this.init();
      if (this.ctx && this.ctx.state === "suspended") {
        await this.ctx.resume().catch(() => {});
      }
    }

    isEnabled() {
      return this.enabled;
    }

    get muted() {
      return !this.enabled;
    }

    setMuted(m) {
      this.setEnabled(!m);
    }

    setEnabled(on) {
      this.enabled = Boolean(on);
      if (this.masterGain && this.ctx) {
        const now = this.ctx.currentTime;
        this.masterGain.gain.cancelScheduledValues(now);
        this.masterGain.gain.setTargetAtTime(this.enabled ? this.masterVolume : 0, now, 0.02);
      }
      if (!this.enabled) {
        this.releaseAllKeyboardVoices();
      }
    }

    syncPanelControls(st) {
      if (!st) return;
      this.masterVolume = clamp((st.masterVol !== undefined ? st.masterVol : 85) / 100, 0, 1.15);
      this.balanceVal = clamp((st.balance !== undefined ? st.balance : 50) / 100, 0, 1);
      if (this.ctx && this.masterGain) {
        const now = this.ctx.currentTime;
        if (this.enabled) {
          this.masterGain.gain.setTargetAtTime(this.masterVolume, now, 0.025);
        }
        const kbdScale = clamp(this.balanceVal * 1.45, 0.2, 1.15);
        const arrScale = clamp((1 - this.balanceVal) * 1.45, 0.18, 1.15);
        this.kbdBus.gain.setTargetAtTime(kbdScale, now, 0.025);
        this.arrangerBus.gain.setTargetAtTime(arrScale, now, 0.025);
        this.drumBus.gain.setTargetAtTime(arrScale * 1.12, now, 0.025);
      }
    }

    setJoystick(xVal, yVal) {
      this.joystickX = clamp(xVal, -1, 1);
      this.joystickY = clamp(yVal, -1, 1);
      this.pitchBendSemis = this.joystickX * 2.0;

      if (this.sfSynth && this.sfLoadedBanks.length > 0) {
        const wheelVal = Math.round(8192 + this.joystickX * 8191);
        const modVal = Math.round(Math.max(0, this.joystickY) * 127);
        for (let ch = 0; ch < 4; ch++) {
          try {
            this.sfSynth.pitchWheel(ch, clamp(wheelVal, 0, 16383));
            this.sfSynth.controllerChange(ch, 1, clamp(modVal, 0, 127));
          } catch (_) {}
        }
      }

      if (!this.ctx) return;
      const now = this.ctx.currentTime;
      const bendCents = this.pitchBendSemis * 100;
      const modDepth = Math.max(0, this.joystickY) * 42;
      this.activeVoices.forEach((v) => {
        v.oscs.forEach((o) => {
          try { o.detune.setTargetAtTime((o._baseDetune || 0) + bendCents, now, 0.015); } catch (_) {}
        });
        if (v.vibGain) {
          try { v.vibGain.gain.setTargetAtTime((v.baseVib || 0) + modDepth, now, 0.02); } catch (_) {}
        }
      });
    }

    getMeterLevel() {
      if (!this.analyser || !this.meterArray || !this.enabled) return 0;
      this.analyser.getByteTimeDomainData(this.meterArray);
      let peak = 0;
      for (let i = 0; i < this.meterArray.length; i++) {
        const dev = Math.abs((this.meterArray[i] - 128) / 128);
        if (dev > peak) peak = dev;
      }
      return clamp(peak * 1.85, 0, 1);
    }

    // =========================================================================
    // SPESSASYNTH SOUNDFONT ENGINE + MULTI-LIBRARY & INDEXEDDB MANAGER
    // =========================================================================
    async _ensureSpessaSynthReady() {
      if (this.sfSynth) return this.sfSynth;
      if (this._sfInitPromise) return this._sfInitPromise;
      this._sfInitPromise = (async () => {
        await this.init();
        if (!window.SpessaSynth) {
          if (window.PA700_STANDALONE) {
            throw new Error("Serve via HTTP/github.io for full .sf2/.sf3 SpessaSynth banks");
          }
          await new Promise((res) => {
            const to = setTimeout(res, 2500);
            window.addEventListener("spessasynth-ready", () => { clearTimeout(to); res(); }, { once: true });
          });
        }
        if (!window.SpessaSynth) throw new Error("SpessaSynth module unavailable");

        // Primary: AudioWorklet (works seamlessly on https://*.github.io and localhost)
        if (this.ctx.audioWorklet) {
          try {
            await this.ctx.audioWorklet.addModule("./vendor/spessasynth/spessasynth_processor.min.js");
            const synth = new window.SpessaSynth.WorkletSynthesizer(this.ctx);
            synth.connect(this.sfOutputGain);
            await synth.isReady;
            this.sfSynth = synth;
            this.sfMode = "worklet";
            return synth;
          } catch (err) {
            console.warn("AudioWorklet unavailable, switching to SpessaSynth main-thread fallback:", err);
          }
        }
        // Fallback: SpessaSynthProcessor via ScriptProcessor (supports offline file:// standalone HTML)
        if (window.SpessaSynth.SpessaSynthProcessor && this.ctx.createScriptProcessor) {
          const proc = new window.SpessaSynth.SpessaSynthProcessor(this.ctx.sampleRate);
          await proc.ready;
          const node = this.ctx.createScriptProcessor(2048, 0, 2);
          node.onaudioprocess = (ev) => {
            const outL = ev.outputBuffer.getChannelData(0);
            const outR = ev.outputBuffer.getChannelData(1);
            outL.fill(0);
            outR.fill(0);
            proc.process(outL, outR, 0, outL.length);
          };
          node.connect(this.sfOutputGain);
          this.sfScriptNode = node;
          this.sfSynth = proc;
          this.sfMode = "processor";
          return proc;
        }
        throw new Error("No Web Audio synth processor available");
      })();
      try {
        return await this._sfInitPromise;
      } finally {
        this._sfInitPromise = null;
      }
    }

    async _restoreCachedBanksAsync() {
      try {
        const savedLib = window.localStorage && window.localStorage.getItem("pa700_sf_lib");
        if (savedLib && SOUND_LIBRARIES[savedLib] && savedLib !== "fluidr3_stream" && savedLib !== "procedural") {
          const buf = await SF_CACHE.get(`bank:${savedLib}`);
          if (buf && buf.byteLength > 10000) {
            await this._mountBankBuffer(savedLib, buf, savedLib);
            this.activeLibId = savedLib;
            this.libLoadState = "loaded";
            this.libProgressPct = 100;
            this.libStatusMsg = `Cached ${SOUND_LIBRARIES[savedLib].label}`;
            this._emitStatus();
          }
        }
      } catch (_) {}
    }

    async _mountBankBuffer(bankId, arrayBuffer, libId) {
      const synth = await this._ensureSpessaSynthReady();
      if (this.sfMode === "processor" && window.SpessaSynth.SoundBankLoader) {
        const bankObj = window.SpessaSynth.SoundBankLoader.fromArrayBuffer(arrayBuffer.slice(0));
        synth.soundBankManager.addSoundBank(bankObj, bankId);
      } else {
        await synth.soundBankManager.addSoundBank(arrayBuffer.slice(0), bankId);
      }
      if (!this.sfLoadedBanks.includes(bankId)) {
        this.sfLoadedBanks.unshift(bankId);
      }
      // Prioritize FreePats at top if loaded, followed by latest main SoundFont
      try {
        const ordered = [...this.sfLoadedBanks].sort((a, b) => {
          if (a.startsWith("freepats") && !b.startsWith("freepats")) return -1;
          if (!a.startsWith("freepats") && b.startsWith("freepats")) return 1;
          return a === bankId ? -1 : 0;
        });
        synth.soundBankManager.priorityOrder = ordered;
      } catch (_) {}
      this.sfChannelProgramKey = {};
    }

    async setSoundLibrary(libId, options = {}) {
      const lib = SOUND_LIBRARIES[libId];
      if (!lib) return this.getLibraryStatus();
      this.activeLibId = libId;
      try { window.localStorage && window.localStorage.setItem("pa700_sf_lib", libId); } catch (_) {}

      if (lib.mode === "stream" || lib.mode === "procedural") {
        if (lib.mode === "stream") this.failedPrograms.clear();
        this.libLoadState = "ready";
        this.libProgressPct = 100;
        this.libStatusMsg = lib.mode === "stream" ? "Streaming ready" : "Procedural WebAudio active";
        this._emitStatus();
        return this.getLibraryStatus();
      }

      // Check IndexedDB cache first
      await this.init();
      const cached = !options.forceDownload ? await SF_CACHE.get(`bank:${libId}`) : null;
      if (cached && cached.byteLength > 10000) {
        try {
          await this._mountBankBuffer(libId, cached, libId);
          this.libLoadState = "loaded";
          this.libProgressPct = 100;
          this.libStatusMsg = `${lib.label} ready (IDB Cache)`;
          this._emitStatus();
          return this.getLibraryStatus();
        } catch (err) {
          console.warn("Cached bank mount failed:", err);
        }
      }

      // Download in background with progress reporting (never delays active note playing)
      this.libLoadState = "loading";
      this.libProgressPct = 1;
      this.libStatusMsg = `Fetching ${lib.label}...`;
      this._emitStatus();

      let fetchedBuf = null;
      let lastErr = null;
      for (const url of lib.urls || []) {
        try {
          fetchedBuf = await this._fetchWithProgress(url, (pct) => {
            this.libProgressPct = pct;
            this.libStatusMsg = `${lib.label} ${pct}%`;
            this._emitStatus();
          });
          if (fetchedBuf && fetchedBuf.byteLength > 10000) break;
        } catch (err) {
          lastErr = err;
        }
      }

      if (!fetchedBuf) {
        this.libLoadState = "error";
        this.libProgressPct = 0;
        this.libStatusMsg = libId === "freepats"
          ? "Upload FreePats .sf2 (CORS-free local/IDB)"
          : `Load unavailable (${lastErr ? lastErr.message : "network"}) - using fallback`;
        this._emitStatus();
        return this.getLibraryStatus();
      }

      try {
        await SF_CACHE.set(`bank:${libId}`, fetchedBuf.slice(0));
        await this._mountBankBuffer(libId, fetchedBuf, libId);
        // Optional percussion stack for FreePats
        if (lib.stackUrls) {
          for (let i = 0; i < lib.stackUrls.length; i++) {
            try {
              const stackBuf = await this._fetchWithProgress(lib.stackUrls[i]);
              if (stackBuf && stackBuf.byteLength > 5000) {
                await this._mountBankBuffer(`${libId}_stack_${i}`, stackBuf, libId);
              }
            } catch (_) {}
          }
        }
        this.libLoadState = "loaded";
        this.libProgressPct = 100;
        this.libStatusMsg = `${lib.label} loaded`;
      } catch (err) {
        this.libLoadState = "error";
        this.libStatusMsg = `Mount failed: ${err.message}`;
      }
      this._emitStatus();
      return this.getLibraryStatus();
    }

    async _fetchWithProgress(url, onProgress) {
      const resp = await fetch(url);
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      const total = parseInt(resp.headers.get("content-length") || "0", 10);
      if (!resp.body || !total) {
        const ab = await resp.arrayBuffer();
        if (onProgress) onProgress(100);
        return ab;
      }
      const reader = resp.body.getReader();
      const chunks = [];
      let received = 0;
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        chunks.push(value);
        received += value.byteLength;
        if (onProgress && total > 0) {
          onProgress(Math.min(99, Math.round((received / total) * 100)));
        }
      }
      const combined = new Uint8Array(received);
      let offset = 0;
      for (const c of chunks) {
        combined.set(c, offset);
        offset += c.byteLength;
      }
      if (onProgress) onProgress(100);
      return combined.buffer;
    }

    async loadLocalSoundFontFiles(fileList) {
      if (!fileList || !fileList.length) return this.getLibraryStatus();
      await this.init();
      this.libLoadState = "loading";
      this.libStatusMsg = "Loading local .sf2/.sf3...";
      this._emitStatus();

      let count = 0;
      for (const file of fileList) {
        const ab = await file.arrayBuffer();
        const isFreePats = file.name.toLowerCase().includes("freepat");
        const bankId = isFreePats ? `freepats_${file.name}` : `custom_${file.name}`;
        await SF_CACHE.set(`bank:${bankId}`, ab.slice(0));
        await this._mountBankBuffer(bankId, ab, isFreePats ? "freepats" : "custom");
        if (isFreePats) this.activeLibId = "freepats";
        count += 1;
      }
      this.libLoadState = "loaded";
      this.libProgressPct = 100;
      this.libStatusMsg = `Mounted ${count} local SoundFont${count > 1 ? "s" : ""}`;
      this._emitStatus();
      return this.getLibraryStatus();
    }

    async clearCachedBanks() {
      await SF_CACHE.clearAll();
      this.fluidPatchCache.clear();
      this.fluidAudioCache.clear();
      this.failedPrograms.clear();
      this.latencyMetrics.droppedCount = 0;
      this.latencyMetrics.lastDropReason = "";
      this.latencyMetrics.loadedPatchesCount = 0;
      this.libStatusMsg = "Cleared SoundFont cache";
      this._emitStatus();
    }

    _syncSfChannelProgram(channel, rec, panOverride) {
      if (!this.sfSynth || !rec) return;
      const isDrum = Boolean(rec.isDrum || channel === 9);
      const cc00 = isDrum ? 128 : (rec.cc00 || 0) & 0x7f;
      const cc32 = isDrum ? 0 : (rec.cc32 || 0) & 0x7f;
      const pc = isDrum
        ? (rec.gsDrumPc !== undefined ? rec.gsDrumPc : (rec.pc || 0)) & 0x7f
        : (rec.pc !== undefined ? rec.pc : (rec.gmProgram || 0)) & 0x7f;
      const panVal = panOverride !== undefined ? clamp(Math.round(panOverride), 0, 127) : (rec.pan !== undefined ? rec.pan : 64);
      const key = `${cc00}:${cc32}:${pc}:${panVal}:${isDrum ? 1 : 0}`;
      if (this.sfChannelProgramKey[channel] === key) return;
      this.sfChannelProgramKey[channel] = key;
      try {
        if (!isDrum) {
          this.sfSynth.controllerChange(channel, 0, cc00);
          this.sfSynth.controllerChange(channel, 32, cc32);
          this.sfSynth.controllerChange(channel, 10, panVal);
          this.sfSynth.controllerChange(channel, 91, channel === 5 ? 18 : 44);
        }
        this.sfSynth.programChange(channel, pc);
      } catch (_) {}
    }

    // =========================================================================
    // FLUIDR3 GM ON-DEMAND STREAMING LOADER (NO DOWNLOAD TIMEOUT)
    // =========================================================================
    async _loadFluidPatch(gmProg) {
      const p = clamp(Math.round(gmProg || 0), 0, 127);
      if (this.fluidPatchCache.has(p)) {
        return { notes: this.fluidPatchCache.get(p), elapsedMs: 0, cached: true, dropped: false };
      }
      if (this.fluidPatchInflight.has(p)) {
        return this.fluidPatchInflight.get(p);
      }

      const slug = FLUIDR3_SLUGS[p] || "acoustic_grand_piano";
      const url = `${FLUID_CDN_BASE}/${slug}-mp3.js`;
      const startTime = performance.now();

      const loaderPromise = (async () => {
        try {
          const resp = await fetch(url);
          if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
          const text = await resp.text();
          const firstBrace = text.indexOf("{");
          const lastBrace = text.lastIndexOf("}");
          if (firstBrace < 0 || lastBrace <= firstBrace) throw new Error("Invalid soundfont payload");
          const notesObj = JSON.parse(text.slice(firstBrace, lastBrace + 1));
          const elapsedMs = Math.round(performance.now() - startTime);
          this.failedPrograms.delete(p);
          this.fluidPatchCache.set(p, notesObj);
          this.latencyMetrics.lastLoadMs = elapsedMs;
          this.latencyMetrics.loadedPatchesCount = this.fluidPatchCache.size;
          this.libStatusMsg = `Streaming ready (${this.fluidPatchCache.size} cached)`;
          this._emitStatus();
          return { notes: notesObj, elapsedMs, cached: false, dropped: false };
        } catch (err) {
          const elapsedMs = Math.round(performance.now() - startTime);
          this.failedPrograms.set(p, { ms: elapsedMs, reason: err.message });
          return { notes: null, elapsedMs, cached: false, dropped: false, error: err.message };
        } finally {
          this.fluidPatchInflight.delete(p);
        }
      })();

      this.fluidPatchInflight.set(p, loaderPromise);
      return loaderPromise;
    }

    // Backwards-compatible alias
    async _loadFluidPatchWithTimeout(gmProg) {
      return this._loadFluidPatch(gmProg);
    }

    async _decodeFluidNoteBuffer(gmProg, midiNote, tStart = performance.now()) {
      const p = clamp(Math.round(gmProg || 0), 0, 127);
      const patchRes = await this._loadFluidPatch(p);
      if (!patchRes || !patchRes.notes) return null;

      const noteName = midiToFlatName(clamp(midiNote, 21, 108));
      const cacheKey = `${p}:${noteName}`;
      if (this.fluidAudioCache.has(cacheKey)) {
        return { buffer: this.fluidAudioCache.get(cacheKey), dropped: false };
      }

      const dataUri = patchRes.notes[noteName] || patchRes.notes["C4"] || Object.values(patchRes.notes)[0];
      if (!dataUri || !this.ctx) return null;

      try {
        const b64 = dataUri.includes(",") ? dataUri.split(",")[1] : dataUri;
        const binStr = atob(b64);
        const bytes = new Uint8Array(binStr.length);
        for (let i = 0; i < binStr.length; i++) bytes[i] = binStr.charCodeAt(i);
        const audioBuf = await this.ctx.decodeAudioData(bytes.buffer);
        const totalElapsed = Math.round(performance.now() - tStart);
        this.fluidAudioCache.set(cacheKey, audioBuf);
        this.latencyMetrics.lastLoadMs = totalElapsed;
        return { buffer: audioBuf, dropped: false };
      } catch (err) {
        return { buffer: null, dropped: false, error: err.message };
      }
    }

    /**
     * Public preload hook - warms newly picked FluidR3 sounds in the background
     * regardless of connection speed.
     */
    async preloadSound(soundName) {
      if (this.activeLibId !== "fluidr3_stream") return;
      const rec = this.resolveSoundRecord(soundName);
      if (!rec || rec.isDrum) return;
      await this._loadFluidPatch(rec.gmProgram || rec.pc || 0);
    }

    // =========================================================================
    // LIVE KEYBOARD NOTE TRIGGERING & RELEASE
    // =========================================================================
    async playKeyboardNotes(arg1, arg2) {
      const midiList = Array.isArray(arg1) ? arg1 : (Array.isArray(arg2) ? arg2 : []);
      const st = Array.isArray(arg1) ? arg2 : arg1;
      if (!this.enabled || !st) return;
      await this.resume();
      this.releaseAllKeyboardVoices(st);
      if (!midiList || !midiList.length) return;

      this.currentPressSession += 1;
      const pressId = this.currentPressSession;
      this.isAnyKeyHeld = true;

      const splitPoint = st.splitPoint !== undefined ? st.splitPoint : 60;
      const tr = st.masterTranspose || 0;
      const useSf2Bank = Boolean(
        this.sfSynth &&
        this.sfLoadedBanks.length > 0 &&
        this.activeLibId !== "procedural" &&
        this.activeLibId !== "fluidr3_stream"
      );

      // Right-hand notes (always >= splitPoint if split active) & Left-hand notes
      const rightHandMidi = st.splitEnabled ? midiList.filter((m) => m >= splitPoint) : midiList;
      const leftHandMidi = st.splitEnabled ? midiList.filter((m) => m < splitPoint) : [];

      const activeTracks = [
        { tk: "up1", ch: 0, notes: rightHandMidi },
        { tk: "up2", ch: 1, notes: rightHandMidi },
        { tk: "up3", ch: 2, notes: rightHandMidi },
        { tk: "low", ch: 3, notes: st.splitEnabled ? leftHandMidi : (st.arrangerRunning ? [] : []) }
      ];

      // Note on Lower: when split is enabled and Lower isn't muted, Lower sounds left-hand keys;
      // in Manual Bass mode, Lower overrides with Manual Bass punch.
      activeTracks.forEach(({ tk, ch, notes }) => {
        const track = st.tracks && st.tracks[tk];
        if (!track || track.muted || !notes.length) return;
        const soundName = (tk === "low" && st.manualBass) ? "Acoustic Bass" : track.sound;
        const rec = this.resolveSoundRecord(soundName);
        const octShift = (track.octave || 0) * 12;
        const trkVol = clamp(((track.volume !== undefined ? track.volume : 100) / 127) * 0.42, 0.04, 0.55);

        notes.forEach((rawMidi, idx) => {
          const midi = clamp(rawMidi + tr + octShift, 21, 108);
          this._playLiveTrackNote({ rec, ch, midi, gain: trkVol, trackKey: tk, isLeadIdx: idx === 0, pressId, st });

          if (st.ensembleOn && tk === "up1" && idx === 0) {
            const harmOffset = st.ensembleType === "Octave" ? -12 : -4;
            this._playLiveTrackNote({
              rec, ch, midi: clamp(midi + harmOffset, 21, 108), gain: trkVol * 0.62,
              trackKey: tk, isLeadIdx: false, pressId, st
            });
          }
        });
      });
    }

    _playLiveTrackNote({ rec, ch, midi, gain, trackKey, isLeadIdx, pressId, st }) {
      // 1. SpessaSynth full .sf2/.sf3 active
      if (this.sfSynth && this.sfLoadedBanks.length > 0 && this.activeLibId !== "procedural" && this.activeLibId !== "fluidr3_stream") {
        this._syncSfChannelProgram(ch, rec);
        const vel = clamp(Math.round(gain * 240), 18, 127);
        try {
          this.sfSynth.noteOn(ch, midi, vel);
          this.activeSfNotes.push({ ch, midi });
          return;
        } catch (_) {}
      }

      // 2. FluidR3 GM Streaming (on-demand CDN fetch & decode, cached in memory)
      if (this.activeLibId === "fluidr3_stream" && !rec.isDrum) {
        const prog = rec.gmProgram !== undefined ? rec.gmProgram : (rec.pc || 0);
        const cacheKey = `${prog}:${midiToFlatName(midi)}`;
        if (this.fluidAudioCache.has(cacheKey)) {
          this._spawnSampleVoice(this.fluidAudioCache.get(cacheKey), midi, gain, rec, st);
          return;
        }
        const tStart = performance.now();
        this._decodeFluidNoteBuffer(prog, midi, tStart).then((res) => {
          if (!this.isAnyKeyHeld || this.currentPressSession !== pressId || !this.enabled) {
            // Key was already released while fetching -> suppress delayed ghost note
            return;
          }
          if (!res || !res.buffer) {
            // Network/offline failure -> graceful procedural synth fallback while held
            const fallbackPatch = classifyPatch(rec.name);
            this._spawnSynthVoice(fallbackPatch, midi, gain, this.kbdBus, st, null, rec);
            return;
          }
          this._spawnSampleVoice(res.buffer, midi, gain, rec, st);
        });
        return;
      }

      // 3. Procedural WebAudio Fallback (zero network)
      const patch = classifyPatch(rec.name);
      this._spawnSynthVoice(patch, midi, gain, this.kbdBus, st, null, rec);

      // DNC articulation preview when Assignable Switch 1/2 or Joystick Y active on a DNC sound
      if (rec.dnc && isLeadIdx && st.assignableSwitches) {
        if (st.assignableSwitches[1] && (rec.dnc.sc1On || "").toLowerCase().includes("riff")) {
          // Graceful DNC Riff Up grace note!
          setTimeout(() => {
            if (this.currentPressSession === pressId && this.isAnyKeyHeld) {
              this._spawnSynthVoice(patch, clamp(midi + 2, 21, 108), gain * 0.72, this.kbdBus, st, 0.14, rec);
            }
          }, 55);
        }
      }
    }

    releaseAllKeyboardVoices(st) {
      this.isAnyKeyHeld = false;
      if (this.sfSynth && this.activeSfNotes.length > 0) {
        while (this.activeSfNotes.length > 0) {
          const n = this.activeSfNotes.pop();
          try { this.sfSynth.noteOff(n.ch, n.midi); } catch (_) {}
        }
      }
      if (!this.ctx) return;
      const now = this.ctx.currentTime;
      while (this.activeVoices.length > 0) {
        const v = this.activeVoices.pop();
        try {
          const rel = v.releaseTime || 0.18;
          v.env.gain.cancelScheduledValues(now);
          v.env.gain.setValueAtTime(Math.max(0.0001, v.env.gain.value), now);
          v.env.gain.exponentialRampToValueAtTime(0.0001, now + rel);
          if (v.srcNode) v.srcNode.stop(now + rel + 0.04);
          v.oscs.forEach((o) => o.stop(now + rel + 0.04));
          if (v.vibOsc) v.vibOsc.stop(now + rel + 0.04);
        } catch (_) {}
      }
    }

    _spawnSampleVoice(audioBuffer, midiNote, peakGain, rec, st) {
      if (!this.ctx || !audioBuffer) return;
      const now = this.ctx.currentTime;
      const src = this.ctx.createBufferSource();
      src.buffer = audioBuffer;
      const profile = (rec && rec.profile) || {};
      const relTime = clamp(0.24 * (profile.releaseScale || 1), 0.06, 0.9);
      const atkTime = clamp(0.006 * (profile.attackScale || 1), 0.003, 0.25);

      // Gentle pitch bend modulation
      if (this.pitchBendSemis) {
        src.detune.setValueAtTime(this.pitchBendSemis * 100, now);
      }

      const filter = this.ctx.createBiquadFilter();
      filter.type = "lowpass";
      const cutoff = clamp(7200 * (profile.brightness || 1), 1100, 16000);
      filter.frequency.setValueAtTime(cutoff, now);

      const env = this.ctx.createGain();
      env.gain.setValueAtTime(0.0001, now);
      env.gain.linearRampToValueAtTime(peakGain * 1.18, now + atkTime);

      src.connect(filter);
      filter.connect(env);
      env.connect(this.kbdBus);
      src.start(now);

      this.activeVoices.push({
        oscs: [],
        srcNode: src,
        env,
        vibOsc: null,
        vibGain: null,
        baseVib: 0,
        releaseTime: relTime
      });
    }

    // =========================================================================
    // PROCEDURAL 128-GM + KORG PROFILE SYNTHESIZER
    // =========================================================================
    _spawnSynthVoice(patch, midiNote, peakGain, destBus, st, fixedDurationSec, rec, startTimeOverride) {
      if (!this.ctx) return;
      const now = startTimeOverride !== undefined ? Math.max(this.ctx.currentTime, startTimeOverride) : this.ctx.currentTime;
      const freq = midiToFreq(midiNote);
      if (!isFinite(freq) || freq < 22 || freq > 14000) return;

      const prof = (rec && rec.profile) || {};
      const brightScale = prof.brightness || 1.0;
      const extraDetune = prof.detuneCents || 0;
      const atkScale = prof.attackScale || 1.0;
      const relScale = prof.releaseScale || 1.0;

      const env = this.ctx.createGain();
      env.gain.setValueAtTime(0.0001, now);

      const voiceFilter = this.ctx.createBiquadFilter();
      voiceFilter.type = "lowpass";
      voiceFilter.frequency.setValueAtTime(clamp(6800 * brightScale, 600, 14000), now);
      voiceFilter.connect(env);
      const outTarget = destBus || this.kbdBus;
      if (rec && rec.pan !== undefined && rec.pan !== 64 && typeof this.ctx.createStereoPanner === "function") {
        const panner = this.ctx.createStereoPanner();
        panner.pan.setValueAtTime(clamp((rec.pan - 64) / 64, -1, 1), now);
        env.connect(panner);
        panner.connect(outTarget);
      } else {
        env.connect(outTarget);
      }

      const oscs = [];
      let vibOsc = null;
      let vibGain = null;
      let baseVib = (prof.vibrato || 0) * 65;
      let releaseTime = 0.20 * relScale;

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

      const addTransient = (brightFreq, amt) => {
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
        tg.connect(destBus || this.kbdBus);
        src.start(now);
        src.stop(now + 0.03);
      };

      switch (patch) {
        case "piano":
        case "honky_piano":
        case "m1_piano": {
          const det = (patch === "honky_piano" ? 11 : (patch === "m1_piano" ? 4.5 : 1.5)) + extraDetune * 0.2;
          addOsc("triangle", 1, -det, 0.74);
          addOsc("sawtooth", 1, det, patch === "m1_piano" ? 0.42 : 0.25);
          addOsc("sine", 2, 0, 0.22);
          voiceFilter.frequency.setValueAtTime(clamp((patch === "m1_piano" ? 5200 : 3800) * brightScale, 900, 12000), now);
          voiceFilter.frequency.exponentialRampToValueAtTime(1050, now + 0.9);
          addTransient(2600, 0.45);
          env.gain.linearRampToValueAtTime(peakGain, now + 0.006 * atkScale);
          env.gain.exponentialRampToValueAtTime(peakGain * 0.22, now + 1.45);
          releaseTime = 0.22 * relScale;
          break;
        }
        case "epiano": {
          addOsc("sine", 1, 0, 0.85);
          addOsc("triangle", 2, 2 + extraDetune * 0.15, 0.22);
          const tine = addOsc("sine", 6, 0, 0.26);
          tine.g.gain.exponentialRampToValueAtTime(0.01, now + 0.24);
          voiceFilter.frequency.setValueAtTime(4200 * brightScale, now);
          env.gain.linearRampToValueAtTime(peakGain, now + 0.008 * atkScale);
          env.gain.exponentialRampToValueAtTime(peakGain * 0.38, now + 1.2);
          releaseTime = 0.24 * relScale;
          break;
        }
        case "bell": {
          // Metallic / Tubular Bell / Celesta / Glockenspiel / Sleigh Bell inharmonic partials!
          addOsc("sine", 1, 0, 0.75);
          addOsc("sine", 2.0, extraDetune * 0.2, 0.38);
          addOsc("sine", 2.756, 0, 0.24);
          addOsc("sine", 5.404, 0, 0.14);
          voiceFilter.frequency.setValueAtTime(clamp(7600 * brightScale, 2500, 14000), now);
          addTransient(4200, 0.32);
          env.gain.linearRampToValueAtTime(peakGain, now + 0.004);
          env.gain.exponentialRampToValueAtTime(peakGain * 0.08, now + 1.6);
          releaseTime = 0.45 * relScale;
          break;
        }
        case "jazz_organ":
        case "rock_organ":
        case "pipe_organ": {
          const rotaryFast = Boolean(prof.rotary || (st && st.assignableSwitches && st.assignableSwitches[3]));
          addOsc("sine", 0.5, 0, 0.42);
          addOsc("sine", 1, 0, 0.75);
          addOsc(patch === "rock_organ" ? "sawtooth" : "sine", 2, 2, 0.42);
          addOsc("sine", 3, 0, 0.28);
          addOsc("sine", 4, -2, patch === "pipe_organ" ? 0.35 : 0.20);
          if (patch === "jazz_organ") {
            const perc = addOsc("sine", 3, 0, 0.45);
            perc.g.gain.exponentialRampToValueAtTime(0.001, now + 0.11);
          }
          voiceFilter.frequency.setValueAtTime((patch === "rock_organ" ? 3600 : 5400) * brightScale, now);
          baseVib = Math.max(baseVib, rotaryFast ? 18 : 5);
          env.gain.linearRampToValueAtTime(peakGain * 0.85, now + 0.012);
          releaseTime = 0.08;
          break;
        }
        case "nylon_guitar":
        case "steel_guitar":
        case "clean_guitar":
        case "lead_guitar": {
          const isLead = patch === "lead_guitar";
          addOsc(isLead ? "sawtooth" : "triangle", 1, -2, 0.65);
          addOsc("sawtooth", 1, 3 + extraDetune * 0.25, patch === "nylon_guitar" ? 0.28 : 0.48);
          voiceFilter.frequency.setValueAtTime((patch === "nylon_guitar" ? 2900 : 5200) * brightScale, now);
          voiceFilter.frequency.exponentialRampToValueAtTime(patch === "nylon_guitar" ? 850 : 1500, now + 0.38);
          addTransient(3400, 0.35);
          env.gain.linearRampToValueAtTime(peakGain, now + 0.005);
          env.gain.exponentialRampToValueAtTime(peakGain * (isLead ? 0.62 : 0.18), now + 0.85);
          releaseTime = 0.18 * relScale;
          break;
        }
        case "strings":
        case "solo_violin": {
          const d = 8 + extraDetune * 0.3;
          addOsc("sawtooth", 1, -d, 0.42);
          addOsc("sawtooth", 1, 0, 0.48);
          addOsc("sawtooth", 1, d, 0.42);
          voiceFilter.frequency.setValueAtTime(2600 * brightScale, now);
          baseVib = Math.max(baseVib, patch === "solo_violin" ? 14 : 6);
          env.gain.linearRampToValueAtTime(peakGain * 0.86, now + (patch === "solo_violin" ? 0.06 : 0.11) * atkScale);
          releaseTime = 0.36 * relScale;
          break;
        }
        case "brass":
        case "trumpet":
        case "mute_trumpet":
        case "flugelhorn": {
          addOsc("sawtooth", 1, -4, 0.55);
          addOsc("sawtooth", 1, 4, 0.55);
          if (patch === "mute_trumpet") {
            voiceFilter.type = "bandpass";
            voiceFilter.frequency.setValueAtTime(1950, now);
            voiceFilter.Q.value = 3.2;
          } else {
            const topF = (patch === "flugelhorn" ? 1700 : 3800) * brightScale;
            voiceFilter.frequency.setValueAtTime(450, now);
            voiceFilter.frequency.exponentialRampToValueAtTime(topF, now + 0.055);
            voiceFilter.frequency.exponentialRampToValueAtTime(topF * 0.65, now + 0.25);
          }
          baseVib = Math.max(baseVib, 9);
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
            addTransient(4800, 0.22);
            voiceFilter.frequency.setValueAtTime(3600 * brightScale, now);
            baseVib = Math.max(baseVib, 12);
          } else if (patch === "clarinet") {
            addOsc("square", 1, 0, 0.65);
            voiceFilter.frequency.setValueAtTime(1850 * brightScale, now);
            baseVib = Math.max(baseVib, 6);
          } else {
            addOsc("sawtooth", 1, -3, 0.58);
            addOsc("square", 1, 3, 0.32);
            voiceFilter.frequency.setValueAtTime(700, now);
            voiceFilter.frequency.exponentialRampToValueAtTime(2500 * brightScale, now + 0.05);
            const growlOn = (st && st.assignableSwitches && st.assignableSwitches[1]) || this.joystickY < -0.25;
            baseVib = growlOn ? 32 : Math.max(baseVib, 13);
          }
          env.gain.linearRampToValueAtTime(peakGain * 0.88, now + 0.035);
          releaseTime = 0.14;
          break;
        }
        case "accordion":
        case "harmonica": {
          addOsc("sawtooth", 1, 0, 0.48);
          addOsc("square", 1, patch === "accordion" ? 14 : 6, 0.42);
          voiceFilter.frequency.setValueAtTime(2700 * brightScale, now);
          baseVib = Math.max(baseVib, patch === "harmonica" ? 14 : 4);
          env.gain.linearRampToValueAtTime(peakGain * 0.85, now + 0.03);
          releaseTime = 0.12;
          break;
        }
        case "oud": {
          addOsc("sawtooth", 1, -3, 0.62);
          addOsc("triangle", 1, 3, 0.52);
          voiceFilter.frequency.setValueAtTime(3800 * brightScale, now);
          voiceFilter.frequency.exponentialRampToValueAtTime(950, now + 0.32);
          addTransient(2800, 0.5);
          env.gain.linearRampToValueAtTime(peakGain, now + 0.004);
          env.gain.exponentialRampToValueAtTime(peakGain * 0.14, now + 0.65);
          releaseTime = 0.16;
          break;
        }
        case "bass": {
          addOsc("triangle", 1, 0, 0.85);
          addOsc("sawtooth", 1, 2, 0.42);
          voiceFilter.frequency.setValueAtTime(1400 * brightScale, now);
          voiceFilter.frequency.exponentialRampToValueAtTime(380, now + 0.22);
          env.gain.linearRampToValueAtTime(peakGain, now + 0.006);
          env.gain.exponentialRampToValueAtTime(peakGain * 0.45, now + 0.45);
          releaseTime = 0.12;
          break;
        }
        case "synth_lead": {
          addOsc("sawtooth", 1, -6 - extraDetune * 0.3, 0.52);
          addOsc("square", 1, 6 + extraDetune * 0.3, 0.42);
          voiceFilter.frequency.setValueAtTime(4200 * brightScale, now);
          env.gain.linearRampToValueAtTime(peakGain * 0.86, now + 0.015);
          releaseTime = 0.18;
          break;
        }
        default: { // pad & choir
          addOsc("triangle", 1, -8 - extraDetune * 0.3, 0.55);
          addOsc("sawtooth", 1, 8 + extraDetune * 0.3, 0.38);
          addOsc("sine", 2, 0, 0.20);
          voiceFilter.frequency.setValueAtTime(1850 * brightScale, now);
          env.gain.linearRampToValueAtTime(peakGain * 0.78, now + 0.14 * atkScale);
          releaseTime = 0.45 * relScale;
          break;
        }
      }

      if (oscs.length > 0) {
        vibOsc = this.ctx.createOscillator();
        vibGain = this.ctx.createGain();
        vibOsc.frequency.setValueAtTime(5.6, now);
        const initialVib = baseVib + Math.max(0, this.joystickY) * 42;
        vibGain.gain.setValueAtTime(initialVib, now);
        vibOsc.connect(vibGain);
        oscs.forEach((o) => vibGain.connect(o.detune));
        vibOsc.start(now);
      }

      if (fixedDurationSec && fixedDurationSec > 0) {
        const stopAt = now + fixedDurationSec;
        env.gain.setValueAtTime(Math.max(0.0001, peakGain * 0.5), Math.max(now + 0.02, stopAt - 0.04));
        env.gain.exponentialRampToValueAtTime(0.0001, stopAt);
        oscs.forEach((o) => o.stop(stopAt + 0.03));
        if (vibOsc) vibOsc.stop(stopAt + 0.03);
      } else {
        this.activeVoices.push({ oscs, env, vibOsc, vibGain, baseVib, releaseTime });
      }
    }

    // =========================================================================
    // DRUM & PERCUSSION KIT ENGINE (SpessaSynth GS Ch10 + Full GM Procedural)
    // =========================================================================
    _playDrumNote(time, drumMidi, velocity = 0.7, gsDrumPc = 0) {
      if (!this.enabled || !this.ctx) return;
      const playAt = Math.max(this.ctx.currentTime, time);

      if (this.sfSynth && this.sfLoadedBanks.length > 0 && this.activeLibId !== "procedural" && this.activeLibId !== "fluidr3_stream") {
        const delayMs = Math.max(0, (playAt - this.ctx.currentTime) * 1000);
        const vel = clamp(Math.round(velocity * 127), 16, 127);
        const tid = setTimeout(() => {
          this.scheduledSfTimers.delete(tid);
          if (!this.enabled || !this.sfSynth) return;
          this._syncSfChannelProgram(9, { isDrum: true, gsDrumPc: gsDrumPc || 0 });
          try {
            this.sfSynth.noteOn(9, drumMidi, vel);
            setTimeout(() => { try { this.sfSynth && this.sfSynth.noteOff(9, drumMidi); } catch (_) {} }, 150);
          } catch (_) {}
        }, delayMs);
        this.scheduledSfTimers.add(tid);
        return;
      }

      // Expanded Procedural GM/GS Drum & World/Latin Percussion Engine (MIDI 35..87)
      const isBrush = gsDrumPc === 40;
      const is808 = gsDrumPc === 25;
      if (drumMidi === 35 || drumMidi === 36) {
        this._playKick(playAt, velocity, drumMidi === 35 ? 118 : 145, is808 ? 0.42 : 0.24);
      } else if (drumMidi === 37) {
        this._playSnare(playAt, velocity, true, false);
      } else if (drumMidi === 38 || drumMidi === 40) {
        this._playSnare(playAt, velocity, false, isBrush || drumMidi === 40 && isBrush);
      } else if (drumMidi === 39) {
        this._playClap(playAt, velocity);
      } else if (drumMidi === 42 || drumMidi === 44) {
        this._playHat(playAt, false, velocity, isBrush && drumMidi === 42);
      } else if (drumMidi === 46) {
        this._playHat(playAt, true, velocity, false);
      } else if (drumMidi === 49 || drumMidi === 52 || drumMidi === 55 || drumMidi === 57) {
        this._playCrash(playAt, velocity, drumMidi === 55 ? 0.45 : 0.95);
      } else if (drumMidi === 51 || drumMidi === 59) {
        this._playRide(playAt, velocity, false);
      } else if (drumMidi === 53) {
        this._playRide(playAt, velocity, true);
      } else if (drumMidi === 54) {
        this._playTambourine(playAt, velocity);
      } else if (drumMidi === 56) {
        this._playMetallicTwoTone(playAt, 540, 800, 0.13, velocity * 0.65);
      } else if (drumMidi >= 41 && drumMidi <= 50) {
        const tf = 88 + (drumMidi - 41) * 19;
        this._playTom(playAt, tf, velocity, gsDrumPc === 48 ? 0.42 : 0.18);
      } else if (drumMidi === 60 || drumMidi === 61) {
        this._playHandDrum(playAt, drumMidi === 60 ? 410 : 275, 0.09, velocity * 0.72, drumMidi === 60);
      } else if (drumMidi === 62 || drumMidi === 63 || drumMidi === 64) {
        const cf = drumMidi === 62 ? 345 : (drumMidi === 63 ? 255 : 165);
        this._playHandDrum(playAt, cf, drumMidi === 62 ? 0.065 : 0.18, velocity * 0.80, drumMidi === 62);
      } else if (drumMidi === 65 || drumMidi === 66) {
        this._playHandDrum(playAt, drumMidi === 65 ? 360 : 240, 0.16, velocity * 0.78, true);
      } else if (drumMidi === 67 || drumMidi === 68) {
        this._playMetallicTwoTone(playAt, drumMidi === 67 ? 880 : 660, drumMidi === 67 ? 1320 : 990, 0.14, velocity * 0.58);
      } else if (drumMidi === 69 || drumMidi === 70 || drumMidi === 82) {
        this._playShaker(playAt, velocity * 0.45, drumMidi === 69 ? 0.08 : 0.055);
      } else if (drumMidi === 71 || drumMidi === 72) {
        this._playWhistle(playAt, velocity * 0.42, drumMidi === 72 ? 0.28 : 0.12);
      } else if (drumMidi === 73 || drumMidi === 74) {
        this._playGuiro(playAt, velocity * 0.48, drumMidi === 74);
      } else if (drumMidi === 75) {
        this._playWoodClick(playAt, 2480, 0.055, velocity * 0.72);
      } else if (drumMidi === 76 || drumMidi === 77) {
        this._playWoodClick(playAt, drumMidi === 76 ? 1180 : 860, 0.065, velocity * 0.75);
      } else if (drumMidi === 80 || drumMidi === 81) {
        this._playTriangle(playAt, velocity * 0.45, drumMidi === 81 ? 0.42 : 0.08);
      } else if (drumMidi === 83) {
        this._playSleighBells(playAt, velocity * 0.52);
      } else if (drumMidi === 85) {
        this._playWoodClick(playAt, 1920, 0.035, velocity * 0.68);
        this._playWoodClick(playAt + 0.024, 2080, 0.035, velocity * 0.54);
      } else if (drumMidi === 86 || drumMidi === 87) {
        this._playKick(playAt, velocity * 0.85, 96, drumMidi === 87 ? 0.34 : 0.14);
      } else {
        this._playTom(playAt, 240 + (drumMidi % 12) * 32, velocity * 0.65, 0.14);
      }
    }

    _playKick(time, gain = 0.75, startFreq = 140, dur = 0.24) {
      if (!this.ctx) return;
      const o = this.ctx.createOscillator();
      const g = this.ctx.createGain();
      o.type = "sine";
      o.frequency.setValueAtTime(startFreq, time);
      o.frequency.exponentialRampToValueAtTime(42, time + 0.085);
      g.gain.setValueAtTime(gain, time);
      g.gain.exponentialRampToValueAtTime(0.001, time + dur);
      o.connect(g);
      g.connect(this.drumBus);
      o.start(time);
      o.stop(time + dur + 0.02);
    }

    _playSnare(time, gain = 0.55, isRim = false, isBrush = false) {
      if (!this.ctx) return;
      const o = this.ctx.createOscillator();
      const og = this.ctx.createGain();
      o.type = "triangle";
      o.frequency.setValueAtTime(isRim ? 440 : 190, time);
      o.frequency.exponentialRampToValueAtTime(isRim ? 280 : 95, time + 0.055);
      og.gain.setValueAtTime(gain * (isBrush ? 0.25 : 0.50), time);
      og.gain.exponentialRampToValueAtTime(0.001, time + (isRim ? 0.045 : 0.12));
      o.connect(og);
      og.connect(this.drumBus);
      o.start(time);
      o.stop(time + 0.14);

      const n = this.ctx.createBufferSource();
      n.buffer = this.noiseBuffer;
      const hp = this.ctx.createBiquadFilter();
      hp.type = isRim || isBrush ? "bandpass" : "highpass";
      hp.frequency.setValueAtTime(isRim ? 2400 : (isBrush ? 2800 : 1200), time);
      const ng = this.ctx.createGain();
      const nDur = isRim ? 0.038 : (isBrush ? 0.22 : 0.16);
      ng.gain.setValueAtTime(gain * (isRim ? 0.35 : (isBrush ? 0.42 : 0.72)), time);
      ng.gain.exponentialRampToValueAtTime(0.001, time + nDur);
      n.connect(hp);
      hp.connect(ng);
      ng.connect(this.drumBus);
      n.start(time);
      n.stop(time + nDur + 0.02);
    }

    _playClap(time, gain = 0.65) {
      if (!this.ctx) return;
      [0, 0.010, 0.021].forEach((off, idx) => {
        const n = this.ctx.createBufferSource();
        n.buffer = this.noiseBuffer;
        const bp = this.ctx.createBiquadFilter();
        bp.type = "bandpass";
        bp.frequency.setValueAtTime(1350, time + off);
        bp.Q.value = 1.4;
        const g = this.ctx.createGain();
        const dur = idx === 2 ? 0.14 : 0.022;
        g.gain.setValueAtTime(gain * (idx === 2 ? 0.72 : 0.52), time + off);
        g.gain.exponentialRampToValueAtTime(0.001, time + off + dur);
        n.connect(bp);
        bp.connect(g);
        g.connect(this.drumBus);
        n.start(time + off);
        n.stop(time + off + dur + 0.01);
      });
    }

    _playHat(time, isOpen = false, gain = 0.28, isBrushSwirl = false) {
      if (!this.ctx) return;
      const n = this.ctx.createBufferSource();
      n.buffer = this.noiseBuffer;
      const hp = this.ctx.createBiquadFilter();
      hp.type = isBrushSwirl ? "bandpass" : "highpass";
      hp.frequency.setValueAtTime(isBrushSwirl ? 3400 : 6600, time);
      const g = this.ctx.createGain();
      const dur = isOpen ? 0.24 : (isBrushSwirl ? 0.14 : 0.045);
      g.gain.setValueAtTime(gain * (isBrushSwirl ? 0.55 : 0.85), time);
      g.gain.exponentialRampToValueAtTime(0.001, time + dur);
      n.connect(hp);
      hp.connect(g);
      g.connect(this.drumBus);
      n.start(time);
      n.stop(time + dur + 0.02);
    }

    _playRide(time, gain = 0.35, isBell = false) {
      if (!this.ctx) return;
      this._playHat(time, true, gain * 0.45, false);
      const o = this.ctx.createOscillator();
      const g = this.ctx.createGain();
      o.type = "triangle";
      o.frequency.setValueAtTime(isBell ? 2860 : 3950, time);
      const dur = isBell ? 0.32 : 0.26;
      g.gain.setValueAtTime(gain * (isBell ? 0.36 : 0.16), time);
      g.gain.exponentialRampToValueAtTime(0.001, time + dur);
      o.connect(g);
      g.connect(this.drumBus);
      o.start(time);
      o.stop(time + dur + 0.02);
    }

    _playCrash(time, gain = 0.38, dur = 0.95) {
      if (!this.ctx) return;
      const n = this.ctx.createBufferSource();
      n.buffer = this.noiseBuffer;
      const hp = this.ctx.createBiquadFilter();
      hp.type = "highpass";
      hp.frequency.setValueAtTime(4200, time);
      const g = this.ctx.createGain();
      g.gain.setValueAtTime(gain * 0.8, time);
      g.gain.exponentialRampToValueAtTime(0.001, time + dur);
      n.connect(hp);
      hp.connect(g);
      g.connect(this.drumBus);
      n.start(time);
      n.stop(time + dur + 0.03);
    }

    _playTom(time, startFreq, gain = 0.5, dur = 0.18) {
      if (!this.ctx) return;
      const o = this.ctx.createOscillator();
      const g = this.ctx.createGain();
      o.type = "sine";
      o.frequency.setValueAtTime(startFreq, time);
      o.frequency.exponentialRampToValueAtTime(Math.max(46, startFreq * 0.48), time + dur * 0.8);
      g.gain.setValueAtTime(gain, time);
      g.gain.exponentialRampToValueAtTime(0.001, time + dur);
      o.connect(g);
      g.connect(this.drumBus);
      o.start(time);
      o.stop(time + dur + 0.02);
    }

    _playHandDrum(time, freq, dur, gain, brightSlap) {
      if (!this.ctx) return;
      const o = this.ctx.createOscillator();
      const g = this.ctx.createGain();
      o.type = brightSlap ? "triangle" : "sine";
      o.frequency.setValueAtTime(freq * 1.18, time);
      o.frequency.exponentialRampToValueAtTime(freq * 0.78, time + dur);
      g.gain.setValueAtTime(gain, time);
      g.gain.exponentialRampToValueAtTime(0.001, time + dur);
      o.connect(g);
      g.connect(this.drumBus);
      o.start(time);
      o.stop(time + dur + 0.02);
      if (brightSlap) this._playShaker(time, gain * 0.35, 0.025);
    }

    _playMetallicTwoTone(time, f1, f2, dur, gain) {
      if (!this.ctx) return;
      const bp = this.ctx.createBiquadFilter();
      bp.type = "bandpass";
      bp.frequency.setValueAtTime((f1 + f2) * 0.55, time);
      bp.Q.value = 3.2;
      const g = this.ctx.createGain();
      g.gain.setValueAtTime(gain, time);
      g.gain.exponentialRampToValueAtTime(0.001, time + dur);
      bp.connect(g);
      g.connect(this.drumBus);
      [f1, f2].forEach((f) => {
        const o = this.ctx.createOscillator();
        o.type = "square";
        o.frequency.setValueAtTime(f, time);
        o.connect(bp);
        o.start(time);
        o.stop(time + dur + 0.02);
      });
    }

    _playShaker(time, gain, dur) {
      if (!this.ctx) return;
      const n = this.ctx.createBufferSource();
      n.buffer = this.noiseBuffer;
      const bp = this.ctx.createBiquadFilter();
      bp.type = "bandpass";
      bp.frequency.setValueAtTime(7200, time);
      bp.Q.value = 2.0;
      const g = this.ctx.createGain();
      g.gain.setValueAtTime(0.001, time);
      g.gain.linearRampToValueAtTime(gain, time + dur * 0.25);
      g.gain.exponentialRampToValueAtTime(0.001, time + dur);
      n.connect(bp);
      bp.connect(g);
      g.connect(this.drumBus);
      n.start(time);
      n.stop(time + dur + 0.01);
    }

    _playTambourine(time, gain) {
      this._playShaker(time, gain * 0.65, 0.095);
      this._playMetallicTwoTone(time, 5200, 7400, 0.075, gain * 0.22);
    }

    _playGuiro(time, gain, isLong) {
      const strokes = isLong ? [0, 0.025, 0.05, 0.075] : [0, 0.022];
      strokes.forEach((off) => this._playWoodClick(time + off, 1650, 0.022, gain * 0.55));
    }

    _playWoodClick(time, freq, dur, gain) {
      if (!this.ctx) return;
      const o = this.ctx.createOscillator();
      const g = this.ctx.createGain();
      o.type = "sine";
      o.frequency.setValueAtTime(freq, time);
      g.gain.setValueAtTime(gain, time);
      g.gain.exponentialRampToValueAtTime(0.001, time + dur);
      o.connect(g);
      g.connect(this.drumBus);
      o.start(time);
      o.stop(time + dur + 0.01);
    }

    _playTriangle(time, gain, dur) {
      if (!this.ctx) return;
      [3850, 7280].forEach((f, idx) => {
        const o = this.ctx.createOscillator();
        const g = this.ctx.createGain();
        o.type = "sine";
        o.frequency.setValueAtTime(f, time);
        g.gain.setValueAtTime(gain * (idx === 0 ? 0.6 : 0.35), time);
        g.gain.exponentialRampToValueAtTime(0.001, time + dur);
        o.connect(g);
        g.connect(this.drumBus);
        o.start(time);
        o.stop(time + dur + 0.02);
      });
    }

    _playSleighBells(time, gain) {
      this._playShaker(time, gain * 0.55, 0.14);
      [2950, 4180, 5620].forEach((f, idx) => {
        this._playWoodClick(time + idx * 0.012, f, 0.13, gain * 0.24);
      });
    }

    _playWhistle(time, gain, dur) {
      if (!this.ctx) return;
      const o = this.ctx.createOscillator();
      const g = this.ctx.createGain();
      o.type = "sine";
      o.frequency.setValueAtTime(2680, time);
      o.frequency.linearRampToValueAtTime(2820, time + dur * 0.5);
      g.gain.setValueAtTime(0.001, time);
      g.gain.linearRampToValueAtTime(gain, time + 0.015);
      g.gain.exponentialRampToValueAtTime(0.001, time + dur);
      o.connect(g);
      g.connect(this.drumBus);
      o.start(time);
      o.stop(time + dur + 0.02);
    }

    // =========================================================================
    // 8-TRACK BAND & PAD NOTE SCHEDULER (SpessaSynth + FluidR3 + Full Synth)
    // =========================================================================
    _scheduleBandNote(time, channelIndex, trackOrProg, midiNote, durSec, peakGain, st) {
      if (!this.enabled || !this.ctx) return;
      const midi = clamp(Math.round(midiNote), 24, 108);
      const playAt = Math.max(this.ctx.currentTime, time);
      const isTrackObj = trackOrProg && typeof trackOrProg === "object";
      const gmProg = isTrackObj
        ? (trackOrProg.gmProgram !== undefined ? trackOrProg.gmProgram : (trackOrProg.pc || 0))
        : (trackOrProg || 0);
      const soundRec = isTrackObj
        ? (this.resolveSoundRecord(trackOrProg.sound) || trackOrProg)
        : { name: FLUIDR3_SLUGS[gmProg] || "piano", isDrum: false, cc00: 0, cc32: 0, pc: gmProg, gmProgram: gmProg };
      const panVal = isTrackObj && trackOrProg.pan !== undefined ? trackOrProg.pan : 64;

      // 1. SpessaSynth full .sf2/.sf3 bank active -> route with exact CC0/CC32/PC & Pan
      if (this.sfSynth && this.sfLoadedBanks.length > 0 && this.activeLibId !== "procedural" && this.activeLibId !== "fluidr3_stream") {
        const delayMs = Math.max(0, (playAt - this.ctx.currentTime) * 1000);
        const tid = setTimeout(() => {
          this.scheduledSfTimers.delete(tid);
          if (!this.enabled || !this.sfSynth) return;
          this._syncSfChannelProgram(channelIndex, soundRec, panVal);
          const vel = clamp(Math.round(peakGain * 225), 16, 124);
          try {
            this.sfSynth.noteOn(channelIndex, midi, vel);
            const offTid = setTimeout(() => {
              this.scheduledSfTimers.delete(offTid);
              try { this.sfSynth && this.sfSynth.noteOff(channelIndex, midi); } catch (_) {}
            }, Math.max(55, durSec * 1000));
            this.scheduledSfTimers.add(offTid);
          } catch (_) {}
        }, delayMs);
        this.scheduledSfTimers.add(tid);
        return;
      }

      // 2. FluidR3 Streaming: play cached buffer if ready; background-warm on demand & use rich synth until cached!
      if (this.activeLibId === "fluidr3_stream" && !soundRec.isDrum) {
        const cacheKey = `${gmProg}:${midiToFlatName(midi)}`;
        const cachedBuf = this.fluidAudioCache.get(cacheKey);
        if (cachedBuf) {
          const src = this.ctx.createBufferSource();
          src.buffer = cachedBuf;
          const g = this.ctx.createGain();
          g.gain.setValueAtTime(clamp(peakGain * 1.35, 0.02, 0.9), playAt);
          const stopAt = playAt + Math.max(0.06, durSec);
          g.gain.setValueAtTime(clamp(peakGain * 1.1, 0.01, 0.8), Math.max(playAt + 0.02, stopAt - 0.04));
          g.gain.exponentialRampToValueAtTime(0.0001, stopAt + 0.05);
          src.connect(g);
          if (panVal !== 64 && typeof this.ctx.createStereoPanner === "function") {
            const p = this.ctx.createStereoPanner();
            p.pan.setValueAtTime(clamp((panVal - 64) / 64, -1, 1), playAt);
            g.connect(p);
            p.connect(this.arrangerBus);
          } else {
            g.connect(this.arrangerBus);
          }
          src.start(playAt);
          src.stop(stopAt + 0.07);
          return;
        }
        if (!this.failedPrograms.has(gmProg)) {
          this._decodeFluidNoteBuffer(gmProg, midi, performance.now()).catch(() => {});
        }
      }

      // 3. Rich Patch-Classified Procedural Band Instrument Synthesis (zero latency)
      const patch = channelIndex === 5 ? "bass" : classifyPatch(soundRec.name);
      const recWithPan = panVal !== 64 ? { ...soundRec, pan: panVal } : soundRec;
      this._spawnSynthVoice(patch, midi, peakGain, this.arrangerBus, st, Math.max(0.05, durSec), recWithPan, playAt);
    }

    async triggerPadHit(padIndex, padObj, st) {
      if (!this.enabled) return;
      await this.resume();
      const rec = this.resolvePadRecord(padObj);
      const now = this.ctx.currentTime;
      const chordObj = parseChordToMidi((st && st.recognizedChord) || "C") || parseChordToMidi("C");
      const tr = (st && st.masterTranspose) || 0;

      if (rec.bankType === "HIT" || rec.type === "OneShot") {
        if (rec.drumNote) {
          this._playDrumNote(now, rec.drumNote, 0.85, 0);
        } else {
          const gmProg = rec.gmProgram || 55;
          chordObj.compNotes.slice(0, 3).forEach((m, idx) => {
            this._scheduleBandNote(now + idx * 0.015, 4, gmProg, m + tr + 12, 0.42, 0.24, st);
          });
        }
        return;
      }

      // SEQ / Loop multi-step musical phrase synced to style tempo!
      const tempo = (st && st.tempo) || 110;
      const stepDur = (60 / tempo) / 2;
      const prog = rec.gmProgram || 0;
      const notes = chordObj.compNotes.map((n) => n + tr + 12);
      for (let i = 0; i < 8; i++) {
        const at = now + i * stepDur;
        if (rec.phrase === "drum_groove" || rec.phrase === "perc_latin") {
          const dm = i % 2 === 0 ? (rec.phrase === "perc_latin" ? 63 : 42) : 64;
          this._playDrumNote(at, dm, i % 4 === 0 ? 0.72 : 0.48, 0);
        } else if (rec.phrase === "bass_pulse") {
          const b = i % 2 === 0 ? chordObj.bassRoot + tr : chordObj.fifthMidi + tr;
          this._scheduleBandNote(at, 4, prog, b, stepDur * 0.85, 0.34, st);
        } else {
          const m = notes[i % notes.length] + (i === 7 ? 12 : 0);
          this._scheduleBandNote(at, 4, prog, m, stepDur * 0.9, 0.22, st);
        }
      }
    }

    // =========================================================================
    // 379-STYLE MULTI-BAR 8-TRACK NTT MIDI ARRANGER ENGINE
    // =========================================================================
    resetGroovePosition() {
      this.subStepIndex = 0;
      this.barSubStepsSeen = 0;
      if (this.ctx) {
        this.nextSubStepTime = this.ctx.currentTime + 0.04;
      }
    }

    startEngineLoop(getStateFn, onBeatCallback) {
      this.getStateFn = getStateFn;
      this.onBeatCallback = typeof onBeatCallback === "function" ? onBeatCallback : null;
      if (this.loopTimerId) clearInterval(this.loopTimerId);
      this.loopTimerId = setInterval(() => this._schedulerTick(), 25);
    }

    stopEngineLoop() {
      if (this.loopTimerId) {
        clearInterval(this.loopTimerId);
        this.loopTimerId = null;
      }
      this.scheduledSfTimers.forEach((tid) => clearTimeout(tid));
      this.scheduledSfTimers.clear();
    }

    _getStyleStepCache(styleObj) {
      if (!styleObj || !styleObj.midi) return null;
      if (styleObj._stepCache) return styleObj._stepCache;
      const indexList = (arr) => {
        const map = new Map();
        (arr || []).forEach((ev) => {
          const s = ev[0];
          let bucket = map.get(s);
          if (!bucket) {
            bucket = [];
            map.set(s, bucket);
          }
          bucket.push(ev);
        });
        return map;
      };
      const m = styleObj.midi;
      styleObj._stepCache = {
        events: indexList(m.events),
        intro: indexList(m.intro),
        countIn: indexList(m.countIn),
        fill: indexList(m.fill),
        brk: indexList(m.brk),
        ending: indexList(m.ending),
      };
      return styleObj._stepCache;
    }

    _schedulerTick() {
      if (!this.ctx || !this.getStateFn) return;
      let st = this.getStateFn();
      const shouldRun = Boolean(st.arrangerRunning || (st.metronomeOn && !st.arrangerRunning));

      if (!shouldRun) {
        this.lastArrangerRunning = false;
        this.nextSubStepTime = this.ctx.currentTime + 0.04;
        return;
      }

      if (!this.lastArrangerRunning && shouldRun) {
        this.lastArrangerRunning = true;
        this.subStepIndex = 0;
        this.barSubStepsSeen = 0;
        this.nextSubStepTime = this.ctx.currentTime + 0.03;
      }

      const stylesList = (window.PA700_DATA && window.PA700_DATA.styles) || [];
      const currentStyle = st.currentStyleObj || stylesList[st.currentStyleIdx || 0] || { beatsPerBar: 4, subPerBeat: 4 };
      const tempo = clamp(st.tempo || currentStyle.tempo || 110, 40, 240);
      const beatsPerBar = currentStyle.beatsPerBar || 4;
      const subPerBeat = currentStyle.subPerBeat || 4;
      const beatDurScale = currentStyle.beatDurScale || 1.0;
      const subStepDur = ((60 / tempo) * beatDurScale) / subPerBeat;
      const totalBarSteps = beatsPerBar * subPerBeat;
      const lookahead = 0.14;

      while (this.nextSubStepTime < this.ctx.currentTime + lookahead) {
        const stepInBar = this.subStepIndex % totalBarSteps;
        const beatInBar = Math.floor(stepInBar / subPerBeat);
        const subInBeat = stepInBar % subPerBeat;

        if (subInBeat === 0) {
          const isBarWrap = stepInBar === 0 && this.barSubStepsSeen > 0;
          if (typeof st.onAudioBeatAdvance === "function") {
            st.onAudioBeatAdvance(beatInBar + 1, isBarWrap);
          }
          if (this.onBeatCallback) {
            this.onBeatCallback(beatInBar + 1, isBarWrap);
          }
          st = this.getStateFn();
        }
        this.barSubStepsSeen += 1;

        if (st.metronomeOn && subInBeat === 0) {
          this._playDrumNote(this.nextSubStepTime, beatInBar === 0 ? 76 : 77, beatInBar === 0 ? 0.55 : 0.36, 0);
        }

        if (st.arrangerRunning && this.enabled) {
          let swingOffset = 0;
          const sw = currentStyle.swing || 0;
          if (sw > 0) {
            if (currentStyle.swing8 && subPerBeat === 4) {
              if (subInBeat === 2) swingOffset = sw * (2 * subStepDur) * 0.55;
              else if (subInBeat === 3) swingOffset = sw * subStepDur * 0.35;
            } else if (!currentStyle.swing8 && stepInBar % 2 === 1) {
              swingOffset = sw * subStepDur;
            }
          }
          this._scheduleArrangerSubStep(
            this.nextSubStepTime + swingOffset, stepInBar, subPerBeat, beatsPerBar, subStepDur, currentStyle, st
          );
        }

        this.nextSubStepTime += subStepDur;
        this.subStepIndex += 1;
      }
    }

    _scheduleArrangerSubStep(t, stepInBar, subPerBeat, beatsPerBar, subDur, styleObj, st) {
      const barSteps = beatsPerBar * subPerBeat;
      const cache = this._getStyleStepCache(styleObj);
      if (!cache) return;

      const tracks = styleObj.styleTracks || [];
      const mutes = st.styleTrackMutes || [];
      const gsDrumPc = styleObj.gsDrumPc || 0;
      const tr = st.masterTranspose || 0;
      const fadeScale = clamp((st.fadeLevel !== undefined ? st.fadeLevel : 100) / 100, 0, 1.05);
      if (fadeScale <= 0.005) return;

      // Determine active section event table, step offset, variation/section bitmask, and cadence transpose!
      const sec = st.activeSection || "var";
      const curBar = Math.max(1, st.currentBar || 1);
      const twoBarStep = ((curBar - 1) % 2) * barSteps + stepInBar;
      let evList = null;
      let reqMask = 0;
      let harmShift = 0;

      if (sec === "intro") {
        const iNum = st.activeIntro || 2;
        if (iNum === 3) {
          evList = cache.countIn.get(stepInBar);
        } else {
          evList = cache.intro.get(twoBarStep);
          reqMask = 1 << (iNum - 1);
          if (iNum === 1 && styleObj.midi.intro1Harm) {
            const qIdx = Math.min(3, Math.floor((twoBarStep / (barSteps * 2)) * 4));
            harmShift = styleObj.midi.intro1Harm[qIdx] || 0;
          }
        }
      } else if (sec === "break") {
        evList = cache.brk.get(stepInBar);
      } else if (sec === "fill") {
        evList = cache.fill.get(stepInBar);
        reqMask = 1 << (clamp(st.activeFill || st.variation || 2, 1, 4) - 1);
      } else if (sec === "ending") {
        const eNum = clamp(st.activeEnding || 2, 1, 3);
        evList = cache.ending.get(twoBarStep);
        reqMask = 1 << (eNum - 1);
        if (eNum === 1 && styleObj.midi.end1Harm) {
          const qIdx = Math.min(3, Math.floor((twoBarStep / (barSteps * 2)) * 4));
          harmShift = styleObj.midi.end1Harm[qIdx] || 0;
        }
      } else {
        const vNum = clamp(st.variation || 1, 1, 4);
        evList = cache.events.get(twoBarStep);
        reqMask = 1 << (vNum - 1);
      }

      if (!evList || !evList.length) return;

      // Resolve recognized chord (Intro 1 & Ending 1 can sound on default C if no chord held yet)
      const chordName = st.recognizedChord || ((sec === "intro" && st.activeIntro === 1) ? "C" : null);
      const chordObj = parseChordToMidi(chordName, harmShift);
      const pitchedAllowed = st.accompOn && !st.manualBass && Boolean(chordObj);

      // Dedicated MIDI channels for the 8 Pa700 Style Accompaniment Tracks
      const TRACK_MIDI_CHANNELS = [9, 9, 5, 6, 7, 10, 11, 12];

      for (let i = 0; i < evList.length; i++) {
        const ev = evList[i];
        const trkIdx = ev[1];
        if (mutes[trkIdx]) continue;
        if (reqMask !== 0 && ev.length >= 6 && (ev[5] & reqMask) === 0) continue;

        const code = ev[2];
        const durSteps = ev[3];
        const rawVel = ev[4];
        const trkDesc = tracks[trkIdx] || {};
        const trkGain = trkDesc.gain !== undefined ? trkDesc.gain : 0.82;

        if (trkIdx === 0 || trkIdx === 1) {
          const drumVel = clamp((rawVel / 127) * trkGain * fadeScale, 0.08, 1.0);
          this._playDrumNote(t, code, drumVel, gsDrumPc);
        } else {
          if (!pitchedAllowed) continue;
          const isBass = trkIdx === 2;
          const ch = TRACK_MIDI_CHANNELS[trkIdx] || 6;
          const notes = resolveStylePitchEvents(chordObj, code, isBass, trkDesc.oct || 0, tr);
          const basePeak = (rawVel / 127) * trkGain * (isBass ? 0.44 : 0.24) * fadeScale;

          for (let nIdx = 0; nIdx < notes.length; nIdx++) {
            const np = notes[nIdx];
            const noteDur = Math.max(0.045, durSteps * subDur * np.durScale * 0.92);
            const noteGain = clamp(basePeak * np.velScale, 0.02, 0.52);
            this._scheduleBandNote(t + np.delaySec, ch, trkDesc, np.midi, noteDur, noteGain, st);
          }
        }
      }
    }
  }

  window.PA700_SOUND_LIBRARIES = SOUND_LIBRARIES;
  window.pa700Audio = new Pa700AudioEngine();
  window.classifyPa700Patch = classifyPatch;
})(window);
