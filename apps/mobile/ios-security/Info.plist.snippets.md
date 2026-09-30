# iOS App Transport Security

After `npx cap add ios`, confirm `Info.plist`:

- Do **not** set `NSAllowsArbitraryLoads` to `true`
- Prefer default ATS (HTTPS only)
- Localhost for Capacitor live reload is handled by debug tooling; do not add broad exception domains

Universal Links (later): associated domains `applinks:interstitiumlabs.dev` only after `apple-app-site-association` is published.

Status bar: light content on the void `#070B16` background via the Capacitor StatusBar plugin (`Style.Dark`).

Scene lifecycle: since Capacitor 8.5 the app uses UIScene (`SceneDelegate.swift` + `UIApplicationSceneManifest`). URL opens and universal links now arrive through `SceneDelegate`, which forwards them to Capacitor; do not add handling to the AppDelegate `open url` / `continue userActivity` methods, which iOS no longer calls.

## Lab Muse — microphone (Web Speech dictation)

Add to `App/App/Info.plist` before TestFlight / App Store if voice dictation is enabled in the WebView:

```xml
<key>NSMicrophoneUsageDescription</key>
<string>Lab Muse uses the microphone for optional on-device dictation of study questions. Audio stays in the browser Web Speech path — Interstitium does not upload voice to Meta or third-party connectors.</string>
<key>NSSpeechRecognitionUsageDescription</key>
<string>Lab Muse may use on-device speech recognition so you can dictate stuck questions hands-free. Optional; typing always works.</string>
```

Keep Interstitium display name / lockup language. Do not copy Meta Muse permission strings.
