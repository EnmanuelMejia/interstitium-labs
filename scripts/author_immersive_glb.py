#!/usr/bin/env python3
"""
Interstitium Labs — glTF 2.0 binary (.glb) authoring kit (P920-class polish path).

Honest provenance: kit-authored meshes (POSITION + NORMAL, TRIANGLES, PBR materials,
pedagogical node names, optional LOD child meshes, extras for Blender handoff).
Blender-compatible glTF 2.0 binary — open/polish on P920 via scripts/blender_polish_glb.py.
NOT hand-sculpted in Blender UI yet. Palette: cyan #5EEAD4 · gold #D4A853 · void #070B16.

Usage:
  python3 scripts/author_immersive_glb.py [--out docs/assets/immersive] [--only name.glb ...]
  python3 scripts/blender_polish_glb.py --in docs/assets/immersive/cert-cka.glb  # if blender CLI
"""
from __future__ import annotations

import argparse
import json
import math
import struct
import sys
from pathlib import Path

# Interstitium brand (linear-ish sRGB for glTF baseColorFactor)
CYAN = (0.369, 0.918, 0.831, 1.0)
GOLD = (0.831, 0.659, 0.325, 1.0)
VOID = (0.027, 0.043, 0.086, 1.0)
INK = (0.10, 0.14, 0.20, 1.0)
PAPER = (0.91, 0.933, 0.961, 1.0)


def _norm3(x, y, z):
    l = math.sqrt(x * x + y * y + z * z) or 1.0
    return (x / l, y / l, z / l)


class MeshBuilder:
    def __init__(self):
        self.positions: list[float] = []
        self.normals: list[float] = []
        self.indices: list[int] = []

    def add_tri(self, a, b, c, n=None):
        if n is None:
            ux, uy, uz = b[0] - a[0], b[1] - a[1], b[2] - a[2]
            vx, vy, vz = c[0] - a[0], c[1] - a[1], c[2] - a[2]
            n = _norm3(uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx)
        base = len(self.positions) // 3
        for p in (a, b, c):
            self.positions.extend(p)
            self.normals.extend(n)
        self.indices.extend([base, base + 1, base + 2])

    def add_quad(self, a, b, c, d, n=None):
        self.add_tri(a, b, c, n)
        self.add_tri(a, c, d, n)

    def add_box(self, cx, cy, cz, sx, sy, sz):
        hx, hy, hz = sx / 2, sy / 2, sz / 2
        # +Z
        self.add_quad(
            (cx - hx, cy - hy, cz + hz),
            (cx + hx, cy - hy, cz + hz),
            (cx + hx, cy + hy, cz + hz),
            (cx - hx, cy + hy, cz + hz),
            (0, 0, 1),
        )
        # -Z
        self.add_quad(
            (cx + hx, cy - hy, cz - hz),
            (cx - hx, cy - hy, cz - hz),
            (cx - hx, cy + hy, cz - hz),
            (cx + hx, cy + hy, cz - hz),
            (0, 0, -1),
        )
        # +Y
        self.add_quad(
            (cx - hx, cy + hy, cz - hz),
            (cx - hx, cy + hy, cz + hz),
            (cx + hx, cy + hy, cz + hz),
            (cx + hx, cy + hy, cz - hz),
            (0, 1, 0),
        )
        # -Y
        self.add_quad(
            (cx - hx, cy - hy, cz + hz),
            (cx - hx, cy - hy, cz - hz),
            (cx + hx, cy - hy, cz - hz),
            (cx + hx, cy - hy, cz + hz),
            (0, -1, 0),
        )
        # +X
        self.add_quad(
            (cx + hx, cy - hy, cz + hz),
            (cx + hx, cy - hy, cz - hz),
            (cx + hx, cy + hy, cz - hz),
            (cx + hx, cy + hy, cz + hz),
            (1, 0, 0),
        )
        # -X
        self.add_quad(
            (cx - hx, cy - hy, cz - hz),
            (cx - hx, cy - hy, cz + hz),
            (cx - hx, cy + hy, cz + hz),
            (cx - hx, cy + hy, cz - hz),
            (-1, 0, 0),
        )

    def add_cylinder(self, cx, cy, cz, radius, height, segments=16, capped=True):
        hy = height / 2
        seg = max(6, segments)
        ring_bot = []
        ring_top = []
        for i in range(seg):
            a = (i / seg) * math.pi * 2
            x = math.cos(a) * radius
            z = math.sin(a) * radius
            ring_bot.append((cx + x, cy - hy, cz + z))
            ring_top.append((cx + x, cy + hy, cz + z))
        for i in range(seg):
            j = (i + 1) % seg
            n = _norm3(ring_bot[i][0] - cx, 0, ring_bot[i][2] - cz)
            # two tris with per-vertex outward normals approximated via face mid
            n2 = _norm3(ring_bot[j][0] - cx, 0, ring_bot[j][2] - cz)
            # use averaged for each corner via explicit verts
            base = len(self.positions) // 3
            for p, nn in (
                (ring_bot[i], n),
                (ring_bot[j], n2),
                (ring_top[j], n2),
                (ring_top[i], n),
            ):
                self.positions.extend(p)
                self.normals.extend(nn)
            self.indices.extend([base, base + 1, base + 2, base, base + 2, base + 3])
        if capped:
            bot_c = (cx, cy - hy, cz)
            top_c = (cx, cy + hy, cz)
            for i in range(seg):
                j = (i + 1) % seg
                self.add_tri(bot_c, ring_bot[j], ring_bot[i], (0, -1, 0))
                self.add_tri(top_c, ring_top[i], ring_top[j], (0, 1, 0))

    def add_sphere(self, cx, cy, cz, radius, stacks=12, slices=16):
        """UV sphere with smooth-ish normals (P920 polish precursor)."""
        stacks = max(4, stacks)
        slices = max(6, slices)
        for i in range(stacks):
            v0 = i / stacks
            v1 = (i + 1) / stacks
            phi0 = (v0 - 0.5) * math.pi
            phi1 = (v1 - 0.5) * math.pi
            y0 = math.sin(phi0) * radius
            y1 = math.sin(phi1) * radius
            r0 = math.cos(phi0) * radius
            r1 = math.cos(phi1) * radius
            for j in range(slices):
                u0 = j / slices
                u1 = (j + 1) / slices
                a0 = u0 * math.pi * 2
                a1 = u1 * math.pi * 2
                p00 = (cx + math.cos(a0) * r0, cy + y0, cz + math.sin(a0) * r0)
                p01 = (cx + math.cos(a1) * r0, cy + y0, cz + math.sin(a1) * r0)
                p10 = (cx + math.cos(a0) * r1, cy + y1, cz + math.sin(a0) * r1)
                p11 = (cx + math.cos(a1) * r1, cy + y1, cz + math.sin(a1) * r1)
                n00 = _norm3(p00[0] - cx, p00[1] - cy, p00[2] - cz)
                n01 = _norm3(p01[0] - cx, p01[1] - cy, p01[2] - cz)
                n10 = _norm3(p10[0] - cx, p10[1] - cy, p10[2] - cz)
                n11 = _norm3(p11[0] - cx, p11[1] - cy, p11[2] - cz)
                # two tris with per-vertex normals
                base = len(self.positions) // 3
                for p, n in ((p00, n00), (p01, n01), (p11, n11), (p10, n10)):
                    self.positions.extend(p)
                    self.normals.extend(n)
                self.indices.extend([base, base + 1, base + 2, base, base + 2, base + 3])

    def add_chamfer_box(self, cx, cy, cz, sx, sy, sz, bevel=0.04):
        """Box with slightly inset faces + edge rails for less toy-block look."""
        b = min(bevel, sx * 0.2, sy * 0.2, sz * 0.2)
        self.add_box(cx, cy, cz, sx - 2 * b, sy - 2 * b, sz - 2 * b)
        # edge rails (thin boxes along edges)
        hx, hy, hz = sx / 2, sy / 2, sz / 2
        for dx in (-hx, hx):
            for dy in (-hy, hy):
                self.add_box(cx + dx * 0.92, cy + dy * 0.92, cz, b * 1.2, b * 1.2, sz - 2 * b)
        for dx in (-hx, hx):
            for dz in (-hz, hz):
                self.add_box(cx + dx * 0.92, cy, cz + dz * 0.92, b * 1.2, sy - 2 * b, b * 1.2)
        for dy in (-hy, hy):
            for dz in (-hz, hz):
                self.add_box(cx, cy + dy * 0.92, cz + dz * 0.92, sx - 2 * b, b * 1.2, b * 1.2)

    def bounds(self):
        if not self.positions:
            return [0, 0, 0], [0, 0, 0]
        xs = self.positions[0::3]
        ys = self.positions[1::3]
        zs = self.positions[2::3]
        return [min(xs), min(ys), min(zs)], [max(xs), max(ys), max(zs)]


