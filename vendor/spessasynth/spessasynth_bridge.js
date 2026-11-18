/**
 * Browser ES module bridge exposing local vendored SpessaSynth v4.4 modules
 * onto window.SpessaSynth for classic script consumers (pa700_audio.js) on static hosts.
 */
import {
  WorkletSynthesizer,
  SoundBankManager,
} from "./spessasynth_lib.js";
import {
  SpessaSynthProcessor,
  SoundBankLoader,
  BasicMIDI,
  MIDIControllers,
  SpessaSynthCoreUtils,
} from "./spessasynth_core.js";

window.SpessaSynth = {
  ready: true,
  WorkletSynthesizer,
  SoundBankManager,
  SpessaSynthProcessor,
  SoundBankLoader,
  BasicMIDI,
  MIDIControllers,
  SpessaSynthCoreUtils,
};

window.dispatchEvent(new CustomEvent("spessasynth-ready"));
