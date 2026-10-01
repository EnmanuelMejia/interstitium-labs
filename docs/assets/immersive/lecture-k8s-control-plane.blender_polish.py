# Auto-generated Interstitium Blender polish sidecar
# Input: docs/assets/immersive/lecture-k8s-control-plane.glb
# Run on P920 / box with Blender CLI:
#   blender --background --python lecture-k8s-control-plane.blender_polish.py -- lecture-k8s-control-plane.glb lecture-k8s-control-plane.polished.glb

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
