"""Build editable, original Noah geometry in Blender 5.2.2.

Run the verified portable blender.exe in background with --python this file.
After '--', use build, poster, animation, or verify. No third-party media is used.
The animation has 480 unique frames at 24 fps, with frame 481 equal to frame 1.
"""
import hashlib
import json
import math
import random
import sys
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs/assets/noah"
SOURCE = OUTPUT / "noah-neural.glb"
MASTER = OUTPUT / "noah-neural.blend"
FRAMES = ROOT / ".tools/noah-loop-frames"
RENDER_MASTERS = ROOT / ".tools/noah-render-masters"
PERIOD = 480
FPS = 24
MODE = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "build"


def material(name, color, metallic=0.0, roughness=0.3, emission=0.0):
    value = bpy.data.materials.new(name)
    value.use_nodes = True
    shader = value.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value = (*color, 1.0)
    shader.inputs["Metallic"].default_value = metallic
    shader.inputs["Roughness"].default_value = roughness
    shader.inputs["Emission Color"].default_value = (*color, 1.0)
    shader.inputs["Emission Strength"].default_value = emission
    return value


def smooth(obj):
    if obj.type == "MESH":
        for polygon in obj.data.polygons:
            polygon.use_smooth = True


def aim(obj, point):
    obj.rotation_euler = (Vector(point) - obj.location).to_track_quat("-Z", "Y").to_euler()


def area(name, position, color, energy, size):
    bpy.ops.object.light_add(type="AREA", location=position)
    obj = bpy.context.object
    obj.name = name
    obj.data.color = color
    obj.data.energy = energy
    obj.data.shape = "DISK"
    obj.data.size = size
    aim(obj, (0, 0, 0))


def torus(name, major, minor, rotation, mat, parent=None, z=0):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor,
                                    major_segments=128, minor_segments=12,
                                    location=(0, 0, z), rotation=rotation)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat)
    smooth(obj)
    if parent:
        obj.parent = parent
    return obj


def curve(name, points, radius, mat, parent):
    data = bpy.data.curves.new(name, "CURVE")
    data.dimensions = "3D"
    data.bevel_depth = radius
    data.bevel_resolution = 3
    spline = data.splines.new("BEZIER")
    spline.bezier_points.add(len(points) - 1)
    for point, position in zip(spline.bezier_points, points):
        point.co = position
        point.handle_left_type = "AUTO"
        point.handle_right_type = "AUTO"
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    obj.parent = parent
    return obj


