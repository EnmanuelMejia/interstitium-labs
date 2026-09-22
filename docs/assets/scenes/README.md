# Curriculum 3D scenes

Place exported **glTF 2.0** (`.glb` preferred) here. Naming:

| Pattern | Use |
|---------|-----|
| `lecture-<slug>.glb` | Lecture / theory stages |
| `cert-<slug>.glb` | Cert lab environments |
| `sim-<slug>.glb` | Simulations |
| `lab-<slug>.glb` | Non-cert / open labs |

Pipeline: Blender → glTF Binary → this folder → `data-gltf="/assets/scenes/…"`.  
Until a `.glb` lands, `il-immersive.js` uses the procedural WebGL stage (CSP-safe).  
Godot can export glTF too. Unreal high-fidelity: Pixel Streaming — see `/ops/IMMERSIVE-3D.md`.