def pack_glb(meshes_with_mats: list[tuple], scene_extras: dict | None = None) -> bytes:
    """
    meshes_with_mats: list of (MeshBuilder, material_dict, node_name[, extras_dict])
    material_dict keys: name, baseColorFactor, metallicFactor, roughnessFactor, emissiveFactor
    """
    bin_parts: list[bytes] = []
    buffer_views = []
    accessors = []
    meshes = []
    nodes = []
    materials = []
    mat_index = {}

    def ensure_mat(mat: dict) -> int:
        key = mat["name"]
        if key in mat_index:
            return mat_index[key]
        idx = len(materials)
        mat_index[key] = idx
        pbr = {
            "baseColorFactor": list(mat.get("baseColorFactor", CYAN)),
            "metallicFactor": float(mat.get("metallicFactor", 0.15)),
            "roughnessFactor": float(mat.get("roughnessFactor", 0.45)),
        }
        entry = {"name": key, "pbrMetallicRoughness": pbr}
        if mat.get("emissiveFactor"):
            entry["emissiveFactor"] = list(mat["emissiveFactor"])
        if float(pbr["baseColorFactor"][3]) < 1.0:
            # translucent pedagogy shells (e.g. NetworkPolicy shield)
            entry["alphaMode"] = "BLEND"
            entry["doubleSided"] = True
        materials.append(entry)
        return idx

    def append_bytes(data: bytes, target: int) -> int:
        # pad to 4-byte alignment inside BIN
        pad = (4 - (len(b"".join(bin_parts)) % 4)) % 4
        if pad:
            bin_parts.append(b"\x00" * pad)
        offset = sum(len(p) for p in bin_parts)
        bin_parts.append(data)
        bv_idx = len(buffer_views)
        buffer_views.append(
            {
                "buffer": 0,
                "byteOffset": offset,
                "byteLength": len(data),
                "target": target,
            }
        )
        return bv_idx

    for item in meshes_with_mats:
        mb, mat, name = item[0], item[1], item[2]
        node_extras = item[3] if len(item) > 3 else None
        if not mb.indices:
            continue
        mi = ensure_mat(mat)
        pos = struct.pack(f"<{len(mb.positions)}f", *mb.positions)
        nrm = struct.pack(f"<{len(mb.normals)}f", *mb.normals)
        # use uint16 if fits, else uint32
        if max(mb.indices) < 65535:
            idx = struct.pack(f"<{len(mb.indices)}H", *mb.indices)
            comp = 5123
        else:
            idx = struct.pack(f"<{len(mb.indices)}I", *mb.indices)
            comp = 5125

        # pad idx to 4 bytes
        if len(idx) % 4:
            idx = idx + b"\x00" * (4 - len(idx) % 4)

        bv_pos = append_bytes(pos, 34962)
        bv_nrm = append_bytes(nrm, 34962)
        bv_idx = append_bytes(idx, 34963)

        bmin, bmax = mb.bounds()
        acc_pos = len(accessors)
        accessors.append(
            {
                "bufferView": bv_pos,
                "componentType": 5126,
                "count": len(mb.positions) // 3,
                "type": "VEC3",
                "max": bmax,
                "min": bmin,
            }
        )
        acc_nrm = len(accessors)
        accessors.append(
            {
                "bufferView": bv_nrm,
                "componentType": 5126,
                "count": len(mb.normals) // 3,
                "type": "VEC3",
            }
        )
        acc_idx = len(accessors)
        accessors.append(
            {
                "bufferView": bv_idx,
                "componentType": comp,
                "count": len(mb.indices),
                "type": "SCALAR",
            }
        )

        mesh_idx = len(meshes)
        meshes.append(
            {
                "name": name,
                "primitives": [
                    {
                        "attributes": {"POSITION": acc_pos, "NORMAL": acc_nrm},
                        "indices": acc_idx,
                        "material": mi,
                        "mode": 4,  # TRIANGLES
                    }
                ],
            }
        )
        node = {"name": name, "mesh": mesh_idx}
        if node_extras:
            node["extras"] = node_extras
        nodes.append(node)

    bin_blob = b"".join(bin_parts)
    # pad BIN to 4-byte
    if len(bin_blob) % 4:
        bin_blob += b"\x00" * (4 - len(bin_blob) % 4)

    scene_obj = {"name": "Scene", "nodes": list(range(len(nodes)))}
    if scene_extras:
        scene_obj["extras"] = scene_extras
    gltf = {
        "asset": {
            "version": "2.0",
            "generator": "Interstitium Labs glTF kit (author_immersive_glb.py) v2",
            "copyright": "Interstitium Labs — kit-authored, Blender-compatible; polish on P920",
            "extras": {
                "interstitium": {
                    "kit": "author_immersive_glb",
                    "kitVersion": 2,
                    "blenderHandoff": "scripts/blender_polish_glb.py",
                    "palette": {"cyan": "#5EEAD4", "gold": "#D4A853", "void": "#070B16"},
                }
            },
        },
        "scene": 0,
        "scenes": [scene_obj],
        "nodes": nodes,
        "meshes": meshes,
        "materials": materials,
        "accessors": accessors,
        "bufferViews": buffer_views,
        "buffers": [{"byteLength": len(bin_blob)}],
    }

    json_bytes = json.dumps(gltf, separators=(",", ":")).encode("utf-8")
    while len(json_bytes) % 4:
        json_bytes += b" "

    # GLB: header + JSON chunk + BIN chunk
    total = 12 + 8 + len(json_bytes) + 8 + len(bin_blob)
    out = bytearray()
    out += struct.pack("<4sII", b"glTF", 2, total)
    out += struct.pack("<I4s", len(json_bytes), b"JSON")
    out += json_bytes
    out += struct.pack("<I4s", len(bin_blob), b"BIN\x00")
    out += bin_blob
    assert len(out) == total
    return bytes(out)


def mat(name, color, metallic=0.15, roughness=0.45, emissive=None):
    d = {
        "name": name,
        "baseColorFactor": color,
        "metallicFactor": metallic,
        "roughnessFactor": roughness,
    }
    if emissive:
        d["emissiveFactor"] = emissive
    return d


MAT_CYAN = mat("il-cyan", CYAN, 0.2, 0.4, (0.05, 0.18, 0.15))
MAT_GOLD = mat("il-gold", GOLD, 0.35, 0.35, (0.12, 0.08, 0.02))
MAT_VOID = mat("il-void", VOID, 0.05, 0.85)
MAT_INK = mat("il-ink", INK, 0.1, 0.7)
MAT_LED = mat("il-led", CYAN, 0.0, 0.3, (0.2, 0.7, 0.55))
MAT_PAPER = mat("il-paper", PAPER, 0.05, 0.55)
MAT_CRYSTAL = mat("il-crystal", CYAN, 0.05, 0.18, (0.12, 0.45, 0.38))
MAT_DEE_GOLD = mat("il-dee-gold", GOLD, 0.45, 0.28, (0.22, 0.14, 0.04))


def scene_k8s_control_plane() -> list:
    """Control-plane cylinder + surrounding worker boxes (procedural:k8s family)."""
    parts = []
    ped = {"il": {"role": "pedagogy", "topic": "kubernetes-control-plane"}}
    floor = MeshBuilder()
    floor.add_cylinder(0, -0.2, 0, 2.0, 0.06, 32)
    parts.append((floor, MAT_INK, "floor-ring", {**ped, "label": "cluster-floor"}))
    cp = MeshBuilder()
    cp.add_cylinder(0, 0.9, 0, 0.45, 0.55, 28)
    parts.append((cp, MAT_GOLD, "control-plane", {**ped, "label": "control-plane", "cka": "cp"}))
    api = MeshBuilder()
    api.add_chamfer_box(0, 1.35, 0, 0.42, 0.42, 0.42, 0.03)
    parts.append((api, MAT_CYAN, "api-server", {**ped, "label": "kube-apiserver"}))
    # scheduler + controller-manager side pods
    sched = MeshBuilder()
    sched.add_box(-0.55, 1.15, 0.35, 0.22, 0.22, 0.22)
    parts.append((sched, MAT_LED, "scheduler", {**ped, "label": "kube-scheduler"}))
    cm = MeshBuilder()
    cm.add_box(0.55, 1.15, 0.35, 0.22, 0.22, 0.22)
    parts.append((cm, MAT_LED, "controller-manager", {**ped, "label": "kube-controller-manager"}))
    halo = MeshBuilder()
    halo.add_cylinder(0, 0.55, 0, 0.75, 0.05, 28, capped=True)
    parts.append((halo, MAT_CYAN, "cp-halo", {**ped, "label": "cp-halo"}))
    n = 5
    for i in range(n):
        a = (i / n) * math.pi * 2
        x, z = math.cos(a) * 1.55, math.sin(a) * 1.55
        w = MeshBuilder()
        w.add_chamfer_box(x, 0.2, z, 0.4, 0.55, 0.4, 0.025)
        # kubelet LED
        led = MeshBuilder()
        led.add_sphere(x, 0.52, z + 0.18, 0.05, 8, 10)
        parts.append((w, MAT_CYAN if i % 2 == 0 else MAT_INK, f"worker-{i}", {**ped, "label": f"worker-node-{i}"}))
        parts.append((led, MAT_LED, f"kubelet-led-{i}", {**ped, "label": f"kubelet-{i}"}))
    # LOD1 simplified proxy (single low-poly disk) for Blender LOD workflow demo
    lod = MeshBuilder()
    lod.add_cylinder(0, 0.4, 0, 1.8, 0.08, 12)
    parts.append((lod, MAT_VOID, "lod1-proxy", {"il": {"lod": 1, "role": "lod-proxy"}}))
    return parts


def scene_cert_cka() -> list:
    """CKA shell — k8s family variant with exam pedestal."""
    parts = scene_k8s_control_plane()
    pedestal = MeshBuilder()
    pedestal.add_box(0, -0.55, 0, 1.2, 0.15, 1.2)
    parts.append((pedestal, MAT_GOLD, "cka-pedestal"))
    badge = MeshBuilder()
    badge.add_box(0, 1.7, 0, 0.25, 0.12, 0.25)
    parts.append((badge, MAT_GOLD, "cka-badge"))
    return parts


def scene_rack_19u() -> list:
    """Three rack frames with bay LEDs."""
    parts = []
    floor = MeshBuilder()
    floor.add_box(0, -0.9, 0, 4.4, 0.1, 2.0)
    parts.append((floor, MAT_VOID, "dc-floor"))
    for ri, x in enumerate((-1.35, 0.0, 1.35)):
        frame = MeshBuilder()
        frame.add_box(x, 0.15, 0, 1.0, 2.0, 0.65)
        parts.append((frame, MAT_INK, f"rack-frame-{ri}"))
        posts = MeshBuilder()
        posts.add_box(x - 0.48, 0.15, -0.28, 0.06, 2.0, 0.06)
        posts.add_box(x + 0.48, 0.15, -0.28, 0.06, 2.0, 0.06)
        posts.add_box(x - 0.48, 0.15, 0.28, 0.06, 2.0, 0.06)
        posts.add_box(x + 0.48, 0.15, 0.28, 0.06, 2.0, 0.06)
        parts.append((posts, MAT_VOID, f"rack-posts-{ri}"))
        for bay in range(6):
            led = MeshBuilder()
            y = -0.55 + bay * 0.28
            led.add_box(x, y, 0.28, 0.7, 0.08, 0.1)
            mat_led = MAT_LED if (bay + ri) % 3 != 0 else MAT_GOLD
            parts.append((led, mat_led, f"bay-{ri}-{bay}"))
    return parts


def scene_hermetic_monas() -> list:
    """Hermetica / Monas lecture set — concentric rings + sigil axis."""
    parts = []
    tablet = MeshBuilder()
    tablet.add_box(0, -0.35, 0.7, 1.5, 0.08, 0.9)
    parts.append((tablet, MAT_INK, "tablet"))
    for i, (r, h, m) in enumerate(
        ((1.3, 0.05, MAT_INK), (0.95, 0.04, MAT_CYAN), (0.6, 0.04, MAT_GOLD))
    ):
        ring = MeshBuilder()
        ring.add_cylinder(0, 0.1 + i * 0.12, 0, r, h, 24)
        parts.append((ring, m, f"orrery-ring-{i}"))
    core = MeshBuilder()
    core.add_box(0, 0.85, 0, 0.5, 0.5, 0.5)
    parts.append((core, MAT_CYAN, "monas-core"))
    axis = MeshBuilder()
    axis.add_box(0, 1.35, 0, 0.12, 0.7, 0.12)
    parts.append((axis, MAT_GOLD, "sigil-axis"))
    tip = MeshBuilder()
    tip.add_cylinder(0, 1.8, 0, 0.1, 0.15, 10)
    parts.append((tip, MAT_GOLD, "sigil-tip"))
    return parts


def scene_sim_superlab() -> list:
    """SuperLab sim — rack row + cluster combo."""
    parts = []
    # left: mini rack
    for ri, x in enumerate((-1.8, -0.7)):
        frame = MeshBuilder()
        frame.add_box(x, 0.1, -0.8, 0.85, 1.6, 0.55)
        parts.append((frame, MAT_INK, f"sl-rack-{ri}"))
        for bay in range(4):
            led = MeshBuilder()
            led.add_box(x, -0.4 + bay * 0.28, -0.55, 0.55, 0.08, 0.08)
            parts.append((led, MAT_LED if bay % 2 == 0 else MAT_GOLD, f"sl-bay-{ri}-{bay}"))
    # right: mini cluster
    cp = MeshBuilder()
    cp.add_cylinder(1.2, 0.7, 0.4, 0.35, 0.45, 16)
    parts.append((cp, MAT_GOLD, "sl-cp"))
    for i in range(4):
        a = (i / 4) * math.pi * 2
        x = 1.2 + math.cos(a) * 0.95
        z = 0.4 + math.sin(a) * 0.95
        w = MeshBuilder()
        w.add_box(x, 0.15, z, 0.3, 0.4, 0.3)
        parts.append((w, MAT_CYAN, f"sl-worker-{i}"))
    floor = MeshBuilder()
    floor.add_box(0, -0.75, 0, 4.5, 0.08, 3.0)
    parts.append((floor, MAT_VOID, "sl-floor"))
    return parts