def setup_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = 32
    scene.cycles.use_denoising = True
    scene.render.threads_mode = "FIXED"
    scene.render.threads = 32
    scene.render.resolution_x = 5120
    scene.render.resolution_y = 1440
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    scene.render.image_settings.color_depth = "8"
    scene.render.fps = FPS
    # Keep native ultrawide output within the verified GPU's shadow budget.
    scene.eevee.shadow_pool_size = "512"
    scene.eevee.shadow_resolution_scale = 0.5
    scene.frame_start = 1
    scene.frame_end = PERIOD
    scene.world.use_nodes = True
    world = scene.world.node_tree.nodes.get("Background")
    world.inputs[0].default_value = (0.003, 0.007, 0.015, 1)
    world.inputs[1].default_value = 0.22
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"
    scene.view_settings.exposure = -0.3

    azure = material("Noah | electric azure metal", (0.018, 0.42, 0.76), 0.5, 0.18, 4.5)
    gold = material("Noah | restrained gold", (0.78, 0.42, 0.095), 0.85, 0.24, 0.65)
    links = material("Noah | neural conduits", (0.012, 0.20, 0.34), 0.45, 0.28, 1.4)
    silk = material("Noah | inner signal filaments", (0.03, 0.65, 0.9), 0.18, 0.30, 2.5)
    obsidian = material("Noah | obsidian alloy", (0.009, 0.016, 0.026), 0.78, 0.22)
    glass = material("Noah | translucent computation core", (0.03, 0.13, 0.19), 0.1, 0.12)
    shader = glass.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Transmission Weight"].default_value = 0.68
    shader.inputs["IOR"].default_value = 1.18

    bpy.ops.object.empty_add(type="PLAIN_AXES")
    rig = bpy.context.object
    rig.name = "Noah | editable periodic rotation rig"
    rig["period_frames"] = PERIOD
    rig.rotation_euler[2] = 0
    rig.keyframe_insert(data_path="rotation_euler", index=2, frame=1)
    rig.rotation_euler[2] = math.tau
    rig.keyframe_insert(data_path="rotation_euler", index=2, frame=PERIOD + 1)
    # Blender 5 uses layered Actions; its public channelbag API resolves curves.
    for layer in rig.animation_data.action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for fcurve in bag.fcurves:
                    for keyframe in fcurve.keyframe_points:
                        keyframe.interpolation = "LINEAR"

    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=str(SOURCE))
    imported = [obj for obj in bpy.data.objects if obj not in before]
    for obj in imported:
        if obj.parent is None:
            obj.parent = rig
        if obj.type != "MESH":
            continue
        mat = gold if "Gold" in obj.name else links if "edge" in obj.name.lower() else azure
        obj.data.materials.clear()
        obj.data.materials.append(mat)
        smooth(obj)
        obj["provenance"] = "Imported original scripts/build-noah-neural.py geometry"

    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4, radius=0.49)
    core = bpy.context.object
    core.name = "Noah | translucent computation core"
    core.data.materials.append(glass)
    core.parent = rig
    smooth(core)
    torus("Noah | nucleus gold orbit", 0.60, 0.019, (1.0, 0.4, 0.2), gold, rig)
    torus("Noah | nucleus azure orbit", 0.68, 0.009, (0.35, 1.1, 0.1), silk, rig)
    torus("Noah | containment meridian", 1.83, 0.012, (1.2, 0.17, 0.3), gold, rig)
    torus("Noah | containment equator", 1.72, 0.006, (0.2, 0.28, 0.12), links, rig)

    # Original smooth interior circuits. Each curve remains individually editable.
    for index in range(32):
        phase = math.tau * index / 32
        height = -0.8 + 1.6 * index / 31
        points = []
        for step in range(6):
            fraction = step / 5
            angle = phase + fraction * 0.65
            radius = 0.20 + fraction * 1.12
            points.append((radius * math.cos(angle), radius * math.sin(angle), height * fraction))
        curve("Noah | signal circuit %02d" % index, points, 0.0028,
              gold if index % 8 == 0 else silk, rig)

    rng = random.Random(2601001)
    for index in range(110):
        position = (rng.uniform(-5.7, 5.7), rng.uniform(-0.5, 3.5), rng.uniform(-1.0, 2.1))
        if Vector(position).length < 2.0:
            continue
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=rng.uniform(0.006, 0.016), location=position)
        mote = bpy.context.object
        mote.name = "Noah | background signal %03d" % index
        mote.data.materials.append(gold if index % 9 == 0 else silk)
        smooth(mote)

    bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, -1.3))
    floor = bpy.context.object
    floor.name = "Noah | obsidian reflective stage"
    floor.data.materials.append(obsidian)
    torus("Noah | stage locator", 1.55, 0.009, (0, 0, 0), gold, z=-1.285)
    torus("Noah | stage secondary locator", 1.64, 0.0035, (0, 0, 0), links, z=-1.283)

    area("Noah | azure softbox", (-4, -3, 4), (0.15, 0.57, 1.0), 750, 4.0)
    area("Noah | gold rim", (3, 1, 2.5), (1.0, 0.53, 0.15), 1000, 3.0)
    area("Noah | neutral overhead", (0, 2, 5), (0.55, 0.72, 1.0), 500, 3.0)
    bpy.ops.object.camera_add(location=(4.4, -16, 5.06))
    camera = bpy.context.object
    camera.name = "Noah | native ultrawide camera"
    camera.data.lens = 44
    aim(camera, (0, 0, 0.12))
    scene.camera = camera

    tree = bpy.data.node_groups.new("Noah | editable SDR bloom", "CompositorNodeTree")
    scene.compositing_node_group = tree
    scene.render.use_compositing = True
    image = tree.nodes.new("CompositorNodeRLayers")
    bloom = tree.nodes.new("CompositorNodeGlare")
    bloom.inputs["Type"].default_value = "Fog Glow"
    bloom.inputs["Quality"].default_value = "High"
    bloom.inputs["Threshold"].default_value = 1.4
    bloom.inputs["Size"].default_value = 0.42
    tree.interface.new_socket(name="Image", in_out="OUTPUT", socket_type="NodeSocketColor")
    composite = tree.nodes.new("NodeGroupOutput")
    tree.links.new(image.outputs["Image"], bloom.inputs["Image"])
    tree.links.new(bloom.outputs["Image"], composite.inputs["Image"])
    scene["asset_provenance"] = "Original Interstitium Labs procedural geometry; no external imagery or film footage"
    scene["source_glb_sha256"] = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    scene["build_source"] = "scripts/build-noah-blender.py"
    scene["loop_seconds"] = 20
    scene["color_master"] = "AgX SDR, 8-bit PNG output; not HDR10"
    scene.frame_set(1)
    scene.render.filepath = "//noah-neural-poster.png"
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(MASTER), compress=True)
    print(json.dumps({"stage": "master_saved", "objects": len(scene.objects), "meshes": len(bpy.data.meshes), "resolution": [5120, 1440], "periodFrames": PERIOD, "fps": FPS}))


