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

  // =========================================================================
  // INSTRUMENT STATE (Matches Pa700 OS v1.5 Startup State)
  // =========================================================================
  const state = {
    powerOn: true,
    mode: "style", // 'style' | 'song' | 'seq' | 'sound'
    overlayWindow: null, // null | 'style_select' | 'kbd_lib_select' | 'sound_select' | 'songbook' | 'global' | 'media' | 'menu' | 'lyrics' | 'marker' | 'score' | 'search' | 'metronome' | 'demo'
    splitDialogOpen: false,
    mainBottomTab: "kbd_set", // 'kbd_set' | 'volume' | 'pad' | 'split' | 'sub_scale' | 'kaoss' | 'mic'
    volumeTrackView: "grouped", // 'grouped' | 'style_tracks' (toggled by TRACK SELECT)
    focusedParam: "tempo", // 'tempo' | 'split' | 'style' | 'kbdset' | 'sound'
    selectedTrackKey: "up1", // 'up1' | 'up2' | 'up3' | 'low'

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
    currentStyleIdx: 0, // Brush Ballad (default in manual p. 23!)
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

    kbdSetName: "My Setting",
    kbdSetSource: "Kbd Set Library",
    activeLibCategory: "piano_ep",
    activeLibIndex: 0,
    setListMode: false, // SET LIST button LED: false = Kbd Set Library, true = SongBook Set List 1-9
    activeSetListSlot: 1,
    tracks: clone(DATA.mySetting.tracks),

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
      if (window.pa700Audio) window.pa700Audio.syncPanelControls(state);
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
      if (window.pa700Audio) window.pa700Audio.syncPanelControls(state);
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
      selectStyleByIndex(next);
      return;
    }

    if (state.focusedParam === "split" || state.mainBottomTab === "split") {
      const sp = Math.max(36, Math.min(96, getEffectiveSplit() + dir));
      setLocalSplitPoint(sp, "VALUE dial");
      return;
    }

    if (state.focusedParam === "sound") {
      const trk = state.tracks[state.selectedTrackKey];
      const curIdx = Math.max(0, DATA.soundsCatalog.indexOf(trk.sound));
      const nextIdx = (curIdx + dir + DATA.soundsCatalog.length) % DATA.soundsCatalog.length;
      trk.sound = DATA.soundsCatalog[nextIdx];
      logAction(`VALUE Dial -> ${state.selectedTrackKey.toUpperCase()} voice changed to "${trk.sound}"`);
      renderAll();
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
        logAction(`Switched to SOUND mode — Editing/Browsing single Sound "${state.tracks[state.selectedTrackKey].sound}".`);
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
        logAction(`PLAYER SELECT -> Loaded "${DATA.playerSongs[state.currentSongIdx].name}".`);
        break;
      case "player_home":
        state.playerBar = 1;
        logAction(`PLAYER |◄ (HOME) -> Returned "${DATA.playerSongs[state.currentSongIdx].name}" to Measure 001.`);
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
          ? `PLAYER ►/■ -> Playing Song "${DATA.playerSongs[state.currentSongIdx].name}".`
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

      // Pads 1-4 + Stop
      case "pad_1":
      case "pad_2":
      case "pad_3":
      case "pad_4": {
        const pIdx = parseInt(id.split("_")[1], 10) - 1;
        const padInfo = getCurrentStyle().pads[pIdx];
        if (padInfo.type === "OneShot") {
          state.padsActive[pIdx] = true;
          if (window.pa700Audio) window.pa700Audio.triggerPadHit(pIdx, padInfo, state);
          logAction(`Triggered PAD ${pIdx + 1}: "${padInfo.name}" (One-Shot hit)!`);
          setTimeout(() => {
            state.padsActive[pIdx] = false;
            renderAll();
          }, 1100);
        } else {
          state.padsActive[pIdx] = !state.padsActive[pIdx];
          if (state.padsActive[pIdx] && window.pa700Audio) {
            window.pa700Audio.triggerPadHit(pIdx, padInfo, state);
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
        logAction("Pressed STYLE SELECT -> Choose a Style on the TouchView display (or turn VALUE dial).");
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
    state.tracks = clone(DATA.mySetting.tracks);
    state.kbdSetName = "My Setting";
    state.kbdSetSource = "Kbd Set Library";
    state.activeStyleKbdSlot = null;
    state.splitOn = DATA.mySetting.splitOn;
    state.localSplitPoint = DATA.mySetting.localSplit;
    state.useGlobalSplit = state.localSplitPoint === null;
    logAction(`Recalled MY SETTING -> Upper 1: "${state.tracks.up1.sound}", Split ${state.splitOn ? "ON (" + midiToName(getEffectiveSplit()) + ")" : "OFF"}.`);
  }

  function recallStyleKeyboardSet(slot, triggerLabel) {
    const st = getCurrentStyle();
    const ks = st.kbdSets[slot];
    if (!ks) return;
    state.activeStyleKbdSlot = slot;
    state.kbdSetName = ks.name;
    state.kbdSetSource = `Style: ${st.name} [#${slot + 1}]`;
    state.tracks.up1 = { sound: ks.up1, muted: false, octave: 0, volume: 100 };
    state.tracks.up2 = { sound: ks.up2, muted: ks.up2Muted, octave: 0, volume: 82 };
    state.tracks.up3 = { sound: ks.up3, muted: ks.up3Muted, octave: 0, volume: 80 };
    state.tracks.low = { sound: ks.low, muted: false, octave: 1, volume: 75, backing: true };
    logAction(`${triggerLabel} -> Loaded Voice Set #${slot + 1} "${ks.name}" (UP1: ${ks.up1}${!ks.up2Muted ? " + UP2: " + ks.up2 : ""}).`);
  }

  function handleLibraryOrSetListButton(num) {
    if (state.setListMode) {
      // Recall SongBook Set List tile 1..9!
      const entry = DATA.setListEntries[num - 1];
      if (!entry) return;
      state.activeSetListSlot = num;
      const sIdx = DATA.styles.findIndex(s => s.id === entry.styleId);
      if (sIdx >= 0) state.currentStyleIdx = sIdx;
      if (!state.tempoLock) state.tempo = entry.tempo;
      state.activeVariation = entry.variation;
      recallStyleKeyboardSet(entry.kbdIdx, `SET LIST #${num} "${entry.title}"`);
      logAction(`SET LIST #${num} -> Loaded SongBook Entry "${entry.title}" (Style "${getCurrentStyle().name}", ${state.tempo} BPM, Variation ${entry.variation}).`);
      return;
    }

    // Standard KEYBOARD SET LIBRARY Category Selection (1..9)
    const cat = DATA.libraryCategories[num - 1];
    const list = DATA.keyboardSetLibrary[cat.id] || [];
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
    state.activeLibCategory = catId;
    state.activeLibIndex = idx;
    state.activeStyleKbdSlot = null;
    state.kbdSetName = item.name;
    state.kbdSetSource = `Library: ${catObj ? catObj.short : catId}`;
    state.tracks.up1 = { ...item.up1, volume: 100 };
    state.tracks.up2 = { ...item.up2, volume: 85 };
    state.tracks.up3 = { ...item.up3, volume: 80 };
    state.tracks.low = { ...item.low, volume: 75, backing: true };
    logAction(`Keyboard Set Library [${catObj ? catObj.label : catId}] -> Selected "${item.name}" (Upper 1: ${item.up1.sound}${!item.up2.muted ? " + Upper 2: " + item.up2.sound : ""}).`);
  }

  function selectStyleByIndex(idx) {
    state.currentStyleIdx = idx;
    const st = getCurrentStyle();
    if (!state.tempoLock) {
      state.tempo = st.tempo;
    }
    state.padsActive = [false, false, false, false];
    if (state.styleToKbdMode === "on") {
      recallStyleKeyboardSet(0, `Style "${st.name}" (Style to Kbd Set ON)`);
    } else if (state.styleToKbdMode === "blink") {
      recallStyleKeyboardSet(state.activeVariation - 1, `Style "${st.name}" (Style to Kbd Set BLINK)`);
    }
    logAction(`Selected Style "${st.name}" (${st.bank}, Meter ${st.meter}, ${state.tempo} BPM${state.tempoLock ? " [LOCKED]" : ""}).`);
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
    if (window.pa700Audio) window.pa700Audio.syncPanelControls(state);
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
      window.pa700Audio.startEngineLoop(() => state, onBeatTick);
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
    const preset = DATA.subScalePresets.find(p => p.id === scId);
    if (!preset) return;
    if (state.activeSubScalePreset === scId) {
      state.activeSubScalePreset = null;
      state.subScaleNotes = [];
      logAction(`Cleared Sub-Scale Preset ${preset.label} -> Equal Temperament restored.`);
    } else {
      state.activeSubScalePreset = scId;
      state.subScaleNotes = [...preset.notes];
      logAction(`Recalled Sub-Scale ${preset.label}: ${preset.name}.`);
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
      window.pa700Audio.playKeyboardNotes(chordNotes, state);
    }

    const noteNames = chordNotes.map(midiToName).join(", ");
    const activeVoiceDesc = describePlayingVoices(rootMidi, chordNotes);
    logAction(`Played ${midiToName(rootMidi)} -> [${noteNames}] | ${activeVoiceDesc}`);

    checkDrillProgress(null, rootMidi);
    renderAll();
  }

  function releaseKeyboardNotes() {
    if (window.pa700Audio) {
      window.pa700Audio.releaseAllKeyboardVoices();
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
        setLed(`ksl_${activeCatObj.num}`, "red", false);
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
    const pStyle = document.getElementById("hudPillStyle");
    const pChord = document.getElementById("hudPillChord");
    const pSplit = document.getElementById("hudPillSplit");
    if (!pVoice) return;

    if (!state.powerOn) {
      pVoice.textContent = "Standby (Power OFF)";
      pStyle.textContent = "---";
      pChord.textContent = "---";
      pSplit.textContent = "---";
      return;
    }

    const upActive = ["up1", "up2", "up3"]
      .filter(k => !state.tracks[k].muted)
      .map(k => state.tracks[k].sound);
    pVoice.textContent = `${state.kbdSetName}: ${upActive.join(" + ") || "Muted"}`;

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
              <div class="tv-song-name">${escapeHtml(songObj.name)}</div>
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
      return st.pads.map((p, idx) => `
        <div class="tv-kbdset-slot ${state.padsActive[idx] ? "active" : ""}" data-tv-pad="${idx}">
          <span class="slot-num">PAD ${idx + 1} (${p.type})</span>
          <span class="slot-label">${escapeHtml(p.name)}</span>
        </div>
      `).join("");
    }

    if (state.mainBottomTab === "volume") {
      if (state.volumeTrackView === "style_tracks") {
        const names = ["Drum", "Perc", "Bass", "Acc1", "Acc2", "Acc3", "Acc4", "Acc5"];
        return names.map((nm, idx) => {
          const muted = idx >= 2 && (!state.accompOn || state.manualBass);
          return `
            <div class="tv-kbdset-slot" style="padding:1px;">
              <span class="slot-num">${nm}</span>
              <span style="font-size:0.52cqi;color:${muted ? "#f87171" : "#4ade80"};">${muted ? "MUTE" : "PLAY"}</span>
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

  function renderOverlayWindow(st) {
    // 1. SongBook Set List 3x3 Grid (exact match to upscaled_full_control_panel.png!)
    if (state.overlayWindow === "songbook") {
      const tiles = DATA.setListEntries.map(e => `
        <div class="tv-setlist-tile ${state.activeSetListSlot === e.slot ? "active" : ""}" data-tv-setlist="${e.slot}">
          <div class="sl-top">
            <span style="background:#fff;color:#b91c1c;padding:0 2px;border-radius:1px;">${e.type}</span>
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

    // 2. Style Select Window
    if (state.overlayWindow === "style_select") {
      const cats = DATA.styleCategories.map(c =>
        `<button type="button" class="tv-cat-btn ${st.category === c ? "active" : ""}" data-tv-stylecat="${c}">${c}</button>`
      ).join("");
      const tiles = DATA.styles.map((s, idx) => `
        <div class="tv-select-tile ${state.currentStyleIdx === idx ? "active" : ""}" data-tv-pickstyle="${idx}">
          <span>${escapeHtml(s.name)}</span>
          <span style="font-size:0.50cqi;opacity:0.85;">${s.meter} • ${s.tempo}</span>
        </div>
      `).join("");
      return `
        <div class="tv-window">
          <div class="tv-win-cats">${cats}</div>
          <div class="tv-select-grid">${tiles}</div>
        </div>
      `;
    }

    // 3. Keyboard Set Library Select Window
    if (state.overlayWindow === "kbd_lib_select") {
      const cats = DATA.libraryCategories.map(c =>
        `<button type="button" class="tv-cat-btn ${state.activeLibCategory === c.id ? "active" : ""}" data-tv-libcat="${c.id}">${c.short}</button>`
      ).join("");
      const items = DATA.keyboardSetLibrary[state.activeLibCategory] || [];
      const tiles = items.map((it, idx) => `
        <div class="tv-select-tile ${state.kbdSetName === it.name ? "active" : ""}" data-tv-picklib="${idx}">
          <span>${escapeHtml(it.name)}</span>
          <span style="font-size:0.48cqi;opacity:0.85;">${escapeHtml(it.up1.sound)}</span>
        </div>
      `).join("");
      return `
        <div class="tv-window">
          <div class="tv-win-cats">${cats}</div>
          <div class="tv-select-grid">${tiles}</div>
        </div>
      `;
    }

    // 4. Sound Select Window (for UP1/UP2/UP3/LOW individual voice or SOUND mode)
    if (state.overlayWindow === "sound_select") {
      const curSound = state.tracks[state.selectedTrackKey].sound;
      const tiles = DATA.soundsCatalog.map(snd => `
        <div class="tv-select-tile ${curSound === snd ? "active" : ""}" data-tv-picksound="${escapeHtml(snd)}">
          <span>${escapeHtml(snd)}</span>
        </div>
      `).join("");
      return `
        <div class="tv-window">
          <div style="background:#18191c;padding:2px 6px;font-size:0.56cqi;color:#5eead4;font-weight:700;">
            Assigning Sound to Track: <strong>${state.selectedTrackKey.toUpperCase()}</strong> (Press EXIT when done)
          </div>
          <div class="tv-select-grid">${tiles}</div>
        </div>
      `;
    }

    // 5. Lyrics / Score / Marker / Global / Menu / Media / Search Windows
    const song = DATA.playerSongs[state.currentSongIdx];
    let infoTitle = state.overlayWindow.toUpperCase();
    let infoBody = "";
    if (state.overlayWindow === "lyrics") {
      infoTitle = `LYRICS — ${song.name}`;
      infoBody = `<pre style="margin:4px 0;white-space:pre-wrap;font-family:inherit;color:#fde047;">${escapeHtml(song.lyrics)}</pre>`;
    } else if (state.overlayWindow === "score") {
      infoTitle = `MUSICAL SCORE — ${song.name}`;
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
        } else if (act === "focus_tempo") {
          state.focusedParam = "tempo";
          logAction("Focused Tempo on TouchView -> Turn the silver VALUE dial or click TEMPO -/+.");
        } else if (act === "cycle_song") {
          state.currentSongIdx = (state.currentSongIdx + 1) % DATA.playerSongs.length;
          logAction(`Selected Song "${DATA.playerSongs[state.currentSongIdx].name}".`);
        } else if (act === "open_kbd_select") {
          state.overlayWindow = "kbd_lib_select";
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
          logAction(`Tapped ${tk.toUpperCase()} again -> Opened Sound Select window for ${tk.toUpperCase()}.`);
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

    // Pad tiles
    screen.querySelectorAll("[data-tv-pad]").forEach(el => {
      el.addEventListener("click", () => {
        const idx = parseInt(el.dataset.tvPad, 10) + 1;
        handleButtonPress(`pad_${idx}`, false);
      });
    });

    // Select window actions
    screen.querySelectorAll("[data-tv-pickstyle]").forEach(el => {
      el.addEventListener("click", () => {
        selectStyleByIndex(parseInt(el.dataset.tvPickstyle, 10));
      });
    });
    screen.querySelectorAll("[data-tv-stylecat]").forEach(el => {
      el.addEventListener("click", () => {
        const cat = el.dataset.tvStylecat;
        const idx = DATA.styles.findIndex(s => s.category === cat);
        if (idx >= 0) selectStyleByIndex(idx);
      });
    });
    screen.querySelectorAll("[data-tv-libcat]").forEach(el => {
      el.addEventListener("click", () => {
        state.activeLibCategory = el.dataset.tvLibcat;
        renderAll();
      });
    });
    screen.querySelectorAll("[data-tv-picklib]").forEach(el => {
      el.addEventListener("click", () => {
        applyLibraryKbdSet(state.activeLibCategory, parseInt(el.dataset.tvPicklib, 10));
        renderAll();
      });
    });
    screen.querySelectorAll("[data-tv-picksound]").forEach(el => {
      el.addEventListener("click", () => {
        const snd = el.dataset.tvPicksound;
        state.tracks[state.selectedTrackKey].sound = snd;
        state.tracks[state.selectedTrackKey].muted = false;
        logAction(`Assigned Sound "${snd}" to ${state.selectedTrackKey.toUpperCase()}!`);
        renderAll();
      });
    });
    screen.querySelectorAll("[data-tv-setlist]").forEach(el => {
      el.addEventListener("click", () => {
        state.setListMode = true;
        handleLibraryOrSetListButton(parseInt(el.dataset.tvSetlist, 10));
        renderAll();
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
      state.currentStyleIdx = 0;
      state.tempo = DATA.styles[0].tempo;
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
        window.pa700Audio.syncPanelControls(state);
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
    if (window.pa700Audio) window.pa700Audio.syncPanelControls(state);
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