def scene_muse_dee_monas() -> list:
    """Lab Muse Dee / Monas familiar — crystalline avatar for voice-reactive coach (glTF path)."""
    parts = []
    ped = {"il": {"role": "muse-avatar", "avatar": "dee", "voiceReactive": True}}
    # void plinth
    base = MeshBuilder()
    base.add_cylinder(0, -0.55, 0, 0.85, 0.08, 28)
    parts.append((base, MAT_VOID, "muse-plinth", {**ped, "label": "plinth"}))
    # monas core (icosa-ish via sphere)
    core = MeshBuilder()
    core.add_sphere(0, 0.35, 0, 0.38, 14, 18)
    parts.append((core, MAT_CRYSTAL, "monas-core", {**ped, "label": "monas-core", "state": "idle|listen|speak"}))
    # crescent / Dee shell (partial torus approx via thin torus + offset sphere cut look)
    shell = MeshBuilder()
    shell.add_sphere(0.12, 0.42, 0, 0.48, 12, 16)
    parts.append((shell, MAT_DEE_GOLD, "dee-crescent", {**ped, "label": "dee-crescent"}))
    # orrery rings
    for i, (R, y, mname, mat_) in enumerate(
        ((0.72, 0.35, "orrery-inner", MAT_GOLD), (0.98, 0.32, "orrery-outer", MAT_CYAN))
    ):
        ring = MeshBuilder()
        # approximate torus with stacked thin cylinders at angles via many segments box ring
        seg = 28
        for s in range(seg):
            a = (s / seg) * math.pi * 2
            x, z = math.cos(a) * R, math.sin(a) * R
            bead = MeshBuilder()
            bead.add_sphere(x, y, z, 0.035 if i == 0 else 0.028, 6, 8)
            parts.append((bead, mat_, f"{mname}-bead-{s}", {**ped, "label": mname, "ring": i}))
    # sigil stem + cross
    stem = MeshBuilder()
    stem.add_cylinder(0, -0.05, 0, 0.04, 0.7, 12)
    parts.append((stem, MAT_GOLD, "sigil-stem", {**ped, "label": "sigil-stem"}))
    cross = MeshBuilder()
    cross.add_box(0, -0.15, 0, 0.55, 0.05, 0.05)
    parts.append((cross, MAT_GOLD, "sigil-cross", {**ped, "label": "sigil-cross"}))
    # tip crystal
    tip = MeshBuilder()
    tip.add_sphere(0, 0.85, 0, 0.1, 8, 10)
    parts.append((tip, MAT_LED, "sigil-tip", {**ped, "label": "sigil-tip"}))
    # LOD proxy
    lod = MeshBuilder()
    lod.add_sphere(0, 0.3, 0, 0.5, 6, 8)
    parts.append((lod, MAT_VOID, "lod1-muse-proxy", {"il": {"lod": 1, "role": "lod-proxy"}}))
    return parts


def scene_cka_etcd_quorum() -> list:
    """CKA etcd quorum immersive — 3-member raft + API front (honest CKA pedagogy exceed)."""
    parts = []
    ped = {"il": {"role": "pedagogy", "topic": "cka-etcd-quorum", "cert": "CKA"}}
    floor = MeshBuilder()
    floor.add_box(0, -0.85, 0, 4.2, 0.08, 3.0)
    parts.append((floor, MAT_VOID, "exam-floor", {**ped, "label": "exam-floor"}))
    # three etcd members in triangle
    positions = [(0, 0.9), (-1.1, -0.7), (1.1, -0.7)]
    for i, (x, z) in enumerate(positions):
        body = MeshBuilder()
        body.add_cylinder(x, 0.35, z, 0.32, 0.7, 20)
        parts.append((body, MAT_GOLD if i == 0 else MAT_CYAN, f"etcd-member-{i}", {
            **ped, "label": f"etcd-{i}", "raft": "leader" if i == 0 else "follower"
        }))
        cap = MeshBuilder()
        cap.add_sphere(x, 0.78, z, 0.14, 10, 12)
        parts.append((cap, MAT_LED if i == 0 else MAT_INK, f"etcd-heart-{i}", {
            **ped, "label": f"raft-heartbeat-{i}"
        }))
    # quorum ring linking members
    for i in range(3):
        j = (i + 1) % 3
        x0, z0 = positions[i]
        x1, z1 = positions[j]
        mx, mz = (x0 + x1) / 2, (z0 + z1) / 2
        link = MeshBuilder()
        dx, dz = x1 - x0, z1 - z0
        length = math.sqrt(dx * dx + dz * dz) or 1
        link.add_box(mx, 0.55, mz, length * 0.85, 0.04, 0.06)
        parts.append((link, MAT_CYAN, f"raft-link-{i}-{j}", {**ped, "label": "raft-replication"}))
    # API server front desk
    api = MeshBuilder()
    api.add_chamfer_box(0, 0.15, 1.35, 1.1, 0.55, 0.4, 0.03)
    parts.append((api, MAT_INK, "apiserver-front", {**ped, "label": "kube-apiserver"}))
    badge = MeshBuilder()
    badge.add_box(0, 0.55, 1.35, 0.35, 0.12, 0.12)
    parts.append((badge, MAT_GOLD, "cka-badge", {**ped, "label": "CKA"}))
    # exam prompt tablet
    tablet = MeshBuilder()
    tablet.add_box(1.6, -0.35, 1.1, 0.7, 0.06, 0.5)
    parts.append((tablet, MAT_PAPER, "exam-prompt", {**ped, "label": "exam-prompt"}))
    return parts



def scene_cni_pod_network() -> list:
    """CNI / pod networking — nodes, pods, CNI bridge/overlay arcs (CKA networking domain)."""
    parts = []
    ped = {"il": {"role": "pedagogy", "topic": "cni-pod-network", "cert": "CKA", "domain": "networking"}}
    floor = MeshBuilder()
    floor.add_box(0, -0.9, 0, 5.0, 0.08, 3.4)
    parts.append((floor, MAT_VOID, "net-floor", {**ped, "label": "cluster-network-plane"}))
    # two worker nodes as racks/boxes
    node_pos = [(-1.6, 0.0), (1.6, 0.0)]
    for ni, (nx, nz) in enumerate(node_pos):
        node = MeshBuilder()
        node.add_chamfer_box(nx, 0.15, nz, 1.35, 0.85, 1.1, 0.04)
        parts.append((node, MAT_INK, f"node-{ni}", {**ped, "label": f"worker-node-{ni}", "cka": "node"}))
        # kubelet LED
        led = MeshBuilder()
        led.add_sphere(nx, 0.65, nz + 0.45, 0.07, 8, 10)
        parts.append((led, MAT_LED, f"kubelet-{ni}", {**ped, "label": f"kubelet-{ni}"}))
        # pods on node (3 each)
        for pi in range(3):
            px = nx - 0.4 + pi * 0.4
            pz = nz - 0.15
            pod = MeshBuilder()
            pod.add_sphere(px, 0.55, pz, 0.16, 10, 12)
            parts.append((pod, MAT_CYAN if pi != 1 else MAT_GOLD, f"pod-{ni}-{pi}", {
                **ped, "label": f"pod-{ni}-{pi}", "ip": f"10.{ni}.{pi}.2"
            }))
            # veth stub under pod
            veth = MeshBuilder()
            veth.add_cylinder(px, 0.32, pz, 0.03, 0.22, 8)
            parts.append((veth, MAT_GOLD, f"veth-{ni}-{pi}", {**ped, "label": "veth-pair"}))
    # CNI bridge (center cyan bar) + overlay arcs between nodes
    bridge = MeshBuilder()
    bridge.add_chamfer_box(0, 0.05, 0, 2.6, 0.12, 0.35, 0.02)
    parts.append((bridge, MAT_CYAN, "cni-bridge", {**ped, "label": "cni-bridge", "plugin": "bridge|calico|cilium"}))
    # overlay tunnel arcs (approximated as elevated boxes along path)
    for ai, (y, zoff) in enumerate(((0.95, 0.55), (1.15, -0.55))):
        for t in range(7):
            # interpolate x from -1.6 to 1.6
            u = t / 6
            x = -1.6 + 3.2 * u
            # parabolic height
            h = y + 0.35 * math.sin(u * math.pi)
            bead = MeshBuilder()
            bead.add_sphere(x, h, zoff, 0.05, 6, 8)
            parts.append((bead, MAT_GOLD if ai == 0 else MAT_CYAN, f"overlay-arc-{ai}-{t}", {
                **ped, "label": "overlay-tunnel", "encap": "VXLAN|Geneve"
            }))
    # service VIP / ClusterIP orb
    vip = MeshBuilder()
    vip.add_sphere(0, 1.55, 0, 0.18, 10, 12)
    parts.append((vip, MAT_GOLD, "cluster-ip", {**ped, "label": "Service ClusterIP", "cka": "service"}))
    # DNS stub
    dns = MeshBuilder()
    dns.add_chamfer_box(0, 0.35, -1.35, 0.55, 0.35, 0.35, 0.02)
    parts.append((dns, MAT_PAPER, "coredns", {**ped, "label": "CoreDNS"}))
    # LOD proxy
    lod = MeshBuilder()
    lod.add_box(0, 0.2, 0, 4.2, 0.15, 2.4)
    parts.append((lod, MAT_VOID, "lod1-cni-proxy", {"il": {"lod": 1, "role": "lod-proxy"}}))
    return parts


