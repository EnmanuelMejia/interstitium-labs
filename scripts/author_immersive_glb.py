#!/usr/bin/env python3
"""
Interstitium Labs — glTF 2.0 binary (.glb) authoring kit.

Honest provenance: kit-authored meshes (POSITION + NORMAL, TRIANGLES, PBR materials).
Blender-compatible glTF 2.0 binary — open/polish on P920. NOT hand-sculpted in Blender UI.
Palette: cyan #5EEAD4 · gold #D4A853 · void #070B16.

Usage:
  python3 scripts/author_immersive_glb.py [--out docs/assets/immersive]
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

    def bounds(self):
        if not self.positions:
            return [0, 0, 0], [0, 0, 0]
        xs = self.positions[0::3]
        ys = self.positions[1::3]
        zs = self.positions[2::3]
        return [min(xs), min(ys), min(zs)], [max(xs), max(ys), max(zs)]


def pack_glb(meshes_with_mats: list[tuple[MeshBuilder, dict, str]]) -> bytes:
    """
    meshes_with_mats: list of (MeshBuilder, material_dict, node_name)
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

    for mb, mat, name in meshes_with_mats:
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
        nodes.append({"name": name, "mesh": mesh_idx})

    bin_blob = b"".join(bin_parts)
    # pad BIN to 4-byte
    if len(bin_blob) % 4:
        bin_blob += b"\x00" * (4 - len(bin_blob) % 4)

    gltf = {
        "asset": {
            "version": "2.0",
            "generator": "Interstitium Labs glTF kit (author_immersive_glb.py)",
            "copyright": "Interstitium Labs — kit-authored, Blender-compatible; polish on P920",
        },
        "scene": 0,
        "scenes": [{"name": "Scene", "nodes": list(range(len(nodes)))}],
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


def scene_k8s_control_plane() -> list:
    """Control-plane cylinder + surrounding worker boxes (procedural:k8s family)."""
    parts = []
    # floor ring
    floor = MeshBuilder()
    floor.add_cylinder(0, -0.2, 0, 2.0, 0.06, 24)
    parts.append((floor, MAT_INK, "floor-ring"))
    # control plane body
    cp = MeshBuilder()
    cp.add_cylinder(0, 0.9, 0, 0.45, 0.55, 20)
    parts.append((cp, MAT_GOLD, "control-plane"))
    # etcd/api cube on top
    api = MeshBuilder()
    api.add_box(0, 1.35, 0, 0.42, 0.42, 0.42)
    parts.append((api, MAT_CYAN, "api-server"))
    # halo ring (thin cylinder)
    halo = MeshBuilder()
    halo.add_cylinder(0, 0.55, 0, 0.75, 0.05, 20, capped=True)
    parts.append((halo, MAT_CYAN, "cp-halo"))
    # workers
    n = 5
    for i in range(n):
        a = (i / n) * math.pi * 2
        x, z = math.cos(a) * 1.55, math.sin(a) * 1.55
        w = MeshBuilder()
        w.add_box(x, 0.2, z, 0.4, 0.55, 0.4)
        parts.append((w, MAT_CYAN if i % 2 == 0 else MAT_INK, f"worker-{i}"))
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


SCENES = {
    "lecture-k8s-control-plane.glb": scene_k8s_control_plane,
    "cert-cka.glb": scene_cert_cka,
    "rack-19u.glb": scene_rack_19u,
    "hermetic-monas.glb": scene_hermetic_monas,
    "sim-superlab.glb": scene_sim_superlab,
    "k8s-cluster.glb": scene_k8s_control_plane,  # alias
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
        blob = pack_glb(parts)
        path = out / name
        path.write_bytes(blob)
        magic = blob[:4]
        assert magic == b"glTF", magic
        written.append((name, len(blob), len(parts)))
        print(f"wrote {path} ({len(blob)} bytes, {len(parts)} meshes)")
    return 0 if written else 1


if __name__ == "__main__":
    raise SystemExit(main())
