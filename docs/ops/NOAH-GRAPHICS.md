# Noah original 3D source and web media

Verified on October 2, 2026. These assets are original procedural Interstitium Labs geometry. No film footage, stock photograph, third-party character, or external music was incorporated.

## Delivered source and poster

| Asset | Verified properties | Purpose |
| --- | --- | --- |
| `assets/noah/noah-neural.glb` | Valid glTF 2.0 binary; 96 spatial neural nodes and 165 connections from `scripts/build-noah-neural.py` | Portable original geometry |
| `assets/noah/noah-neural.json` | Shared node/connection positions; 20-second period | Browser WebGL geometry and activity display |
| `assets/noah/noah-neural.blend` | Independently reopened in Blender 5.2.2; 141 objects, 104 mesh objects, 7 materials, editable signal curves, stage, lights, and camera | Editable native 3D source |
| `assets/noah/noah-neural-poster.webp` | 5120×1440 pixels, 32:9, 261,904 bytes, quality 92 WebP from a native-resolution render | Lightweight ultrawide poster |
| `assets/noah/noah-neural-loop.mp4` | 1920×540 pixels, 32:9, 20.000 seconds, 24 fps, 480 decoded frames, H.264, 4,993,015 bytes | Original web loop, no audio |

Actual source/media SHA-256 hashes, sizes, formats, and verification measurements are recorded in `assets/noah/noah-assets.json`. Hashes identify the reviewed bytes; they do not prove copyright ownership or independently rerun Blender/media validation.

The Blender scene preserves the imported GLB's SHA-256 as a custom property. Verification compares it with the current GLB, confirms an active camera, and checks the native 5120×1440 render configuration. This is a real 3D scene, rather than a `.blend` containing only a flat image.

The rotation rig uses linear keyframes 1 and 481, at 24 fps, for 480 unique animation frames. Independently reopened start/end world matrices differ by at most `1.7484555314695172e-7`, below the `1e-5` verification threshold. Geometry periodicity verifies the animation transform; an encoded video's duration/frame count require their own media checks.

The web poster is rendered with Eevee at native dimensions. The scene uses AgX, a restrained azure/gold palette, emissive conduits, an obsidian stage, and an original translucent core. The final poster render completed without a shadow-buffer warning after setting a 512 MiB shadow pool and half-resolution shadows to fit the verified GPU's budget. Its PNG master is 8-bit SDR and retained outside public assets in ignored `.tools/noah-render-masters/`. Neither the poster nor the source is an HDR10, 4K/8K film master, or a photorealism claim.

## Reproducible generation

The portable runtime came from the [official Blender 5.2.2 Windows ZIP](https://mirror.blender.org/release/Blender5.2/blender-5.2.2-windows-x64.zip). Its ZIP SHA-256 was verified against the [official release manifest](https://mirror.blender.org/release/Blender5.2/blender-5.2.2.sha256):

```text
3849d17a682cba006075aaa3f3597ecb5c9c30ec31035b2e092c53e40679b535
```

No system-wide Blender installation or saved user preference was changed. The portable runtime, intermediate animation frames, PNG master, and source backup remain under ignored `.tools/`.

Run from the repository root with the verified portable executable:

```powershell
python scripts/build-noah-neural.py
& '.\.tools\blender-5.2.2-windows-x64\blender.exe' --background --python scripts/build-noah-blender.py -- build
& '.\.tools\blender-5.2.2-windows-x64\blender.exe' --background --python scripts/build-noah-blender.py -- verify
& '.\.tools\blender-5.2.2-windows-x64\blender.exe' --background --python scripts/build-noah-blender.py -- poster eevee 64
ffmpeg -hide_banner -loglevel error -y -i '.tools/noah-render-masters/noah-neural-poster.png' -quality 92 -compression_level 6 'docs/assets/noah/noah-neural-poster.webp'
```

Animation frames can be rendered in bounded ranges and resumed without rebuilding the source:

```powershell
& '.\.tools\blender-5.2.2-windows-x64\blender.exe' --background --python scripts/build-noah-blender.py -- animation 1 480 8
ffmpeg -hide_banner -loglevel error -y -framerate 24 -start_number 1 -i '.tools/noah-loop-frames/frame-%04d.png' -frames:v 480 -an -vf 'scale=in_range=pc:out_range=tv:out_color_matrix=bt709' -c:v libx264 -threads 8 -preset slow -crf 20 -pix_fmt yuv420p -color_range tv -color_primaries bt709 -color_trc iec61966-2-1 -colorspace bt709 -movflags +faststart 'docs/assets/noah/noah-neural-loop.mp4'
```

The `8` selects Eevee temporal samples for the small web loop; the 5120×1440 poster uses 64. The master remains editable for higher-quality future renders. `poster cycles` is available, but the attempted CPU Cycles export did not complete on this machine; delivered poster media uses the verified Eevee path.

## Browser behavior

The native WebGL visualization has a periodic 20-second rotation, responds to Noah's reported activity state, pauses while hidden/offscreen, respects reduced-motion preferences, and offers an explicit motion control. This depicts reported application activity, rather than model reasoning, consciousness, or an actual neural-network topology. WebGL fallback behavior and accessibility are verified separately by the browser test suite.

## Video verification

All 480 unique PNG frames were rendered successfully at 1920×540. The complete H.264 export decoded without errors, and FFprobe independently counted 480 decoded frames at `24/1` fps and exactly `20.000000` seconds. Actual first, quarter-turn, halfway, and final rendered/decoded frames were visually reviewed. The 20-second transform period is independently verified in the native source; this does not assert that rendered boundary images are pixel-identical.

The loop is 8-bit SDR, with BT.709 primaries/matrix and the sRGB transfer function used by the PNG source. It contains no audio. This small web preview is distinct from the native 5120×1440 poster and editable scene; it is not a 5K video or HDR master. Video playback is exposed as a user-selected watch/download link, avoiding an automatic multi-megabyte download.