def scene_rbac_authz_graph() -> list:
    """K8s RBAC spatial graph — User → Role → RoleBinding → API resources."""
    parts = []
    ped = {"il": {"role": "pedagogy", "topic": "rbac-authz", "cert": "CKA", "domain": "security"}}
    floor = MeshBuilder()
    floor.add_box(0, -0.85, 0, 4.8, 0.08, 3.2)
    parts.append((floor, MAT_VOID, "rbac-floor", {**ped, "label": "authz-plane"}))
    # layers along +Z depth: users, bindings, roles, resources
    # Users (left / front)
    users = [(-1.4, 0.4, 1.2), (-0.5, 0.4, 1.2), (0.4, 0.4, 1.2)]
    for i, (x, y, z) in enumerate(users):
        u = MeshBuilder()
        u.add_sphere(x, y, z, 0.18, 10, 12)
        parts.append((u, MAT_GOLD, f"user-{i}", {**ped, "label": f"User/SA-{i}", "kind": "User|ServiceAccount"}))
    # RoleBindings (middle)
    bindings = [(-1.0, 0.55, 0.35), (0.0, 0.55, 0.35), (1.0, 0.55, 0.35)]
    for i, (x, y, z) in enumerate(bindings):
        b = MeshBuilder()
        b.add_chamfer_box(x, y, z, 0.45, 0.22, 0.35, 0.02)
        parts.append((b, MAT_CYAN, f"rolebinding-{i}", {**ped, "label": f"RoleBinding-{i}", "kind": "RoleBinding"}))
    # Roles / ClusterRoles
    roles = [(-1.2, 0.7, -0.55), (0.2, 0.7, -0.55), (1.4, 0.7, -0.55)]
    for i, (x, y, z) in enumerate(roles):
        r = MeshBuilder()
        r.add_cylinder(x, y, z, 0.22, 0.45, 16)
        parts.append((r, MAT_LED if i == 2 else MAT_GOLD, f"role-{i}", {
            **ped, "label": "ClusterRole" if i == 2 else f"Role-{i}", "kind": "Role|ClusterRole"
        }))
    # API resources (back row)
    resources = ["pods", "secrets", "deployments", "nodes"]
    for i, name in enumerate(resources):
        x = -1.5 + i * 1.0
        z = -1.35
        res = MeshBuilder()
        res.add_chamfer_box(x, 0.35, z, 0.55, 0.4, 0.28, 0.02)
        parts.append((res, MAT_INK, f"api-{name}", {**ped, "label": name, "apiGroup": "core|apps"}))
        # verb chips (get/list/watch)
        chip = MeshBuilder()
        chip.add_box(x, 0.65, z, 0.35, 0.08, 0.12)
        parts.append((chip, MAT_CYAN, f"verbs-{name}", {**ped, "label": "get,list,watch", "verbs": True}))
    # edges: user→binding→role→resource (thin cylinders / boxes as arcs)
    def link(a, b, name, mat_=MAT_CYAN):
        x0, y0, z0 = a
        x1, y1, z1 = b
        mx, my, mz = (x0 + x1) / 2, (y0 + y1) / 2 + 0.08, (z0 + z1) / 2
        dx, dy, dz = x1 - x0, y1 - y0, z1 - z0
        length = math.sqrt(dx * dx + dy * dy + dz * dz) or 1
        edge = MeshBuilder()
        edge.add_box(mx, my, mz, max(0.08, length * 0.9), 0.035, 0.035)
        parts.append((edge, mat_, name, {**ped, "label": "authz-edge"}))

    link(users[0], bindings[0], "edge-u0-b0")
    link(users[1], bindings[1], "edge-u1-b1")
    link(users[2], bindings[2], "edge-u2-b2", MAT_GOLD)
    link(bindings[0], roles[0], "edge-b0-r0")
    link(bindings[1], roles[1], "edge-b1-r1")
    link(bindings[2], roles[2], "edge-b2-r2", MAT_GOLD)
    link(roles[0], (-1.5, 0.35, -1.35), "edge-r0-pods")
    link(roles[1], (-0.5, 0.35, -1.35), "edge-r1-secrets")
    link(roles[2], (0.5, 0.35, -1.35), "edge-r2-deploys", MAT_LED)
    link(roles[2], (1.5, 0.35, -1.35), "edge-r2-nodes", MAT_LED)
    # apiserver gate
    api = MeshBuilder()
    api.add_chamfer_box(0, 1.35, 0, 1.0, 0.35, 0.35, 0.03)
    parts.append((api, MAT_PAPER, "kube-apiserver", {**ped, "label": "kube-apiserver authz"}))
    lod = MeshBuilder()
    lod.add_box(0, 0.2, 0, 4.0, 0.12, 2.6)
    parts.append((lod, MAT_VOID, "lod1-rbac-proxy", {"il": {"lod": 1, "role": "lod-proxy"}}))
    return parts


def scene_service_mesh_sidecar() -> list:
    """Service mesh — sidecar data-plane vs control-plane (Istio/Linkerd pedagogy)."""
    parts = []
    ped = {"il": {"role": "pedagogy", "topic": "service-mesh-sidecar", "domain": "networking"}}
    floor = MeshBuilder()
    floor.add_box(0, -0.85, 0, 4.6, 0.08, 3.0)
    parts.append((floor, MAT_VOID, "mesh-floor", {**ped, "label": "mesh-plane"}))
    # control plane (gold cylinder center-back)
    cp = MeshBuilder()
    cp.add_cylinder(0, 0.9, -1.0, 0.4, 0.7, 22)
    parts.append((cp, MAT_GOLD, "mesh-control-plane", {**ped, "label": "control-plane", "examples": "istiod|linkerd-control"}))
    halo = MeshBuilder()
    halo.add_cylinder(0, 0.55, -1.0, 0.65, 0.05, 22)
    parts.append((halo, MAT_CYAN, "cp-halo", {**ped, "label": "xDS/config"}))
    # two services with app + sidecar
    for si, sx in enumerate((-1.35, 1.35)):
        app = MeshBuilder()
        app.add_chamfer_box(sx, 0.35, 0.55, 0.7, 0.7, 0.55, 0.03)
        parts.append((app, MAT_INK, f"app-{si}", {**ped, "label": f"workload-{si}", "plane": "app"}))
        side = MeshBuilder()
        side.add_chamfer_box(sx + (0.42 if si == 0 else -0.42), 0.35, 0.55, 0.28, 0.55, 0.45, 0.02)
        parts.append((side, MAT_CYAN, f"sidecar-{si}", {**ped, "label": "envoy|linkerd-proxy", "plane": "data"}))
        # mTLS padlock LED
        lock = MeshBuilder()
        lock.add_sphere(sx, 0.85, 0.55, 0.08, 8, 10)
        parts.append((lock, MAT_LED, f"mtls-{si}", {**ped, "label": "mTLS"}))
    # data-plane traffic between sidecars
    for t in range(6):
        u = t / 5
        x = -0.9 + 1.8 * u
        bead = MeshBuilder()
        bead.add_sphere(x, 0.55, 0.55, 0.045, 6, 8)
        parts.append((bead, MAT_GOLD, f"dataplane-hop-{t}", {**ped, "label": "mTLS hop"}))
    # config push arcs from CP to sidecars
    for si, sx in enumerate((-1.35, 1.35)):
        for t in range(4):
            u = t / 3
            x = 0 + (sx - 0) * u
            z = -1.0 + (0.55 - (-1.0)) * u
            y = 0.9 + 0.25 * math.sin(u * math.pi)
            bead = MeshBuilder()
            bead.add_sphere(x, y, z, 0.04, 6, 8)
            parts.append((bead, MAT_CYAN, f"xds-{si}-{t}", {**ped, "label": "xDS config"}))
    lod = MeshBuilder()
    lod.add_box(0, 0.15, 0, 3.8, 0.1, 2.4)
    parts.append((lod, MAT_VOID, "lod1-mesh-proxy", {"il": {"lod": 1, "role": "lod-proxy"}}))
    return parts


def scene_storage_csi_pv() -> list:
    """Storage pedagogy — StorageClass → PV → PVC → Pod mount + CSI driver (CKA storage)."""
    parts = []
    ped = {"il": {"role": "pedagogy", "topic": "storage-csi-pv", "cert": "CKA", "domain": "storage"}}
    floor = MeshBuilder()
    floor.add_box(0, -0.9, 0, 5.2, 0.08, 3.4)
    parts.append((floor, MAT_VOID, "storage-floor", {**ped, "label": "storage-plane"}))
    # Backend disks (void/ink boxes left-back)
    for i, x in enumerate((-1.8, -0.9, 0.0)):
        disk = MeshBuilder()
        disk.add_chamfer_box(x, 0.15, -1.2, 0.7, 0.45, 0.35, 0.025)
        parts.append((disk, MAT_INK, f"backend-disk-{i}", {**ped, "label": f"volume-backend-{i}", "cka": "volume"}))
        platter = MeshBuilder()
        platter.add_cylinder(x, 0.42, -1.2, 0.22, 0.06, 16)
        parts.append((platter, MAT_GOLD, f"platter-{i}", {**ped, "label": "block-device"}))
    # StorageClass (gold cylinder elevated)
    sc = MeshBuilder()
    sc.add_cylinder(-0.9, 1.15, -0.35, 0.32, 0.4, 20)
    parts.append((sc, MAT_GOLD, "storage-class", {**ped, "label": "StorageClass", "kind": "StorageClass"}))
    sc_halo = MeshBuilder()
    sc_halo.add_cylinder(-0.9, 0.9, -0.35, 0.48, 0.04, 20)
    parts.append((sc_halo, MAT_CYAN, "sc-provisioner", {**ped, "label": "provisioner", "plugin": "csi"}))
    # CSI driver node (cyan chamfer)
    csi = MeshBuilder()
    csi.add_chamfer_box(0.9, 0.55, -0.35, 0.85, 0.55, 0.55, 0.03)
    parts.append((csi, MAT_CYAN, "csi-driver", {**ped, "label": "CSI driver", "cka": "csi"}))
    csi_led = MeshBuilder()
    csi_led.add_sphere(0.9, 0.95, -0.35, 0.08, 8, 10)
    parts.append((csi_led, MAT_LED, "csi-controller", {**ped, "label": "csi-controller"}))
    # PersistentVolumes (middle row)
    for i, x in enumerate((-1.4, -0.2, 1.0)):
        pv = MeshBuilder()
        pv.add_chamfer_box(x, 0.35, 0.45, 0.7, 0.4, 0.4, 0.025)
        parts.append((pv, MAT_PAPER if i == 0 else MAT_INK, f"pv-{i}", {
            **ped, "label": f"PersistentVolume-{i}", "kind": "PersistentVolume", "phase": "Bound" if i < 2 else "Available"
        }))
    # PVCs (front-middle cyan)
    for i, x in enumerate((-0.85, 0.55)):
        pvc = MeshBuilder()
        pvc.add_chamfer_box(x, 0.45, 1.15, 0.55, 0.32, 0.35, 0.02)
        parts.append((pvc, MAT_CYAN, f"pvc-{i}", {**ped, "label": f"PersistentVolumeClaim-{i}", "kind": "PersistentVolumeClaim"}))
    # Pod with volume mount (gold sphere + mount cylinder)
    pod = MeshBuilder()
    pod.add_sphere(1.7, 0.7, 1.15, 0.28, 12, 14)
    parts.append((pod, MAT_GOLD, "consumer-pod", {**ped, "label": "Pod", "cka": "pod"}))
    mount = MeshBuilder()
    mount.add_cylinder(1.7, 0.28, 1.15, 0.08, 0.35, 10)
    parts.append((mount, MAT_CYAN, "volume-mount", {**ped, "label": "volumeMount", "path": "/data"}))
    # Node mount stub
    node = MeshBuilder()
    node.add_chamfer_box(1.7, 0.15, 0.35, 0.7, 0.35, 0.55, 0.02)
    parts.append((node, MAT_INK, "worker-node", {**ped, "label": "Node volume attach"}))
    # Edges: SC→CSI→PV→PVC→Pod and backend→PV
    def link(a, b, name, mat_=MAT_CYAN):
        x0, y0, z0 = a
        x1, y1, z1 = b
        mx, my, mz = (x0 + x1) / 2, (y0 + y1) / 2 + 0.06, (z0 + z1) / 2
        dx, dy, dz = x1 - x0, y1 - y0, z1 - z0
        length = math.sqrt(dx * dx + dy * dy + dz * dz) or 1
        edge = MeshBuilder()
        edge.add_box(mx, my, mz, max(0.08, length * 0.85), 0.03, 0.03)
        parts.append((edge, mat_, name, {**ped, "label": "storage-edge"}))

    link((-0.9, 1.15, -0.35), (0.9, 0.55, -0.35), "edge-sc-csi", MAT_GOLD)
    link((0.9, 0.55, -0.35), (-1.4, 0.35, 0.45), "edge-csi-pv0")
    link((0.9, 0.55, -0.35), (-0.2, 0.35, 0.45), "edge-csi-pv1")
    link((-1.4, 0.35, 0.45), (-0.85, 0.45, 1.15), "edge-pv0-pvc0")
    link((-0.2, 0.35, 0.45), (0.55, 0.45, 1.15), "edge-pv1-pvc1", MAT_GOLD)
    link((0.55, 0.45, 1.15), (1.7, 0.7, 1.15), "edge-pvc-pod", MAT_LED)
    link((-1.8, 0.15, -1.2), (-1.4, 0.35, 0.45), "edge-disk-pv0", MAT_GOLD)
    link((-0.9, 0.15, -1.2), (-0.2, 0.35, 0.45), "edge-disk-pv1", MAT_GOLD)
    # data beads along PVC→Pod
    for t in range(5):
        u = t / 4
        x = 0.55 + (1.7 - 0.55) * u
        y = 0.45 + (0.7 - 0.45) * u + 0.12 * math.sin(u * math.pi)
        z = 1.15
        bead = MeshBuilder()
        bead.add_sphere(x, y, z, 0.04, 6, 8)
        parts.append((bead, MAT_CYAN, f"io-bead-{t}", {**ped, "label": "read/write path"}))
    lod = MeshBuilder()
    lod.add_box(0, 0.15, 0, 4.4, 0.1, 2.6)
    parts.append((lod, MAT_VOID, "lod1-storage-proxy", {"il": {"lod": 1, "role": "lod-proxy"}}))
    return parts


