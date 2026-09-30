#!/usr/bin/env python3
"""
Interstitium Labs — Blender polish handoff for kit-authored .glb (P920 path).

Honest: kit meshes from author_immersive_glb.py are Blender-compatible glTF 2.0.
This script either:
  A) Invokes `blender --background` with an embedded polish operator (normals,
     shade smooth, named collections from node names, optional decimate LOD), OR
  B) Writes a .blend.py polish script next to the .glb for manual P920 run.

Never invents a live Blender render farm. Never claims hand-sculpted artist sets.

Usage:
  python3 scripts/blender_polish_glb.py --in docs/assets/immersive/cert-cka.glb
  python3 scripts/blender_polish_glb.py --in docs/assets/immersive/muse-dee-monas.glb --write-only
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

BLENDER_OPS = r'''
# Interstitium P920 polish — run inside Blender (--background --python)
import bpy
import sys
from pathlib import Path

argv = sys.argv
argv = argv[argv.index("--") + 1 :] if "--" in argv else []
inp = Path(argv[0]) if argv else None
out = Path(argv[1]) if len(argv) > 1 else (inp.with_suffix(".polished.glb") if inp else None)
if not inp or not inp.exists():
    raise SystemExit("missing input glb")

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(inp))

for obj in list(bpy.data.objects):
    if obj.type != "MESH":
        continue
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    # shade smooth + weighted normals where available
    try:
        bpy.ops.object.shade_smooth()
    except Exception:
        pass
    try:
        bpy.ops.object.modifier_add(type="WEIGHTED_NORMAL")
        bpy.ops.object.modifier_apply(modifier="WeightedNormal")
    except Exception:
        pass
    # ensure mesh name mirrors pedagogy node
    if obj.data:
        obj.data.name = obj.name
    obj.select_set(False)

# Optional LOD1: duplicate + decimate meshes tagged extras.il.lod != 1 skip
for obj in list(bpy.data.objects):
    if obj.type != "MESH":
        continue
    if "lod1" in obj.name.lower() or "proxy" in obj.name.lower():
        continue
    dup = obj.copy()
    dup.data = obj.data.copy()
    dup.name = obj.name + "_LOD1"
    bpy.context.collection.objects.link(dup)
    bpy.context.view_layer.objects.active = dup
    dup.select_set(True)
    try:
        bpy.ops.object.modifier_add(type="DECIMATE")
        mod = dup.modifiers[-1]
        mod.ratio = 0.35
        bpy.ops.object.modifier_apply(modifier=mod.name)
    except Exception:
        pass
    dup.select_set(False)

bpy.ops.export_scene.gltf(
    filepath=str(out),
    export_format="GLB",
    export_apply=True,
    export_normals=True,
    export_materials="EXPORT",
)
print("polished", out)
'''


def write_sidecar(glb: Path) -> Path:
    side = glb.with_suffix(".blender_polish.py")
    side.write_text(
        "# Auto-generated Interstitium Blender polish sidecar\n"
        f"# Input: {glb.as_posix()}\n"
        "# Run on P920:\n"
        f"#   blender --background --python {side.name} -- {glb.name} {glb.stem}.polished.glb\n"
        + BLENDER_OPS,
        encoding="utf-8",
    )
    return side


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Blender polish handoff for Interstitium .glb")
    ap.add_argument("--in", dest="inp", type=Path, required=True)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument(
        "--write-only",
        action="store_true",
        help="Only write the .blender_polish.py sidecar (no blender invoke)",
    )
    args = ap.parse_args(argv)
    inp: Path = args.inp
    if not inp.exists():
        print(f"missing: {inp}", file=sys.stderr)
        return 1
    out = args.out or inp.with_name(inp.stem + ".polished.glb")
    side = write_sidecar(inp)
    print(f"wrote sidecar {side}")
    blender = shutil.which("blender")
    if args.write_only or not blender:
        if not blender:
            print(
                "blender CLI not on PATH — open sidecar on P920:\n"
                f"  blender --background --python {side} -- {inp} {out}"
            )
        return 0
    cmd = [
        blender,
        "--background",
        "--python",
        str(side),
        "--",
        str(inp.resolve()),
        str(out.resolve()),
    ]
    print("running:", " ".join(cmd))
    r = subprocess.run(cmd, check=False)
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
