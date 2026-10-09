# ViewController Lifecycle — Narration Script

**Course:** IOS · Interview Prep  
**Video:** `bc-bbg-ios-lifecycle.mp4` (silent preview, 30s, 1280x720)  
**Status:** Preview — narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.

## Concept

UIViewController: viewDidLoad once, viewWillAppear/viewDidAppear every appearance, disappear in reverse. Load once, appear often — put setup and refresh in the right callbacks.

## Voiceover cues

- `[0:04–0:10]` viewDidLoad: once — build the hierarchy
- `[0:10–0:16]` viewWillAppear: every time — refresh data
- `[0:16–0:22]` viewDidAppear: animations start here
- `[0:22–0:26]` Disappear: reverse — pause, save, release

## Full script

Welcome to Interstitium Labs. viewDidLoad: once — build the hierarchy viewWillAppear: every time — refresh data viewDidAppear: animations start here Disappear: reverse — pause, save, release This is a captioned preview; full voiceover ships with the next render pass.