def scene_ingress_gateway() -> list:
    """Ingress path — Client → Ingress/Gateway → Service → Endpoints/Pods (CKA networking)."""
    parts = []
    ped = {"il": {"role": "pedagogy", "topic": "ingress-gateway", "cert": "CKA", "domain": "networking"}}
    floor = MeshBuilder()
    floor.add_box(0, -0.9, 0, 5.0, 0.08, 3.2)
    parts.append((floor, MAT_VOID, "ingress-floor", {**ped, "label": "north-south-plane"}))
    # External clients (front gold spheres)
    for i, x in enumerate((-1.2, 0.0, 1.2)):
        client = MeshBuilder()
        client.add_sphere(x, 0.35, 1.35, 0.16, 10, 12)
        parts.append((client, MAT_GOLD, f"client-{i}", {**ped, "label": f"client-{i}", "proto": "HTTPS"}))
    # Ingress / Gateway controller (wide cyan bar)
    ing = MeshBuilder()
    ing.add_chamfer_box(0, 0.55, 0.45, 2.8, 0.35, 0.45, 0.03)
    parts.append((ing, MAT_CYAN, "ingress-controller", {**ped, "label": "Ingress / Gateway", "kind": "Ingress"}))
    # TLS termination LED
    tls = MeshBuilder()
    tls.add_sphere(0, 0.9, 0.45, 0.1, 8, 10)
    parts.append((tls, MAT_LED, "tls-terminate", {**ped, "label": "TLS terminate"}))
    # Host/path rules as paper chips on ingress
    for i, x in enumerate((-0.9, 0.0, 0.9)):
        rule = MeshBuilder()
        rule.add_box(x, 0.75, 0.45, 0.45, 0.08, 0.2)
        parts.append((rule, MAT_PAPER, f"rule-{i}", {**ped, "label": f"host/path-{i}", "cka": "ingress-rule"}))
    # Services (middle)
    for i, x in enumerate((-1.1, 1.1)):
        svc = MeshBuilder()
        svc.add_cylinder(x, 0.45, -0.35, 0.28, 0.4, 16)
        parts.append((svc, MAT_GOLD, f"service-{i}", {**ped, "label": f"Service-{i}", "kind": "Service", "type": "ClusterIP"}))
    # Pods / endpoints (back)
    pods = [(-1.6, -1.25), (-0.7, -1.25), (0.7, -1.25), (1.6, -1.25)]
    for i, (x, z) in enumerate(pods):
        pod = MeshBuilder()
        pod.add_sphere(x, 0.4, z, 0.18, 10, 12)
        parts.append((pod, MAT_CYAN if i % 2 == 0 else MAT_INK, f"endpoint-pod-{i}", {
            **ped, "label": f"Pod-{i}", "kind": "Pod"
        }))
    # Traffic beads: clients → ingress → services → pods
    for ci, cx in enumerate((-1.2, 0.0, 1.2)):
        for t in range(4):
            u = t / 3
            x = cx + (0 - cx) * u * 0.3
            y = 0.35 + 0.2 * u
            z = 1.35 + (0.45 - 1.35) * u
            bead = MeshBuilder()
            bead.add_sphere(x, y, z, 0.04, 6, 8)
            parts.append((bead, MAT_GOLD, f"req-{ci}-{t}", {**ped, "label": "HTTP request"}))
    for si, sx in enumerate((-1.1, 1.1)):
        for t in range(5):
            u = t / 4
            x = 0 + (sx - 0) * u
            y = 0.55 + 0.15 * math.sin(u * math.pi)
            z = 0.45 + (-0.35 - 0.45) * u
            bead = MeshBuilder()
            bead.add_sphere(x, y, z, 0.045, 6, 8)
            parts.append((bead, MAT_CYAN, f"route-{si}-{t}", {**ped, "label": "ingress→service"}))
    # service to pods
    for pi, (px, pz) in enumerate(pods):
        sx = -1.1 if px < 0 else 1.1
        for t in range(3):
            u = t / 2
            x = sx + (px - sx) * u
            y = 0.45 + 0.1 * math.sin(u * math.pi)
            z = -0.35 + (pz - (-0.35)) * u
            bead = MeshBuilder()
            bead.add_sphere(x, y, z, 0.035, 6, 8)
            parts.append((bead, MAT_LED, f"ep-{pi}-{t}", {**ped, "label": "endpoint"}))
    lod = MeshBuilder()
    lod.add_box(0, 0.12, 0, 4.2, 0.1, 2.5)
    parts.append((lod, MAT_VOID, "lod1-ingress-proxy", {"il": {"lod": 1, "role": "lod-proxy"}}))
    return parts


def scene_hpa_autoscaling() -> list:
    """HPA pedagogy — Metrics → HPA controller → Deployment replicas stretch (CKA workloads)."""
    parts = []
    ped = {"il": {"role": "pedagogy", "topic": "hpa-autoscaling", "cert": "CKA", "domain": "workloads"}}
    floor = MeshBuilder()
    floor.add_box(0, -0.9, 0, 5.0, 0.08, 3.2)
    parts.append((floor, MAT_VOID, "hpa-floor", {**ped, "label": "autoscaling-plane"}))
    # Metrics server (left gold)
    metrics = MeshBuilder()
    metrics.add_chamfer_box(-1.9, 0.55, 0.0, 0.7, 0.7, 0.7, 0.03)
    parts.append((metrics, MAT_GOLD, "metrics-server", {**ped, "label": "metrics-server", "cka": "metrics"}))
    for i in range(3):
        bar = MeshBuilder()
        h = 0.25 + i * 0.15
        bar.add_box(-1.9 - 0.15 + i * 0.15, 0.15 + h / 2, 0.4, 0.1, h, 0.08)
        parts.append((bar, MAT_CYAN, f"cpu-bar-{i}", {**ped, "label": "resource metric", "metric": "cpu|memory"}))
    # HPA controller (center cyan cylinder)
    hpa = MeshBuilder()
    hpa.add_cylinder(0, 0.7, 0.0, 0.38, 0.55, 22)
    parts.append((hpa, MAT_CYAN, "hpa-controller", {**ped, "label": "HorizontalPodAutoscaler", "kind": "HorizontalPodAutoscaler"}))
    halo = MeshBuilder()
    halo.add_cylinder(0, 0.4, 0.0, 0.55, 0.05, 22)
    parts.append((halo, MAT_GOLD, "hpa-halo", {**ped, "label": "scale loop"}))
    # Deployment / ReplicaSet spine
    deploy = MeshBuilder()
    deploy.add_chamfer_box(1.5, 0.85, -0.9, 1.6, 0.28, 0.4, 0.02)
    parts.append((deploy, MAT_PAPER, "deployment", {**ped, "label": "Deployment", "kind": "Deployment"}))
    rs = MeshBuilder()
    rs.add_chamfer_box(1.5, 0.45, -0.9, 1.4, 0.2, 0.35, 0.02)
    parts.append((rs, MAT_INK, "replicaset", {**ped, "label": "ReplicaSet", "kind": "ReplicaSet"}))
    # Replicas stretching along +X (visual scale-out)
    for i in range(5):
        x = 0.7 + i * 0.4
        z = 0.55
        # taller / brighter as "desired" grows
        scale = 0.7 + i * 0.12
        pod = MeshBuilder()
        pod.add_sphere(x, 0.35 * scale + 0.15, z, 0.14 * scale, 10, 12)
        mat_ = MAT_CYAN if i < 3 else MAT_LED
        parts.append((pod, mat_, f"replica-{i}", {
            **ped, "label": f"replica-{i}", "desired": i >= 2, "cka": "pod"
        }))
        # stretch rail under replicas
        rail = MeshBuilder()
        rail.add_box(x, 0.02, z, 0.12, 0.04, 0.5)
        parts.append((rail, MAT_GOLD if i >= 2 else MAT_VOID, f"scale-rail-{i}", {**ped, "label": "replica stretch"}))
    # Metric → HPA → Deployment arcs
    for t in range(6):
        u = t / 5
        x = -1.9 + (0 - (-1.9)) * u
        y = 0.55 + 0.35 * math.sin(u * math.pi)
        z = 0.0
        bead = MeshBuilder()
        bead.add_sphere(x, y, z, 0.045, 6, 8)
        parts.append((bead, MAT_GOLD, f"metric-hop-{t}", {**ped, "label": "metrics scrape"}))
    for t in range(6):
        u = t / 5
        x = 0 + (1.5 - 0) * u
        y = 0.7 + 0.25 * math.sin(u * math.pi)
        z = 0.0 + (-0.9 - 0.0) * u
        bead = MeshBuilder()
        bead.add_sphere(x, y, z, 0.045, 6, 8)
        parts.append((bead, MAT_CYAN, f"scale-cmd-{t}", {**ped, "label": "scale decision"}))
    # Desired vs current callouts
    desired = MeshBuilder()
    desired.add_chamfer_box(1.9, 1.35, 0.55, 0.55, 0.22, 0.3, 0.02)
    parts.append((desired, MAT_GOLD, "desired-replicas", {**ped, "label": "desiredReplicas", "value": "5"}))
    current = MeshBuilder()
    current.add_chamfer_box(0.9, 1.35, 0.55, 0.55, 0.22, 0.3, 0.02)
    parts.append((current, MAT_CYAN, "current-replicas", {**ped, "label": "currentReplicas", "value": "3"}))
    lod = MeshBuilder()
    lod.add_box(0, 0.12, 0, 4.2, 0.1, 2.5)
    parts.append((lod, MAT_VOID, "lod1-hpa-proxy", {"il": {"lod": 1, "role": "lod-proxy"}}))
    return parts



MAT_DENY = mat("il-deny", (0.86, 0.26, 0.24, 1.0), 0.1, 0.5, (0.28, 0.04, 0.03))
MAT_MUTED = mat("il-muted", (0.32, 0.36, 0.42, 1.0), 0.05, 0.8)
MAT_SHIELD = mat("il-shield", (0.369, 0.918, 0.831, 0.55), 0.05, 0.2, (0.06, 0.24, 0.2))
MAT_SECRET = mat("il-secret-gold", GOLD, 0.6, 0.22, (0.32, 0.22, 0.05))
MAT_TAINT = mat("il-taint", (0.95, 0.55, 0.18, 1.0), 0.15, 0.45, (0.25, 0.12, 0.02))