if MODE == "build":
    setup_scene()
elif MODE == "poster":
    bpy.ops.wm.open_mainfile(filepath=str(MASTER))
    scene = bpy.context.scene
    arguments = sys.argv[sys.argv.index("--") + 2:]
    if not arguments or arguments[0] == "eevee":
        scene.render.engine = "BLENDER_EEVEE"
        scene.eevee.taa_render_samples = int(arguments[1]) if len(arguments) > 1 else 64
    elif arguments[0] != "cycles":
        raise ValueError("Poster engine must be eevee or cycles")
    RENDER_MASTERS.mkdir(parents=True, exist_ok=True)
    scene.render.filepath = (RENDER_MASTERS / "noah-neural-poster.png").as_posix()
    bpy.ops.render.render(write_still=True)
    print(json.dumps({"stage": "poster_rendered", "engine": scene.render.engine,
                      "resolution": [scene.render.resolution_x, scene.render.resolution_y]}))
elif MODE == "animation":
    bpy.ops.wm.open_mainfile(filepath=str(MASTER))
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 540
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    # Rendering can be resumed by selecting a bounded inclusive frame range.
    arguments = sys.argv[sys.argv.index("--") + 2:]
    scene.frame_start = int(arguments[0]) if arguments else 1
    scene.frame_end = int(arguments[1]) if len(arguments) > 1 else PERIOD
    scene.eevee.taa_render_samples = int(arguments[2]) if len(arguments) > 2 else 32
    FRAMES.mkdir(parents=True, exist_ok=True)
    scene.render.filepath = (FRAMES / "frame-").as_posix()
    bpy.ops.render.render(animation=True)
    print(json.dumps({"stage": "animation_rendered", "start": scene.frame_start, "end": scene.frame_end, "fps": FPS}))
elif MODE == "verify":
    bpy.ops.wm.open_mainfile(filepath=str(MASTER))
    scene = bpy.context.scene
    rig = bpy.data.objects.get("Noah | editable periodic rotation rig")
    assert rig is not None and scene.camera is not None
    assert scene["source_glb_sha256"] == hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    assert scene.render.resolution_x == 5120 and scene.render.resolution_y == 1440
    assert scene.render.fps == FPS and scene.frame_end == PERIOD
    scene.frame_set(1)
    start = rig.matrix_world.copy()
    scene.frame_set(PERIOD + 1)
    end = rig.matrix_world.copy()
    seam_delta = max(abs(start[row][col] - end[row][col]) for row in range(4) for col in range(4))
    assert seam_delta < 1e-5, "Loop boundary transforms must match"
    print(json.dumps({"stage": "reopen_verified", "objects": len(scene.objects), "meshObjects": sum(obj.type == "MESH" for obj in scene.objects), "materials": len(bpy.data.materials), "camera": scene.camera.name, "loopBoundaryMatrixError": seam_delta, "sourceGeometryHashMatches": True, "hdr10": False}))
else:
    raise ValueError("Use build, poster, animation, or verify")
