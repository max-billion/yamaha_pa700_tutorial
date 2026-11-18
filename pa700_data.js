// Authentic Korg Pa700 Musical Resource Catalog & Guided Gig Drills
// Derived from Pa700 / Pa700 ORIENTAL User Manual v1.5 and upscaled_full_control_panel.png

window.PA700_DATA = {
  mySetting: {
    name: "My Setting",
    source: "Kbd Set Library",
    splitOn: true,
    localSplit: null, // uses Global split (C4)
    ensembleOn: false,
    ensembleType: "Duet",
    tracks: {
      up1: { sound: "Concert Grand", muted: false, octave: 0, volume: 100, family: "Piano" },
      up2: { sound: "Dark Pad", muted: true, octave: 0, volume: 78, family: "Synth" },
      up3: { sound: "Strings Ens.2 GM", muted: true, octave: 0, volume: 82, family: "Strings" },
      low: { sound: "Movie Strings 1", muted: false, octave: 1, volume: 75, family: "Strings", backing: true }
    }
  },

  libraryCategories: [
    { id: "piano_ep", num: 1, label: "PIANO & EP", short: "Piano & EP" },
    { id: "organ", num: 2, label: "ORGAN", short: "Organ" },
    { id: "guitar", num: 3, label: "GUITAR", short: "Guitar" },
    { id: "strings", num: 4, label: "STRINGS", short: "Strings" },
    { id: "brass", num: 5, label: "BRASS", short: "Brass" },
    { id: "trumpet", num: 6, label: "TRUMPET", short: "Trumpet" },
    { id: "sax_wood", num: 7, label: "SAX&WOOD.", short: "Sax & Wood." },
    { id: "synth", num: 8, label: "SYNTH", short: "Synth" },
    { id: "ethnic", num: 9, label: "ETHNIC", short: "Ethnic" }
  ],

  keyboardSetLibrary: {
    piano_ep: [
      {
        name: "Concert Grand",
        up1: { sound: "Concert Grand", muted: false, octave: 0 },
        up2: { sound: "Warm Pad", muted: true, octave: 0 },
        up3: { sound: "Symphonic Strings", muted: true, octave: 0 },
        low: { sound: "Acoustic Bass & Ride", muted: false, octave: 0 }
      },
      {
        name: "Honky-Tonk",
        up1: { sound: "Honky-Tonk Piano", muted: false, octave: 0 },
        up2: { sound: "Ragtime Upright", muted: false, octave: 0 },
        up3: { sound: "Sub Octave Piano", muted: true, octave: -1 },
        low: { sound: "Upright Jazz Bass", muted: false, octave: 0 }
      },
      {
        name: "Classic Grand",
        up1: { sound: "Classic Grand DNC", muted: false, octave: 0 },
        up2: { sound: "Soft String Pad", muted: true, octave: 0 },
        up3: { sound: "Bell Choir", muted: true, octave: 1 },
        low: { sound: "Warm Strings Low", muted: false, octave: 1 }
      },
      {
        name: "Jazz Piano",
        up1: { sound: "Club Jazz Piano", muted: false, octave: 0 },
        up2: { sound: "Vibes Companion", muted: true, octave: 0 },
        up3: { sound: "Brush Ride Layer", muted: true, octave: 0 },
        low: { sound: "Walking Acoustic Bass", muted: false, octave: 0 }
      },
      {
        name: "Grand Piano Live",
        up1: { sound: "Stage Grand Live", muted: false, octave: 0 },
        up2: { sound: "Bright Rock Piano", muted: false, octave: 0 },
        up3: { sound: "Analog Strings", muted: true, octave: 0 },
        low: { sound: "Movie Strings 1", muted: false, octave: 1 }
      },
      {
        name: "Korg M1 Piano",
        up1: { sound: "M1 House Piano", muted: false, octave: 0 },
        up2: { sound: "90s Organ Layer", muted: true, octave: 0 },
        up3: { sound: "Digital Choir", muted: true, octave: 0 },
        low: { sound: "House Synth Bass", muted: false, octave: 0 }
      },
      {
        name: "Piano & Strings",
        up1: { sound: "Concert Grand", muted: false, octave: 0 },
        up2: { sound: "Lush Legato Strings", muted: false, octave: 0 },
        up3: { sound: "Warm Analog Pad", muted: true, octave: 0 },
        low: { sound: "Cello & Bass Sect.", muted: false, octave: 0 }
      },
      {
        name: "Suitcase EP",
        up1: { sound: "Suitcase Tine EP", muted: false, octave: 0 },
        up2: { sound: "FM Dyno Bell EP", muted: true, octave: 0 },
        up3: { sound: "Phaser Pad", muted: true, octave: 0 },
        low: { sound: "Finger Electric Bass", muted: false, octave: 0 }
      }
    ],
    organ: [
      {
        name: "Jimmy Organ",
        up1: { sound: "Jimmy Jazz Organ", muted: false, octave: 0 },
        up2: { sound: "Percussion 3rd", muted: false, octave: 0 },
        up3: { sound: "Key Click Layer", muted: true, octave: 0 },
        low: { sound: "Lower Drawbars 88", muted: false, octave: 0 }
      },
      {
        name: "Gospel BX3",
        up1: { sound: "Full Drawbars BX3", muted: false, octave: 0 },
        up2: { sound: "Rotary Horn Warm", muted: false, octave: 0 },
        up3: { sound: "Gospel Piano", muted: true, octave: 0 },
        low: { sound: "Pedal Organ Bass", muted: false, octave: 0 }
      },
      {
        name: "Rock Rotary",
        up1: { sound: "Overdriven Rock Organ", muted: false, octave: 0 },
        up2: { sound: "Double Rock Organ", muted: true, octave: -1 },
        up3: { sound: "Lead Synth", muted: true, octave: 0 },
        low: { sound: "Picked Rock Bass", muted: false, octave: 0 }
      },
      {
        name: "Church Pipe Tutti",
        up1: { sound: "Cathedral Principal", muted: false, octave: 0 },
        up2: { sound: "Pipe Mixture IV", muted: false, octave: 0 },
        up3: { sound: "Cathedral Choir", muted: true, octave: 0 },
        low: { sound: "16ft Bourdon Pedal", muted: false, octave: -1 }
      }
    ],
    guitar: [
      {
        name: "Nylon Guitar",
        up1: { sound: "Concert Nylon DNC", muted: false, octave: 0 },
        up2: { sound: "Soft Breath Pad", muted: true, octave: 0 },
        up3: { sound: "Classical Harmonics", muted: true, octave: 0 },
        low: { sound: "Warm Fretless Bass", muted: false, octave: 0 }
      },
      {
        name: "Steel Folk Gtr",
        up1: { sound: "Steel Acoustic DNC", muted: false, octave: 0 },
        up2: { sound: "12-String Shimmer", muted: true, octave: 0 },
        up3: { sound: "Warm Pad", muted: true, octave: 0 },
        low: { sound: "Acoustic Folk Bass", muted: false, octave: 0 }
      },
      {
        name: "Clean Funk Strat",
        up1: { sound: "Single Coil Clean", muted: false, octave: 0 },
        up2: { sound: "Chorus Strat", muted: false, octave: 0 },
        up3: { sound: "Clavinet Funk", muted: true, octave: 0 },
        low: { sound: "Slap Funk Bass", muted: false, octave: 0 }
      },
      {
        name: "Blues Lead Gtr",
        up1: { sound: "Tube Overdrive Gtr", muted: false, octave: 0 },
        up2: { sound: "Feedback Harmonics", muted: true, octave: 1 },
        up3: { sound: "Warm Organ Pad", muted: true, octave: 0 },
        low: { sound: "Finger Bass", muted: false, octave: 0 }
      }
    ],
    strings: [
      {
        name: "Symphonic Strings",
        up1: { sound: "Orchestra Strings 1", muted: false, octave: 0 },
        up2: { sound: "Legato Violins", muted: false, octave: 0 },
        up3: { sound: "Timpani Roll", muted: true, octave: -1 },
        low: { sound: "Cellos & Contrabass", muted: false, octave: 0 }
      },
      {
        name: "Solo Violin DNC",
        up1: { sound: "Solo Romance Violin", muted: false, octave: 0 },
        up2: { sound: "Chamber Strings", muted: true, octave: 0 },
        up3: { sound: "Harp Arpeggio", muted: true, octave: 0 },
        low: { sound: "Pizzicato & Arco Low", muted: false, octave: 0 }
      },
      {
        name: "Cinema Lush Pad",
        up1: { sound: "Movie Strings 1", muted: false, octave: 0 },
        up2: { sound: "Warm Choir Aahs", muted: false, octave: 0 },
        up3: { sound: "Celesta Sparkle", muted: true, octave: 1 },
        low: { sound: "Deep Cinema Strings", muted: false, octave: 0 }
      },
      {
        name: "Disco Strings",
        up1: { sound: "70s Disco Violins", muted: false, octave: 1 },
        up2: { sound: "Octave Fall Strings", muted: false, octave: 0 },
        up3: { sound: "Brass Hit", muted: true, octave: 0 },
        low: { sound: "Disco Octave Bass", muted: false, octave: 0 }
      }
    ],
    brass: [
      {
        name: "Big Band Brass",
        up1: { sound: "Tight Brass Section", muted: false, octave: 0 },
        up2: { sound: "Tenor & Bari Saxes", muted: false, octave: -1 },
        up3: { sound: "Lead Scream Trumpet", muted: true, octave: 0 },
        low: { sound: "Swing Upright Bass", muted: false, octave: 0 }
      },
      {
        name: "Funk Horn Sect.",
        up1: { sound: "Tower Funk Horns", muted: false, octave: 0 },
        up2: { sound: "Trombone Section", muted: false, octave: 0 },
        up3: { sound: "Fall Brass FX", muted: true, octave: 0 },
        low: { sound: "Funk Finger Bass", muted: false, octave: 0 }
      },
      {
        name: "French Horns",
        up1: { sound: "Noble French Horns", muted: false, octave: 0 },
        up2: { sound: "Orchestral Strings", muted: true, octave: 0 },
        up3: { sound: "Tuba & Trombones", muted: true, octave: -1 },
        low: { sound: "Low Brass Ensemble", muted: false, octave: 0 }
      },
      {
        name: "Latin Mambo Brass",
        up1: { sound: "Salsa Trumpets", muted: false, octave: 0 },
        up2: { sound: "Mambo Trombones", muted: false, octave: -1 },
        up3: { sound: "Montuno Piano", muted: true, octave: 0 },
        low: { sound: "Baby Salsa Bass", muted: false, octave: 0 }
      }
    ],
    trumpet: [
      {
        name: "Expressive Tpt",
        up1: { sound: "Solo Trumpet DNC", muted: false, octave: 0 },
        up2: { sound: "Soft Strings", muted: true, octave: 0 },
        up3: { sound: "Breath Nuance", muted: true, octave: 0 },
        low: { sound: "Warm Backing Pad", muted: false, octave: 1 }
      },
      {
        name: "Trumpet & Mute",
        up1: { sound: "Harmon Mute Trumpet", muted: false, octave: 0 },
        up2: { sound: "Jazz Vibes", muted: true, octave: 0 },
        up3: { sound: "Brush Pad", muted: true, octave: 0 },
        low: { sound: "Jazz Lounge Strings", muted: false, octave: 1 }
      },
      {
        name: "Flugelhorn Solo",
        up1: { sound: "Warm Flugelhorn DNC", muted: false, octave: 0 },
        up2: { sound: "Suitcase EP", muted: true, octave: 0 },
        up3: { sound: "Velvet Strings", muted: true, octave: 0 },
        low: { sound: "Movie Strings 1", muted: false, octave: 1 }
      },
      {
        name: "Mariachi Duo",
        up1: { sound: "Mariachi Trumpet 1", muted: false, octave: 0 },
        up2: { sound: "Mariachi Trumpet 2", muted: false, octave: 0 },
        up3: { sound: "Violins Section", muted: true, octave: 0 },
        low: { sound: "Guitarron Bass", muted: false, octave: 0 }
      }
    ],
    sax_wood: [
      {
        name: "Sweet Tenor Sax",
        up1: { sound: "Tenor Sax Growl DNC", muted: false, octave: 0 },
        up2: { sound: "Breath Sub-Tone", muted: false, octave: 0 },
        up3: { sound: "Soft EP Pad", muted: true, octave: 0 },
        low: { sound: "Warm Strings Pad", muted: false, octave: 1 }
      },
      {
        name: "Jazz Alto Sax",
        up1: { sound: "Bebop Alto Sax DNC", muted: false, octave: 0 },
        up2: { sound: "Tenor Section", muted: true, octave: 0 },
        up3: { sound: "Muted Trumpet", muted: true, octave: 0 },
        low: { sound: "Acoustic Jazz Bass", muted: false, octave: 0 }
      },
      {
        name: "Silver Flute",
        up1: { sound: "Concert Flute DNC", muted: false, octave: 1 },
        up2: { sound: "Chiff Overblow", muted: false, octave: 1 },
        up3: { sound: "Celesta", muted: true, octave: 1 },
        low: { sound: "Chamber Strings", muted: false, octave: 1 }
      },
      {
        name: "Jazz Clarinet",
        up1: { sound: "Wood Clarinet DNC", muted: false, octave: 0 },
        up2: { sound: "Vibraphone", muted: true, octave: 0 },
        up3: { sound: "Swing Guitar", muted: true, octave: 0 },
        low: { sound: "Swing Bass", muted: false, octave: 0 }
      }
    ],
    synth: [
      {
        name: "Analog Saw Lead",
        up1: { sound: "Fat Poly Saw Lead", muted: false, octave: 0 },
        up2: { sound: "Sub Oscillator", muted: false, octave: -1 },
        up3: { sound: "Fifth Sync Lead", muted: true, octave: 0 },
        low: { sound: "Analog Warm Pad", muted: false, octave: 0 }
      },
      {
        name: "80s Poly Brass",
        up1: { sound: "OB Jump Brass", muted: false, octave: 0 },
        up2: { sound: "JP Super Strings", muted: false, octave: 0 },
        up3: { sound: "Bell Arpeggio", muted: true, octave: 1 },
        low: { sound: "80s Synth Bass", muted: false, octave: 0 }
      },
      {
        name: "Warm Heaven Pad",
        up1: { sound: "Heavenly Choir Pad", muted: false, octave: 0 },
        up2: { sound: "Crystal Digital Bell", muted: false, octave: 1 },
        up3: { sound: "Sweep Pad", muted: true, octave: 0 },
        low: { sound: "Deep Sub Pad", muted: false, octave: 0 }
      },
      {
        name: "Euro Dance Lead",
        up1: { sound: "Supersaw Anthem", muted: false, octave: 0 },
        up2: { sound: "Pluck Synth", muted: false, octave: 0 },
        up3: { sound: "White Noise Rise", muted: true, octave: 0 },
        low: { sound: "Offbeat Euro Bass", muted: false, octave: 0 }
      }
    ],
    ethnic: [
      {
        name: "French Musette",
        up1: { sound: "Accordion Musette", muted: false, octave: 0 },
        up2: { sound: "Bassoon Reed", muted: true, octave: -1 },
        up3: { sound: "Clarinet Doubler", muted: true, octave: 0 },
        low: { sound: "Accordion Left Chords", muted: false, octave: 0 }
      },
      {
        name: "Oriental Oud&Nay",
        up1: { sound: "Arabic Oud DNC", muted: false, octave: 0 },
        up2: { sound: "Breath Nay Flute", muted: false, octave: 1 },
        up3: { sound: "Oriental Strings", muted: true, octave: 0 },
        low: { sound: "Qanun & Drone", muted: false, octave: 0 }
      },
      {
        name: "Harmonica",
        up1: { sound: "Chromatic Harmonica", muted: false, octave: 0 },
        up2: { sound: "Blues Harp Bend", muted: true, octave: 0 },
        up3: { sound: "Soft Strings", muted: true, octave: 0 },
        low: { sound: "Movie Strings 1", muted: false, octave: 1 }
      },
      {
        name: "Kanun & Strings",
        up1: { sound: "Turkish Kanun Trem", muted: false, octave: 0 },
        up2: { sound: "Cairo Violin Sect.", muted: false, octave: 0 },
        up3: { sound: "Zurna Lead", muted: true, octave: 0 },
        low: { sound: "Oriental Backing Pad", muted: false, octave: 0 }
      }
    ]
  },

  soundsCatalog: [
    "Concert Grand", "Classic Grand DNC", "Honky-Tonk Piano", "M1 House Piano",
    "Suitcase Tine EP", "FM Dyno Bell EP", "Jimmy Jazz Organ", "Full Drawbars BX3",
    "Overdriven Rock Organ", "Concert Nylon DNC", "Steel Acoustic DNC", "Single Coil Clean",
    "Tube Overdrive Gtr", "Orchestra Strings 1", "Movie Strings 1", "Strings Ens.2 GM",
    "Solo Romance Violin", "Tight Brass Section", "Tower Funk Horns", "Solo Trumpet DNC",
    "Harmon Mute Trumpet", "Warm Flugelhorn DNC", "Tenor Sax Growl DNC", "Bebop Alto Sax DNC",
    "Concert Flute DNC", "Fat Poly Saw Lead", "OB Jump Brass", "Dark Pad",
    "Warm Pad", "Accordion Musette", "Arabic Oud DNC", "Chromatic Harmonica"
  ],

  styleCategories: [
    "Ballad", "Pop", "8 Beat", "16 Beat", "Rock", "Jazz", "Latin", "Dance", "World"
  ],

  styles: [
    {
      id: "brush_ballad",
      name: "Brush Ballad",
      category: "Ballad",
      bank: "Fty-Ballad",
      meter: "6/8",
      beatsPerBar: 6,
      patternBars: 8,
      tempo: 73,
      pads: [
        { name: "Brush Swirl", type: "Loop" },
        { name: "Nylon Arpeggio", type: "Loop" },
        { name: "Soft Windchime", type: "OneShot" },
        { name: "Warm String Swell", type: "Loop" }
      ],
      kbdSets: [
        { name: "Nylon Guitar", up1: "Concert Nylon DNC", up2: "Warm Pad", up2Muted: true, up3: "Strings Ens.2 GM", up3Muted: true, low: "Movie Strings 1" },
        { name: "Organ", up1: "Jimmy Jazz Organ", up2: "Suitcase Tine EP", up2Muted: true, up3: "Dark Pad", up3Muted: true, low: "Movie Strings 1" },
        { name: "Trumpet & Mute", up1: "Harmon Mute Trumpet", up2: "Warm Flugelhorn DNC", up2Muted: true, up3: "Dark Pad", up3Muted: true, low: "Movie Strings 1" },
        { name: "Harmonica", up1: "Chromatic Harmonica", up2: "Concert Grand", up2Muted: true, up3: "Strings Ens.2 GM", up3Muted: false, low: "Movie Strings 1" }
      ]
    },
    {
      id: "8beat_standard",
      name: "8 Beat Standard",
      category: "8 Beat",
      bank: "Fty-8 Beat",
      meter: "4/4",
      beatsPerBar: 4,
      patternBars: 4,
      tempo: 112,
      pads: [
        { name: "Tambourine 8th", type: "Loop" },
        { name: "Acoustic Strumming", type: "Loop" },
        { name: "Pop Brass Hit", type: "OneShot" },
        { name: "EP Comping", type: "Loop" }
      ],
      kbdSets: [
        { name: "Stage Grand", up1: "Concert Grand", up2: "Warm Pad", up2Muted: false, up3: "Strings Ens.2 GM", up3Muted: true, low: "Movie Strings 1" },
        { name: "Suitcase EP", up1: "Suitcase Tine EP", up2: "Dark Pad", up2Muted: true, up3: "Single Coil Clean", up3Muted: true, low: "Movie Strings 1" },
        { name: "Sweet Tenor", up1: "Tenor Sax Growl DNC", up2: "Tight Brass Section", up2Muted: true, up3: "Warm Pad", up3Muted: true, low: "Movie Strings 1" },
        { name: "Pop Lead & Strings", up1: "Fat Poly Saw Lead", up2: "Orchestra Strings 1", up2Muted: false, up3: "Concert Grand", up3Muted: true, low: "Movie Strings 1" }
      ]
    },
    {
      id: "pop_chart",
      name: "Modern Pop Hit",
      category: "Pop",
      bank: "Fty-Pop",
      meter: "4/4",
      beatsPerBar: 4,
      patternBars: 4,
      tempo: 120,
      pads: [
        { name: "Clap Groove", type: "Loop" },
        { name: "Funky Mute Gtr", type: "Loop" },
        { name: "Synth Riser FX", type: "OneShot" },
        { name: "Pluck Synth Arp", type: "Loop" }
      ],
      kbdSets: [
        { name: "Pop Piano & Pad", up1: "Concert Grand", up2: "Dark Pad", up2Muted: false, up3: "Strings Ens.2 GM", up3Muted: true, low: "Warm Pad" },
        { name: "Clean Funk Gtr", up1: "Single Coil Clean", up2: "FM Dyno Bell EP", up2Muted: false, up3: "Dark Pad", up3Muted: true, low: "Warm Pad" },
        { name: "Funk Horns", up1: "Tower Funk Horns", up2: "Tenor Sax Growl DNC", up2Muted: false, up3: "OB Jump Brass", up3Muted: true, low: "Warm Pad" },
        { name: "Anthem Lead", up1: "OB Jump Brass", up2: "Fat Poly Saw Lead", up2Muted: false, up3: "Orchestra Strings 1", up3Muted: false, low: "Warm Pad" }
      ]
    },
    {
      id: "16beat_soul",
      name: "16 Beat Soul",
      category: "16 Beat",
      bank: "Fty-16 Beat",
      meter: "4/4",
      beatsPerBar: 4,
      patternBars: 4,
      tempo: 96,
      pads: [
        { name: "Conga 16th", type: "Loop" },
        { name: "Wah Guitar Chick", type: "Loop" },
        { name: "Horn Fall", type: "OneShot" },
        { name: "Rhodes Chord Riff", type: "Loop" }
      ],
      kbdSets: [
        { name: "Dyno Tine EP", up1: "FM Dyno Bell EP", up2: "Warm Pad", up2Muted: false, up3: "Strings Ens.2 GM", up3Muted: true, low: "Movie Strings 1" },
        { name: "Gospel Organ", up1: "Full Drawbars BX3", up2: "Jimmy Jazz Organ", up2Muted: true, up3: "Concert Grand", up3Muted: true, low: "Movie Strings 1" },
        { name: "Soul Alto Sax", up1: "Bebop Alto Sax DNC", up2: "Tower Funk Horns", up2Muted: true, up3: "Warm Pad", up3Muted: true, low: "Movie Strings 1" },
        { name: "Cinema Strings", up1: "Orchestra Strings 1", up2: "Concert Grand", up2Muted: false, up3: "Warm Flugelhorn DNC", up3Muted: true, low: "Movie Strings 1" }
      ]
    },
    {
      id: "classic_rock",
      name: "Classic Stadium Rock",
      category: "Rock",
      bank: "Fty-Rock",
      meter: "4/4",
      beatsPerBar: 4,
      patternBars: 4,
      tempo: 128,
      pads: [
        { name: "Cowbell Beat", type: "Loop" },
        { name: "Power Chord Riff", type: "Loop" },
        { name: "Crash Cymbal", type: "OneShot" },
        { name: "Hammond Gliss", type: "OneShot" }
      ],
      kbdSets: [
        { name: "Rock Piano", up1: "Classic Grand DNC", up2: "Overdriven Rock Organ", up2Muted: false, up3: "Dark Pad", up3Muted: true, low: "Warm Pad" },
        { name: "Rotary Rock Org", up1: "Overdriven Rock Organ", up2: "Classic Grand DNC", up2Muted: true, up3: "Dark Pad", up3Muted: true, low: "Warm Pad" },
        { name: "Tube Lead Guitar", up1: "Tube Overdrive Gtr", up2: "Single Coil Clean", up2Muted: true, up3: "Dark Pad", up3Muted: true, low: "Warm Pad" },
        { name: "80s Jump Synth", up1: "OB Jump Brass", up2: "Fat Poly Saw Lead", up2Muted: false, up3: "Overdriven Rock Organ", up3Muted: true, low: "Warm Pad" }
      ]
    },
    {
      id: "big_band_swing",
      name: "Big Band Swing",
      category: "Jazz",
      bank: "Fty-Jazz",
      meter: "4/4",
      beatsPerBar: 4,
      patternBars: 4,
      tempo: 138,
      pads: [
        { name: "Hi-Hat Foot 2&4", type: "Loop" },
        { name: "Freddie Jazz Gtr", type: "Loop" },
        { name: "Big Band Hit!", type: "OneShot" },
        { name: "Vibes Comping", type: "Loop" }
      ],
      kbdSets: [
        { name: "Swing Trio Piano", up1: "Concert Grand", up2: "Jimmy Jazz Organ", up2Muted: true, up3: "Strings Ens.2 GM", up3Muted: true, low: "Movie Strings 1" },
        { name: "Jazz Clarinet", up1: "Concert Flute DNC", up2: "Bebop Alto Sax DNC", up2Muted: false, up3: "Concert Grand", up3Muted: true, low: "Movie Strings 1" },
        { name: "Solo Trumpet", up1: "Solo Trumpet DNC", up2: "Tight Brass Section", up2Muted: true, up3: "Warm Pad", up3Muted: true, low: "Movie Strings 1" },
        { name: "Full Tutti Brass", up1: "Tight Brass Section", up2: "Tenor Sax Growl DNC", up2Muted: false, up3: "Solo Trumpet DNC", up3Muted: false, low: "Movie Strings 1" }
      ]
    },
    {
      id: "bossa_nova",
      name: "Ipanema Bossa",
      category: "Latin",
      bank: "Fty-Latin",
      meter: "4/4",
      beatsPerBar: 4,
      patternBars: 4,
      tempo: 124,
      pads: [
        { name: "Shaker & Clave", type: "Loop" },
        { name: "Bossa Nylon Comp", type: "Loop" },
        { name: "Agogo Bell", type: "Loop" },
        { name: "Ocean Wave FX", type: "OneShot" }
      ],
      kbdSets: [
        { name: "Bossa Nylon Gtr", up1: "Concert Nylon DNC", up2: "Warm Pad", up2Muted: true, up3: "Concert Flute DNC", up3Muted: true, low: "Movie Strings 1" },
        { name: "Silver Flute", up1: "Concert Flute DNC", up2: "Suitcase Tine EP", up2Muted: false, up3: "Warm Pad", up3Muted: true, low: "Movie Strings 1" },
        { name: "Getz Tenor Sax", up1: "Tenor Sax Growl DNC", up2: "Warm Pad", up2Muted: true, up3: "Concert Nylon DNC", up3Muted: true, low: "Movie Strings 1" },
        { name: "Warm Flugelhorn", up1: "Warm Flugelhorn DNC", up2: "Strings Ens.2 GM", up2Muted: false, up3: "Suitcase Tine EP", up3Muted: true, low: "Movie Strings 1" }
      ]
    },
    {
      id: "disco_fever",
      name: "70s Disco Fever",
      category: "Dance",
      bank: "Fty-Dance",
      meter: "4/4",
      beatsPerBar: 4,
      patternBars: 4,
      tempo: 122,
      pads: [
        { name: "Disco Handclaps", type: "Loop" },
        { name: "Nile Funk Guitar", type: "Loop" },
        { name: "String Fall!", type: "OneShot" },
        { name: "Synth Octave Seq", type: "Loop" }
      ],
      kbdSets: [
        { name: "M1 House Piano", up1: "M1 House Piano", up2: "Orchestra Strings 1", up2Muted: false, up3: "Dark Pad", up3Muted: true, low: "Warm Pad" },
        { name: "Disco Violins", up1: "Orchestra Strings 1", up2: "Movie Strings 1", up2Muted: false, up3: "Tower Funk Horns", up3Muted: true, low: "Warm Pad" },
        { name: "Disco Brass", up1: "Tower Funk Horns", up2: "Tight Brass Section", up2Muted: false, up3: "Orchestra Strings 1", up3Muted: true, low: "Warm Pad" },
        { name: "Synth Lead", up1: "Fat Poly Saw Lead", up2: "OB Jump Brass", up2Muted: false, up3: "M1 House Piano", up3Muted: true, low: "Warm Pad" }
      ]
    },
    {
      id: "arabic_maqsoum",
      name: "Oriental Maqsoum",
      category: "World",
      bank: "Fty-World",
      meter: "4/4",
      beatsPerBar: 4,
      patternBars: 4,
      tempo: 108,
      pads: [
        { name: "Darbuka Solo Roll", type: "Loop" },
        { name: "Riq & Sagat", type: "Loop" },
        { name: "Zaghareet / Hit", type: "OneShot" },
        { name: "Qanun Tremolo", type: "Loop" }
      ],
      kbdSets: [
        { name: "Arabic Oud", up1: "Arabic Oud DNC", up2: "Movie Strings 1", up2Muted: true, up3: "Dark Pad", up3Muted: true, low: "Warm Pad" },
        { name: "Cairo Strings", up1: "Solo Romance Violin", up2: "Orchestra Strings 1", up2Muted: false, up3: "Arabic Oud DNC", up3Muted: true, low: "Warm Pad" },
        { name: "Oriental Accordion", up1: "Accordion Musette", up2: "Arabic Oud DNC", up2Muted: false, up3: "Dark Pad", up3Muted: true, low: "Warm Pad" },
        { name: "Synth Rababa", up1: "Fat Poly Saw Lead", up2: "Solo Romance Violin", up2Muted: false, up3: "Orchestra Strings 1", up3Muted: true, low: "Warm Pad" }
      ]
    },
    {
      id: "viennese_waltz",
      name: "Romantic Waltz",
      category: "World",
      bank: "Fty-Ballroom",
      meter: "3/4",
      beatsPerBar: 3,
      patternBars: 4,
      tempo: 156,
      pads: [
        { name: "Triangle 3/4", type: "Loop" },
        { name: "Harp Waltz Arp", type: "Loop" },
        { name: "Bell Glissando", type: "OneShot" },
        { name: "Strings Pizzicato", type: "Loop" }
      ],
      kbdSets: [
        { name: "French Musette", up1: "Accordion Musette", up2: "Strings Ens.2 GM", up2Muted: true, up3: "Concert Grand", up3Muted: true, low: "Movie Strings 1" },
        { name: "Waltz Strings", up1: "Orchestra Strings 1", up2: "Concert Flute DNC", up2Muted: false, up3: "Concert Grand", up3Muted: true, low: "Movie Strings 1" },
        { name: "Grand Piano", up1: "Concert Grand", up2: "Orchestra Strings 1", up2Muted: false, up3: "Warm Pad", up3Muted: true, low: "Movie Strings 1" },
        { name: "Solo Violin", up1: "Solo Romance Violin", up2: "Strings Ens.2 GM", up2Muted: false, up3: "Concert Flute DNC", up3Muted: true, low: "Movie Strings 1" }
      ]
    }
  ],

  // Exact 9 SongBook Set List entries visible on upscaled_full_control_panel.png!
  setListEntries: [
    { slot: 1, title: "(Wanna come) Home", type: "STY", styleId: "8beat_standard", tempo: 114, variation: 1, kbdIdx: 0 },
    { slot: 2, title: "1/2 minute", type: "STY", styleId: "16beat_soul", tempo: 94, variation: 1, kbdIdx: 0 },
    { slot: 3, title: "A believer", type: "STY", styleId: "classic_rock", tempo: 132, variation: 2, kbdIdx: 1 },
    { slot: 4, title: "A gigolo'", type: "STY", styleId: "big_band_swing", tempo: 136, variation: 2, kbdIdx: 2 },
    { slot: 5, title: "A hard day/night", type: "STY", styleId: "classic_rock", tempo: 138, variation: 2, kbdIdx: 0 },
    { slot: 6, title: "A walk on wild", type: "STY", styleId: "brush_ballad", tempo: 84, variation: 1, kbdIdx: 2 },
    { slot: 7, title: "Apache song", type: "STY", styleId: "8beat_standard", tempo: 126, variation: 2, kbdIdx: 1 },
    { slot: 8, title: "As song", type: "STY", styleId: "16beat_soul", tempo: 104, variation: 3, kbdIdx: 1 },
    { slot: 9, title: "Baker road", type: "STY", styleId: "pop_chart", tempo: 118, variation: 3, kbdIdx: 2 }
  ],

  playerSongs: [
    { name: "01_Autumn_Leaves_Backing.mid", type: "MID", tempo: 118, length: "03:42", lyrics: "The falling leaves drift by the window...\nThe autumn leaves of red and gold..." },
    { name: "02_Fly_Me_To_The_Moon.kar", type: "KAR", tempo: 124, length: "02:54", lyrics: "Fly me to the moon, let me play among the stars...\nLet me see what spring is like on Jupiter and Mars..." },
    { name: "03_Stand_By_Me_Live.mp3", type: "MP3", tempo: 118, length: "03:05", lyrics: "When the night has come, and the land is dark...\nAnd the moon is the only light we'll see..." },
    { name: "04_Smooth_Latin_Groove.mid", type: "MID", tempo: 116, length: "04:10", lyrics: "Man, it's a hot one...\nLike seven inches from the midday sun..." }
  ],

  subScalePresets: [
    { id: 1, label: "SC1", name: "Rast on C (E & B -50c)", notes: [4, 11] },
    { id: 2, label: "SC2", name: "Bayati on D (E & B -50c)", notes: [4, 11] },
    { id: 3, label: "SC3", name: "Sikah / Huzam (E -50c)", notes: [4] },
    { id: 4, label: "SC4", name: "Arabic Saba (E, A, B -50c)", notes: [4, 9, 11] }
  ],

  drills: [
    {
      id: "voices",
      title: "Drill 1: Changing Voices Fast (4 Ways + Set List Trap)",
      steps: [
        {
          prompt: "1. Notice SET LIST (bottom-right) is OFF. Click 'ORGAN' (button 2 in KEYBOARD SET LIBRARY) to load a Jazz Organ voice set.",
          targetBtn: "ksl_2"
        },
        {
          prompt: "2. Click note G4 (right side of the keyboard) to play a G Major triad (G4-B4-D5) with your new Organ voice!",
          targetKey: 67
        },
        {
          prompt: "3. Now test Style-matched voices: click KEYBOARD SET '3' right under the TouchView screen to switch to the Style's 3rd voice.",
          targetBtn: "kbd_set_3"
        },
        {
          prompt: "4. Watch out for the #1 gig trap: click 'SET LIST' (left of PIANO & EP). When its red LED is ON, buttons 1-9 switch SongBook songs instead of instrument families! Click 'SET LIST' again to return to Voice Library mode.",
          targetBtn: "set_list"
        },
        {
          prompt: "5. Emergency Home Voice: click 'MY SETTING' (white label, bottom-right of center) to instantly restore your favorite Concert Grand piano setup!",
          targetBtn: "my_setting"
        }
      ]
    },
    {
      id: "arranger",
      title: "Drill 2: Running Auto-Arranger (Intro -> Variations -> Fill -> Ending)",
      steps: [
        {
          prompt: "1. Make sure SPLIT, ACCOMP., MEMORY, and AUTO FILL are ON. Click 'SYNCHRO START' (round button left of red START/STOP) so the band waits for your left hand!",
          targetBtn: "synchro_start"
        },
        {
          prompt: "2. Book your song's opening: click 'VARIATION 1' (sparse verse), then click 'INTRO 2' (intro using your chord). Notice VARIATION 1 starts blinking (booked after Intro)!",
          targetBtn: "intro_2"
        },
        {
          prompt: "3. Trigger the band! Click note G2 (left of C4 split point) to feed a G Major triad (G2-B2-D3) to the Arranger.",
          targetKey: 43
        },
        {
          prompt: "4. Build energy into the Chorus! Click 'VARIATION 3'. Because AUTO FILL is lit, Pa700 plays a drum fill first, then drops into Variation 3!",
          targetBtn: "var_3"
        },
        {
          prompt: "5. Add a dramatic 1-bar pause by clicking 'BREAK', or wrap up the song right now by clicking 'ENDING 3' (immediate 2-bar ending + auto-stop)!",
          targetBtn: "ending_3"
        }
      ]
    },
    {
      id: "split",
      title: "Drill 3: Changing the Split Point & Full-Piano Mode",
      steps: [
        {
          prompt: "1. Press and HOLD the 'SPLIT' button (right panel, above Strings/Brass) for ~0.6s until the green 'Split Point' popup opens on screen!",
          targetBtn: "split"
        },
        {
          prompt: "2. Click key F3 on the 61-key keyboard to move the Split Point lower to F3 (giving your right hand more room)!",
          targetKey: 53
        },
        {
          prompt: "3. Want solo full-range piano with NO split? Click 'SPLIT' briefly to turn its LED OFF—now your Upper voice spans all 61 keys!",
          targetBtn: "split"
        }
      ]
    }
  ]
};