def _edge(parts, a, b, name, mat_, ped, label, thick=0.035, lift=0.06, extra=None):
    """Axis-aligned bead chain edge from a→b (kit-v2 style, readable at LOD0)."""
    x0, y0, z0 = a
    x1, y1, z1 = b
    dist = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2 + (z1 - z0) ** 2) or 1.0
    steps = max(3, int(dist / 0.22))
    mb = MeshBuilder()
    for t in range(steps + 1):
        u = t / steps
        mb.add_sphere(
            x0 + (x1 - x0) * u,
            y0 + (y1 - y0) * u + lift * math.sin(u * math.pi),
            z0 + (z1 - z0) * u,
            thick,
            6,
            8,
        )
    parts.append((mb, mat_, name, {**ped, "label": label, **(extra or {})}))


def scene_network_policy_isolation() -> list:
    """NetworkPolicy isolation — namespaces, pods, policy shield, allowed (cyan) vs denied (red/muted) edges."""
    parts = []
    ped = {"il": {"role": "pedagogy", "topic": "network-policy-isolation", "cert": "CKA", "domain": "networking"}}
    floor = MeshBuilder()
    floor.add_box(0, -0.9, 0, 5.4, 0.08, 3.6)
    parts.append((floor, MAT_VOID, "netpol-floor", {**ped, "label": "cluster-network-plane"}))
    # Namespace pads: frontend (left), backend (center, protected), monitoring (right)
    namespaces = [("frontend", -1.85, MAT_INK), ("backend", 0.0, MAT_INK), ("untrusted", 1.85, MAT_MUTED)]
    pod_pos = {}
    for ns, nx, m in namespaces:
        pad = MeshBuilder()
        pad.add_chamfer_box(nx, -0.7, 0, 1.55, 0.18, 2.4, 0.03)
        parts.append((pad, m, f"ns-{ns}", {**ped, "label": f"Namespace/{ns}", "kind": "Namespace"}))
        for pi, pz in enumerate((-0.6, 0.6)):
            pod = MeshBuilder()
            pod.add_sphere(nx, -0.3, pz, 0.2, 12, 14)
            pm = MAT_GOLD if ns == "backend" else (MAT_CYAN if ns == "frontend" else MAT_MUTED)
            app = {"frontend": "web", "backend": "api", "untrusted": "scanner"}[ns]
            parts.append((pod, pm, f"pod-{ns}-{pi}", {
                **ped, "label": f"Pod {app}-{pi}", "kind": "Pod", "labels": f"app={app}", "namespace": ns
            }))
            pod_pos[(ns, pi)] = (nx, -0.3, pz)
    # NetworkPolicy shield around backend: ring + translucent dome posts
    ring = MeshBuilder()
    ring.add_cylinder(0, -0.55, 0, 1.15, 0.05, 32)
    parts.append((ring, MAT_SHIELD, "netpol-shield-ring", {
        **ped, "label": "NetworkPolicy podSelector app=api", "kind": "NetworkPolicy", "policyTypes": "Ingress"
    }))
    for i in range(12):
        a = (i / 12) * math.pi * 2
        post = MeshBuilder()
        post.add_cylinder(math.cos(a) * 1.15, 0.05, math.sin(a) * 1.15, 0.035, 1.2, 8)
        parts.append((post, MAT_SHIELD, f"netpol-shield-post-{i}", {**ped, "label": "policy boundary"}))
    crown = MeshBuilder()
    crown.add_cylinder(0, 0.68, 0, 1.15, 0.04, 32, capped=False)
    parts.append((crown, MAT_SHIELD, "netpol-shield-crown", {**ped, "label": "default-deny ingress"}))
    # Policy manifest tablet
    tablet = MeshBuilder()
    tablet.add_chamfer_box(0, 1.1, -1.35, 1.2, 0.5, 0.06, 0.02)
    parts.append((tablet, MAT_PAPER, "netpol-manifest", {
        **ped, "label": "ingress.from: namespaceSelector name=frontend · ports: 8080/TCP"
    }))
    # Allowed edges: frontend → backend (cyan)
    for pi in range(2):
        _edge(parts, pod_pos[("frontend", pi)], pod_pos[("backend", pi)], f"edge-allow-{pi}", MAT_CYAN, ped,
              "ALLOW frontend→api :8080", 0.04, 0.35, {"verdict": "allow"})
    # Denied edges: untrusted → backend (red, stops at shield)
    for pi in range(2):
        sx, sy, sz = pod_pos[("untrusted", pi)]
        stop = (1.2, sy, sz * 0.9)
        _edge(parts, (sx, sy, sz), stop, f"edge-deny-{pi}", MAT_DENY, ped,
              "DENY untrusted→api (no matching rule)", 0.04, 0.25, {"verdict": "deny"})
        x = MeshBuilder()
        x.add_box(1.22, sy + 0.12, stop[2], 0.06, 0.32, 0.32)
        parts.append((x, MAT_DENY, f"deny-block-{pi}", {**ped, "label": "dropped at policy", "verdict": "deny"}))
    # Egress to DNS stays allowed (muted dashed hint)
    dns = MeshBuilder()
    dns.add_chamfer_box(0, -0.35, 1.55, 0.5, 0.3, 0.3, 0.02)
    parts.append((dns, MAT_PAPER, "kube-dns", {**ped, "label": "kube-dns :53 (egress allow)"}))
    _edge(parts, pod_pos[("backend", 1)], (0, -0.35, 1.55), "edge-egress-dns", MAT_LED, ped,
          "egress DNS allow", 0.03, 0.15, {"verdict": "allow"})
    # CNI enforcement node (policy enforced by CNI, not apiserver)
    cni = MeshBuilder()
    cni.add_cylinder(-1.85, 0.75, -1.35, 0.25, 0.25, 18)
    parts.append((cni, MAT_LED, "cni-enforcer", {**ped, "label": "CNI enforces (Calico/Cilium)", "cka": "cni"}))
    lod = MeshBuilder()
    lod.add_box(0, -0.4, 0, 5.0, 0.12, 3.0)
    parts.append((lod, MAT_VOID, "lod1-netpol-proxy", {"il": {"lod": 1, "role": "lod-proxy"}}))
    return parts


def scene_secrets_configmaps() -> list:
    """Secrets vs ConfigMaps — Pod with mounted Secret (gold/emissive) + ConfigMap (paper) volumes, env + volumeMount edges."""
    parts = []
    ped = {"il": {"role": "pedagogy", "topic": "secrets-configmaps", "cert": "CKA", "domain": "workloads"}}
    floor = MeshBuilder()
    floor.add_box(0, -0.9, 0, 5.0, 0.08, 3.2)
    parts.append((floor, MAT_VOID, "cfg-floor", {**ped, "label": "config-plane"}))
    # etcd vault (Secrets stored base64 / encrypted-at-rest optional)
    etcd = MeshBuilder()
    etcd.add_cylinder(0, 0.2, -1.25, 0.35, 0.6, 22)
    parts.append((etcd, MAT_INK, "etcd-store", {**ped, "label": "etcd (EncryptionConfiguration at rest)"}))
    # Secret object (gold, emissive vault)
    secret = MeshBuilder()
    secret.add_chamfer_box(-1.5, 0.45, -0.2, 0.8, 0.6, 0.6, 0.04)
    parts.append((secret, MAT_SECRET, "secret-db-creds", {
        **ped, "label": "Secret db-creds (type Opaque, base64)", "kind": "Secret"
    }))
    lock = MeshBuilder()
    lock.add_cylinder(-1.5, 0.92, -0.2, 0.1, 0.18, 14)
    parts.append((lock, MAT_DEE_GOLD, "secret-lock", {**ped, "label": "RBAC-gated get secrets"}))
    for i in range(3):
        key = MeshBuilder()
        key.add_box(-1.5 - 0.22 + i * 0.22, 0.45, 0.13, 0.12, 0.3, 0.04)
        parts.append((key, MAT_GOLD, f"secret-key-{i}", {**ped, "label": ["username", "password", "tls.key"][i]}))
    # ConfigMap object (paper sheets)
    cm = MeshBuilder()
    cm.add_chamfer_box(1.5, 0.4, -0.2, 0.8, 0.5, 0.6, 0.03)
    parts.append((cm, MAT_PAPER, "configmap-app-config", {
        **ped, "label": "ConfigMap app-config (plaintext)", "kind": "ConfigMap"
    }))
    for i in range(3):
        sheet = MeshBuilder()
        sheet.add_box(1.5, 0.72 + i * 0.05, -0.2 + (i - 1) * 0.06, 0.62, 0.025, 0.42)
        parts.append((sheet, MAT_PAPER, f"configmap-sheet-{i}", {
            **ped, "label": ["LOG_LEVEL", "app.properties", "nginx.conf"][i]
        }))
    # Pod (center) with container + volumes
    pod = MeshBuilder()
    pod.add_chamfer_box(0, -0.12, 1.0, 1.4, 0.22, 0.8, 0.03)
    parts.append((pod, MAT_INK, "pod-shell", {**ped, "label": "Pod api-0", "kind": "Pod"}))
    podring = MeshBuilder()
    podring.add_cylinder(0, 0.45, 1.0, 0.36, 0.04, 24, capped=False)
    parts.append((podring, MAT_CYAN, "pod-boundary", {**ped, "label": "Pod sandbox"}))
    ctr = MeshBuilder()
    ctr.add_sphere(0, 0.45, 1.0, 0.24, 12, 14)
    parts.append((ctr, MAT_CYAN, "container-app", {**ped, "label": "container app"}))
    # Volume mounts (cylinders on pod faces)
    vsec = MeshBuilder()
    vsec.add_cylinder(-0.55, 0.35, 1.0, 0.13, 0.5, 14)
    parts.append((vsec, MAT_SECRET, "volume-secret", {
        **ped, "label": "volume secret → /etc/creds (tmpfs, readOnly)", "mountPath": "/etc/creds"
    }))
    vcm = MeshBuilder()
    vcm.add_cylinder(0.55, 0.35, 1.0, 0.13, 0.5, 14)
    parts.append((vcm, MAT_PAPER, "volume-configmap", {
        **ped, "label": "volume configMap → /etc/config", "mountPath": "/etc/config"
    }))
    # env chips (envFrom / valueFrom)
    for i, (lbl, m) in enumerate((("env DB_PASS ← secretKeyRef", MAT_GOLD), ("env LOG_LEVEL ← configMapKeyRef", MAT_PAPER))):
        chip = MeshBuilder()
        chip.add_box(-0.25 + i * 0.5, 0.92, 1.0, 0.36, 0.07, 0.2)
        parts.append((chip, m, f"env-chip-{i}", {**ped, "label": lbl}))
    # volumeMount edges
    _edge(parts, (-1.5, 0.45, -0.2), (-0.55, 0.35, 1.0), "edge-secret-mount", MAT_SECRET, ped,
          "volumeMount secret", 0.045, 0.3, {"source": "Secret"})
    _edge(parts, (1.5, 0.4, -0.2), (0.55, 0.35, 1.0), "edge-configmap-mount", MAT_CYAN, ped,
          "volumeMount configMap", 0.045, 0.3, {"source": "ConfigMap"})
    _edge(parts, (0, 0.2, -1.25), (-1.5, 0.45, -0.2), "edge-etcd-secret", MAT_INK, ped,
          "stored in etcd", 0.03, 0.12)
    _edge(parts, (0, 0.2, -1.25), (1.5, 0.4, -0.2), "edge-etcd-configmap", MAT_INK, ped,
          "stored in etcd", 0.03, 0.12)
    # kubelet projection node
    kubelet = MeshBuilder()
    kubelet.add_chamfer_box(0, -0.55, 1.0, 1.8, 0.2, 1.1, 0.03)
    parts.append((kubelet, MAT_VOID, "node-kubelet", {**ped, "label": "kubelet projects volumes (tmpfs for Secret)"}))
    led = MeshBuilder()
    led.add_sphere(0.8, -0.35, 1.5, 0.06, 8, 10)
    parts.append((led, MAT_LED, "kubelet-led", {**ped, "label": "kubelet"}))
    lod = MeshBuilder()
    lod.add_box(0, 0.1, 0, 4.2, 0.1, 2.6)
    parts.append((lod, MAT_VOID, "lod1-config-proxy", {"il": {"lod": 1, "role": "lod-proxy"}}))
    return parts


