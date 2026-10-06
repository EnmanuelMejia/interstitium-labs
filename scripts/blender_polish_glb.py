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
  python3 scripts/blender_polish_glb.py --all --dir docs/assets/immersive
  python3 scripts/blender_polish_glb.py --in docs/assets/immersive/muse-dee-monas.glb --write-only
  python3 scripts/blender_polish_glb.py --all --promote   # polished.glb → replace source after OK
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
    export_extras=True,  # 2026-10-06: keep kit pedagogy extras (labels/kind/simOnly) through polish
)
print("polished", out)
'''

# Priority polish set (Musk-bar A path)
DEFAULT_TARGETS = (
    "cert-cka.glb",
    "cka-etcd-quorum.glb",
    "muse-dee-monas.glb",
    "lecture-k8s-control-plane.glb",
    "cni-pod-network.glb",
    "rbac-authz-graph.glb",
    "service-mesh-sidecar.glb",
    "storage-csi-pv.glb",
    "ingress-gateway.glb",
    "hpa-autoscaling.glb",
    "network-policy-isolation.glb",
    "secrets-configmaps.glb",
    "scheduling-affinity.glb",
    "aws-vpc-multi-az.glb",
    "aws-iam-policy-eval.glb",
    "rack-19u.glb",
    "hermetic-monas.glb",
    "sim-superlab.glb",
    "k8s-cluster.glb",
)


def write_sidecar(glb: Path) -> Path:
    side = glb.with_suffix(".blender_polish.py")
    side.write_text(
        "# Auto-generated Interstitium Blender polish sidecar\n"
        f"# Input: {glb.as_posix()}\n"
        "# Run on P920 / box with Blender CLI:\n"
        f"#   blender --background --python {side.name} -- {glb.name} {glb.stem}.polished.glb\n"
        + BLENDER_OPS,
        encoding="utf-8",
    )
    return side


def find_blender() -> str | None:
    """Resolve blender executable: PATH, then /workspace/bin, then /workspace/opt/blender."""
    which = shutil.which("blender")
    if which:
        return which
    for candidate in (
        Path("/workspace/bin/blender"),
        Path("/workspace/opt/blender/blender"),
        Path("/opt/blender/blender"),
        Path.home() / "blender" / "blender",
    ):
        if candidate.is_file() and candidate.stat().st_mode & 0o111:
            return str(candidate)
    return None



def looks_already_polished(glb: Path) -> bool:
    """Heuristic: Blender re-export embeds *_LOD1 mesh names from prior polish pass."""
    try:
        data = glb.read_bytes()
        # search JSON chunk for LOD1 marker without full parse
        return b"_LOD1" in data or b".polished" in data[:512]
    except Exception:
        return False

def polish_one(
    inp: Path,
    out: Path | None,
    *,
    write_only: bool,
    promote: bool,
    blender: str | None,
) -> int:
    if not inp.exists():
        print(f"missing: {inp}", file=sys.stderr)
        return 1
    if inp.suffix.lower() != ".glb":
        print(f"skip non-glb: {inp}", file=sys.stderr)
        return 1
    # Never re-polish already-polished sidecars into loops
    if inp.name.endswith(".polished.glb"):
        print(f"skip already-polished name: {inp.name}")
        return 0
    if looks_already_polished(inp) and not getattr(polish_one, "_force", False):
        # allow override via env IL_POLISH_FORCE=1
        import os
        if os.environ.get("IL_POLISH_FORCE") != "1":
            print(
                f"skip {inp.name}: appears already Blender-polished (_LOD1 in glb). "
                f"Re-author from kit first, or IL_POLISH_FORCE=1 to override."
            )
            return 0
    out = out or inp.with_name(inp.stem + ".polished.glb")
    side = write_sidecar(inp)
    print(f"wrote sidecar {side}")
    if write_only:
        print(f"write-only: skip blender invoke for {inp.name}")
        return 0
    if not blender:
        print(
            "ERROR: blender CLI not found on PATH (or /workspace/opt/blender).\n"
            "Install Blender LTS, or re-run with --write-only to emit sidecars only.\n"
            f"  Suggested: blender --background --python {side} -- {inp} {out}",
            file=sys.stderr,
        )
        return 2
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
    if r.returncode != 0:
        print(f"blender failed ({r.returncode}) for {inp}", file=sys.stderr)
        return r.returncode
    if not out.exists():
        print(f"ERROR: expected polish output missing: {out}", file=sys.stderr)
        return 3
    print(f"polished OK → {out} ({out.stat().st_size} bytes)")
    if promote:
        # Backup kit original once, then replace in-place with polished
        bak = inp.with_name(inp.stem + ".kit-v2.bak.glb")
        if not bak.exists():
            shutil.copy2(inp, bak)
            print(f"backup kit → {bak}")
        shutil.copy2(out, inp)
        print(f"promoted polished → {inp}")
    return 0


def collect_targets(args: argparse.Namespace) -> list[Path]:
    targets: list[Path] = []
    if args.all:
        d = Path(args.dir)
        if not d.is_dir():
            print(f"ERROR: --dir not a directory: {d}", file=sys.stderr)
            return []
        # Prefer known pedagogical set when present; else every .glb
        preferred = [d / n for n in DEFAULT_TARGETS if (d / n).exists()]
        if preferred:
            targets = preferred
        else:
            targets = sorted(p for p in d.glob("*.glb") if not p.name.endswith(".polished.glb"))
    elif args.inp:
        targets = [Path(args.inp)]
    return targets


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Blender polish handoff for Interstitium .glb")
    ap.add_argument("--in", dest="inp", type=Path, default=None, help="Single input .glb")
    ap.add_argument("--out", type=Path, default=None, help="Output .polished.glb (single mode)")
    ap.add_argument(
        "--all",
        action="store_true",
        help="Batch polish DEFAULT_TARGETS (or all .glb) under --dir",
    )
    ap.add_argument(
        "--dir",
        type=Path,
        default=Path("docs/assets/immersive"),
        help="Asset directory for --all (default: docs/assets/immersive)",
    )
    ap.add_argument(
        "--write-only",
        action="store_true",
        help="Only write .blender_polish.py sidecars (no blender invoke)",
    )
    ap.add_argument(
        "--promote",
        action="store_true",
        help="After polish OK, copy .polished.glb over source (keeps .kit-v2.bak.glb)",
    )
    args = ap.parse_args(argv)

    if not args.all and not args.inp:
        ap.error("provide --in PATH or --all")

    targets = collect_targets(args)
    if not targets:
        print("ERROR: no .glb targets", file=sys.stderr)
        return 1

    blender = None if args.write_only else find_blender()
    if not args.write_only and not blender:
        # Fail loudly once before looping (still write sidecars for each)
        print(
            "ERROR: blender CLI missing. Refusing batch polish without --write-only.\n"
            "Install: official Linux tarball under /workspace/opt/blender, or apt/snap.\n"
            "Then ensure `blender` is on PATH (e.g. ln -s /workspace/opt/blender/blender /workspace/bin/blender).",
            file=sys.stderr,
        )
        # Still emit sidecars so P920 can proceed offline
        for t in targets:
            if t.exists():
                write_sidecar(t)
                print(f"wrote sidecar for {t.name} (no blender)")
        return 2

    rc = 0
    for t in targets:
        out = args.out if (not args.all and args.out) else None
        code = polish_one(t, out, write_only=args.write_only, promote=args.promote, blender=blender)
        if code != 0:
            rc = code
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
