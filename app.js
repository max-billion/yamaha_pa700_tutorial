// Korg Pa700 Professional Arranger — Complete Hardware Panel, TouchView OS v1.5 & Arranger Engine

(function () {
  "use strict";

  const DATA = window.PA700_DATA;
  const NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];

  function midiToName(midi) {
    const pitch = ((midi % 12) + 12) % 12;
    const oct = Math.floor(midi / 12) - 1;
    return `${NOTE_NAMES[pitch]}${oct}`;
  }

  function clone(obj) {
    return JSON.parse(JSON.stringify(obj));
  }

  function findStyleIndexById(id) {
    if (!id || !DATA.styles) return 0;
    const idx = DATA.styles.findIndex(s => s.id === id);
    return idx >= 0 ? idx : 0;
  }

  function getMySettingTracks() {
    const ms = DATA.mySetting || {};
    const src = ms.tracks || ms.kbdSet || {};
    const defTrack = (key, fallbackName, vol, isLow) => {
      const t = src[key] || { sound: fallbackName, muted: false, octave: 0 };
      return {
        sound: t.sound || fallbackName,
        muted: Boolean(t.muted),
        octave: t.octave || 0,
        volume: t.volume !== undefined ? t.volume : vol,
        ...(isLow ? { backing: true } : {})
      };
    };
    return {
      up1: defTrack("up1", "Concert Grand", 115, false),
      up2: defTrack("up2", "Real Strings 1", 88, false),
      up3: defTrack("up3", "Warm Pad GM", 72, false),
      low: defTrack("low", "Warm Strings", 84, true)
    };
  }

  function songDisplayTitle(songObj) {
    if (!songObj) return "---";
    return songObj.title || songObj.name || songObj.id || "---";
  }

  function resolveSoundRecord(soundName) {
    if (window.pa700Audio && typeof window.pa700Audio.resolveSoundRecord === "function") {
      return window.pa700Audio.resolveSoundRecord(soundName);
    }
    const low = String(soundName || "").toLowerCase();
    return (DATA.sounds || []).find(s => s.name.toLowerCase() === low) || null;
  }

  function getSoundBankItems(typeName, groupName) {
    const groups = (DATA.soundGroupsByType && DATA.soundGroupsByType[typeName]) || {};
    const ids = groups[groupName] || [];
    if (!window._pa700SoundById) {
      window._pa700SoundById = new Map((DATA.sounds || []).map(s => [s.id, s]));
    }
    return ids.map(id => window._pa700SoundById.get(id)).filter(Boolean);
  }

  function getPadBankItems(groupName) {
    const grp = (DATA.padGroups || []).find(g => g.name === groupName);
    if (!grp) return [];
    if (!window._pa700PadById) {
      window._pa700PadById = new Map((DATA.pads || []).map(p => [p.id, p]));
    }
    return grp.padIds.map(id => window._pa700PadById.get(id)).filter(Boolean);
  }

  // =========================================================================
  // INSTRUMENT STATE (Matches Pa700 OS v1.5 Startup State)
  // =========================================================================
  const state = {
    powerOn: true,
    mode: "style", // 'style' | 'song' | 'seq' | 'sound'
    overlayWindow: null, // null | 'style_select' | 'kbd_lib_select' | 'sound_select' | 'pad_select' | 'songbook' | 'global' | 'media' | 'menu' | 'lyrics' | 'marker' | 'score' | 'search' | 'metronome' | 'demo'
    splitDialogOpen: false,
    mainBottomTab: "kbd_set", // 'kbd_set' | 'volume' | 'pad' | 'split' | 'sub_scale' | 'kaoss' | 'mic'
    volumeTrackView: "grouped", // 'grouped' | 'style_tracks' (toggled by TRACK SELECT)
    styleTrackMutes: [false, false, false, false, false, false, false, false], // Drum, Perc, Bass, Acc1..Acc5
    focusedParam: "tempo", // 'tempo' | 'split' | 'style' | 'kbdset' | 'sound'
    selectedTrackKey: "up1", // 'up1' | 'up2' | 'up3' | 'low'

    // TouchView Browser State (379 Styles, 298 Kbd Sets, 1,845 Sounds, 415 Pads)
    styleBrowseCat: "Ballad",
    styleBrowsePage: 0,
    kbdBrowseCat: "piano",
    kbdBrowsePage: 0,
    soundBrowseType: "Factory",
    soundBrowseGroup: "Piano",
    soundBrowsePage: 0,
    padBrowseBank: "HIT",
    padBrowseGroup: "HIT - Drum",
    padBrowsePage: 0,
    padSelectSlot: 0,
    customStylePads: {},
    displayHold: true,
    searchQuery: "",
    searchScope: "all",
    audioSfStatus: null,

    // Shift & Modifiers
    shiftLatched: false,
    displayBrightness: 85,

    // Knobs & Left-Cheek Controllers
    knobs: {
      master_volume: 0.82,
      balance: 0.50,
      assign_knob_1: 0.50,
      assign_knob_2: 0.35
    },
    dialAngle: 0,
    assignableSwitches: { 1: false, 2: false, 3: false },
    joystick: { x: 0, y: 0 },

    // Style & Arranger State
    currentStyleIdx: findStyleIndexById("brush_ballad"), // Brush Ballad (default in manual p. 23)
    tempo: 73,
    tempoLock: false,
    metronomeOn: false,
    arrangerRunning: false,
    currentBar: 1,
    currentBeat: 1,

    activeVariation: 1, // 1..4
    bookedVariation: null, // 1..4 while waiting for bar/fill/intro
    activeSection: "var", // 'intro' | 'var' | 'fill' | 'break' | 'ending'
    activeIntro: null, // 1..3 when playing or booked while stopped
    activeFill: null, // 1..4
    activeEnding: null, // 1..3
    loopSection: false,

    autoFill: true,
    synchroStart: false,
    synchroStop: false,
    accompOn: true,
    memoryOn: true,
    manualBass: false,
    chordSeqState: "off", // 'off' | 'rec' | 'play'
    chordSeqProg: ["C Maj", "G Maj", "A min", "F Maj"],
    fadeState: null, // null | 'in' | 'out'
    fadeLevel: 100,
    mp3Recording: false,

    // Style to Kbd Set: 'off' | 'on' (solid) | 'blink' (Variation links to Kbd Set 1-4)
    styleToKbdMode: "off",
    activeStyleKbdSlot: null, // 0..3 when one of KEYBOARD SET 1-4 is active

    // Pads 1-4 running flags
    padsActive: [false, false, false, false],

    // Keyboard & Voice Setup
    splitOn: true,
    globalSplitPoint: 60, // C4 (MIDI 60)
    localSplitPoint: null,
    useGlobalSplit: true,
    bassInversion: false,
    ensembleOn: false,
    ensembleType: "Duet",
    upperOctave: 0, // -2..+2
    masterTranspose: 0, // -12..+12

    kbdSetName: (DATA.mySetting && DATA.mySetting.kbdSet && DATA.mySetting.kbdSet.name) || "My Setting",
    kbdSetSource: "Kbd Set Library",
    activeLibCategory: "piano",
    activeLibIndex: 0,
    setListMode: false, // SET LIST button LED: false = Kbd Set Library, true = SongBook Set List 1-9
    activeSetListSlot: 1,
    tracks: getMySettingTracks(),

    // Oriental Quarter-Tone Sub-Scale (pitch classes 0..11 lowered by -50 cents)
    subScaleNotes: [], // array of 0..11 pitch classes with -50c
    activeSubScalePreset: null, // 1..4

    // Song Player State
    currentSongIdx: 0,
    playerRunning: false,
    playerBar: 1,

    // Chord & Keyboard Mouse State
    recognizedChord: null, // e.g. "G Maj"
    mouseChordMode: "major", // 'major' | 'minor' | 'dom7' | 'single'
    latchKeys: false,
    pressedMidiNotes: [],
    clickedRootMidi: null,
    tapTimestamps: [],

    // Guided Drills State
    drillsOpen: false,
    drillIdx: 0,
    drillStepIdx: 0
  };

  function getEffectiveSplit() {
    return (!state.useGlobalSplit && state.localSplitPoint !== null)
      ? state.localSplitPoint
      : state.globalSplitPoint;
  }

  function getCurrentStyle() {
    return DATA.styles[state.currentStyleIdx] || DATA.styles[0];
  }

  function getStylePads(st) {
    const s = st || getCurrentStyle();
    return state.customStylePads[s.id] || s.pads;
  }

  function buildAudioState() {
    return {
      ...state,
      splitEnabled: state.splitOn,
      splitPoint: getEffectiveSplit(),
      masterVol: Math.round((state.knobs.master_volume !== undefined ? state.knobs.master_volume : 0.82) * 100),
      balance: Math.round((state.knobs.balance !== undefined ? state.knobs.balance : 0.50) * 100),
      variation: state.activeVariation,
      currentStyleObj: getCurrentStyle()
    };
  }

  function syncBrowserToStyle(idx) {
    const st = DATA.styles[idx] || getCurrentStyle();
    state.styleBrowseCat = st.category;
    const ids = (DATA.styleIdsByCategory && DATA.styleIdsByCategory[st.category]) || [];
    const pos = ids.indexOf(st.id);
    state.styleBrowsePage = pos >= 0 ? Math.floor(pos / 8) : 0;
  }

  function syncBrowserToKbdSet(catId, idx) {
    state.kbdBrowseCat = catId || state.activeLibCategory || "piano";
    state.kbdBrowsePage = idx >= 0 ? Math.floor(idx / 8) : 0;
  }

  function syncBrowserToSound(soundName) {
    const rec = resolveSoundRecord(soundName);
    if (!rec) return;
    state.soundBrowseType = rec.type || "Factory";
    state.soundBrowseGroup = rec.group || "Piano";
    const list = getSoundBankItems(state.soundBrowseType, state.soundBrowseGroup);
    const pos = list.findIndex(s => s.id === rec.id || s.name === rec.name);
    state.soundBrowsePage = pos >= 0 ? Math.floor(pos / 8) : 0;
  }

  function syncBrowserToPad(padObj) {
    if (!padObj || !padObj.group) return;
    const grp = (DATA.padGroups || []).find(g => g.name === padObj.group);
    if (!grp) return;
    state.padBrowseBank = grp.bankType;
    state.padBrowseGroup = grp.name;
    const items = getPadBankItems(grp.name);
    const pos = items.findIndex(p => p.id === padObj.id || p.name === padObj.name);
    state.padBrowsePage = pos >= 0 ? Math.floor(pos / 8) : 0;
  }

  syncBrowserToStyle(state.currentStyleIdx);
  syncBrowserToSound(state.tracks.up1.sound);

  // =========================================================================
  // LOGGING & LIVE READOUT UPDATER
  // =========================================================================
  const logEntries = [];

  function logAction(msg) {
    const now = new Date();
    const ts = now.toTimeString().slice(0, 8);
    logEntries.unshift({ ts, msg });
    if (logEntries.length > 40) logEntries.pop();
    renderEventLog();
  }

  function renderEventLog() {
    const el = document.getElementById("eventLogList");
    if (!el) return;
    el.innerHTML = logEntries
      .map(item => `<div class="event-log-item"><span class="ts">[${item.ts}]</span>${escapeHtml(item.msg)}</div>`)
      .join("");
  }

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  // =========================================================================
  // HARDWARE BUTTON & KNOB SPECIFICATION (EXACT FACEPLATE COORDINATES)
  // =========================================================================
  const BUTTON_DEFS = [
    // Upper-Left Mode + System Row (y: 43.2%)
    { id: "mode_style", x: 14.2, y: 43.2, shape: "rect-black", led: true, top: "STYLE\nPLAY" },
    { id: "mode_song", x: 17.3, y: 43.2, shape: "rect-black", led: true, top: "SONG\nPLAY" },
    { id: "mode_seq", x: 20.4, y: 43.2, shape: "rect-black", led: true, top: "SEQUENCER" },
    { id: "mode_sound", x: 23.5, y: 43.2, shape: "rect-black", led: true, top: "SOUND" },
    { id: "global", x: 26.9, y: 43.2, shape: "rect-black", led: false, top: "⚙\nGLOBAL" },
    { id: "media", x: 30.0, y: 43.2, shape: "rect-black", led: false, top: "💾\nMEDIA" },

    // Upper-Left Player Row (y: 59.0%)
    { id: "player_select", x: 14.2, y: 59.0, shape: "round-black", led: false, top: "SELECT" },
    { id: "player_rew", x: 17.5, y: 59.0, shape: "rect-black", led: false, top: "◄◄" },
    { id: "player_ff", x: 20.8, y: 59.0, shape: "rect-black", led: false, top: "►►" },
    { id: "player_home", x: 24.1, y: 59.0, shape: "rect-black", led: false, top: "|◄" },
    { id: "player_play", x: 27.4, y: 59.0, shape: "rect-black", led: true, top: "►/■" },

    // Upper-Right Display Navigation & Power
    { id: "lyrics", x: 70.0, y: 43.2, shape: "square-black", led: false, top: "LYRICS" },
    { id: "marker", x: 73.1, y: 43.2, shape: "square-black", led: false, top: "MARKER" },
    { id: "score", x: 76.2, y: 43.2, shape: "square-black", led: false, top: "SCORE" },
    { id: "exit", x: 70.0, y: 59.0, shape: "rect-black", led: false, top: "EXIT", whiteBox: true },
    { id: "menu", x: 76.2, y: 59.0, shape: "rect-black", led: false, top: "MENU", whiteBox: true },
    { id: "power", x: 95.5, y: 59.0, shape: "rect-black", led: true, top: "⏻", whiteBox: true },

    // Row 3 — Continuous Strip Across Panel (y: 74.8%)
    { id: "chord_seq", x: 2.5, y: 74.8, shape: "rect-black", led: true, top: "CHORD\nSEQUENCER", whiteBox: true },
    { id: "accomp", x: 5.6, y: 74.8, shape: "rect-black", led: true, top: "ACCOMP." },
    { id: "memory", x: 8.7, y: 74.8, shape: "rect-black", led: true, top: "MEMORY" },
    { id: "manual_bass", x: 11.8, y: 74.8, shape: "rect-black", led: true, top: "MANUAL\nBASS" },
    { id: "pad_1", x: 15.4, y: 74.8, shape: "rect-black", led: false, top: "1" },
    { id: "pad_2", x: 18.4, y: 74.8, shape: "rect-black", led: false, top: "2" },
    { id: "pad_3", x: 21.4, y: 74.8, shape: "rect-black", led: false, top: "3" },
    { id: "pad_4", x: 24.4, y: 74.8, shape: "rect-black", led: false, top: "4" },
    { id: "pad_stop", x: 27.3, y: 74.8, shape: "round-black", led: false, top: "STOP" },
    { id: "style_to_kbd", x: 30.4, y: 74.8, shape: "round-black", led: true, top: "STYLE TO\nKBD SET" },
    { id: "style_select", x: 33.5, y: 74.8, shape: "rect-black", led: false, top: "STYLE\nSELECT" },
    { id: "mp3_rec", x: 36.8, y: 74.8, shape: "square-black", led: true, top: "mp3 rec\nRECORD" },
    { id: "track_select", x: 39.9, y: 74.8, shape: "square-black", led: false, top: "↺TRACK↻\nSELECT" },
    { id: "kbd_set_1", x: 43.8, y: 74.8, shape: "rect-black", led: false, top: "1" },
    { id: "kbd_set_2", x: 47.1, y: 74.8, shape: "rect-black", led: false, top: "2" },
    { id: "kbd_set_3", x: 50.4, y: 74.8, shape: "rect-black", led: false, top: "3" },
    { id: "kbd_set_4", x: 53.7, y: 74.8, shape: "rect-black", led: false, top: "4" },
    { id: "search", x: 57.8, y: 74.8, shape: "square-black", led: false, top: "🔍\nSEARCH" },
    { id: "shift", x: 60.9, y: 74.8, shape: "square-black", led: false, top: "SHIFT" },
    { id: "tempo_minus", x: 65.2, y: 74.8, shape: "square-black", led: false, top: "−" },
    { id: "tempo_plus", x: 68.2, y: 74.8, shape: "square-black", led: false, top: "+" },
    { id: "tempo_lock", x: 71.2, y: 74.8, shape: "square-black", led: true, top: "🔒" },
    { id: "metronome", x: 74.2, y: 74.8, shape: "square-black", led: true, top: "◬" },
    { id: "split", x: 78.4, y: 74.8, shape: "square-black", led: true, top: "SPLIT", holdable: true },
    { id: "ensemble", x: 81.5, y: 74.8, shape: "square-black", led: true, top: "ENSEMBLE" },
    { id: "octave_minus", x: 85.7, y: 74.8, shape: "square-black", led: false, top: "−" },
    { id: "octave_plus", x: 88.7, y: 74.8, shape: "square-black", led: false, top: "+" },
    { id: "transpose_flat", x: 92.9, y: 74.8, shape: "square-black", led: false, top: "♭" },
    { id: "transpose_sharp", x: 95.9, y: 74.8, shape: "square-black", led: false, top: "♯" },

    // Row 4 — Bottom Performance Strip (y: 90.6%)
    { id: "intro_1", x: 2.6, y: 90.6, shape: "tall-black", led: true, top: "1" },
    { id: "intro_2", x: 5.8, y: 90.6, shape: "tall-black", led: true, top: "2" },
    { id: "intro_3", x: 9.0, y: 90.6, shape: "tall-black", led: true, top: "3/COUNT IN" },
    { id: "var_1", x: 13.0, y: 90.6, shape: "tall-black", led: true, top: "1" },
    { id: "var_2", x: 16.2, y: 90.6, shape: "tall-black", led: true, top: "2" },
    { id: "var_3", x: 19.4, y: 90.6, shape: "tall-black", led: true, top: "3" },
    { id: "var_4", x: 22.6, y: 90.6, shape: "tall-black", led: true, top: "4" },
    { id: "auto_fill", x: 26.2, y: 90.6, shape: "round-black", led: true, top: "AUTO\nFILL" },
    { id: "break_btn", x: 29.7, y: 90.6, shape: "tall-black", led: true, top: "BREAK" },
    { id: "ending_1", x: 33.6, y: 90.6, shape: "tall-black", led: true, top: "1" },
    { id: "ending_2", x: 36.8, y: 90.6, shape: "tall-black", led: true, top: "2" },
    { id: "ending_3", x: 40.0, y: 90.6, shape: "tall-black", led: true, top: "3" },
    { id: "synchro_start", x: 44.0, y: 90.6, shape: "round-black", led: true, top: "START" },
    { id: "synchro_stop", x: 47.1, y: 90.6, shape: "round-black", led: true, top: "STOP" },
    { id: "start_stop", x: 50.6, y: 90.6, shape: "tall-red", led: true, top: "START/STOP", whiteBox: true },
    { id: "reset_tap", x: 54.1, y: 90.6, shape: "round-black", led: false, top: "RESET\nTAP TEMPO" },
    { id: "fade_inout", x: 57.2, y: 90.6, shape: "round-black", led: true, top: "FADE\nIN/OUT" },
    { id: "my_setting", x: 60.9, y: 90.6, shape: "tall-black", led: false, top: "MY\nSETTING", whiteBox: true },
    { id: "song_book", x: 64.3, y: 90.6, shape: "tall-black", led: true, top: "SONG\nBOOK" },
    { id: "set_list", x: 67.9, y: 90.6, shape: "tall-black", led: true, top: "SET\nLIST" },

    // 9 Keyboard Set Library / Set List Buttons
    { id: "ksl_1", x: 71.4, y: 90.6, shape: "tall-black", led: true, top: "PIANO & EP", bottom: "1" },
    { id: "ksl_2", x: 74.5, y: 90.6, shape: "tall-black", led: true, top: "ORGAN", bottom: "2" },
    { id: "ksl_3", x: 77.6, y: 90.6, shape: "tall-black", led: true, top: "GUITAR", bottom: "3" },
    { id: "ksl_4", x: 80.7, y: 90.6, shape: "tall-black", led: true, top: "STRINGS", bottom: "4" },
    { id: "ksl_5", x: 83.8, y: 90.6, shape: "tall-black", led: true, top: "BRASS", bottom: "5" },
    { id: "ksl_6", x: 86.9, y: 90.6, shape: "tall-black", led: true, top: "TRUMPET", bottom: "6" },
    { id: "ksl_7", x: 90.0, y: 90.6, shape: "tall-black", led: true, top: "SAX&WOOD.", bottom: "7" },
    { id: "ksl_8", x: 93.1, y: 90.6, shape: "tall-black", led: true, top: "SYNTH", bottom: "8" },
    { id: "ksl_9", x: 96.2, y: 90.6, shape: "tall-black", led: true, top: "ETHNIC", bottom: "9" }
  ];

  const KNOB_DEFS = [
    { id: "master_volume", x: 4.2, y: 42.6, top: "MASTER\nVOLUME", leftSub: "🔈", rightSub: "🔊" },
    { id: "balance", x: 9.4, y: 42.6, top: "BALANCE", leftSub: "ACC/SONG", rightSub: "KBD" },
    { id: "assign_knob_1", x: 4.2, y: 58.8, top: "1", leftSub: "", rightSub: "" },
    { id: "assign_knob_2", x: 9.4, y: 58.8, top: "2", leftSub: "", rightSub: "" }
  ];

  // =========================================================================
  // MOUNT HARDWARE CONTROLS ON FACEPLATE + ORIENTAL SUB-SCALE
  // =========================================================================
  function mountFaceplateControls() {
    const layer = document.getElementById("faceplateControlsLayer");
    layer.innerHTML = "";

    // 1. Mount 4 Rotary Knobs
    KNOB_DEFS.forEach(kd => {
      const el = document.createElement("div");
      el.className = "hw-knob";
      el.dataset.knobId = kd.id;
      el.style.left = `${kd.x}%`;
      el.style.top = `${kd.y}%`;
      el.title = `${kd.top.replace("\n", " ")} — Drag up/down or scroll wheel`;
      el.innerHTML = `
        <div class="knob-label-top">${escapeHtml(kd.top).replace("\n", "<br/>")}</div>
        <div class="knob-arc"></div>
        <div class="knob-base"></div>
        <div class="knob-cap" id="knob_cap_${kd.id}"></div>
        ${(kd.leftSub || kd.rightSub) ? `<div class="knob-sub-ends"><span>${kd.leftSub}</span><span>${kd.rightSub}</span></div>` : ""}
      `;
      bindKnobInteraction(el, kd.id);
      layer.appendChild(el);
    });

    // 2. Mount Brushed Silver VALUE Dial
    const dial = document.createElement("div");
    dial.className = "hw-value-dial";
    dial.title = "VALUE Dial — Drag up/down, scroll wheel, or click left/right half to step parameter";
    dial.innerHTML = `
      <div class="dial-label">VALUE</div>
      <div class="dial-wheel" id="valueDialWheel"></div>
    `;
    bindValueDialInteraction(dial);
    layer.appendChild(dial);

    // 3. Mount All 74 Hardware Buttons
    BUTTON_DEFS.forEach(bd => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.id = `hw_${bd.id}`;
      btn.dataset.btnId = bd.id;
      btn.className = `hw-btn ${bd.shape}`;
      btn.style.left = `${bd.x}%`;
      btn.style.top = `${bd.y}%`;

      const topCls = bd.whiteBox ? "btn-label-top white-box" : "btn-label-top";
      const topHtml = `<span class="${topCls}">${escapeHtml(bd.top).replace(/\n/g, "<br/>")}</span>`;
      const ledHtml = bd.led ? `<span class="hw-led" id="led_${bd.id}"></span>` : "";
      const botHtml = bd.bottom ? `<span class="btn-label-bottom">${bd.bottom}</span>` : "";
      btn.innerHTML = topHtml + ledHtml + botHtml;

      bindHardwareButton(btn, bd);
      layer.appendChild(btn);
    });
  }

  function buildOrientalTrayElement(prefix) {
    const tray = document.createElement("div");
    tray.className = "oriental-tray";
    tray.innerHTML = `<span class="preset-caption">PRESET</span>`;

    // 7 white-key pitch classes (C=0, D=2, E=4, F=5, G=7, A=9, B=11)
    const whitePitches = [0, 2, 4, 5, 7, 9, 11];
    whitePitches.forEach((pc, i) => {
      const xPct = ((59 + i * 69) / 680) * 100;
      const b = document.createElement("button");
      b.type = "button";
      b.className = "oriental-btn sq";
      b.style.left = `${xPct}%`;
      b.style.top = "75%";
      b.title = `Sub-Scale ${NOTE_NAMES[pc]} (-50 cents quarter-tone toggle)`;
      b.innerHTML = `<span class="hw-led" data-subscale-led="${pc}"></span>`;
      b.addEventListener("click", () => toggleSubScalePitch(pc));
      tray.appendChild(b);
    });

    // 5 black-key pitch classes (C#=1, D#=3, F#=6, G#=8, A#=10)
    const blackSpecs = [
      { pc: 1, slot: 0 },
      { pc: 3, slot: 1 },
      { pc: 6, slot: 3 },
      { pc: 8, slot: 4 },
      { pc: 10, slot: 5 }
    ];
    blackSpecs.forEach(sp => {
      const cx = 26 + (sp.slot + 1) * 69 - 1.5;
      const xPct = (cx / 680) * 100;
      const b = document.createElement("button");
      b.type = "button";
      b.className = "oriental-btn sq";
      b.style.left = `${xPct}%`;
      b.style.top = "32%";
      b.title = `Sub-Scale ${NOTE_NAMES[sp.pc]} (-50 cents quarter-tone toggle)`;
      b.innerHTML = `<span class="hw-led" data-subscale-led="${sp.pc}"></span>`;
      b.addEventListener("click", () => toggleSubScalePitch(sp.pc));
      tray.appendChild(b);
    });

    // 4 Preset round buttons SC1-SC4
    const scCoords = [
      { id: 1, lbl: "SC1", x: 80.5, y: 36 },
      { id: 2, lbl: "SC2", x: 91.0, y: 36 },
      { id: 3, lbl: "SC3", x: 80.5, y: 75 },
      { id: 4, lbl: "SC4", x: 91.0, y: 75 }
    ];
    scCoords.forEach(sc => {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "oriental-btn rd";
      b.style.left = `${sc.x}%`;
      b.style.top = `${sc.y}%`;
      b.title = `Quarter-Tone Preset ${sc.lbl} (Long-press or Shift-click to save current scale)`;
      b.innerHTML = `<span class="sc-lbl">${sc.lbl}</span><span class="hw-led" data-sc-led="${sc.id}"></span>`;
      b.addEventListener("click", () => recallSubScalePreset(sc.id));
      tray.appendChild(b);
    });

    return tray;
  }

  function mountOrientalPanels() {
    const dockC = document.getElementById("dockOrientalContainer");
    const wingC = document.getElementById("wingOrientalContainer");
    dockC.innerHTML = "";
    wingC.innerHTML = "";
    dockC.appendChild(buildOrientalTrayElement("dock"));
    wingC.appendChild(buildOrientalTrayElement("wing"));
  }

  // =========================================================================
  // KNOB & VALUE DIAL INTERACTION
  // =========================================================================
  function bindKnobInteraction(el, knobId) {
    let dragging = false;
    let startY = 0;
    let startVal = 0;

    el.addEventListener("mousedown", e => {
      dragging = true;
      startY = e.clientY;
      startVal = state.knobs[knobId];
      e.preventDefault();
    });

    window.addEventListener("mousemove", e => {
      if (!dragging) return;
      const delta = (startY - e.clientY) / 130;
      state.knobs[knobId] = Math.max(0, Math.min(1, startVal + delta));
      if (window.pa700Audio) window.pa700Audio.syncPanelControls(buildAudioState());
      updateKnobVisuals();
      updateReadouts();
    });

    window.addEventListener("mouseup", () => {
      if (dragging) {
        dragging = false;
        const pct = Math.round(state.knobs[knobId] * 100);
        logAction(`Adjusted ${knobId.replace(/_/g, " ").toUpperCase()} knob to ${pct}%`);
      }
    });

    el.addEventListener("wheel", e => {
      e.preventDefault();
      const step = e.deltaY < 0 ? 0.05 : -0.05;
      state.knobs[knobId] = Math.max(0, Math.min(1, state.knobs[knobId] + step));
      if (window.pa700Audio) window.pa700Audio.syncPanelControls(buildAudioState());
      updateKnobVisuals();
      updateReadouts();
    }, { passive: false });
  }

  function updateKnobVisuals() {
    Object.keys(state.knobs).forEach(k => {
      const cap = document.getElementById(`knob_cap_${k}`);
      if (cap) {
        const deg = -135 + state.knobs[k] * 270;
        cap.style.transform = `rotate(${deg}deg)`;
      }
    });
  }

  function assignSoundToSelectedTrack(soundName, sourceLabel) {
    const tk = state.selectedTrackKey || "up1";
    state.tracks[tk].sound = soundName;
    state.tracks[tk].muted = false;
    syncBrowserToSound(soundName);
    if (window.pa700Audio && typeof window.pa700Audio.preloadSound === "function") {
      window.pa700Audio.preloadSound(soundName);
    }
    const rec = resolveSoundRecord(soundName);
    const dncTag = rec && rec.dnc ? " [DNC Control Active]" : "";
    logAction(`${sourceLabel || "Sound"} -> ${tk.toUpperCase()} set to "${soundName}"${dncTag}`);
  }

  function assignPadToSlot(padObj, slotIdx, sourceLabel) {
    const st = getCurrentStyle();
    const currentPads = getStylePads(st).slice();
    currentPads[slotIdx] = padObj;
    state.customStylePads[st.id] = currentPads;
    syncBrowserToPad(padObj);
    logAction(`${sourceLabel || "Pad"} -> PAD ${slotIdx + 1} set to "${padObj.name}" (${padObj.type}).`);
  }

  function stepValueDial(dir) {
    if (!state.powerOn) return;
    state.dialAngle += dir * 18;
    const wheel = document.getElementById("valueDialWheel");
    if (wheel) wheel.style.transform = `rotate(${state.dialAngle}deg)`;

    if (state.shiftLatched) {
      changeTempo(dir * 4);
      return;
    }

    if (state.overlayWindow === "style_select") {
      const next = (state.currentStyleIdx + dir + DATA.styles.length) % DATA.styles.length;
      selectStyleByIndex(next, { keepOverlayOpen: true });
      return;
    }

    if (state.overlayWindow === "kbd_lib_select") {
      const list = DATA.keyboardSetLibrary[state.kbdBrowseCat || state.activeLibCategory] || [];
      if (list.length) {
        const curName = state.kbdSetName;
        let idx = list.findIndex(k => k.name === curName);
        idx = idx < 0 ? 0 : (idx + dir + list.length) % list.length;
        applyLibraryKbdSet(state.kbdBrowseCat || state.activeLibCategory, idx);
        renderAll();
      }
      return;
    }

    if (state.overlayWindow === "pad_select") {
      const list = getPadBankItems(state.padBrowseGroup);
      if (list.length) {
        const curPads = getStylePads();
        const curPad = curPads[state.padSelectSlot];
        let idx = curPad ? list.findIndex(p => p.id === curPad.id || p.name === curPad.name) : -1;
        idx = idx < 0 ? 0 : (idx + dir + list.length) % list.length;
        assignPadToSlot(list[idx], state.padSelectSlot, "VALUE Dial");
        renderAll();
      }
      return;
    }

    if (state.focusedParam === "split" || state.mainBottomTab === "split") {
      const sp = Math.max(36, Math.min(96, getEffectiveSplit() + dir));
      setLocalSplitPoint(sp, "VALUE dial");
      return;
    }

    if (state.overlayWindow === "sound_select" || state.focusedParam === "sound") {
      const bankList = state.overlayWindow === "sound_select"
        ? getSoundBankItems(state.soundBrowseType, state.soundBrowseGroup)
        : (DATA.sounds || []);
      const list = bankList.length ? bankList : (DATA.sounds || []);
      const curName = state.tracks[state.selectedTrackKey].sound;
      let curIdx = list.findIndex(s => s.name === curName);
      curIdx = curIdx < 0 ? 0 : (curIdx + dir + list.length) % list.length;
      const nextSound = list[curIdx];
      if (nextSound) {
        assignSoundToSelectedTrack(nextSound.name, "VALUE Dial");
        renderAll();
      }
      return;
    }

    // Default: adjust Tempo
    changeTempo(dir);
  }

  function bindValueDialInteraction(el) {
    let dragging = false;
    let accumY = 0;
    let lastY = 0;

    el.addEventListener("mousedown", e => {
      dragging = true;
      lastY = e.clientY;
      accumY = 0;
      e.preventDefault();
    });

    window.addEventListener("mousemove", e => {
      if (!dragging) return;
      accumY += (lastY - e.clientY);
      lastY = e.clientY;
      while (Math.abs(accumY) >= 14) {
        const dir = accumY > 0 ? 1 : -1;
        stepValueDial(dir);
        accumY -= dir * 14;
      }
    });

    window.addEventListener("mouseup", () => {
      dragging = false;
    });

    el.addEventListener("click", e => {
      if (Math.abs(accumY) > 4) return;
      const rect = el.getBoundingClientRect();
      const dir = (e.clientX - rect.left) < rect.width / 2 ? -1 : 1;
      stepValueDial(dir);
    });

    el.addEventListener("wheel", e => {
      e.preventDefault();
      stepValueDial(e.deltaY < 0 ? 1 : -1);
    }, { passive: false });
  }

  // =========================================================================
  // HARDWARE BUTTON DISPATCH (SHORT CLICK, LONG PRESS & SHIFT COMBOS)
  // =========================================================================
  function bindHardwareButton(btn, bd) {
    let holdTimer = null;
    let heldTriggered = false;
    let lastClickTime = 0;

    btn.addEventListener("mousedown", e => {
      if (e.button === 2 && bd.id === "split") {
        e.preventDefault();
        openSplitPointDialog();
        return;
      }
      heldTriggered = false;
      holdTimer = setTimeout(() => {
        heldTriggered = true;
        handleLongPress(bd.id);
      }, 520);
    });

    btn.addEventListener("contextmenu", e => {
      if (bd.id === "split") {
        e.preventDefault();
        openSplitPointDialog();
      }
    });

    const clearHold = () => {
      if (holdTimer) {
        clearTimeout(holdTimer);
        holdTimer = null;
      }
    };
    btn.addEventListener("mouseup", clearHold);
    btn.addEventListener("mouseleave", clearHold);

    btn.addEventListener("click", () => {
      if (heldTriggered) return;
      const now = performance.now();
      const isDouble = (now - lastClickTime) < 340;
      lastClickTime = now;
      handleButtonPress(bd.id, isDouble);
      checkDrillProgress(bd.id, null);
    });
  }

  function handleLongPress(id) {
    if (id === "power") {
      state.powerOn = !state.powerOn;
      if (!state.powerOn) stopArrangerImmediate();
      logAction(state.powerOn ? "Pa700 Powered ON (Style Play Main Page)" : "Pa700 entered Standby Mode (Power OFF)");
      renderAll();
      return;
    }
    if (!state.powerOn) return;

    if (id === "split") {
      openSplitPointDialog();
    } else if (id === "my_setting") {
      DATA.mySetting.tracks = clone(state.tracks);
      DATA.mySetting.kbdSet = { name: state.kbdSetName, ...clone(state.tracks) };
      DATA.mySetting.localSplit = state.localSplitPoint;
      logAction("Long-pressed MY SETTING -> Saved current voices & split into 'My Setting'!");
      renderAll();
    } else if (id.startsWith("kbd_set_")) {
      const slot = parseInt(id.split("_")[2], 10) - 1;
      const st = getCurrentStyle();
      st.kbdSets[slot] = {
        name: state.kbdSetName,
        up1: state.tracks.up1.sound,
        up2: state.tracks.up2.sound,
        up2Muted: state.tracks.up2.muted,
        up3: state.tracks.up3.sound,
        up3Muted: state.tracks.up3.muted,
        low: state.tracks.low.sound
      };
      logAction(`Long-pressed KEYBOARD SET ${slot + 1} -> Wrote "${state.kbdSetName}" into Style "${st.name}" Slot ${slot + 1}!`);
      renderAll();
    } else if (id === "style_select") {
      logAction(`Long-pressed STYLE SELECT -> Opened 'Write Current Style Settings' saved for "${getCurrentStyle().name}".`);
    } else if (id === "song_book") {
      logAction(`Long-pressed SONG BOOK -> Created new SongBook Entry snapshot for "${getCurrentStyle().name}".`);
    }
  }

  function openSplitPointDialog() {
    if (!state.powerOn) return;
    state.splitDialogOpen = true;
    state.focusedParam = "split";
    logAction("SPLIT held -> Split Point Dialog open: Click any key on the 61-key keyboard to set Split Point (or EXIT to cancel).");
    renderAll();
  }

  function handleButtonPress(id, isDouble) {
    if (id === "power") {
      state.powerOn = !state.powerOn;
      if (!state.powerOn) stopArrangerImmediate();
      logAction(state.powerOn ? "POWER ON — Welcome to Korg Pa700!" : "POWER Standby Mode (click POWER to wake).");
      renderAll();
      return;
    }
    if (!state.powerOn) return;

    if (id === "shift") {
      state.shiftLatched = !state.shiftLatched;
      logAction(state.shiftLatched
        ? "SHIFT latched ON (click another button or turn VALUE dial for Shift shortcut)"
        : "SHIFT released");
      renderAll();
      return;
    }

    // Handle SHIFT + Button hardware shortcuts (Manual p. 1025)
    if (state.shiftLatched) {
      state.shiftLatched = false;
      if (handleShiftShortcut(id)) {
        renderAll();
        return;
      }
    }

    switch (id) {
      // Modes
      case "mode_style":
        state.mode = "style";
        state.overlayWindow = null;
        logAction("Switched to STYLE PLAY mode (Main Page).");
        break;
      case "mode_song":
        state.mode = "song";
        state.overlayWindow = null;
        logAction("Switched to SONG PLAY mode.");
        break;
      case "mode_seq":
        state.mode = "seq";
        state.overlayWindow = null;
        logAction("Switched to SEQUENCER (16-Track Backing Sequence) mode.");
        break;
      case "mode_sound":
        state.mode = "sound";
        state.overlayWindow = "sound_select";
        state.focusedParam = "sound";
        syncBrowserToSound(state.tracks[state.selectedTrackKey].sound);
        logAction(`Switched to SOUND mode — Browsing ${DATA.sounds.length} manual Sounds (current: "${state.tracks[state.selectedTrackKey].sound}").`);
        break;
      case "global":
        state.overlayWindow = state.overlayWindow === "global" ? null : "global";
        logAction("Opened GLOBAL Settings (Mode Preferences, Tuning, Controllers, Speakers).");
        break;
      case "media":
        state.overlayWindow = state.overlayWindow === "media" ? null : "media";
        logAction("Opened MEDIA mode (Load / Save / USB / Internal SSD).");
        break;

      // Navigation
      case "exit":
        if (state.splitDialogOpen) {
          state.splitDialogOpen = false;
          logAction("Pressed EXIT -> Closed Split Point dialog without changes.");
        } else if (state.overlayWindow) {
          logAction(`Pressed EXIT -> Closed ${state.overlayWindow.replace(/_/g, " ")} window, returned to Main Page.`);
          state.overlayWindow = null;
        } else {
          state.mainBottomTab = "kbd_set";
          logAction("Pressed EXIT -> Returned to Main Page default view.");
        }
        break;
      case "menu":
        state.overlayWindow = state.overlayWindow === "menu" ? null : "menu";
        logAction("Pressed MENU -> Opened Edit Sections grid.");
        break;
      case "lyrics":
      case "marker":
      case "score":
        state.overlayWindow = state.overlayWindow === id ? null : id;
        logAction(`Opened ${id.toUpperCase()} page on TouchView display.`);
        break;
      case "search":
        state.overlayWindow = state.overlayWindow === "search" ? null : "search";
        logAction("Pressed SEARCH -> Search Styles, Songs, Sounds, and SongBook Entries.");
        break;

      // Player Controls
      case "player_select":
        state.currentSongIdx = (state.currentSongIdx + 1) % DATA.playerSongs.length;
        logAction(`PLAYER SELECT -> Loaded "${songDisplayTitle(DATA.playerSongs[state.currentSongIdx])}".`);
        break;
      case "player_home":
        state.playerBar = 1;
        logAction(`PLAYER |◄ (HOME) -> Returned "${songDisplayTitle(DATA.playerSongs[state.currentSongIdx])}" to Measure 001.`);
        break;
      case "player_rew":
        state.playerBar = Math.max(1, state.playerBar - 2);
        logAction(`PLAYER ◄◄ -> Rewound Song to Measure ${String(state.playerBar).padStart(3, "0")}.`);
        break;
      case "player_ff":
        state.playerBar += 2;
        logAction(`PLAYER ►► -> Fast-forwarded Song to Measure ${String(state.playerBar).padStart(3, "0")}.`);
        break;
      case "player_play":
        state.playerRunning = !state.playerRunning;
        if (state.playerRunning) state.padsActive = [false, false, false, false];
        logAction(state.playerRunning
          ? `PLAYER ►/■ -> Playing Song "${songDisplayTitle(DATA.playerSongs[state.currentSongIdx])}".`
          : `PLAYER ►/■ -> Stopped Song Player.`);
        break;

      // Accompaniment & Chord Controls
      case "chord_seq":
        if (state.chordSeqState === "off") {
          state.chordSeqState = "rec";
          logAction("CHORD SEQUENCER -> Armed Recording (LED blinking red). Play chords, then click again to loop!");
        } else if (state.chordSeqState === "rec") {
          state.chordSeqState = "play";
          logAction(`CHORD SEQUENCER -> Looping progression [${state.chordSeqProg.join(" -> ")}] (LED green)!`);
        } else {
          state.chordSeqState = "off";
          logAction("CHORD SEQUENCER -> Turned OFF.");
        }
        break;
      case "accomp":
        state.accompOn = !state.accompOn;
        logAction(state.accompOn
          ? "ACCOMP. ON -> Full 8-part band accompaniment (Drums, Perc, Bass + 5 Pitched tracks) enabled."
          : "ACCOMP. OFF -> Pitched accompaniment & Auto-Bass muted; only Drums & Percussion will play.");
        break;
      case "memory":
        state.memoryOn = !state.memoryOn;
        if (!state.memoryOn && state.pressedMidiNotes.length === 0) {
          state.recognizedChord = null;
        }
        logAction(state.memoryOn
          ? "MEMORY ON -> Recognized chord & Lower sound keep holding after you lift your left hand."
          : "MEMORY OFF -> Chord & Lower sound stop as soon as you release the keys.");
        break;
      case "manual_bass":
        state.manualBass = !state.manualBass;
        if (state.manualBass) state.accompOn = false;
        logAction(state.manualBass
          ? "MANUAL BASS ON -> Auto-accompaniment muted (except Drums/Perc); left-hand Lower plays Bass directly!"
          : "MANUAL BASS OFF -> NormalLower sound restored.");
        break;

      // Pads 1-4 + Stop (Double-click opens Pad Select across all 415 Pads!)
      case "pad_1":
      case "pad_2":
      case "pad_3":
      case "pad_4": {
        const pIdx = parseInt(id.split("_")[1], 10) - 1;
        const padInfo = getStylePads()[pIdx];
        if (isDouble) {
          state.padSelectSlot = pIdx;
          state.overlayWindow = "pad_select";
          syncBrowserToPad(padInfo);
          logAction(`Double-clicked PAD ${pIdx + 1} -> Opened Pad Select (${DATA.pads.length} manual Pads) to assign Slot ${pIdx + 1}.`);
          break;
        }
        if (padInfo.type === "OneShot") {
          state.padsActive[pIdx] = true;
          if (window.pa700Audio) window.pa700Audio.triggerPadHit(pIdx, padInfo, buildAudioState());
          logAction(`Triggered PAD ${pIdx + 1}: "${padInfo.name}" (One-Shot hit)!`);
          setTimeout(() => {
            state.padsActive[pIdx] = false;
            renderAll();
          }, 1100);
        } else {
          state.padsActive[pIdx] = !state.padsActive[pIdx];
          if (state.padsActive[pIdx] && window.pa700Audio) {
            window.pa700Audio.triggerPadHit(pIdx, padInfo, buildAudioState());
          }
          logAction(state.padsActive[pIdx]
            ? `Started Looping PAD ${pIdx + 1}: "${padInfo.name}" (synced to ${state.tempo} BPM & chord ${state.recognizedChord || "N/A"}).`
            : `Stopped PAD ${pIdx + 1}: "${padInfo.name}".`);
        }
        break;
      }
      case "pad_stop":
        state.padsActive = [false, false, false, false];
        logAction("PADS STOP -> Stopped all active Pads (1-4).");
        break;

      // Style to Kbd Set & Style Select
      case "style_to_kbd":
        if (state.styleToKbdMode === "off") {
          state.styleToKbdMode = "on";
          recallStyleKeyboardSet(0, "STYLE TO KBD SET ON");
          logAction("STYLE TO KBD SET = ON (Solid LED): Selecting a new Style automatically loads its Keyboard Set 1.");
        } else if (state.styleToKbdMode === "on") {
          state.styleToKbdMode = "blink";
          recallStyleKeyboardSet(state.activeVariation - 1, "STYLE TO KBD SET BLINKING");
          logAction("STYLE TO KBD SET = BLINKING: Switching Variation 1-4 now automatically switches Keyboard Set 1-4!");
        } else {
          state.styleToKbdMode = "off";
          logAction("STYLE TO KBD SET = OFF: Changing Styles or Variations keeps your current voice unchanged.");
        }
        break;
      case "style_select":
        state.mode = "style";
        state.overlayWindow = state.overlayWindow === "style_select" ? null : "style_select";
        state.focusedParam = "style";
        if (state.overlayWindow === "style_select") syncBrowserToStyle(state.currentStyleIdx);
        logAction(`Pressed STYLE SELECT -> Choose from ${DATA.styles.length} manual Styles on TouchView (or turn VALUE dial).`);
        break;
      case "mp3_rec":
        state.mp3Recording = !state.mp3Recording;
        logAction(state.mp3Recording
          ? "MP3 RECORD -> Recording live performance to virtual MP3!"
          : "MP3 RECORD -> Stopped MP3 recording.");
        break;
      case "track_select":
        state.mainBottomTab = "volume";
        state.overlayWindow = null;
        state.volumeTrackView = state.volumeTrackView === "grouped" ? "style_tracks" : "grouped";
        logAction(`TRACK SELECT -> Switched Volume mixer view to ${state.volumeTrackView === "grouped" ? "Keyboard & Group Faders" : "Individual 8 Style Accompaniment Tracks"}.`);
        break;

      // Keyboard Set 1-4 (Under Display)
      case "kbd_set_1":
      case "kbd_set_2":
      case "kbd_set_3":
      case "kbd_set_4": {
        const slot = parseInt(id.split("_")[2], 10) - 1;
        recallStyleKeyboardSet(slot, `KEYBOARD SET ${slot + 1} button`);
        break;
      }

      // Tempo / Lock / Metronome / Split / Ensemble / Octave / Transpose
      case "tempo_minus":
        changeTempo(-1);
        break;
      case "tempo_plus":
        changeTempo(1);
        break;
      case "tempo_lock":
        state.tempoLock = !state.tempoLock;
        logAction(state.tempoLock
          ? `TEMPO LOCK ON -> Tempo locked at ${state.tempo} BPM when switching Styles.`
          : "TEMPO LOCK OFF -> Selecting a Style recalls its memorized Tempo.");
        break;
      case "metronome":
        state.metronomeOn = !state.metronomeOn;
        logAction(state.metronomeOn
          ? `METRONOME ON -> Clicking ${ getCurrentStyle().meter } at ${state.tempo} BPM.`
          : "METRONOME OFF.");
        break;
      case "split":
        state.splitOn = !state.splitOn;
        logAction(state.splitOn
          ? `SPLIT ON -> Keyboard divided at ${midiToName(getEffectiveSplit())} (Lower < ${midiToName(getEffectiveSplit())}, Upper >= ${midiToName(getEffectiveSplit())}). Tip: Hold SPLIT to move split note!`
          : "SPLIT OFF (Full Keyboard Mode) -> Upper 1-3 voices play across all 61 keys like an acoustic piano!");
        break;
      case "ensemble":
        state.ensembleOn = !state.ensembleOn;
        logAction(state.ensembleOn
          ? `ENSEMBLE ON (${state.ensembleType}) -> Right-hand melody automatically harmonized with left-hand chord!`
          : "ENSEMBLE OFF -> Right-hand plays normal unharmonized notes.");
        break;
      case "octave_minus":
        state.upperOctave = Math.max(-2, state.upperOctave - 1);
        logAction(`UPPER OCTAVE = ${state.upperOctave > 0 ? "+" : ""}${state.upperOctave} octave(s).`);
        break;
      case "octave_plus":
        state.upperOctave = Math.min(2, state.upperOctave + 1);
        logAction(`UPPER OCTAVE = ${state.upperOctave > 0 ? "+" : ""}${state.upperOctave} octave(s).`);
        break;
      case "transpose_flat":
        state.masterTranspose = Math.max(-12, state.masterTranspose - 1);
        logAction(`MASTER TRANSPOSE = ${state.masterTranspose > 0 ? "+" : ""}${state.masterTranspose} semitones.`);
        break;
      case "transpose_sharp":
        state.masterTranspose = Math.min(12, state.masterTranspose + 1);
        logAction(`MASTER TRANSPOSE = ${state.masterTranspose > 0 ? "+" : ""}${state.masterTranspose} semitones.`);
        break;

      // Arranger Intros, Variations, Auto Fill, Break, Endings, Synchro, Start/Stop
      case "intro_1":
      case "intro_2":
      case "intro_3":
        triggerIntro(parseInt(id.split("_")[1], 10), isDouble);
        break;
      case "var_1":
      case "var_2":
      case "var_3":
      case "var_4":
        triggerVariation(parseInt(id.split("_")[1], 10));
        break;
      case "auto_fill":
        state.autoFill = !state.autoFill;
        logAction(state.autoFill
          ? "AUTO FILL ON -> Switching Variations while playing automatically plays a 1-bar Drum/Band Fill first!"
          : "AUTO FILL OFF -> Switching Variations changes directly on bar boundary without a Fill.");
        break;
      case "break_btn":
        triggerBreak(isDouble);
        break;
      case "ending_1":
      case "ending_2":
      case "ending_3":
        triggerEnding(parseInt(id.split("_")[1], 10), isDouble);
        break;
      case "synchro_start":
        state.synchroStart = !state.synchroStart;
        logAction(state.synchroStart
          ? "SYNCHRO START ARMED -> Arranger will start automatically the instant you play a chord!"
          : "SYNCHRO START OFF.");
        break;
      case "synchro_stop":
        state.synchroStop = !state.synchroStop;
        logAction(state.synchroStop
          ? "SYNCHRO STOP ARMED -> Arranger will stop automatically as soon as you lift your hands from the keys!"
          : "SYNCHRO STOP OFF.");
        break;
      case "start_stop":
        if (state.arrangerRunning) {
          stopArrangerImmediate();
          logAction("Pressed START/STOP -> Arranger & Pads Stopped.");
        } else {
          startArranger("START/STOP button");
        }
        break;
      case "reset_tap":
        handleResetOrTapTempo();
        break;
      case "fade_inout":
        handleFadeInOut();
        break;

      // My Setting, SongBook, Set List & 9 Keyboard Set Library / Set List Buttons
      case "my_setting":
        recallMySetting();
        break;
      case "song_book":
        state.overlayWindow = state.overlayWindow === "songbook" ? null : "songbook";
        logAction("Pressed SONG BOOK -> Opened SongBook Set List (matches reference panel display!).");
        break;
      case "set_list":
        state.setListMode = !state.setListMode;
        if (state.setListMode) {
          state.overlayWindow = "songbook";
          logAction("SET LIST ON (Red LED) -> Buttons 1-9 on bottom-right now select SongBook Set List songs 1-9!");
        } else {
          if (state.overlayWindow === "songbook") state.overlayWindow = null;
          logAction("SET LIST OFF -> Bottom-right buttons now select KEYBOARD SET LIBRARY voice categories (Piano & EP .. Ethnic)!");
        }
        break;
      case "ksl_1":
      case "ksl_2":
      case "ksl_3":
      case "ksl_4":
      case "ksl_5":
      case "ksl_6":
      case "ksl_7":
      case "ksl_8":
      case "ksl_9": {
        const num = parseInt(id.split("_")[1], 10);
        handleLibraryOrSetListButton(num);
        break;
      }
    }

    renderAll();
  }

  function handleShiftShortcut(id) {
    if (id === "start_stop") {
      state.pressedMidiNotes = [];
      state.padsActive = [false, false, false, false];
      logAction("SHIFT + START/STOP -> MIDI PANIC! All stuck notes & controllers reset.");
      return true;
    }
    if (id === "mode_style" || id === "auto_fill") {
      state.overlayWindow = "global";
      logAction("SHIFT + STYLE PLAY -> Opened Global > Mode Preferences > Style (Global Split & Auto-Fill settings).");
      return true;
    }
    if (id === "ensemble") {
      const types = ["Duet", "Close", "Open 1", "Octave", "Brass", "Reed"];
      const idx = (types.indexOf(state.ensembleType) + 1) % types.length;
      state.ensembleType = types[idx];
      state.ensembleOn = true;
      logAction(`SHIFT + ENSEMBLE -> Cycled Ensemble Harmony Voicing to "${state.ensembleType}".`);
      return true;
    }
    if (id === "octave_minus" || id === "octave_plus") {
      state.upperOctave = 0;
      logAction("SHIFT + UPPER OCTAVE -> Reset Upper Octave to 0.");
      return true;
    }
    if (id === "transpose_flat" || id === "transpose_sharp") {
      state.masterTranspose = 0;
      logAction("SHIFT + TRANSPOSE -> Reset Master Transpose to 0.");
      return true;
    }
    return false;
  }

  // =========================================================================
  // VOICE & KEYBOARD SET FUNCTIONS
  // =========================================================================
  function recallMySetting() {
    state.tracks = getMySettingTracks();
    state.kbdSetName = (DATA.mySetting && DATA.mySetting.kbdSet && DATA.mySetting.kbdSet.name) || "My Setting";
    state.kbdSetSource = "Kbd Set Library";
    state.activeStyleKbdSlot = null;
    state.splitOn = (DATA.mySetting && DATA.mySetting.splitOn !== undefined) ? DATA.mySetting.splitOn : true;
    state.localSplitPoint = (DATA.mySetting && DATA.mySetting.localSplit !== undefined) ? DATA.mySetting.localSplit : null;
    state.useGlobalSplit = state.localSplitPoint === null;
    if (window.pa700Audio && typeof window.pa700Audio.preloadSound === "function") {
      window.pa700Audio.preloadSound(state.tracks.up1.sound);
    }
    logAction(`Recalled MY SETTING -> Upper 1: "${state.tracks.up1.sound}", Split ${state.splitOn ? "ON (" + midiToName(getEffectiveSplit()) + ")" : "OFF"}.`);
  }

  function recallStyleKeyboardSet(slot, triggerLabel) {
    const st = getCurrentStyle();
    const ks = st.kbdSets && st.kbdSets[slot];
    if (!ks) return;
    state.activeStyleKbdSlot = slot;
    state.kbdSetName = ks.name;
    state.kbdSetSource = `Style: ${st.name} [#${slot + 1}]`;
    state.tracks.up1 = { sound: ks.up1, muted: false, octave: 0, volume: 100 };
    state.tracks.up2 = { sound: ks.up2, muted: Boolean(ks.up2Muted), octave: 0, volume: 82 };
    state.tracks.up3 = { sound: ks.up3, muted: Boolean(ks.up3Muted), octave: 0, volume: 80 };
    state.tracks.low = { sound: ks.low, muted: false, octave: 1, volume: 75, backing: true };
    if (window.pa700Audio && typeof window.pa700Audio.preloadSound === "function") {
      window.pa700Audio.preloadSound(ks.up1);
    }
    logAction(`${triggerLabel} -> Loaded Voice Set #${slot + 1} "${ks.name}" (UP1: ${ks.up1}${!ks.up2Muted ? " + UP2: " + ks.up2 : ""}).`);
  }

  function handleLibraryOrSetListButton(num) {
    if (state.setListMode) {
      // Recall SongBook Set List tile 1..9!
      const entry = DATA.setListEntries[num - 1];
      if (!entry) return;
      state.activeSetListSlot = num;
      state.currentStyleIdx = findStyleIndexById(entry.styleId);
      syncBrowserToStyle(state.currentStyleIdx);
      if (!state.tempoLock && entry.tempo) state.tempo = entry.tempo;
      state.activeVariation = entry.variation || 1;
      const kbdIdx = entry.kbdIdx !== undefined ? entry.kbdIdx : (entry.kbdSetIndex || 0);
      recallStyleKeyboardSet(kbdIdx, `SET LIST #${num} "${entry.title}"`);
      logAction(`SET LIST #${num} -> Loaded SongBook Entry "${entry.title}" (Style "${getCurrentStyle().name}", ${state.tempo} BPM, Variation ${state.activeVariation}).`);
      return;
    }

    // Standard KEYBOARD SET LIBRARY Category Selection (1..9)
    const cat = DATA.libraryCategories[num - 1];
    if (!cat) return;
    const list = DATA.keyboardSetLibrary[cat.id] || [];
    if (!list.length) return;
    if (state.activeLibCategory === cat.id && state.overlayWindow === "kbd_lib_select") {
      state.activeLibIndex = (state.activeLibIndex + 1) % list.length;
    } else {
      state.activeLibCategory = cat.id;
      state.activeLibIndex = 0;
      state.overlayWindow = "kbd_lib_select";
    }
    applyLibraryKbdSet(cat.id, state.activeLibIndex);
  }

  function applyLibraryKbdSet(catId, idx) {
    const list = DATA.keyboardSetLibrary[catId] || [];
    const item = list[idx];
    if (!item) return;
    const catObj = DATA.libraryCategories.find(c => c.id === catId);
    const catLabel = catObj ? (catObj.label || catObj.short || catId) : catId;
    state.activeLibCategory = catId;
    state.activeLibIndex = idx;
    syncBrowserToKbdSet(catId, idx);
    state.activeStyleKbdSlot = null;
    state.kbdSetName = item.name;
    state.kbdSetSource = `Library: ${catLabel}`;
    state.tracks.up1 = { ...item.up1, volume: 100 };
    state.tracks.up2 = { ...item.up2, volume: 85 };
    state.tracks.up3 = { ...item.up3, volume: 80 };
    state.tracks.low = { ...item.low, volume: 75, backing: true };
    if (window.pa700Audio && typeof window.pa700Audio.preloadSound === "function") {
      window.pa700Audio.preloadSound(item.up1.sound);
    }
    logAction(`Keyboard Set Library [${catLabel} #${idx + 1}/${list.length}] -> Selected "${item.name}" (Upper 1: ${item.up1.sound}${!item.up2.muted ? " + Upper 2: " + item.up2.sound : ""}).`);
  }

  function selectStyleByIndex(idx, options = {}) {
    state.currentStyleIdx = idx;
    syncBrowserToStyle(idx);
    const st = getCurrentStyle();
    if (!state.tempoLock) {
      state.tempo = st.tempo;
    }
    state.currentBeat = 1;
    state.currentBar = 1;
    if (window.pa700Audio && state.arrangerRunning) {
      window.pa700Audio.resetGroovePosition();
    }
    state.padsActive = [false, false, false, false];
    if (state.styleToKbdMode === "on") {
      recallStyleKeyboardSet(0, `Style "${st.name}" (Style to Kbd Set ON)`);
    } else if (state.styleToKbdMode === "blink") {
      recallStyleKeyboardSet(state.activeVariation - 1, `Style "${st.name}" (Style to Kbd Set BLINK)`);
    }
    if (!options.keepOverlayOpen && !state.displayHold && state.overlayWindow === "style_select") {
      state.overlayWindow = null;
    }
    const bandPreview = Array.isArray(st.styleTracks) && st.styleTracks.length >= 4
      ? ` — Band: ${st.styleTracks[0].sound}, ${st.styleTracks[2].sound}, ${st.styleTracks[3].sound}, ${st.styleTracks[7].sound}`
      : "";
    logAction(`Selected Style "${st.name}" (${st.bank}, Meter ${st.meter}, ${state.tempo} BPM${state.tempoLock ? " [LOCKED]" : ""})${bandPreview}.`);
    renderAll();
  }

  function setLocalSplitPoint(midi, sourceLabel) {
    state.localSplitPoint = midi;
    state.useGlobalSplit = false;
    state.splitOn = true;
    state.splitDialogOpen = false;
    logAction(`Split Point set to ${midiToName(midi)} via ${sourceLabel} (Lower: C2–${midiToName(midi - 1)} | Upper: ${midiToName(midi)}–C7).`);
    renderAll();
  }

  // =========================================================================
  // AUTO-ARRANGER SECTION TRANSITIONS & CLOCK ENGINE
  // =========================================================================
  function changeTempo(delta) {
    state.tempo = Math.max(30, Math.min(300, state.tempo + delta));
    logAction(`Tempo set to ${state.tempo} BPM.`);
    restartClockInterval();
    renderAll();
  }

  function startArranger(reason) {
    if (window.pa700Audio) {
      window.pa700Audio.init();
      window.pa700Audio.resume();
      window.pa700Audio.resetGroovePosition();
    }
    state.arrangerRunning = true;
    state.currentBar = 1;
    state.currentBeat = 1;
    if (state.activeIntro) {
      state.activeSection = "intro";
      logAction(`Arranger STARTED (${reason}) -> Playing INTRO ${state.activeIntro}, then booked VARIATION ${state.activeVariation} in Style "${getCurrentStyle().name}" (${state.tempo} BPM).`);
    } else {
      state.activeSection = "var";
      logAction(`Arranger STARTED (${reason}) -> Playing VARIATION ${state.activeVariation} in Style "${getCurrentStyle().name}" (${state.tempo} BPM).`);
    }
    restartClockInterval();
  }

  function stopArrangerImmediate() {
    state.arrangerRunning = false;
    state.activeSection = "var";
    state.activeIntro = null;
    state.activeFill = null;
    state.activeEnding = null;
    state.bookedVariation = null;
    state.loopSection = false;
    state.fadeState = null;
    state.fadeLevel = 100;
    state.padsActive = [false, false, false, false];
    state.currentBeat = 1;
    state.currentBar = 1;
    if (window.pa700Audio) window.pa700Audio.syncPanelControls(buildAudioState());
  }

  function triggerIntro(num, isDouble) {
    const desc = num === 1
      ? "prerecorded chord progression & melody"
      : num === 2
        ? "intro on your recognized chord"
        : "1-bar Count-In";

    if (!state.arrangerRunning) {
      if (state.activeIntro === num && !isDouble) {
        state.activeIntro = null;
        logAction(`Cancelled booked INTRO ${num}.`);
      } else {
        state.activeIntro = num;
        state.loopSection = Boolean(isDouble);
        logAction(`Booked INTRO ${num} (${desc})${isDouble ? " [LOOPING]" : ""} -> VARIATION ${state.activeVariation} flashing & queued next!`);
      }
    } else {
      state.activeSection = "intro";
      state.activeIntro = num;
      state.currentBar = 1;
      state.loopSection = Boolean(isDouble);
      logAction(`Switched Arranger to INTRO ${num} (${desc})${isDouble ? " [LOOPING]" : ""} -> will return to VARIATION ${state.activeVariation}.`);
    }
  }

  function triggerVariation(num) {
    if (!state.arrangerRunning) {
      state.activeVariation = num;
      state.bookedVariation = null;
      if (state.styleToKbdMode === "blink") {
        recallStyleKeyboardSet(num - 1, `VARIATION ${num} (Style to Kbd Set BLINK)`);
      }
      logAction(`Selected VARIATION ${num} (ready to start).`);
      return;
    }

    // Arranger is currently playing!
    if (state.autoFill) {
      state.activeSection = "fill";
      state.activeFill = num;
      state.bookedVariation = num;
      state.currentBar = 1;
      logAction(`Pressed VARIATION ${num} with AUTO FILL ON -> Playing 1-bar FILL ${num}, then dropping into VARIATION ${num}!`);
    } else {
      state.bookedVariation = num;
      logAction(`Booked VARIATION ${num} -> Will switch on Beat 1 of the next measure.`);
    }
  }

  function triggerBreak(isDouble) {
    if (!state.arrangerRunning) {
      logAction("BREAK is used while the Arranger is playing (1-measure dramatic pause). Start the Arranger first!");
      return;
    }
    state.activeSection = "break";
    state.currentBar = 1;
    state.loopSection = Boolean(isDouble);
    logAction(`Triggered 1-Measure BREAK${isDouble ? " [LOOPING]" : ""} -> Returning to VARIATION ${state.activeVariation} next bar!`);
  }

  function triggerEnding(num, isDouble) {
    const desc = num === 1
      ? "prerecorded cadence & melody"
      : num === 2
        ? "ending on your recognized chord"
        : "immediate 2-bar ending";

    if (!state.arrangerRunning) {
      state.activeEnding = state.activeEnding === num ? null : num;
      logAction(state.activeEnding ? `Booked ENDING ${num} (${desc}).` : `Cancelled ENDING ${num}.`);
      return;
    }

    state.activeSection = "ending";
    state.activeEnding = num;
    state.currentBar = 1;
    if (num === 3) {
      state.currentBeat = 1; // Ending 3 starts immediately!
      if (window.pa700Audio) window.pa700Audio.resetGroovePosition();
    }
    state.loopSection = Boolean(isDouble);
    logAction(`Triggered ENDING ${num} (${desc})${isDouble ? " [LOOPING]" : ""} -> Arranger will auto-stop after Ending completes!`);
  }

  function handleResetOrTapTempo() {
    if (state.arrangerRunning) {
      state.currentBar = 1;
      state.currentBeat = 1;
      if (window.pa700Audio) window.pa700Audio.resetGroovePosition();
      logAction("RESET -> Jumped Style pattern back to Measure 1, Beat 1.");
      return;
    }
    const now = performance.now();
    state.tapTimestamps = state.tapTimestamps.filter(t => now - t < 2600);
    state.tapTimestamps.push(now);
    const needed = getCurrentStyle().beatsPerBar;
    if (state.tapTimestamps.length >= 2) {
      const intervals = [];
      for (let i = 1; i < state.tapTimestamps.length; i++) {
        intervals.push(state.tapTimestamps[i] - state.tapTimestamps[i - 1]);
      }
      const avgMs = intervals.reduce((a, b) => a + b, 0) / intervals.length;
      state.tempo = Math.max(40, Math.min(260, Math.round(60000 / avgMs)));
    }
    if (state.tapTimestamps.length >= needed) {
      state.tapTimestamps = [];
      startArranger(`TAP TEMPO (${state.tempo} BPM)`);
    } else {
      logAction(`TAP TEMPO (${state.tapTimestamps.length}/${needed} beats tapped -> ${state.tempo} BPM)...`);
    }
    restartClockInterval();
  }

  function handleFadeInOut() {
    if (!state.arrangerRunning) {
      state.fadeState = "in";
      state.fadeLevel = 15;
      startArranger("FADE IN");
      logAction("FADE IN -> Smoothly fading Arranger volume from 0% up to 100%...");
    } else {
      state.fadeState = state.fadeState === "out" ? null : "out";
      logAction(state.fadeState === "out"
        ? "FADE OUT -> Smoothly fading Arranger volume down to 0%, then auto-stopping..."
        : "Cancelled FADE OUT (volume restored).");
      if (!state.fadeState) state.fadeLevel = 100;
    }
  }

  // Real-time Beat Clock (driven by sample-accurate Web Audio scheduler when active)
  let clockTimer = null;

  function restartClockInterval() {
    if (clockTimer) {
      clearInterval(clockTimer);
      clockTimer = null;
    }
    if (window.pa700Audio) {
      window.pa700Audio.startEngineLoop(() => buildAudioState(), onBeatTick);
    } else {
      const beatMs = Math.max(120, Math.round(60000 / state.tempo));
      clockTimer = setInterval(onBeatTick, beatMs);
    }
  }

  function onBeatTick() {
    if (!state.powerOn) return;

    if (state.playerRunning) {
      state.playerBar += 1;
    }

    if (!state.arrangerRunning) return;

    const st = getCurrentStyle();
    const beatsPerBar = st.beatsPerBar || 4;

    // Fade In / Out progression
    if (state.fadeState === "in") {
      state.fadeLevel = Math.min(100, state.fadeLevel + 14);
      if (state.fadeLevel >= 100) {
        state.fadeState = null;
        logAction("FADE IN complete (100% volume).");
      }
    } else if (state.fadeState === "out") {
      state.fadeLevel = Math.max(0, state.fadeLevel - 14);
      if (state.fadeLevel <= 0) {
        stopArrangerImmediate();
        logAction("FADE OUT complete -> Arranger Stopped.");
        renderAll();
        return;
      }
    }

    // Advance Beat
    state.currentBeat += 1;
    if (state.currentBeat > beatsPerBar) {
      state.currentBeat = 1;
      state.currentBar += 1;

      // Chord Sequencer playback step on each new bar
      if (state.chordSeqState === "play") {
        const cIdx = (state.currentBar - 1) % state.chordSeqProg.length;
        state.recognizedChord = state.chordSeqProg[cIdx];
      }

      // Section completion logic at measure boundary
      if (state.activeSection === "intro") {
        const introBars = state.activeIntro === 3 ? 1 : 2;
        if (state.currentBar > introBars && !state.loopSection) {
          state.activeSection = "var";
          const finishedIntro = state.activeIntro;
          state.activeIntro = null;
          state.currentBar = 1;
          if (state.styleToKbdMode === "blink") {
            recallStyleKeyboardSet(state.activeVariation - 1, `VARIATION ${state.activeVariation}`);
          }
          logAction(`INTRO ${finishedIntro} finished -> Now playing VARIATION ${state.activeVariation}!`);
        }
      } else if (state.activeSection === "fill") {
        if (state.currentBar > 1) {
          state.activeSection = "var";
          if (state.bookedVariation) state.activeVariation = state.bookedVariation;
          state.bookedVariation = null;
          state.activeFill = null;
          state.currentBar = 1;
          if (state.styleToKbdMode === "blink") {
            recallStyleKeyboardSet(state.activeVariation - 1, `VARIATION ${state.activeVariation} (Auto-linked)`);
          }
          logAction(`Fill complete -> Dropped into VARIATION ${state.activeVariation}!`);
        }
      } else if (state.activeSection === "break") {
        if (state.currentBar > 1 && !state.loopSection) {
          state.activeSection = "var";
          state.currentBar = 1;
          logAction(`Break complete -> Resumed VARIATION ${state.activeVariation}.`);
        }
      } else if (state.activeSection === "ending") {
        if (state.currentBar > 2 && !state.loopSection) {
          const endNum = state.activeEnding;
          stopArrangerImmediate();
          logAction(`ENDING ${endNum} finished -> Arranger automatically stopped.`);
        }
      } else if (state.activeSection === "var") {
        if (state.bookedVariation !== null) {
          state.activeVariation = state.bookedVariation;
          state.bookedVariation = null;
          state.currentBar = 1;
          if (state.styleToKbdMode === "blink") {
            recallStyleKeyboardSet(state.activeVariation - 1, `VARIATION ${state.activeVariation}`);
          }
          logAction(`Measure boundary -> Switched to VARIATION ${state.activeVariation}!`);
        } else if (state.currentBar > (st.patternBars || 4)) {
          state.currentBar = 1;
        }
      }
    }

    updateLedVisuals();
    renderTouchView();
    updateReadouts();
  }

  // =========================================================================
  // SUB-SCALE (QUARTER-TONE) FUNCTIONS
  // =========================================================================
  function toggleSubScalePitch(pc) {
    if (!state.powerOn) return;
    const idx = state.subScaleNotes.indexOf(pc);
    if (idx >= 0) {
      state.subScaleNotes.splice(idx, 1);
    } else {
      state.subScaleNotes.push(pc);
      state.subScaleNotes.sort((a, b) => a - b);
    }
    state.activeSubScalePreset = null;
    logAction(`Oriental Sub-Scale -> ${NOTE_NAMES[pc]} set to ${idx >= 0 ? "Equal (0 cents)" : "Quarter-Flat (-50 cents)"}.`);
    renderAll();
  }

  function recallSubScalePreset(scId) {
    if (!state.powerOn) return;
    const preset = (DATA.subScalePresets || []).find(p => p.id === scId) || (DATA.subScalePresets || [])[scId];
    if (!preset) return;
    const presetNotes = Array.isArray(preset.notes)
      ? preset.notes
      : (Array.isArray(preset.offsets)
          ? preset.offsets.map((off, idx) => (off < 0 ? idx : -1)).filter(i => i >= 0)
          : []);
    const label = preset.label || `SC${scId}`;
    if (state.activeSubScalePreset === scId) {
      state.activeSubScalePreset = null;
      state.subScaleNotes = [];
      logAction(`Cleared Sub-Scale Preset ${label} -> Equal Temperament restored.`);
    } else {
      state.activeSubScalePreset = scId;
      state.subScaleNotes = [...presetNotes];
      logAction(`Recalled Sub-Scale ${label}: ${preset.name}.`);
    }
    renderAll();
  }

  // =========================================================================
  // 61-KEY (C2 - C7) INTERACTIVE KEYBOARD & MAJOR TRIAD ENGINE
  // =========================================================================
  function build61KeyPiano() {
    const bed = document.getElementById("pianoKeys");
    bed.innerHTML = "";

    // Count white keys from C2 (36) to C7 (96) -> 36 white keys!
    const whiteMidis = [];
    for (let m = 36; m <= 96; m++) {
      const pc = m % 12;
      if ([0, 2, 4, 5, 7, 9, 11].includes(pc)) whiteMidis.push(m);
    }
    const totalWhites = whiteMidis.length; // 36
    const whiteWidthPct = 100 / totalWhites;

    const whiteIndexByMidi = {};
    whiteMidis.forEach((m, idx) => {
      whiteIndexByMidi[m] = idx;
      const key = document.createElement("div");
      key.className = "piano-key white";
      key.dataset.midi = m;
      key.style.left = `${idx * whiteWidthPct}%`;
      key.style.width = `${whiteWidthPct}%`;
      const name = midiToName(m);
      key.innerHTML = `<span>${name.startsWith("C") || name === "G4" || name === "F3" ? name : name.slice(0, -1)}</span>`;
      bindPianoKeyEvents(key, m);
      bed.appendChild(key);
    });

    // Black keys
    for (let m = 36; m <= 96; m++) {
      const pc = m % 12;
      if ([1, 3, 6, 8, 10].includes(pc)) {
        const prevWhiteIdx = whiteIndexByMidi[m - 1];
        const bWidth = whiteWidthPct * 0.64;
        const leftPct = (prevWhiteIdx + 1) * whiteWidthPct - bWidth / 2;
        const key = document.createElement("div");
        key.className = "piano-key black";
        key.dataset.midi = m;
        key.style.left = `${leftPct}%`;
        key.style.width = `${bWidth}%`;
        key.innerHTML = `<span>${NOTE_NAMES[pc]}</span>`;
        bindPianoKeyEvents(key, m);
        bed.appendChild(key);
      }
    }
  }

  let mouseKeyDown = false;

  function bindPianoKeyEvents(el, midi) {
    el.addEventListener("mousedown", e => {
      e.preventDefault();
      if (e.button === 2) {
        // Right-click toggles latch on this root key!
        state.latchKeys = true;
        syncLatchButton();
      }
      mouseKeyDown = true;
      pressKeyboardNote(midi);
    });

    el.addEventListener("mouseenter", () => {
      if (mouseKeyDown && !state.splitDialogOpen) {
        pressKeyboardNote(midi);
      }
    });

    el.addEventListener("contextmenu", e => e.preventDefault());
  }

  window.addEventListener("mouseup", () => {
    if (mouseKeyDown) {
      mouseKeyDown = false;
      if (!state.latchKeys) {
        releaseKeyboardNotes();
      }
    }
  });

  function computeTriadNotes(rootMidi) {
    let intervals = [0, 4, 7]; // Default Major Triad (Root + Major 3rd + Perfect 5th)
    if (state.mouseChordMode === "minor") intervals = [0, 3, 7];
    else if (state.mouseChordMode === "dom7") intervals = [0, 4, 7, 10];
    else if (state.mouseChordMode === "single") intervals = [0];

    return intervals.map(iv => {
      let n = rootMidi + iv;
      while (n > 96) n -= 12;
      return n;
    });
  }

  function formatChordLabel(rootMidi) {
    const rootName = NOTE_NAMES[((rootMidi + state.masterTranspose) % 12 + 12) % 12];
    if (state.mouseChordMode === "minor") return `${rootName} min`;
    if (state.mouseChordMode === "dom7") return `${rootName}7`;
    return `${rootName} Major`;
  }

  function pressKeyboardNote(rootMidi) {
    if (!state.powerOn) return;
    if (window.pa700Audio) window.pa700Audio.init();

    // 1. If Split Point Dialog is waiting for a key, set Split Point immediately!
    if (state.splitDialogOpen) {
      setLocalSplitPoint(rootMidi, "Keyboard Key Press");
      checkDrillProgress(null, rootMidi);
      return;
    }

    const chordNotes = computeTriadNotes(rootMidi);
    state.clickedRootMidi = rootMidi;
    state.pressedMidiNotes = chordNotes;

    const splitMidi = getEffectiveSplit();
    const rootInLower = state.splitOn && (rootMidi < splitMidi);
    const recognizeInFullMode = !state.splitOn && chordNotes.length >= 3;

    // Recognize chord if played in Lower zone (Split ON) or as 3+ note triad in Full mode
    if ((rootInLower || recognizeInFullMode) && !state.manualBass) {
      const chordStr = formatChordLabel(rootMidi);
      state.recognizedChord = chordStr;

      if (state.chordSeqState === "rec") {
        state.chordSeqProg.push(chordStr);
        if (state.chordSeqProg.length > 8) state.chordSeqProg.shift();
      }

      // Synchro Start trigger!
      if (state.synchroStart && !state.arrangerRunning) {
        startArranger(`SYNCHRO START on chord ${chordStr}`);
      }
    }

    // Play actual synthesized voices across Split / Upper 1-3 / Lower / Sub-Scale!
    if (window.pa700Audio) {
      window.pa700Audio.playKeyboardNotes(chordNotes, buildAudioState());
    }

    const noteNames = chordNotes.map(midiToName).join(", ");
    const activeVoiceDesc = describePlayingVoices(rootMidi, chordNotes);
    logAction(`Played ${midiToName(rootMidi)} -> [${noteNames}] | ${activeVoiceDesc}`);

    checkDrillProgress(null, rootMidi);
    renderAll();
  }

  function releaseKeyboardNotes() {
    if (window.pa700Audio) {
      window.pa700Audio.releaseAllKeyboardVoices(buildAudioState());
    }
    if (state.pressedMidiNotes.length === 0) return;
    state.pressedMidiNotes = [];
    state.clickedRootMidi = null;

    if (!state.memoryOn && state.chordSeqState !== "play") {
      state.recognizedChord = null;
    }

    if (state.synchroStop && state.arrangerRunning) {
      stopArrangerImmediate();
      logAction("Hands lifted with SYNCHRO STOP ON -> Arranger Stopped automatically!");
    }

    renderAll();
  }

  function describePlayingVoices(rootMidi, notes) {
    const splitMidi = getEffectiveSplit();
    const upperActive = ["up1", "up2", "up3"]
      .filter(k => !state.tracks[k].muted)
      .map((k, idx) => `${k.toUpperCase()}: ${state.tracks[k].sound}`);
    const upperSummary = upperActive.length > 0 ? upperActive.join(" + ") : "(All Upper tracks Muted!)";

    const detuned = notes
      .filter(m => state.subScaleNotes.includes(m % 12))
      .map(midiToName);
    const subScaleNote = detuned.length > 0 ? ` [Quarter-Tone -50c on ${detuned.join(",")}]` : "";
    const ensNote = state.ensembleOn ? ` [+ Ensemble: ${state.ensembleType}]` : "";
    const octNote = state.upperOctave !== 0 ? ` [Octave ${state.upperOctave > 0 ? "+" : ""}${state.upperOctave}]` : "";

    if (!state.splitOn) {
      return `Playing notes [${notes.map(midiToName).join(", ")}] with voice "${upperSummary}" (Full Keyboard — Kbd Set "${state.kbdSetName}")${ensNote}${octNote}${subScaleNote}`;
    }

    const lowerNotes = notes.filter(m => m < splitMidi);
    const upperNotes = notes.filter(m => m >= splitMidi);

    const parts = [];
    if (lowerNotes.length > 0) {
      if (state.manualBass) {
        parts.push(`Lower Manual Bass [< ${midiToName(splitMidi)}]: notes [${lowerNotes.map(midiToName).join(", ")}]`);
      } else {
        const lowSound = state.tracks.low.muted ? "(Lower Muted)" : state.tracks.low.sound;
        parts.push(`Lower [< ${midiToName(splitMidi)}]: Chord ${state.recognizedChord || "N/A"} + Lower voice "${lowSound}" (${lowerNotes.map(midiToName).join(", ")})`);
      }
    }
    if (upperNotes.length > 0) {
      const crossedHint = (rootMidi < splitMidi)
        ? ` (crossed >= ${midiToName(splitMidi)} Split Point!)`
        : "";
      parts.push(`Upper [>= ${midiToName(splitMidi)}]: notes [${upperNotes.map(midiToName).join(", ")}]${crossedHint} with "${upperSummary}"${ensNote}${octNote}${subScaleNote}`);
    }
    return parts.join("  ||  ");
  }

  // =========================================================================
  // UPDATE ALL VISUALS (LEDS, PIANO KEYS, TOUCHVIEW, LIVE CONSOLE)
  // =========================================================================
  function setLed(id, color, blink) {
    const el = document.getElementById(`led_${id}`);
    if (!el) return;
    el.className = "hw-led";
    if (!state.powerOn) {
      if (id === "power") el.classList.add("amber");
      return;
    }
    if (color) el.classList.add(color);
    if (blink) el.classList.add("blink");
  }

  function updateLedVisuals() {
    document.getElementById("faceplate").classList.toggle("standby-off", !state.powerOn);
    const shiftBtn = document.getElementById("hw_shift");
    if (shiftBtn) shiftBtn.classList.toggle("shift-latched", state.shiftLatched);

    // Clear all LEDs first
    BUTTON_DEFS.forEach(bd => {
      if (bd.led) setLed(bd.id, null, false);
    });

    if (!state.powerOn) {
      setLed("power", "amber", false);
      return;
    }

    setLed("power", "red", false);

    // Modes
    setLed("mode_style", state.mode === "style" ? "red" : null, false);
    setLed("mode_song", state.mode === "song" ? "red" : null, false);
    setLed("mode_seq", state.mode === "seq" ? "red" : null, false);
    setLed("mode_sound", state.mode === "sound" ? "red" : null, false);

    // Player
    setLed("player_play", state.playerRunning ? "red" : null, false);

    // Chord Seq (bi-color red/green!)
    if (state.chordSeqState === "rec") setLed("chord_seq", "red", true);
    else if (state.chordSeqState === "play") setLed("chord_seq", "green", false);

    // Accomp / Memory / Manual Bass / Style to Kbd / MP3 Rec
    if (state.accompOn) setLed("accomp", "red", false);
    if (state.memoryOn) setLed("memory", "red", false);
    if (state.manualBass) setLed("manual_bass", "red", false);
    if (state.styleToKbdMode === "on") setLed("style_to_kbd", "red", false);
    else if (state.styleToKbdMode === "blink") setLed("style_to_kbd", "red", true);
    if (state.mp3Recording) setLed("mp3_rec", "red", true);

    // Tempo Lock / Metronome / Split / Ensemble
    if (state.tempoLock) setLed("tempo_lock", "red", false);
    if (state.metronomeOn) setLed("metronome", "red", state.arrangerRunning);
    if (state.splitOn) setLed("split", "red", state.splitDialogOpen);
    if (state.ensembleOn) setLed("ensemble", "red", false);

    // Intros 1-3
    for (let i = 1; i <= 3; i++) {
      if (state.activeIntro === i) {
        const blink = (state.arrangerRunning && state.activeSection === "intro" && state.loopSection);
        setLed(`intro_${i}`, "red", blink);
      }
    }

    // Variations 1-4
    for (let v = 1; v <= 4; v++) {
      if (!state.arrangerRunning) {
        if (state.activeVariation === v) {
          // Blinks if an Intro is booked ahead of it! (Manual p. 59)
          setLed(`var_${v}`, "red", state.activeIntro !== null);
        }
      } else {
        if (state.bookedVariation === v) {
          setLed(`var_${v}`, "red", true);
        } else if (state.activeVariation === v && state.activeSection === "var") {
          setLed(`var_${v}`, "red", false);
        } else if (state.activeVariation === v && state.activeSection !== "var" && !state.bookedVariation) {
          setLed(`var_${v}`, "red", true);
        }
      }
    }

    // Auto Fill & Break & Endings
    if (state.autoFill) {
      setLed("auto_fill", "red", state.arrangerRunning && state.activeSection === "fill");
    }
    if (state.arrangerRunning && state.activeSection === "break") {
      setLed("break_btn", "red", state.loopSection);
    }
    for (let e = 1; e <= 3; e++) {
      if (state.activeEnding === e) {
        setLed(`ending_${e}`, "red", state.loopSection);
      }
    }

    // Synchro Start/Stop, Bi-Color START/STOP, Fade In/Out
    if (state.synchroStart) setLed("synchro_start", "red", !state.arrangerRunning);
    if (state.synchroStop) setLed("synchro_stop", "red", false);
    if (state.arrangerRunning) {
      setLed("start_stop", state.currentBeat === 1 ? "red" : "green", false);
    } else if (state.photoLedOverrideStartGreen) {
      setLed("start_stop", "green", false);
    }
    if (state.fadeState) setLed("fade_inout", "red", true);

    // SongBook, Set List & 9 Kbd Set Library / Set List LEDs
    if (state.overlayWindow === "songbook") setLed("song_book", "red", false);
    if (state.setListMode) {
      setLed("set_list", "red", false);
      for (let i = 1; i <= 9; i++) {
        // In Set List mode all available Set List slots illuminate (active slot solid, or matching photo!)
        setLed(`ksl_${i}`, "red", state.photoLedOverrideAllSetList ? false : (state.activeSetListSlot === i ? false : false));
        if (!state.photoLedOverrideAllSetList && state.activeSetListSlot !== i) {
          setLed(`ksl_${i}`, null, false);
        }
      }
    } else {
      const activeCatObj = DATA.libraryCategories.find(c => c.id === state.activeLibCategory);
      if (activeCatObj && state.activeStyleKbdSlot === null && state.kbdSetName !== "My Setting") {
        setLed(`ksl_${activeCatObj.buttonNumber || activeCatObj.num}`, "red", false);
      }
    }

    // Oriental Sub-Scale LEDs (both dock & wing copies)
    document.querySelectorAll("[data-subscale-led]").forEach(el => {
      const pc = parseInt(el.dataset.subscaleLed, 10);
      el.className = state.subScaleNotes.includes(pc) ? "hw-led red" : "hw-led";
    });
    document.querySelectorAll("[data-sc-led]").forEach(el => {
      const scId = parseInt(el.dataset.scLed, 10);
      el.className = state.activeSubScalePreset === scId ? "hw-led red" : "hw-led";
    });

    const subSum = document.getElementById("subScaleSummary");
    if (subSum) {
      subSum.textContent = state.subScaleNotes.length === 0
        ? "Equal (0c)"
        : state.subScaleNotes.map(n => NOTE_NAMES[n] + "½♭").join(" ");
    }
  }

  function updatePianoVisuals() {
    const splitMidi = getEffectiveSplit();
    const keys = document.querySelectorAll(".piano-key");
    const drillTargetKey = getActiveDrillTarget().targetKey;

    keys.forEach(k => {
      const m = parseInt(k.dataset.midi, 10);
      k.classList.remove("active-upper", "active-lower", "root-pressed", "split-marker-key", "drill-target");
      if (state.splitOn && m === splitMidi) {
        k.classList.add("split-marker-key");
      }
      if (drillTargetKey === m) {
        k.classList.add("drill-target");
      }
      if (state.pressedMidiNotes.includes(m)) {
        if (state.splitOn && m < splitMidi) k.classList.add("active-lower");
        else k.classList.add("active-upper");
      }
      if (state.clickedRootMidi === m) {
        k.classList.add("root-pressed");
      }
    });

    // Update Split Zone Bar proportions above 61 keys
    const lowerEl = document.getElementById("zoneLowerLabel");
    const upperEl = document.getElementById("zoneUpperLabel");
    if (!state.splitOn) {
      lowerEl.style.width = "0%";
      lowerEl.textContent = "";
      upperEl.textContent = `FULL KEYBOARD MODE (SPLIT OFF) — Upper Voices [${state.kbdSetName}] across C2–C7`;
    } else {
      const pct = Math.max(6, Math.min(92, ((splitMidi - 36) / 61) * 100));
      lowerEl.style.width = `${pct}%`;
      const spName = midiToName(splitMidi);
      lowerEl.textContent = `LOWER / CHORDS (< ${spName})`;
      upperEl.textContent = `UPPER 1–3 VOICES (>= ${spName}: ${state.tracks.up1.sound})`;
    }

    // Highlight drill target button on panel
    const drillBtn = getActiveDrillTarget().targetBtn;
    document.querySelectorAll(".hw-btn").forEach(b => {
      b.classList.toggle("drill-target", b.dataset.btnId === drillBtn);
    });
  }

  function updateReadouts() {
    const pVoice = document.getElementById("hudPillVoice");
    const pDnc = document.getElementById("hudPillDnc");
    const pStyle = document.getElementById("hudPillStyle");
    const pChord = document.getElementById("hudPillChord");
    const pSplit = document.getElementById("hudPillSplit");
    if (!pVoice) return;

    if (!state.powerOn) {
      pVoice.textContent = "Standby (Power OFF)";
      if (pDnc) pDnc.style.display = "none";
      pStyle.textContent = "---";
      pChord.textContent = "---";
      pSplit.textContent = "---";
      return;
    }

    const upActive = ["up1", "up2", "up3"]
      .filter(k => !state.tracks[k].muted)
      .map(k => state.tracks[k].sound);
    pVoice.textContent = `${state.kbdSetName}: ${upActive.join(" + ") || "Muted"}`;

    if (pDnc) {
      const selSound = state.tracks[state.selectedTrackKey] ? state.tracks[state.selectedTrackKey].sound : state.tracks.up1.sound;
      const rec = resolveSoundRecord(selSound);
      if (rec && rec.dnc) {
        const d = rec.dnc;
        const notes = [];
        if (d.sc1On) notes.push(`SW1: ${d.sc1On}`);
        if (d.sc2On) notes.push(`SW2: ${d.sc2On}`);
        if (d.yPlus) notes.push(`Y+: ${d.yPlus}`);
        if (d.yMinus) notes.push(`Y-: ${d.yMinus}`);
        if (d.legatoIn) notes.push(`Legato: ${d.legatoIn}`);
        if (d.afterTouch) notes.push(`AT: ${d.afterTouch}`);
        pDnc.style.display = "inline-flex";
        pDnc.textContent = `DNC: ${rec.name}`;
        pDnc.title = notes.join(" | ") || `${rec.name} DNC`;
      } else {
        pDnc.style.display = "none";
      }
    }

    const st = getCurrentStyle();
    let secTag = `Var ${state.activeVariation}`;
    if (state.arrangerRunning) {
      if (state.activeSection === "intro") secTag = `Intro ${state.activeIntro}`;
      else if (state.activeSection === "fill") secTag = `Fill ${state.activeFill}`;
      else if (state.activeSection === "break") secTag = "Break";
      else if (state.activeSection === "ending") secTag = `End ${state.activeEnding}`;
      pStyle.textContent = `▶ ${st.name} (${secTag} • ${state.tempo} BPM)`;
    } else {
      pStyle.textContent = `■ ${st.name} (${secTag} • ${state.tempo} BPM)`;
    }

    pChord.textContent = `Chord: ${state.recognizedChord || "---"}`;
    const spName = midiToName(getEffectiveSplit());
    pSplit.textContent = state.splitOn ? `Split: ${spName}` : "Split: FULL";
  }

  // =========================================================================
  // TOUCHVIEW 7" COLOR DISPLAY RENDERER (AUTHENTIC PA700 OS v1.5)
  // =========================================================================
  function renderTouchView() {
    const screen = document.getElementById("touchviewScreen");
    screen.style.filter = state.powerOn ? `brightness(${0.45 + (state.displayBrightness / 100) * 0.65})` : "brightness(0.03)";
    if (!state.powerOn) {
      screen.innerHTML = "";
      return;
    }

    const st = getCurrentStyle();
    const trStr = `b/#: ${state.masterTranspose > 0 ? "+" : ""}${state.masterTranspose}`;
    const chordBadge = state.recognizedChord || "---";

    // Determine Title Bar Mode Color & Label
    let titleClass = "tv-titlebar";
    let titleLabel = "Style Play";
    if (state.overlayWindow === "songbook") {
      titleClass += " mode-songbook";
      titleLabel = "SongBook";
    } else if (state.overlayWindow === "global") {
      titleClass += " mode-global";
      titleLabel = "Global";
    } else if (state.mode === "song") {
      titleClass += " mode-song";
      titleLabel = "Song Play";
    } else if (state.mode === "seq") {
      titleClass += " mode-seq";
      titleLabel = "Backing Sequencer";
    } else if (state.mode === "sound") {
      titleClass += " mode-sound";
      titleLabel = "Sound Edit";
    }

    let bodyHtml = renderStylePlayMainBody(st);
    if (state.overlayWindow) {
      bodyHtml += renderOverlayWindow(st);
    }
    if (state.splitDialogOpen) {
      bodyHtml += `
        <div class="tv-dialog-backdrop">
          <div class="tv-split-dialog">
            <div class="dlg-head">Split Point</div>
            <div class="dlg-body">
              <strong>Press a key on the keyboard below to set</strong><br/>
              Current: <span style="color:#fde047;font-weight:800;">${midiToName(getEffectiveSplit())}</span><br/>
              or press <strong>EXIT</strong> to Cancel
            </div>
          </div>
        </div>
      `;
    }

    screen.innerHTML = `
      <div class="${titleClass}">
        <span>${escapeHtml(titleLabel)}</span>
        <span>${escapeHtml(trStr)}</span>
        <span class="tv-chord-badge">${escapeHtml(chordBadge)}</span>
        <span style="font-size:0.55cqi;">&#9660;</span>
      </div>
      <div class="tv-body">${bodyHtml}</div>
    `;

    bindTouchViewEvents(screen);
  }

  function renderStylePlayMainBody(st) {
    // Beat dots
    const dots = [];
    for (let b = 1; b <= st.beatsPerBar; b++) {
      let cls = "tv-beat-dot";
      if (state.arrangerRunning && state.currentBeat === b) {
        cls += b === 1 ? " active-1" : " active-n";
      }
      dots.push(`<span class="${cls}"></span>`);
    }

    const secBadge = state.arrangerRunning
      ? (state.activeSection === "var" ? `Var ${state.activeVariation}` : state.activeSection.toUpperCase())
      : `Var ${state.activeVariation}`;

    const trackRowsHtml = ["up1", "up2", "up3", "low"].map(tk => {
      const t = state.tracks[tk];
      const sel = state.selectedTrackKey === tk ? "selected" : "";
      const mut = t.muted ? "muted" : "";
      const oct = (tk === "low" ? t.octave : t.octave + state.upperOctave);
      const octStr = oct > 0 ? `+${oct}` : `${oct}`;
      const labelTag = tk.toUpperCase();
      return `
        <div class="tv-track-row ${sel} ${mut}" data-tv-track="${tk}">
          <div class="tv-trk-info">
            <div class="tv-trk-sound">${escapeHtml(t.sound)}</div>
            <div class="tv-trk-sub">
              ${tk === "low" && t.backing ? `<span class="tv-backing-pill">BACKING</span>` : ""}
              <span>Oct [${octStr}]</span>
            </div>
          </div>
          <button type="button" class="tv-trk-mute-btn ${t.muted ? "muted" : "playing"}" data-tv-mute="${tk}">
            <span>${t.muted ? "MUTE" : "PLAY"}</span>
            <span>${labelTag}</span>
          </button>
        </div>
      `;
    }).join("");

    const lowerPaneHtml = renderMainLowerPane(st);
    const tabs = [
      { id: "kbd_set", label: "Kbd Set" },
      { id: "volume", label: "Volume" },
      { id: "pad", label: "Pad" },
      { id: "split", label: "Split" },
      { id: "sub_scale", label: "Sub Scale" },
      { id: "kaoss", label: "KAOSS" },
      { id: "mic", label: "Mic" }
    ];
    const tabsHtml = tabs.map(tb =>
      `<div class="tv-tab ${state.mainBottomTab === tb.id ? "active" : ""}" data-tv-tab="${tb.id}">${tb.label}</div>`
    ).join("");

    const songObj = DATA.playerSongs[state.currentSongIdx];

    return `
      <div class="tv-main-grid">
        <div class="tv-left-resources">
          <div class="tv-res-box style-box" data-tv-action="open_style_select">
            <div class="tv-vert-tag">S<br/>T<br/>Y<br/>L<br/>E</div>
            <div class="tv-res-content">
              <div class="tv-style-name">${escapeHtml(st.name)}</div>
              <div class="tv-meta-row">
                <span>Bank: ${escapeHtml(st.bank)}</span>
                <span style="color:#fde047;font-weight:700;">${secBadge}</span>
              </div>
              <div class="tv-meta-row">
                <span>Meter: ${st.meter}</span>
                <span>M: ${state.currentBar}/${st.patternBars}</span>
              </div>
              <div class="tv-tempo-row">
                <div class="tv-beat-dots">${dots.join("")}</div>
                <div class="tv-tempo-box ${state.focusedParam === "tempo" ? "focused" : ""}" data-tv-action="focus_tempo">
                  &#9833; = ${state.tempo}${state.tempoLock ? "🔒" : ""}
                </div>
              </div>
            </div>
          </div>

          <div class="tv-res-box song-box" data-tv-action="cycle_song">
            <div class="tv-vert-tag">P<br/>L<br/>Y</div>
            <div class="tv-res-content" style="justify-content:center;">
              <div class="tv-song-name">${escapeHtml(songDisplayTitle(songObj))}</div>
              <div class="tv-meta-row"><span>${state.playerRunning ? "Playing" : "Stopped"} • Bar ${String(state.playerBar).padStart(3, "0")}</span></div>
            </div>
          </div>

          <div class="tv-res-box kbd-box" data-tv-action="open_kbd_select">
            <div class="tv-vert-tag">K<br/>B<br/>D</div>
            <div class="tv-res-content" style="justify-content:center;">
              <div class="tv-kbdset-name">${escapeHtml(state.kbdSetName)}</div>
              <div class="tv-meta-row"><span>${escapeHtml(state.kbdSetSource)}</span></div>
            </div>
          </div>
        </div>

        <div class="tv-right-tracks">${trackRowsHtml}</div>
      </div>

      <div class="tv-lower-pane">${lowerPaneHtml}</div>
      <div class="tv-tabs">${tabsHtml}</div>
    `;
  }

  function renderMainLowerPane(st) {
    if (state.mainBottomTab === "kbd_set") {
      return st.kbdSets.map((ks, idx) => `
        <div class="tv-kbdset-slot ${state.activeStyleKbdSlot === idx ? "active" : ""}" data-tv-stylekbd="${idx}">
          <span class="slot-num">[ ${idx + 1} ]</span>
          <span class="slot-label">${escapeHtml(ks.name)}</span>
        </div>
      `).join("");
    }

    if (state.mainBottomTab === "split") {
      const sp = midiToName(getEffectiveSplit());
      return `
        <div style="display:flex;align-items:center;justify-content:space-between;width:100%;font-size:0.60cqi;gap:6px;">
          <div data-tv-action="open_split_dlg" style="cursor:pointer;background:#2f333a;padding:3px 6px;border:1px solid #fbbf24;border-radius:3px;">
            Set Point: <strong style="color:#fde047;">${sp}</strong> (Touch or use VALUE)
          </div>
          <label style="display:flex;align-items:center;gap:3px;cursor:pointer;">
            <input type="checkbox" id="tvGlobalSplitChk" ${state.useGlobalSplit ? "checked" : ""} /> Global
          </label>
          <label style="display:flex;align-items:center;gap:3px;cursor:pointer;">
            <input type="checkbox" id="tvBassInvChk" ${state.bassInversion ? "checked" : ""} /> Bass Inv.
          </label>
        </div>
      `;
    }

    if (state.mainBottomTab === "pad") {
      return getStylePads(st).map((p, idx) => `
        <div class="tv-kbdset-slot ${state.padsActive[idx] ? "active" : ""}" data-tv-pad="${idx}" title="Click to trigger PAD ${idx + 1}; double-click or click Pick to choose from 415 Pads">
          <div style="display:flex;justify-content:space-between;width:100%;align-items:center;">
            <span class="slot-num">PAD ${idx + 1} (${p.type === "Loop" ? "SEQ" : "HIT"})</span>
            <span data-tv-editpad="${idx}" style="font-size:0.46cqi;background:#334155;color:#fde68a;padding:0 3px;border-radius:2px;cursor:pointer;">Pick</span>
          </div>
          <span class="slot-label">${escapeHtml(p.name)}</span>
        </div>
      `).join("");
    }

    if (state.mainBottomTab === "volume") {
      if (state.volumeTrackView === "style_tracks") {
        const curStyle = getCurrentStyle();
        const sTracks = curStyle.styleTracks || [];
        const names = ["Drum", "Perc", "Bass", "Acc1", "Acc2", "Acc3", "Acc4", "Acc5"];
        return names.map((nm, idx) => {
          const sndName = sTracks[idx] ? sTracks[idx].sound : nm;
          const shortSnd = sndName.length > 10 ? sndName.slice(0, 9) + "…" : sndName;
          const muted = Boolean(state.styleTrackMutes[idx]) || (idx >= 2 && (!state.accompOn || state.manualBass));
          return `
            <div class="tv-kbdset-slot" data-tv-style-mute="${idx}" title="${escapeHtml(nm + ": " + sndName + " (Click to Mute/Play)")}" style="padding:1px;cursor:pointer;">
              <span class="slot-num">${nm}</span>
              <span style="font-size:0.46cqi;color:#cbd5e1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${escapeHtml(shortSnd)}</span>
              <span style="font-size:0.48cqi;color:${muted ? "#f87171" : "#4ade80"};">${muted ? "MUTE" : "PLAY"}</span>
            </div>
          `;
        }).join("");
      }
      return ["up1", "up2", "up3", "low"].map(tk => `
        <div class="tv-kbdset-slot" data-tv-mute="${tk}">
          <span class="slot-num">${tk.toUpperCase()} (${state.tracks[tk].volume})</span>
          <span class="slot-label" style="color:${state.tracks[tk].muted ? "#f87171" : "#4ade80"};">${state.tracks[tk].muted ? "MUTED" : "ACTIVE"}</span>
        </div>
      `).join("");
    }

    if (state.mainBottomTab === "sub_scale") {
      return `
        <div style="display:flex;align-items:center;justify-content:space-between;width:100%;font-size:0.58cqi;">
          <span>Quarter-Tone (-50c): <strong style="color:#fca5a5;">${state.subScaleNotes.length ? state.subScaleNotes.map(n => NOTE_NAMES[n]).join(", ") : "None (Equal)"}</strong></span>
          <button type="button" class="tv-cat-btn" data-tv-action="reset_subscale">Reset Scale</button>
        </div>
      `;
    }

    if (state.mainBottomTab === "kaoss") {
      return `<div style="width:100%;text-align:center;font-size:0.60cqi;color:#38bdf8;">KAOSS XY Midi/FX Pad Ready — Arpeggiator &amp; Filter Sweep Synced (${state.tempo} BPM)</div>`;
    }

    return `<div style="width:100%;text-align:center;font-size:0.60cqi;color:#a7f3d0;">Mic &amp; Voice Processor: 3-Part Vocal Harmony (Follows Chord ${state.recognizedChord || "---"})</div>`;
  }

  function renderSelectWindow(cfg) {
    const cats = cfg.categories || [];
    const splitAt = cats.length <= 12 ? Math.min(6, Math.ceil(cats.length / 2)) : Math.ceil(cats.length / 2);
    const leftCats = cats.slice(0, splitAt);
    const rightCats = cats.slice(splitAt);
    const compactStyle = cats.length > 12 ? ` style="font-size:7px;padding:1px 3px;"` : "";
    const renderCatCol = (colCats) => colCats.map(c =>
      `<button type="button" class="tv-cat-tab ${c.active ? "active" : ""}"${compactStyle} ${cfg.catAttr}="${escapeHtml(c.id)}" title="${escapeHtml(c.label)} (${c.count})">${escapeHtml(c.label)}</button>`
    ).join("");

    const totalItems = cfg.items.length;
    const perPage = 8;
    const totalPages = Math.max(1, Math.ceil(totalItems / perPage));
    const page = Math.max(0, Math.min(cfg.page || 0, totalPages - 1));
    const slice = cfg.items.slice(page * perPage, (page + 1) * perPage);
    const cardsHtml = [];
    for (let i = 0; i < perPage; i++) {
      const it = slice[i];
      if (!it) {
        cardsHtml.push(`<div class="tv-slot-card blank"><span class="tv-slot-name">---</span></div>`);
      } else {
        const card = cfg.renderItemCard(it, page * perPage + i);
        cardsHtml.push(`
          <button type="button" class="tv-slot-card ${card.active ? "active" : ""}" ${card.pickAttr}="${escapeHtml(String(card.pickVal))}" title="${escapeHtml(card.tooltip || card.name)}">
            <span class="tv-slot-name">${escapeHtml(card.name)}</span>
            <span class="tv-slot-sub">${escapeHtml(card.sub || "")}</span>
          </button>
        `);
      }
    }

    const pagePills = [];
    for (let p = 0; p < totalPages; p++) {
      pagePills.push(`<button type="button" class="tv-page-pill ${p === page ? "active" : ""}" data-tv-selpage="${p}">P${p + 1}</button>`);
    }

    return `
      <div class="tv-window">
        <div class="tv-select-win">
          <div class="tv-sel-topbar">
            <span class="tv-sel-title">${escapeHtml(cfg.title)}</span>
            <div class="tv-type-tabs">${cfg.topTabsHtml || ""}</div>
            <div style="display:flex;align-items:center;gap:3px;">
              <button type="button" class="tv-hold-btn ${state.displayHold ? "active" : ""}" data-tv-hold="1" title="Display Hold: keep browser open after tapping an item">HOLD</button>
              <button type="button" class="tv-close-btn" data-tv-close="1" title="Close (EXIT)">&#10005;</button>
            </div>
          </div>
          <div class="tv-sel-body">
            <div class="tv-cat-col">${renderCatCol(leftCats)}</div>
            <div class="tv-col-grid">${cardsHtml.join("")}</div>
            <div class="tv-cat-col">${renderCatCol(rightCats)}</div>
          </div>
          ${cfg.dncBannerHtml || ""}
          <div class="tv-bank-footer">
            <span style="font-size:8px;color:#94a3b8;">${totalItems ? `${page * perPage + 1}-${Math.min(totalItems, (page + 1) * perPage)} / ${totalItems}` : "0 items"}</span>
            <div class="tv-bank-pills">${pagePills.join("")}</div>
          </div>
        </div>
      </div>
    `;
  }

  function getSearchMatches(query, scope) {
    const q = String(query || "").trim().toLowerCase();
    const out = [];
    const maxItems = 60;
    const matchText = (txt) => !q || String(txt || "").toLowerCase().includes(q);

    if (scope === "all" || scope === "style") {
      DATA.styles.forEach((s, idx) => {
        if (out.length < maxItems && (matchText(s.name) || matchText(s.category) || matchText(s.bank))) {
          out.push({ kind: "style", name: s.name, sub: `Style • ${s.category} • ${s.meter} • ${s.tempo} BPM`, val: String(idx) });
        }
      });
    }
    if (scope === "all" || scope === "kbd") {
      (DATA.allKbdSets || []).forEach((k) => {
        if (out.length < maxItems && (matchText(k.name) || matchText(k.category) || matchText(k.up1 && k.up1.sound))) {
          out.push({ kind: "kbd", name: k.name, sub: `Kbd Set • ${k.category} (${k.up1 ? k.up1.sound : ""})`, val: `${k.categoryId}:${k.pc}` });
        }
      });
    }
    if (scope === "all" || scope === "sound") {
      (DATA.sounds || []).forEach((s) => {
        if (out.length < maxItems && (matchText(s.name) || matchText(s.group) || matchText(s.type))) {
          out.push({ kind: "sound", name: s.name, sub: `Sound (${s.type}) • ${s.group}${s.dnc ? " • DNC" : ""}`, val: s.name });
        }
      });
    }
    if (scope === "all" || scope === "pad") {
      (DATA.pads || []).forEach((p) => {
        if (out.length < maxItems && (matchText(p.name) || matchText(p.group))) {
          out.push({ kind: "pad", name: p.name, sub: `Pad (${p.type}) • ${p.group}`, val: p.id });
        }
      });
    }
    return out;
  }

  function renderSearchResultCards(matches) {
    if (!matches.length) {
      return `<div style="grid-column:1 / -1;padding:12px;text-align:center;color:#94a3b8;font-size:9px;">No matching Styles, Keyboard Sets, Sounds, or Pads.</div>`;
    }
    return matches.map((m) => `
      <button type="button" class="tv-slot-card" data-tv-searchkind="${escapeHtml(m.kind)}" data-tv-searchval="${escapeHtml(m.val)}">
        <span class="tv-slot-name">${escapeHtml(m.name)}</span>
        <span class="tv-slot-sub">${escapeHtml(m.sub)}</span>
      </button>
    `).join("");
  }

  function renderOverlayWindow(st) {
    // 1. SongBook Set List 3x3 Grid
    if (state.overlayWindow === "songbook") {
      const tiles = DATA.setListEntries.map(e => `
        <div class="tv-setlist-tile ${state.activeSetListSlot === e.slot ? "active" : ""}" data-tv-setlist="${e.slot}">
          <div class="sl-top">
            <span style="background:#fff;color:#b91c1c;padding:0 2px;border-radius:1px;">${escapeHtml(e.type)}</span>
            <span class="sl-num">${e.slot}</span>
          </div>
          <div class="sl-title">${escapeHtml(e.title)}</div>
        </div>
      `).join("");
      return `
        <div class="tv-window">
          <div style="background:#8a92a8;color:#111;padding:2px 6px;font-size:0.56cqi;font-weight:800;display:flex;justify-content:space-between;">
            <span>List: <strong style="background:#fff;padding:0 8px;">Pop</strong></span>
            <span>Press EXIT to return</span>
          </div>
          <div class="tv-setlist-grid">${tiles}</div>
        </div>
      `;
    }

    // 2. Style Select Window (All 379 Manual Styles across 12 categories + P1..P5 pages)
    if (state.overlayWindow === "style_select") {
      if (!window._pa700StyleIdxById) {
        window._pa700StyleIdxById = new Map(DATA.styles.map((s, idx) => [s.id, idx]));
      }
      const activeCat = state.styleBrowseCat || st.category;
      const catIds = (DATA.styleIdsByCategory && DATA.styleIdsByCategory[activeCat]) || [];
      const catItems = catIds.map(id => {
        const idx = window._pa700StyleIdxById.get(id);
        return idx !== undefined ? { style: DATA.styles[idx], idx } : null;
      }).filter(Boolean);
      return renderSelectWindow({
        title: `STYLE SELECT (${DATA.styles.length})`,
        topTabsHtml: `<button type="button" class="tv-type-tab" data-tv-opensearch="style">Find...</button>`,
        categories: DATA.styleCategories.map(c => ({
          id: c,
          label: c,
          count: (DATA.styleIdsByCategory[c] || []).length,
          active: activeCat === c
        })),
        catAttr: "data-tv-stylecat",
        items: catItems,
        page: state.styleBrowsePage,
        renderItemCard: ({ style, idx }) => ({
          name: style.name,
          sub: `${style.meter} • ${style.tempo} BPM • ${style.bank}`,
          tooltip: `${style.name} (${style.category}, ${style.meter}, ${style.tempo} BPM, PC ${style.pc})`,
          active: state.currentStyleIdx === idx,
          pickAttr: "data-tv-pickstyle",
          pickVal: idx
        })
      });
    }

    // 3. Keyboard Set Library Select Window (All 298 Manual Sets across 9 categories)
    if (state.overlayWindow === "kbd_lib_select") {
      const activeCat = state.kbdBrowseCat || state.activeLibCategory || "piano";
      const items = DATA.keyboardSetLibrary[activeCat] || [];
      return renderSelectWindow({
        title: `KEYBOARD SET LIBRARY (${DATA.allKbdSets ? DATA.allKbdSets.length : 298})`,
        topTabsHtml: `<button type="button" class="tv-type-tab" data-tv-opensearch="kbd">Find...</button>`,
        categories: DATA.libraryCategories.map(c => ({
          id: c.id,
          label: `${c.buttonNumber}. ${c.label}`,
          count: (DATA.keyboardSetLibrary[c.id] || []).length,
          active: activeCat === c.id
        })),
        catAttr: "data-tv-libcat",
        items,
        page: state.kbdBrowsePage,
        renderItemCard: (it, idx) => ({
          name: it.name,
          sub: `${it.up1 ? it.up1.sound : ""}${it.up2 && !it.up2.muted ? " + " + it.up2.sound : ""}`,
          tooltip: `${it.name} — UP1: ${it.up1 ? it.up1.sound : ""}`,
          active: state.activeStyleKbdSlot === null && state.activeLibCategory === activeCat && state.kbdSetName === it.name,
          pickAttr: "data-tv-picklib",
          pickVal: idx
        })
      });
    }

    // 4. Sound Select Window (All 1,845 Manual Sounds + Drum Kits + DNC bar)
    if (state.overlayWindow === "sound_select") {
      const curType = state.soundBrowseType || "Factory";
      const groupsMap = (DATA.soundGroupsByType && DATA.soundGroupsByType[curType]) || {};
      const groupNames = Object.keys(groupsMap);
      const activeGroup = groupNames.includes(state.soundBrowseGroup) ? state.soundBrowseGroup : (groupNames[0] || "Piano");
      const items = getSoundBankItems(curType, activeGroup);
      const curSound = state.tracks[state.selectedTrackKey].sound;
      const curRec = resolveSoundRecord(curSound);
      let dncBannerHtml = "";
      if (curRec && curRec.dnc) {
        const d = curRec.dnc;
        const caps = [
          d.sc1On ? `SW1:${d.sc1On}` : "",
          d.sc2On ? `SW2:${d.sc2On}` : "",
          d.yPlus ? `Y+:${d.yPlus}` : "",
          d.yMinus ? `Y-:${d.yMinus}` : "",
          d.legatoIn ? `Legato:${d.legatoIn}` : ""
        ].filter(Boolean).join(" • ");
        dncBannerHtml = `<div class="tv-dnc-strip">DNC (${escapeHtml(curRec.name)}): ${escapeHtml(caps || "Articulation Active")}</div>`;
      }
      const typeTabs = (DATA.soundTypes || ["Factory", "Legacy", "GM/XG"]).map(tp =>
        `<button type="button" class="tv-type-tab ${curType === tp ? "active" : ""}" data-tv-soundtype="${escapeHtml(tp)}">${escapeHtml(tp)}</button>`
      ).join("") + `<button type="button" class="tv-type-tab" data-tv-cycletrack="1" title="Switch target track (UP1/UP2/UP3/LOW)">[${state.selectedTrackKey.toUpperCase()}]</button>`;

      return renderSelectWindow({
        title: `SOUND SELECT (${DATA.sounds.length})`,
        topTabsHtml: typeTabs,
        categories: groupNames.map(g => ({
          id: g,
          label: g,
          count: (groupsMap[g] || []).length,
          active: activeGroup === g
        })),
        catAttr: "data-tv-soundgroup",
        items,
        page: state.soundBrowsePage,
        dncBannerHtml,
        renderItemCard: (snd) => ({
          name: snd.name,
          sub: `${snd.isDrum ? "DRUM KIT" : `CC ${snd.cc00}.${snd.cc32}.${snd.pc}`}${snd.dnc ? " • DNC" : ""}`,
          tooltip: `${snd.name} (${snd.type} • ${snd.group} • CC0:${snd.cc00} CC32:${snd.cc32} PC:${snd.pc})`,
          active: curSound === snd.name,
          pickAttr: "data-tv-picksound",
          pickVal: snd.name
        })
      });
    }

    // 5. Pad Select Window (All 415 Manual Pads across HIT & SEQ groups)
    if (state.overlayWindow === "pad_select") {
      const bankType = state.padBrowseBank || "HIT";
      const bankGroups = (DATA.padGroups || []).filter(g => g.bankType === bankType);
      const activeGroup = bankGroups.some(g => g.name === state.padBrowseGroup)
        ? state.padBrowseGroup
        : (bankGroups[0] ? bankGroups[0].name : "");
      const items = getPadBankItems(activeGroup);
      const curSlotPad = getStylePads(st)[state.padSelectSlot];
      const topTabs = ["HIT", "SEQ"].map(bk =>
        `<button type="button" class="tv-type-tab ${bankType === bk ? "active" : ""}" data-tv-padbank="${bk}">${bk}</button>`
      ).join("") + `<button type="button" class="tv-type-tab" data-tv-padslot="1" title="Cycle Target Pad Slot 1..4">Slot ${state.padSelectSlot + 1}</button>`;

      return renderSelectWindow({
        title: `PAD SELECT (${DATA.pads.length})`,
        topTabsHtml: topTabs,
        categories: bankGroups.map(g => ({
          id: g.name,
          label: g.name.replace(/^(HIT|SEQ)\s*-\s*/i, ""),
          count: g.padIds.length,
          active: activeGroup === g.name
        })),
        catAttr: "data-tv-padgroup",
        items,
        page: state.padBrowsePage,
        renderItemCard: (p) => ({
          name: p.name,
          sub: `${p.type === "Loop" ? "SEQ Loop" : "HIT Shot"} • #${p.slot}`,
          tooltip: `${p.name} (${p.group})`,
          active: Boolean(curSlotPad && curSlotPad.name === p.name),
          pickAttr: "data-tv-pickpad",
          pickVal: p.id
        })
      });
    }

    // 6. Real-Time Search Overlay across 379 Styles, 298 Kbd Sets, 1,845 Sounds, 415 Pads
    if (state.overlayWindow === "search") {
      const matches = getSearchMatches(state.searchQuery, state.searchScope);
      const scopes = [
        { id: "all", lbl: "All" },
        { id: "style", lbl: "Styles" },
        { id: "kbd", lbl: "Kbd Sets" },
        { id: "sound", lbl: "Sounds" },
        { id: "pad", lbl: "Pads" }
      ];
      return `
        <div class="tv-window">
          <div class="tv-search-win">
            <div class="tv-search-bar">
              <input id="tvSearchInput" class="tv-search-input" type="text" placeholder="Search 379 Styles, 298 Kbd Sets, 1,845 Sounds, 415 Pads..." value="${escapeHtml(state.searchQuery)}" />
              <span id="tvSearchCount" style="font-size:8.5px;color:#93c5fd;white-space:nowrap;">${matches.length}${matches.length >= 60 ? "+" : ""} hits</span>
              <button type="button" class="tv-close-btn" data-tv-close="1">&#10005;</button>
            </div>
            <div class="tv-type-tabs">
              ${scopes.map(sc => `<button type="button" class="tv-type-tab ${state.searchScope === sc.id ? "active" : ""}" data-tv-searchscope="${sc.id}">${sc.lbl}</button>`).join("")}
            </div>
            <div id="tvSearchResults" class="tv-search-results">${renderSearchResultCards(matches)}</div>
          </div>
        </div>
      `;
    }

    // 7. Lyrics / Score / Marker / Global / Menu / Media / Demo Windows
    const song = DATA.playerSongs[state.currentSongIdx];
    const songTitle = songDisplayTitle(song);
    let infoTitle = state.overlayWindow.toUpperCase();
    let infoBody = "";
    if (state.overlayWindow === "lyrics") {
      infoTitle = `LYRICS — ${songTitle}`;
      infoBody = `<pre style="margin:4px 0;white-space:pre-wrap;font-family:inherit;color:#fde047;">${escapeHtml((song && song.lyrics) || `Playing ${songTitle} (${(song && song.tempo) || state.tempo} BPM, Length ${(song && song.length) || "03:40"}) — Embedded SMF/MP3 lyric stream ready.`)}</pre>`;
    } else if (state.overlayWindow === "score") {
      infoTitle = `MUSICAL SCORE — ${songTitle}`;
      infoBody = `Treble & Bass Staff Notation Generated from MIDI Tracks (Key: C, Meter: ${st.meter}, Tempo: ${state.tempo} BPM).`;
    } else if (state.overlayWindow === "marker") {
      infoTitle = "SONG MARKERS";
      infoBody = "M1: Intro (Bar 001)  •  M2: Verse 1 (Bar 009)  •  M3: Chorus (Bar 025) — Jump seamlessly between song sections.";
    } else if (state.overlayWindow === "global") {
      infoTitle = "GLOBAL SETTINGS";
      infoBody = `
        <div style="display:flex;flex-direction:column;gap:5px;margin-top:4px;">
          <div>Global Split Point: <strong>${midiToName(state.globalSplitPoint)}</strong></div>
          <div>Display Brightness: <input type="range" id="tvBrightRange" min="25" max="100" value="${state.displayBrightness}" /> ${state.displayBrightness}%</div>
        </div>
      `;
    } else if (state.overlayWindow === "menu") {
      infoTitle = "EDIT MENU";
      infoBody = "Sections: [Mixer/Tuning]  [Effects]  [Keyboard/Ensemble]  [Style Controls]  [Pad/Switches]  [Mic Setup] — Press EXIT to return.";
    } else {
      infoBody = `Browsing ${infoTitle} — Select any resource or press the physical EXIT button to return to the Main page.`;
    }

    return `
      <div class="tv-window" style="padding:8px;font-size:0.62cqi;line-height:1.4;">
        <div style="color:#ffae34;font-weight:800;border-bottom:1px solid #444;padding-bottom:3px;margin-bottom:4px;">
          ${escapeHtml(infoTitle)} (Press EXIT to close)
        </div>
        <div>${infoBody}</div>
      </div>
    `;
  }

  function bindTouchViewEvents(screen) {
    screen.querySelectorAll("[data-tv-action]").forEach(el => {
      el.addEventListener("click", e => {
        e.stopPropagation();
        const act = el.dataset.tvAction;
        if (act === "open_style_select") {
          state.overlayWindow = "style_select";
          state.focusedParam = "style";
          syncBrowserToStyle(state.currentStyleIdx);
        } else if (act === "focus_tempo") {
          state.focusedParam = "tempo";
          logAction("Focused Tempo on TouchView -> Turn the silver VALUE dial or click TEMPO -/+.");
        } else if (act === "cycle_song") {
          state.currentSongIdx = (state.currentSongIdx + 1) % DATA.playerSongs.length;
          logAction(`Selected Song "${songDisplayTitle(DATA.playerSongs[state.currentSongIdx])}".`);
        } else if (act === "open_kbd_select") {
          state.overlayWindow = "kbd_lib_select";
          syncBrowserToKbdSet(state.activeLibCategory, state.activeLibIndex);
        } else if (act === "open_split_dlg") {
          openSplitPointDialog();
        } else if (act === "reset_subscale") {
          state.subScaleNotes = [];
          state.activeSubScalePreset = null;
          logAction("Reset Quarter-Tone Sub-Scale to Equal Temperament.");
        }
        renderAll();
      });
    });

    // Track selection (1st click selects, 2nd click opens Sound Select — Manual p. 39!)
    screen.querySelectorAll("[data-tv-track]").forEach(el => {
      el.addEventListener("click", () => {
        const tk = el.dataset.tvTrack;
        if (state.selectedTrackKey === tk) {
          state.overlayWindow = "sound_select";
          state.focusedParam = "sound";
          syncBrowserToSound(state.tracks[tk].sound);
          logAction(`Tapped ${tk.toUpperCase()} again -> Opened Sound Select (${DATA.sounds.length} manual Sounds) for ${tk.toUpperCase()}.`);
        } else {
          state.selectedTrackKey = tk;
          state.focusedParam = "sound";
          logAction(`Selected track ${tk.toUpperCase()} ("${state.tracks[tk].sound}") — tap again to swap its Sound!`);
        }
        renderAll();
      });
    });

    // Mute / Play toggle on UP1/UP2/UP3/LOW
    screen.querySelectorAll("[data-tv-mute]").forEach(el => {
      el.addEventListener("click", e => {
        e.stopPropagation();
        const tk = el.dataset.tvMute;
        state.tracks[tk].muted = !state.tracks[tk].muted;
        logAction(`${tk.toUpperCase()} ("${state.tracks[tk].sound}") ${state.tracks[tk].muted ? "MUTED" : "UNMUTED (Active Layer)"}.`);
        renderAll();
      });
    });

    // Mute / Play toggle on the 8 Style Accompaniment Tracks (Drum, Perc, Bass, Acc1..Acc5)
    screen.querySelectorAll("[data-tv-style-mute]").forEach(el => {
      el.addEventListener("click", e => {
        e.stopPropagation();
        const idx = parseInt(el.dataset.tvStyleMute, 10);
        if (isNaN(idx) || idx < 0 || idx > 7) return;
        state.styleTrackMutes[idx] = !state.styleTrackMutes[idx];
        const curStyle = getCurrentStyle();
        const trkObj = (curStyle.styleTracks && curStyle.styleTracks[idx]) || { label: `Track ${idx + 1}`, sound: "---" };
        logAction(`Style Track ${trkObj.label} ("${trkObj.sound}") ${state.styleTrackMutes[idx] ? "MUTED" : "UNMUTED"}.`);
        renderAll();
      });
    });

    // Bottom tabs
    screen.querySelectorAll("[data-tv-tab]").forEach(el => {
      el.addEventListener("click", () => {
        state.mainBottomTab = el.dataset.tvTab;
        if (state.mainBottomTab === "split") state.focusedParam = "split";
        renderAll();
      });
    });

    // Style Kbd Set 1-4 touchscreen tiles
    screen.querySelectorAll("[data-tv-stylekbd]").forEach(el => {
      el.addEventListener("click", () => {
        const slot = parseInt(el.dataset.tvStylekbd, 10);
        recallStyleKeyboardSet(slot, `TouchView Kbd Set [${slot + 1}]`);
        renderAll();
      });
    });

    // Pad tiles (Click triggers, Pick pill or Double-click opens Pad Select!)
    screen.querySelectorAll("[data-tv-editpad]").forEach(el => {
      el.addEventListener("click", e => {
        e.stopPropagation();
        const slot = parseInt(el.dataset.tvEditpad, 10);
        state.padSelectSlot = slot;
        state.overlayWindow = "pad_select";
        syncBrowserToPad(getStylePads()[slot]);
        logAction(`Editing PAD ${slot + 1} -> Choose from ${DATA.pads.length} manual Factory Pads.`);
        renderAll();
      });
    });
    screen.querySelectorAll("[data-tv-pad]").forEach(el => {
      el.addEventListener("click", () => {
        const idx = parseInt(el.dataset.tvPad, 10) + 1;
        handleButtonPress(`pad_${idx}`, false);
      });
      el.addEventListener("dblclick", () => {
        const idx = parseInt(el.dataset.tvPad, 10) + 1;
        handleButtonPress(`pad_${idx}`, true);
      });
    });

    // Select window shared controls (Hold, Close, Page, Open Search)
    screen.querySelectorAll("[data-tv-hold]").forEach(el => {
      el.addEventListener("click", () => {
        state.displayHold = !state.displayHold;
        logAction(`Display Hold ${state.displayHold ? "ON (keeps browser open)" : "OFF (auto-closes on selection)"}.`);
        renderTouchView();
      });
    });
    screen.querySelectorAll("[data-tv-close]").forEach(el => {
      el.addEventListener("click", () => {
        state.overlayWindow = null;
        renderAll();
      });
    });
    screen.querySelectorAll("[data-tv-opensearch]").forEach(el => {
      el.addEventListener("click", () => {
        state.searchScope = el.dataset.tvOpensearch || "all";
        state.overlayWindow = "search";
        renderTouchView();
      });
    });
    screen.querySelectorAll("[data-tv-selpage]").forEach(el => {
      el.addEventListener("click", () => {
        const p = parseInt(el.dataset.tvSelpage, 10);
        if (state.overlayWindow === "style_select") state.styleBrowsePage = p;
        else if (state.overlayWindow === "kbd_lib_select") state.kbdBrowsePage = p;
        else if (state.overlayWindow === "sound_select") state.soundBrowsePage = p;
        else if (state.overlayWindow === "pad_select") state.padBrowsePage = p;
        renderTouchView();
      });
    });

    // Style Select category tabs & cards
    screen.querySelectorAll("[data-tv-stylecat]").forEach(el => {
      el.addEventListener("click", () => {
        state.styleBrowseCat = el.dataset.tvStylecat;
        state.styleBrowsePage = 0;
        renderTouchView();
      });
    });
    screen.querySelectorAll("[data-tv-pickstyle]").forEach(el => {
      el.addEventListener("click", () => {
        selectStyleByIndex(parseInt(el.dataset.tvPickstyle, 10));
      });
    });

    // Kbd Set Library category tabs & cards
    screen.querySelectorAll("[data-tv-libcat]").forEach(el => {
      el.addEventListener("click", () => {
        state.kbdBrowseCat = el.dataset.tvLibcat;
        state.kbdBrowsePage = 0;
        renderTouchView();
      });
    });
    screen.querySelectorAll("[data-tv-picklib]").forEach(el => {
      el.addEventListener("click", () => {
        const cat = state.kbdBrowseCat || state.activeLibCategory;
        applyLibraryKbdSet(cat, parseInt(el.dataset.tvPicklib, 10));
        if (!state.displayHold) state.overlayWindow = null;
        renderAll();
      });
    });

    // Sound Select type tabs, track toggle, group tabs & cards
    screen.querySelectorAll("[data-tv-soundtype]").forEach(el => {
      el.addEventListener("click", () => {
        const tp = el.dataset.tvSoundtype;
        state.soundBrowseType = tp;
        const groups = Object.keys((DATA.soundGroupsByType && DATA.soundGroupsByType[tp]) || {});
        if (!groups.includes(state.soundBrowseGroup)) {
          state.soundBrowseGroup = groups[0] || "Piano";
        }
        state.soundBrowsePage = 0;
        renderTouchView();
      });
    });
    screen.querySelectorAll("[data-tv-cycletrack]").forEach(el => {
      el.addEventListener("click", () => {
        const order = ["up1", "up2", "up3", "low"];
        state.selectedTrackKey = order[(order.indexOf(state.selectedTrackKey) + 1) % order.length];
        syncBrowserToSound(state.tracks[state.selectedTrackKey].sound);
        renderAll();
      });
    });
    screen.querySelectorAll("[data-tv-soundgroup]").forEach(el => {
      el.addEventListener("click", () => {
        state.soundBrowseGroup = el.dataset.tvSoundgroup;
        state.soundBrowsePage = 0;
        renderTouchView();
      });
    });
    screen.querySelectorAll("[data-tv-picksound]").forEach(el => {
      el.addEventListener("click", () => {
        const snd = el.dataset.tvPicksound;
        assignSoundToSelectedTrack(snd, "Sound Select");
        if (!state.displayHold) state.overlayWindow = null;
        renderAll();
      });
    });

    // Pad Select bank tabs, slot cycle, group tabs & cards
    screen.querySelectorAll("[data-tv-padbank]").forEach(el => {
      el.addEventListener("click", () => {
        const bk = el.dataset.tvPadbank;
        state.padBrowseBank = bk;
        const firstGrp = (DATA.padGroups || []).find(g => g.bankType === bk);
        if (firstGrp) state.padBrowseGroup = firstGrp.name;
        state.padBrowsePage = 0;
        renderTouchView();
      });
    });
    screen.querySelectorAll("[data-tv-padslot]").forEach(el => {
      el.addEventListener("click", () => {
        state.padSelectSlot = (state.padSelectSlot + 1) % 4;
        renderTouchView();
      });
    });
    screen.querySelectorAll("[data-tv-padgroup]").forEach(el => {
      el.addEventListener("click", () => {
        state.padBrowseGroup = el.dataset.tvPadgroup;
        state.padBrowsePage = 0;
        renderTouchView();
      });
    });
    screen.querySelectorAll("[data-tv-pickpad]").forEach(el => {
      el.addEventListener("click", () => {
        const padId = el.dataset.tvPickpad;
        const padObj = (DATA.pads || []).find(p => p.id === padId);
        if (padObj) {
          assignPadToSlot(padObj, state.padSelectSlot, "Pad Select");
          if (window.pa700Audio && padObj.type === "OneShot") {
            window.pa700Audio.triggerPadHit(state.padSelectSlot, padObj, buildAudioState());
          }
          if (!state.displayHold) state.overlayWindow = null;
          renderAll();
        }
      });
    });

    // SongBook Set List tiles
    screen.querySelectorAll("[data-tv-setlist]").forEach(el => {
      el.addEventListener("click", () => {
        state.setListMode = true;
        handleLibraryOrSetListButton(parseInt(el.dataset.tvSetlist, 10));
        renderAll();
      });
    });

    // Live Search Overlay bindings (preserves input focus while filtering results!)
    const searchInput = document.getElementById("tvSearchInput");
    const bindSearchResultClicks = () => {
      screen.querySelectorAll("[data-tv-searchkind]").forEach(el => {
        el.addEventListener("click", () => {
          const kind = el.dataset.tvSearchkind;
          const val = el.dataset.tvSearchval;
          if (kind === "style") {
            selectStyleByIndex(parseInt(val, 10), { keepOverlayOpen: true });
            state.overlayWindow = null;
          } else if (kind === "kbd") {
            const [catId, pcStr] = val.split(":");
            const list = DATA.keyboardSetLibrary[catId] || [];
            const idx = list.findIndex(k => String(k.pc) === pcStr);
            applyLibraryKbdSet(catId, idx >= 0 ? idx : 0);
            state.overlayWindow = null;
          } else if (kind === "sound") {
            assignSoundToSelectedTrack(val, "Search");
            state.overlayWindow = null;
          } else if (kind === "pad") {
            const padObj = (DATA.pads || []).find(p => p.id === val);
            if (padObj) assignPadToSlot(padObj, state.padSelectSlot, "Search");
            state.overlayWindow = null;
          }
          renderAll();
        });
      });
    };
    bindSearchResultClicks();

    if (searchInput) {
      searchInput.addEventListener("input", () => {
        state.searchQuery = searchInput.value;
        const matches = getSearchMatches(state.searchQuery, state.searchScope);
        const resEl = document.getElementById("tvSearchResults");
        const cntEl = document.getElementById("tvSearchCount");
        if (cntEl) cntEl.textContent = `${matches.length}${matches.length >= 60 ? "+" : ""} hits`;
        if (resEl) {
          resEl.innerHTML = renderSearchResultCards(matches);
          bindSearchResultClicks();
        }
      });
    }
    screen.querySelectorAll("[data-tv-searchscope]").forEach(el => {
      el.addEventListener("click", () => {
        state.searchScope = el.dataset.tvSearchscope;
        renderTouchView();
      });
    });

    const gChk = document.getElementById("tvGlobalSplitChk");
    if (gChk) {
      gChk.addEventListener("change", () => {
        state.useGlobalSplit = gChk.checked;
        logAction(`Split mode set to ${state.useGlobalSplit ? "Global Split" : "Local Keyboard Set Split"} (${midiToName(getEffectiveSplit())}).`);
        renderAll();
      });
    }
    const bChk = document.getElementById("tvBassInvChk");
    if (bChk) {
      bChk.addEventListener("change", () => {
        state.bassInversion = bChk.checked;
        logAction(`Bass Inversion ${state.bassInversion ? "ON (slash chords enabled, e.g. C/E)" : "OFF"}.`);
        renderAll();
      });
    }
    const brRng = document.getElementById("tvBrightRange");
    if (brRng) {
      brRng.addEventListener("input", () => {
        state.displayBrightness = parseInt(brRng.value, 10);
        renderTouchView();
      });
    }
  }

  // =========================================================================
  // GUIDED GIG CRASH COURSE DRILLS
  // =========================================================================
  function getActiveDrillTarget() {
    if (!state.drillsOpen) return { targetBtn: null, targetKey: null };
    const drill = DATA.drills[state.drillIdx];
    const step = drill && drill.steps[state.drillStepIdx];
    return step || { targetBtn: null, targetKey: null };
  }

  function renderDrillBar() {
    const drawer = document.getElementById("drillDrawer");
    const toggleBtn = document.getElementById("btnToggleDrills");
    drawer.classList.toggle("open", state.drillsOpen);
    toggleBtn.classList.toggle("active", state.drillsOpen);
    if (!state.drillsOpen) return;

    const tabsEl = document.getElementById("drillTabs");
    tabsEl.innerHTML = DATA.drills.map((d, idx) =>
      `<button type="button" class="tb-btn ${state.drillIdx === idx ? "active" : ""}" data-drill-idx="${idx}">${escapeHtml(d.title)}</button>`
    ).join("");
    tabsEl.querySelectorAll("[data-drill-idx]").forEach(b => {
      b.addEventListener("click", () => {
        state.drillIdx = parseInt(b.dataset.drillIdx, 10);
        state.drillStepIdx = 0;
        renderAll();
      });
    });

    const drill = DATA.drills[state.drillIdx];
    const step = drill.steps[state.drillStepIdx];
    document.getElementById("drillPrompt").textContent = step.prompt;
    document.getElementById("drillStepCounter").textContent = `Step ${state.drillStepIdx + 1} / ${drill.steps.length}`;
  }

  function checkDrillProgress(btnId, midiKey) {
    if (!state.drillsOpen) return;
    const drill = DATA.drills[state.drillIdx];
    const step = drill.steps[state.drillStepIdx];
    if (!step) return;
    if ((btnId && step.targetBtn === btnId) || (midiKey !== null && step.targetKey === midiKey)) {
      if (state.drillStepIdx < drill.steps.length - 1) {
        state.drillStepIdx += 1;
      } else {
        logAction(`Completed ${drill.title}! Switch to the next drill tab above or keep experimenting.`);
      }
    }
  }

  // =========================================================================
  // TOP TOOLBAR, HELPER PILLS, ASSIGNABLE SWITCHES & JOYSTICK
  // =========================================================================
  function syncLatchButton() {
    const b = document.getElementById("btnLatchKeys");
    b.classList.toggle("latch-on", state.latchKeys);
    b.textContent = `Hold / Latch Keys: ${state.latchKeys ? "ON" : "OFF"}`;
  }

  function bindToolbarAndHelpers() {
    document.getElementById("btnToggleDrills").addEventListener("click", () => {
      state.drillsOpen = !state.drillsOpen;
      renderAll();
    });
    document.getElementById("btnCloseDrills").addEventListener("click", () => {
      state.drillsOpen = false;
      renderAll();
    });
    document.getElementById("btnPrevStep").addEventListener("click", () => {
      state.drillStepIdx = Math.max(0, state.drillStepIdx - 1);
      renderAll();
    });
    document.getElementById("btnNextStep").addEventListener("click", () => {
      const drill = DATA.drills[state.drillIdx];
      state.drillStepIdx = Math.min(drill.steps.length - 1, state.drillStepIdx + 1);
      renderAll();
    });

    const cabBtn = document.getElementById("btnToggleCabinet");
    cabBtn.addEventListener("click", () => {
      const wrap = document.getElementById("cabinetWrapper");
      const full = wrap.classList.toggle("full-cabinet");
      cabBtn.classList.toggle("active", full);
      cabBtn.textContent = full ? "Stage Zoom View (Large Panel)" : "Full Cabinet View (Speakers)";
    });

    // Match the exact LED + SongBook screen state of upscaled_full_control_panel.png!
    document.getElementById("btnMatchPhoto").addEventListener("click", () => {
      stopArrangerImmediate();
      state.powerOn = true;
      state.mode = "style";
      state.accompOn = true;
      state.memoryOn = true;
      state.activeVariation = 1;
      state.autoFill = true;
      state.activeEnding = 3;
      state.setListMode = true;
      state.overlayWindow = "songbook";
      state.subScaleNotes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11];
      state.photoLedOverrideStartGreen = true;
      state.photoLedOverrideAllSetList = true;
      logAction("Loaded exact visual state from upscaled_full_control_panel.png (SongBook Set List + Oriental Sub-Scale LEDs + Start/Stop Green LED)!");
      renderAll();
    });

    document.getElementById("btnFactoryReset").addEventListener("click", () => {
      stopArrangerImmediate();
      state.powerOn = true;
      state.mode = "style";
      state.overlayWindow = null;
      state.setListMode = false;
      state.photoLedOverrideStartGreen = false;
      state.photoLedOverrideAllSetList = false;
      state.subScaleNotes = [];
      state.activeSubScalePreset = null;
      state.currentStyleIdx = findStyleIndexById("brush_ballad");
      syncBrowserToStyle(state.currentStyleIdx);
      state.tempo = DATA.styles[state.currentStyleIdx].tempo;
      state.tempoLock = false;
      state.autoFill = true;
      state.accompOn = true;
      state.memoryOn = true;
      state.manualBass = false;
      state.upperOctave = 0;
      state.masterTranspose = 0;
      recallMySetting();
      logAction("Reset to Korg Pa700 Power-On Factory Startup State (Style Play Main Page, 'Brush Ballad', 'My Setting').");
      renderAll();
    });

    document.getElementById("btnDemoCombo").addEventListener("click", () => {
      state.overlayWindow = state.overlayWindow === "demo" ? null : "demo";
      logAction("Pressed STYLE PLAY + SONG PLAY together -> Entered Korg Pa700 DEMO Songs showcase!");
      renderAll();
    });

    document.getElementById("btnClearLog").addEventListener("click", () => {
      logEntries.length = 0;
      renderEventLog();
    });

    const audioBtn = document.getElementById("btnAudioToggle");
    if (audioBtn) {
      audioBtn.addEventListener("click", () => {
        if (!window.pa700Audio) return;
        window.pa700Audio.init();
        const nextMuted = !window.pa700Audio.muted;
        window.pa700Audio.setMuted(nextMuted);
        audioBtn.classList.toggle("active", !nextMuted);
        audioBtn.textContent = nextMuted ? "Sound: MUTED" : "Sound: ON";
      });
    }

    // SoundFont Library Controls & Status HUD
    const sfSelect = document.getElementById("sfLibrarySelect");
    const sfBadge = document.getElementById("sfStatusBadge");
    const btnUploadSf = document.getElementById("btnUploadSf");
    const sfFileInput = document.getElementById("sfFileInput");

    const renderSfStatus = (snap) => {
      if (!snap || !sfBadge) return;
      state.audioSfStatus = snap;
      if (sfSelect && snap.activeId && sfSelect.value !== snap.activeId) {
        sfSelect.value = snap.activeId;
      }
      sfBadge.classList.remove("warn", "drop");
      if (snap.state === "loading") {
        sfBadge.classList.add("warn");
        sfBadge.textContent = snap.statusMsg || `Loading ${snap.progressPct || 0}%`;
      } else if (snap.state === "error") {
        sfBadge.classList.add("drop");
        sfBadge.textContent = snap.statusMsg || "Bank fallback active";
      } else if (snap.mode === "stream") {
        sfBadge.textContent = snap.lastLoadMs ? `Ready (${snap.lastLoadMs}ms)` : "Streaming ready";
      } else {
        sfBadge.textContent = snap.statusMsg || "Ready";
      }
      sfBadge.title = [
        `Library: ${snap.activeLabel}`,
        `Status: ${snap.statusMsg}`,
        snap.loadedPatchesCount ? `Loaded patches: ${snap.loadedPatchesCount}` : "",
        snap.lastLoadMs ? `Last load: ${snap.lastLoadMs}ms` : ""
      ].filter(Boolean).join(" | ");
    };

    if (window.pa700Audio) {
      if (typeof window.pa700Audio.onStatusChange === "function") {
        window.pa700Audio.onStatusChange(renderSfStatus);
      }
      if (typeof window.pa700Audio.getLibraryStatus === "function") {
        renderSfStatus(window.pa700Audio.getLibraryStatus());
      }
    }

    if (sfSelect) {
      sfSelect.addEventListener("change", async () => {
        if (!window.pa700Audio || typeof window.pa700Audio.setSoundLibrary !== "function") return;
        await window.pa700Audio.init();
        logAction(`Switching SoundFont engine to "${sfSelect.options[sfSelect.selectedIndex].text}"...`);
        const res = await window.pa700Audio.setSoundLibrary(sfSelect.value);
        logAction(`SoundFont status: ${res.statusMsg}`);
      });
    }

    if (btnUploadSf && sfFileInput) {
      btnUploadSf.addEventListener("click", () => sfFileInput.click());
      sfFileInput.addEventListener("change", async () => {
        const files = sfFileInput.files;
        if (files && files.length && window.pa700Audio && typeof window.pa700Audio.loadLocalSoundFontFiles === "function") {
          await window.pa700Audio.init();
          const res = await window.pa700Audio.loadLocalSoundFontFiles(files);
          logAction(`Loaded local SoundFont (.sf2/.sf3) into IndexedDB cache -> ${res.statusMsg}`);
        }
        sfFileInput.value = "";
      });
    }

    const shellEl = document.querySelector(".app-shell");
    if (shellEl) {
      shellEl.addEventListener("dragover", e => {
        if (e.dataTransfer && Array.from(e.dataTransfer.types || []).includes("Files")) {
          e.preventDefault();
        }
      });
      shellEl.addEventListener("drop", async e => {
        const files = Array.from((e.dataTransfer && e.dataTransfer.files) || [])
          .filter(f => /\.(sf2|sf3|dls)$/i.test(f.name));
        if (!files.length) return;
        e.preventDefault();
        if (window.pa700Audio && typeof window.pa700Audio.loadLocalSoundFontFiles === "function") {
          await window.pa700Audio.init();
          const res = await window.pa700Audio.loadLocalSoundFontFiles(files);
          logAction(`Dropped SoundFont file(s) -> ${res.statusMsg}`);
        }
      });
    }

    const logBtn = document.getElementById("btnToggleLog");
    const logDrawer = document.getElementById("logDrawer");
    if (logBtn && logDrawer) {
      logBtn.addEventListener("click", () => {
        const open = logDrawer.style.display === "none";
        logDrawer.style.display = open ? "block" : "none";
        logBtn.classList.toggle("active", open);
      });
    }

    // Chord mode selector pills
    document.querySelectorAll("[data-chord-mode]").forEach(btn => {
      btn.addEventListener("click", () => {
        state.mouseChordMode = btn.dataset.chordMode;
        document.querySelectorAll("[data-chord-mode]").forEach(b =>
          b.classList.toggle("active", b.dataset.chordMode === state.mouseChordMode)
        );
        logAction(`Mouse Key Click Mode set to: ${btn.textContent}`);
        updateReadouts();
      });
    });

    document.getElementById("btnLatchKeys").addEventListener("click", () => {
      state.latchKeys = !state.latchKeys;
      syncLatchButton();
      if (!state.latchKeys) releaseKeyboardNotes();
      logAction(state.latchKeys
        ? "Hold / Latch Keys ON -> Clicked keys stay held down so you can test MEMORY OFF & SYNCHRO STOP!"
        : "Hold / Latch Keys OFF.");
    });

    document.getElementById("btnReleaseKeys").addEventListener("click", () => {
      releaseKeyboardNotes();
      logAction("Lifted hands from keyboard (all held keys released).");
    });

    // 2-Finger / Hold Hardware Shortcuts
    document.getElementById("btnQuickSplitDialog").addEventListener("click", openSplitPointDialog);
    document.getElementById("btnResetTempo").addEventListener("click", () => {
      state.tempo = getCurrentStyle().tempo;
      restartClockInterval();
      logAction(`Pressed TEMPO - & + together -> Restored Style's memorized Tempo (${state.tempo} BPM).`);
      renderAll();
    });
    document.getElementById("btnResetOctave").addEventListener("click", () => {
      state.upperOctave = 0;
      logAction("Pressed UPPER OCTAVE - & + together -> Reset Upper Octave to 0.");
      renderAll();
    });
    document.getElementById("btnResetTranspose").addEventListener("click", () => {
      state.masterTranspose = 0;
      logAction("Pressed TRANSPOSE b & # together -> Reset Master Transpose to 0.");
      renderAll();
    });

    // Assignable Switches 1-3
    document.querySelectorAll("[data-asw]").forEach(btn => {
      btn.addEventListener("click", () => {
        const n = btn.dataset.asw;
        state.assignableSwitches[n] = !state.assignableSwitches[n];
        btn.classList.toggle("on", state.assignableSwitches[n]);
        const dncDesc = n === "1" ? "DNC Nuance 1 (Growl / Harmonics)" : n === "2" ? "DNC Nuance 2 (Breath / Flutter)" : "Rotary Speaker Fast/Slow";
        logAction(`Assignable Switch ${n} (${dncDesc}): ${state.assignableSwitches[n] ? "ON" : "OFF"}.`);
      });
    });

    // Joystick X/Y Drag (Live Pitch Bend & Vibrato Modulation!)
    const jPad = document.getElementById("joystickPad");
    const jStick = document.getElementById("joystickStick");
    let jDrag = false;
    jPad.addEventListener("mousedown", e => {
      jDrag = true;
      updateJoystick(e);
    });
    window.addEventListener("mousemove", e => {
      if (jDrag) updateJoystick(e);
    });
    window.addEventListener("mouseup", () => {
      if (jDrag) {
        jDrag = false;
        jStick.style.left = "50%";
        jStick.style.top = "50%";
        if (window.pa700Audio) window.pa700Audio.setJoystick(0, 0);
        logAction("Joystick sprung back to center (Pitch Bend 0, Modulation 0).");
      }
    });

    function updateJoystick(e) {
      const r = jPad.getBoundingClientRect();
      const dx = Math.max(-14, Math.min(14, e.clientX - (r.left + r.width / 2)));
      const dy = Math.max(-14, Math.min(14, e.clientY - (r.top + r.height / 2)));
      jStick.style.left = `calc(50% + ${dx}px)`;
      jStick.style.top = `calc(50% + ${dy}px)`;
      if (window.pa700Audio) window.pa700Audio.setJoystick(dx / 14, -dy / 14);
    }

    // Unlock Web Audio on first click anywhere & support optional QWERTY keyboard playing
    const unlockAudio = () => {
      if (window.pa700Audio) {
        window.pa700Audio.init();
        window.pa700Audio.syncPanelControls(buildAudioState());
      }
    };
    window.addEventListener("mousedown", unlockAudio, { passive: true });

    const qwertyMidiMap = {
      z: 48, s: 49, x: 50, d: 51, c: 52, v: 53, g: 54, b: 55, h: 56, n: 57, j: 58, m: 59,
      q: 60, "2": 61, w: 62, "3": 63, e: 64, r: 65, "5": 66, t: 67, "6": 68, y: 69, "7": 70, u: 71, i: 72
    };
    let heldQwertyKey = null;
    window.addEventListener("keydown", e => {
      if (e.repeat || e.ctrlKey || e.metaKey || e.altKey) return;
      const tag = e.target && e.target.tagName;
      if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return;
      const k = e.key.toLowerCase();
      if (qwertyMidiMap[k] !== undefined) {
        unlockAudio();
        heldQwertyKey = k;
        pressKeyboardNote(qwertyMidiMap[k]);
      }
    });
    window.addEventListener("keyup", e => {
      const k = e.key.toLowerCase();
      if (k === heldQwertyKey) {
        heldQwertyKey = null;
        if (!state.latchKeys) releaseKeyboardNotes();
      }
    });
  }

  function startVuMeterLoop() {
    const container = document.getElementById("vuMeterSegments");
    if (!container) return;
    const segs = Array.from(container.querySelectorAll("span"));
    function frame() {
      const lvl = (window.pa700Audio && state.powerOn) ? window.pa700Audio.getMeterLevel() : 0;
      const litCount = Math.round(lvl * segs.length);
      segs.forEach((s, idx) => {
        s.className = "";
        if (idx < litCount) {
          if (idx >= 10) s.className = "lit-red";
          else if (idx >= 7) s.className = "lit-amber";
          else s.className = "lit-green";
        }
      });
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }

  function renderAll() {
    state.photoLedOverrideStartGreen = false;
    state.photoLedOverrideAllSetList = false;
    if (window.pa700Audio) window.pa700Audio.syncPanelControls(buildAudioState());
    updateKnobVisuals();
    updateLedVisuals();
    renderTouchView();
    renderDrillBar();
    updatePianoVisuals();
    updateReadouts();
  }

  // =========================================================================
  // INITIALIZE
  // =========================================================================
  function init() {
    mountFaceplateControls();
    mountOrientalPanels();
    build61KeyPiano();
    bindToolbarAndHelpers();
    startVuMeterLoop();

    document.getElementById("btnMatchPhoto").onclick = () => {
      stopArrangerImmediate();
      state.powerOn = true;
      state.mode = "style";
      state.accompOn = true;
      state.memoryOn = true;
      state.activeVariation = 1;
      state.autoFill = true;
      state.activeEnding = 3;
      state.setListMode = true;
      state.overlayWindow = "songbook";
      state.subScaleNotes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11];
      updateKnobVisuals();
      state.photoLedOverrideStartGreen = true;
      state.photoLedOverrideAllSetList = true;
      updateLedVisuals();
      renderTouchView();
      renderDrillBar();
      updatePianoVisuals();
      updateReadouts();
      logAction("Loaded Reference Photo State (matching upscaled_full_control_panel.png LEDs & SongBook Set List display)!");
    };

    restartClockInterval();
    logAction("Korg Pa700 Web Audio Synthesizer & Arranger Ready!");
    renderAll();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