def scene_scheduling_affinity() -> list:
    """Scheduling — kube-scheduler, worker nodes with affinity/taint badges, pending vs bound pods."""
    parts = []
    ped = {"il": {"role": "pedagogy", "topic": "scheduling-affinity", "cert": "CKA", "domain": "scheduling"}}
    floor = MeshBuilder()
    floor.add_box(0, -0.9, 0, 5.4, 0.08, 3.6)
    parts.append((floor, MAT_VOID, "sched-floor", {**ped, "label": "scheduling-plane"}))
    # kube-scheduler (gold cylinder, back center)
    sched = MeshBuilder()
    sched.add_cylinder(0, 0.75, -1.3, 0.38, 0.6, 24)
    parts.append((sched, MAT_GOLD, "kube-scheduler", {**ped, "label": "kube-scheduler (filter → score → bind)", "cka": "scheduler"}))
    halo = MeshBuilder()
    halo.add_cylinder(0, 0.4, -1.3, 0.6, 0.05, 24)
    parts.append((halo, MAT_CYAN, "scheduler-halo", {**ped, "label": "scheduling cycle"}))
    # filter/score phase chips
    for i, lbl in enumerate(("Filter (predicates)", "Score (priorities)", "Bind")):
        chip = MeshBuilder()
        chip.add_box(-0.55 + i * 0.55, 1.22, -1.3, 0.45, 0.08, 0.18)
        parts.append((chip, MAT_PAPER if i < 2 else MAT_LED, f"sched-phase-{i}", {**ped, "label": lbl}))
    # Worker nodes with badges
    nodes = [
        ("node-a", -1.8, {"labels": "disktype=ssd zone=us-east-1a", "taint": None}, MAT_CYAN),
        ("node-b", 0.0, {"labels": "zone=us-east-1b", "taint": "gpu=true:NoSchedule"}, MAT_INK),
        ("node-c", 1.8, {"labels": "disktype=hdd", "taint": "maintenance:NoExecute"}, MAT_INK),
    ]
    for name, nx, meta, m in nodes:
        n = MeshBuilder()
        n.add_chamfer_box(nx, -0.35, 0.35, 1.2, 0.7, 1.0, 0.04)
        parts.append((n, m, name, {**ped, "label": name, "kind": "Node", **{k: v for k, v in meta.items() if v}}))
        badge = MeshBuilder()
        badge.add_box(nx - 0.3, 0.08, 0.86, 0.45, 0.14, 0.04)
        parts.append((badge, MAT_LED if "ssd" in meta["labels"] else MAT_PAPER, f"{name}-label-badge", {
            **ped, "label": meta["labels"], "badge": "nodeLabel"
        }))
        if meta["taint"]:
            t = MeshBuilder()
            t.add_cylinder(nx + 0.38, 0.12, 0.86, 0.12, 0.06, 6)
            parts.append((t, MAT_TAINT, f"{name}-taint", {**ped, "label": f"taint {meta['taint']}", "badge": "taint"}))
            tt = MeshBuilder()
            tt.add_box(nx + 0.38, 0.12, 0.9, 0.04, 0.16, 0.02)
            parts.append((tt, MAT_DENY, f"{name}-taint-mark", {**ped, "label": "repels pods without toleration"}))
    # Bound pod on node-a (nodeAffinity disktype=ssd satisfied)
    bound = MeshBuilder()
    bound.add_sphere(-1.8, 0.28, 0.35, 0.22, 12, 14)
    parts.append((bound, MAT_CYAN, "pod-bound-affinity", {
        **ped, "label": "Pod web (nodeAffinity disktype=ssd) → Bound node-a", "phase": "Running", "nodeName": "node-a"
    }))
    # Pod with toleration bound to node-b
    tol = MeshBuilder()
    tol.add_sphere(0.0, 0.28, 0.35, 0.22, 12, 14)
    parts.append((tol, MAT_GOLD, "pod-bound-toleration", {
        **ped, "label": "Pod trainer (toleration gpu=true:NoSchedule) → Bound node-b", "phase": "Running", "nodeName": "node-b"
    }))
    tring = MeshBuilder()
    tring.add_cylinder(0.0, 0.28, 0.35, 0.3, 0.03, 20, capped=False)
    parts.append((tring, MAT_TAINT, "toleration-ring", {**ped, "label": "tolerations[] matches taint"}))
    # Pending pod hovering (no node satisfies requiredDuringScheduling)
    pend = MeshBuilder()
    pend.add_sphere(1.0, 1.25, 1.35, 0.22, 12, 14)
    parts.append((pend, MAT_MUTED, "pod-pending", {
        **ped, "label": "Pod db (nodeAffinity disktype=nvme) → Pending · 0/3 nodes available", "phase": "Pending"
    }))
    pend_note = MeshBuilder()
    pend_note.add_chamfer_box(1.0, 1.7, 1.35, 0.9, 0.22, 0.06, 0.02)
    parts.append((pend_note, MAT_DENY, "event-failed-scheduling", {
        **ped, "label": "Event FailedScheduling: node(s) didn't match affinity / had untolerated taint"
    }))
    # Scheduler decision edges
    _edge(parts, (0, 0.75, -1.3), (-1.8, 0.28, 0.35), "edge-bind-node-a", MAT_CYAN, ped,
          "bind → node-a (affinity score)", 0.04, 0.45, {"verdict": "bind"})
    _edge(parts, (0, 0.75, -1.3), (0.0, 0.28, 0.35), "edge-bind-node-b", MAT_GOLD, ped,
          "bind → node-b (tolerates taint)", 0.04, 0.4, {"verdict": "bind"})
    _edge(parts, (1.0, 1.25, 1.35), (1.8, 0.1, 0.5), "edge-reject-node-c", MAT_DENY, ped,
          "filtered: NoExecute taint + label mismatch", 0.035, 0.15, {"verdict": "reject"})
    _edge(parts, (0, 0.75, -1.3), (1.0, 1.25, 1.35), "edge-sched-pending", MAT_MUTED, ped,
          "queued: unschedulable", 0.03, 0.2, {"verdict": "pending"})
    lod = MeshBuilder()
    lod.add_box(0, -0.2, 0, 5.0, 0.12, 3.0)
    parts.append((lod, MAT_VOID, "lod1-sched-proxy", {"il": {"lod": 1, "role": "lod-proxy"}}))
    return parts


# ── AWS SAA / CCP spatial track (2026-10-06) ──────────────────────────────
# Naming contract for interactive sims (docs/assets/il-immersive-sims.js):
#   az-a-* / az-b-*  → per-AZ resources (sim tints them on AZ failure)
#   sim-*            → hidden until a sim state reveals them (e.g. ASG surge)
#   gate-<id>-*      → IAM evaluation gates (sim lights the gate that decides)
MAT_AWS_ORANGE = mat("il-aws-orange", (0.96, 0.60, 0.16, 1.0), 0.25, 0.4, (0.22, 0.11, 0.02))


def _rail_frame(parts, cx, cy, cz, sx, sz, name, mat_, ped, label, rail=0.045):
    """Flat rectangular boundary (four rails) — readable VPC/subnet edge that never occludes contents."""
    mb = MeshBuilder()
    hx, hz = sx / 2, sz / 2
    mb.add_box(cx, cy, cz - hz, sx, rail, rail)
    mb.add_box(cx, cy, cz + hz, sx, rail, rail)
    mb.add_box(cx - hx, cy, cz, rail, rail, sz)
    mb.add_box(cx + hx, cy, cz, rail, rail, sz)
    parts.append((mb, mat_, name, {**ped, "label": label}))


def scene_aws_vpc_multi_az() -> list:
    """AWS SAA — VPC across two AZs: IGW → ALB → ASG EC2 (private app subnets) → RDS Multi-AZ (sync standby)."""
    parts = []
    ped = {"il": {"role": "pedagogy", "topic": "aws-vpc-multi-az", "cert": "AWS SAA-C03 / CLF-C02",
                  "domain": "resilient-architectures"}}
    floor = MeshBuilder()
    floor.add_box(0, -0.92, 0.1, 5.8, 0.08, 4.6)
    parts.append((floor, MAT_VOID, "region-floor", {**ped, "label": "Region us-east-1"}))
    _rail_frame(parts, 0, -0.84, 0.1, 5.5, 3.5, "vpc-boundary", MAT_AWS_ORANGE, ped, "VPC 10.0.0.0/16")
    rows = (("public", -1.05, MAT_CYAN, "10.0.{n}.0/24 public (route 0.0.0.0/0 → IGW)"),
            ("app", 0.1, MAT_INK, "10.0.1{n}.0/24 private app (0.0.0.0/0 → NAT)"),
            ("data", 1.2, MAT_INK, "10.0.2{n}.0/24 private data (no internet route)"))
    for az, ax, n in (("a", -1.38, 1), ("b", 1.38, 2)):
        pad = MeshBuilder()
        pad.add_chamfer_box(ax, -0.82, 0.1, 2.5, 0.06, 3.3, 0.02)
        parts.append((pad, MAT_INK, f"az-{az}-pad", {**ped, "label": f"Availability Zone us-east-1{az}", "kind": "AZ"}))
        for row, rz, m, lbl in rows:
            tile = MeshBuilder()
            tile.add_chamfer_box(ax, -0.74, rz, 2.25, 0.07, 0.82, 0.02)
            parts.append((tile, m if row == "public" else MAT_MUTED, f"az-{az}-subnet-{row}",
                          {**ped, "label": lbl.format(n=n), "kind": "Subnet"}))
    # Internet gateway + users outside the VPC
    users = MeshBuilder()
    users.add_sphere(0, 0.55, -2.35, 0.2, 12, 14)
    parts.append((users, MAT_PAPER, "internet-users", {**ped, "label": "Internet clients"}))
    igw = MeshBuilder()
    igw.add_cylinder(0, 0.05, -1.82, 0.26, 0.42, 6)
    parts.append((igw, MAT_AWS_ORANGE, "igw", {**ped, "label": "Internet Gateway (one per VPC, HA by design)"}))
    _edge(parts, (0, 0.5, -2.3), (0, 0.15, -1.85), "edge-users-igw", MAT_PAPER, ped, "HTTPS 443", 0.035, 0.1)
    # ALB spans both public subnets (one node per AZ)
    alb = MeshBuilder()
    alb.add_chamfer_box(0, -0.42, -1.05, 3.9, 0.14, 0.26, 0.02)
    parts.append((alb, MAT_GOLD, "alb", {**ped, "label": "Application Load Balancer (cross-zone, health checks)"}))
    for az, ax in (("a", -1.38), ("b", 1.38)):
        node = MeshBuilder()
        node.add_sphere(ax, -0.2, -1.05, 0.16, 12, 14)
        parts.append((node, MAT_LED, f"az-{az}-alb-node", {**ped, "label": f"ALB node us-east-1{az}"}))
        nat = MeshBuilder()
        nat.add_cylinder(ax + (-0.82 if az == "a" else 0.82), -0.5, -1.05, 0.15, 0.32, 14)
        parts.append((nat, MAT_AWS_ORANGE, f"az-{az}-nat", {**ped, "label": f"NAT gateway (zonal) us-east-1{az}"}))
    _edge(parts, (0, 0.0, -1.8), (-1.38, -0.2, -1.05), "edge-igw-alb-a", MAT_CYAN, ped, "IGW → ALB", 0.035, 0.2)
    _edge(parts, (0, 0.0, -1.8), (1.38, -0.2, -1.05), "edge-igw-alb-b", MAT_CYAN, ped, "IGW → ALB", 0.035, 0.2)
    # ASG boundary across both app subnets
    _rail_frame(parts, 0, -0.62, 0.1, 5.1, 0.95, "asg-boundary", MAT_GOLD, ped,
                "Auto Scaling group (min 2 · desired 4 · max 6) spread across AZs", 0.03)
    for az, ax in (("a", -1.38), ("b", 1.38)):
        for i, dx in enumerate((-0.48, 0.48)):
            ec2 = MeshBuilder()
            ec2.add_chamfer_box(ax + dx, -0.42, 0.1, 0.5, 0.42, 0.42, 0.04)
            parts.append((ec2, MAT_CYAN, f"az-{az}-ec2-{i}", {
                **ped, "label": f"EC2 web-{az}{i} (target healthy)", "kind": "EC2"}))
            _edge(parts, (ax, -0.25, -1.0), (ax + dx, -0.2, 0.05), f"az-{az}-edge-alb-ec2-{i}", MAT_CYAN, ped,
                  "ALB → target :8080", 0.03, 0.15)
        # Hidden surge capacity — revealed when the other AZ fails and the ASG rebalances here
        for i, dz in enumerate((-0.3, 0.3)):
            surge = MeshBuilder()
            surge.add_chamfer_box(ax + (0.0), -0.42, 0.1 + dz, 0.34, 0.3, 0.26, 0.03)
            parts.append((surge, MAT_LED, f"sim-az-{az}-ec2-surge-{i}", {
                **ped, "label": f"ASG replacement instance in us-east-1{az}", "simOnly": True}))
    # RDS Multi-AZ: primary in a, synchronous standby in b
    for az, ax, m, role in (("a", -1.38, MAT_GOLD, "primary (writer)"), ("b", 1.38, MAT_INK, "standby (sync, no reads)")):
        db = MeshBuilder()
        db.add_cylinder(ax, -0.38, 1.2, 0.34, 0.52, 24)
        parts.append((db, m, f"az-{az}-rds", {**ped, "label": f"RDS {role} us-east-1{az}", "kind": "RDS"}))
        ring = MeshBuilder()
        ring.add_cylinder(ax, -0.08, 1.2, 0.36, 0.04, 24, capped=False)
        parts.append((ring, MAT_LED if az == "a" else MAT_MUTED, f"az-{az}-rds-role-ring",
                      {**ped, "label": "writer endpoint" if az == "a" else "standby"}))
        for i, dx in enumerate((-0.48, 0.48)):
            _edge(parts, (ax + dx, -0.3, 0.3), (-1.38, -0.2, 1.05), f"az-{az}-edge-ec2-db-{i}", MAT_INK, ped,
                  "app → RDS endpoint :5432", 0.025, 0.12)
    _edge(parts, (-1.04, -0.38, 1.2), (1.04, -0.38, 1.2), "edge-rds-sync-replication", MAT_GOLD, ped,
          "synchronous replication (Multi-AZ)", 0.04, 0.18)
    endpoint = MeshBuilder()
    endpoint.add_chamfer_box(0, 0.25, 1.75, 1.5, 0.2, 0.06, 0.02)
    parts.append((endpoint, MAT_PAPER, "rds-endpoint-dns", {
        **ped, "label": "mydb.xxxx.us-east-1.rds.amazonaws.com (CNAME flips on failover)"}))
    return parts


def _gate(parts, gx, gid, mat_, ped, label, tablet_label):
    """IAM evaluation gate: two posts + lintel + policy tablet; every mesh prefixed gate-<gid>-."""
    for side, dz in (("l", -0.55), ("r", 0.55)):
        post = MeshBuilder()
        post.add_chamfer_box(gx, -0.25, dz, 0.16, 1.2, 0.16, 0.02)
        parts.append((post, mat_, f"gate-{gid}-post-{side}", {**ped, "label": label}))
    lintel = MeshBuilder()
    lintel.add_chamfer_box(gx, 0.42, 0, 0.2, 0.14, 1.3, 0.02)
    parts.append((lintel, mat_, f"gate-{gid}-lintel", {**ped, "label": label}))
    tablet = MeshBuilder()
    tablet.add_chamfer_box(gx, 0.82, 0, 0.06, 0.42, 0.9, 0.02)
    parts.append((tablet, MAT_PAPER, f"gate-{gid}-policy", {**ped, "label": tablet_label}))


def scene_aws_iam_policy_eval() -> list:
    """AWS IAM policy evaluation — request walks Deny → SCP/RCP → resource policy → identity → boundary → session gates."""
    parts = []
    ped = {"il": {"role": "pedagogy", "topic": "aws-iam-policy-eval", "cert": "AWS SAA-C03 / CLF-C02",
                  "domain": "secure-architectures"}}
    floor = MeshBuilder()
    floor.add_box(0, -0.9, 0, 6.0, 0.08, 3.2)
    parts.append((floor, MAT_VOID, "iam-floor", {**ped, "label": "IAM policy evaluation (single account)"}))
    lane = MeshBuilder()
    lane.add_chamfer_box(-0.1, -0.82, 0, 5.4, 0.06, 0.7, 0.02)
    parts.append((lane, MAT_INK, "iam-request-lane", {**ped, "label": "request context"}))
    req = MeshBuilder()
    req.add_sphere(-2.55, -0.3, 0, 0.24, 14, 16)
    parts.append((req, MAT_PAPER, "iam-request", {
        **ped, "label": "Request: principal=role/app · action=s3:DeleteObject · resource=arn:aws:s3:::prod-bucket/*"}))
    gates = (
        (-1.75, "explicit-deny", MAT_DENY, "1 · Any explicit Deny?", "\"Effect\": \"Deny\" in ANY policy wins"),
        (-0.95, "scp", MAT_AWS_ORANGE, "2 · Organizations SCP / RCP allow?", "SCPs cap the account; never grant"),
        (-0.15, "resource-policy", MAT_GOLD, "3 · Resource-based policy allow?", "bucket policy Principal=arn (same account)"),
        (0.65, "identity-policy", MAT_CYAN, "4 · Identity-based policy allow?", "role / user / group policies"),
        (1.45, "permission-boundary", MAT_LED, "5 · Permissions boundary allow?", "boundary = max, never grants"),
        (2.2, "session-policy", MAT_MUTED, "6 · Session policy allow?", "AssumeRole Policy / federation"),
    )
    prev = (-2.3, -0.3, 0)
    for gx, gid, m, lbl, tab in gates:
        _gate(parts, gx, gid, m, ped, lbl, tab)
        _edge(parts, prev, (gx - 0.12, -0.3, 0), f"flow-to-{gid}", MAT_CYAN, ped, "evaluate next", 0.03, 0.06)
        prev = (gx + 0.12, -0.3, 0)
    # Decision pedestals at the end of the lane
    for dz, did, m, lbl in ((-0.95, "allow", MAT_CYAN, "ALLOW"),
                            (0.0, "implicit-deny", MAT_MUTED, "implicit deny (no matching Allow)"),
                            (0.95, "explicit-deny", MAT_DENY, "EXPLICIT DENY")):
        ped_ = MeshBuilder()
        ped_.add_cylinder(2.75, -0.62, dz, 0.24, 0.36, 20)
        parts.append((ped_, m, f"decision-{did}", {**ped, "label": lbl, "kind": "Decision"}))
        orb = MeshBuilder()
        orb.add_sphere(2.75, -0.3, dz, 0.13, 10, 12)
        parts.append((orb, m, f"decision-{did}-orb", {**ped, "label": lbl}))
    # Deny short-circuit rail: from the deny gate straight to the explicit-deny pedestal
    _edge(parts, (-1.75, 0.55, 0.55), (2.75, -0.2, 0.95), "deny-short-circuit", MAT_DENY, ped,
          "explicit Deny short-circuits evaluation", 0.03, 0.5)
    return parts


SCENES = {
    "lecture-k8s-control-plane.glb": scene_k8s_control_plane,
    "cert-cka.glb": scene_cert_cka,
    "rack-19u.glb": scene_rack_19u,
    "hermetic-monas.glb": scene_hermetic_monas,
    "sim-superlab.glb": scene_sim_superlab,
    "k8s-cluster.glb": scene_k8s_control_plane,  # alias
    "muse-dee-monas.glb": scene_muse_dee_monas,
    "cka-etcd-quorum.glb": scene_cka_etcd_quorum,
    "cni-pod-network.glb": scene_cni_pod_network,
    "rbac-authz-graph.glb": scene_rbac_authz_graph,
    "service-mesh-sidecar.glb": scene_service_mesh_sidecar,
    "storage-csi-pv.glb": scene_storage_csi_pv,
    "ingress-gateway.glb": scene_ingress_gateway,
    "hpa-autoscaling.glb": scene_hpa_autoscaling,
    "network-policy-isolation.glb": scene_network_policy_isolation,
    "secrets-configmaps.glb": scene_secrets_configmaps,
    "scheduling-affinity.glb": scene_scheduling_affinity,
    "aws-vpc-multi-az.glb": scene_aws_vpc_multi_az,
    "aws-iam-policy-eval.glb": scene_aws_iam_policy_eval,
}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Author Interstitium immersive .glb assets")
    ap.add_argument(
        "--out",
        type=Path,
        default=Path("docs/assets/immersive"),
        help="Output directory for .glb files",
    )
    ap.add_argument("--only", nargs="*", help="Optional subset of filenames")
    args = ap.parse_args(argv)
    out: Path = args.out
    out.mkdir(parents=True, exist_ok=True)
    selected = args.only or list(SCENES.keys())
    written = []
    for name in selected:
        if name not in SCENES:
            print(f"unknown scene: {name}", file=sys.stderr)
            continue
        parts = SCENES[name]()
        extras = {
            "interstitium": {
                "sceneId": name.replace(".glb", ""),
                "authored": "kit-v2",
                "blenderPolish": "scripts/blender_polish_glb.py",
            }
        }
        blob = pack_glb(parts, scene_extras=extras)
        path = out / name
        path.write_bytes(blob)
        magic = blob[:4]
        assert magic == b"glTF", magic
        written.append((name, len(blob), len(parts)))
        print(f"wrote {path} ({len(blob)} bytes, {len(parts)} meshes)")
    return 0 if written else 1


if __name__ == "__main__":
    raise SystemExit(main())
