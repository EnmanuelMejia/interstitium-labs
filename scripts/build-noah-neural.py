"""Original Noah neural geometry. Standard library, deterministic, Blender-compatible GLB.
Rebuild with python scripts/build-noah-neural.py; no copyrighted footage or external assets.
"""
import json
import math
from pathlib import Path
from author_immersive_glb import MeshBuilder, pack_glb

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/assets/noah'
OUT.mkdir(parents=True, exist_ok=True)
nodes = []
for i in range(96):
    y = 1 - 2 * (i + 0.5) / 96
    r = math.sqrt(1 - y * y)
    a = i * math.pi * (3 - math.sqrt(5))
    # Original ellipsoidal neural shell, composed in true spatial coordinates.
    nodes.append([round(r * math.cos(a) * 1.55, 6), round(y * 1.05, 6), round(r * math.sin(a), 6)])
edges = set()
for i, p in enumerate(nodes):
    near = sorted(range(len(nodes)), key=lambda j: sum((p[k] - nodes[j][k]) ** 2 for k in range(3)))
    for j in near[1:4]:
        edges.add(tuple(sorted((i, j))))
edges = sorted(edges)
node_mesh = MeshBuilder()
gold_mesh = MeshBuilder()
links = MeshBuilder()
for i, p in enumerate(nodes):
    (gold_mesh if i % 8 == 0 else node_mesh).add_sphere(*p, 0.025 if i % 8 else 0.038, 6, 8)

def tube(mesh, start, end, radius=0.005, segments=6):
    direction = [end[k] - start[k] for k in range(3)]
    length = math.sqrt(sum(v*v for v in direction))
    n = [v / length for v in direction]
    seed = [0, 1, 0] if abs(n[1]) < 0.9 else [1, 0, 0]
    u = [n[1]*seed[2]-n[2]*seed[1], n[2]*seed[0]-n[0]*seed[2], n[0]*seed[1]-n[1]*seed[0]]
    size = math.sqrt(sum(v*v for v in u)); u = [v/size for v in u]
    v = [n[1]*u[2]-n[2]*u[1], n[2]*u[0]-n[0]*u[2], n[0]*u[1]-n[1]*u[0]]
    def point(center, angle):
        return tuple(center[k] + radius * (u[k]*math.cos(angle) + v[k]*math.sin(angle)) for k in range(3))
    for t in range(segments):
        a = 2*math.pi*t/segments; b = 2*math.pi*(t+1)/segments
        mesh.add_quad(point(start,a),point(end,a),point(end,b),point(start,b))
for i,j in edges:
    tube(links, nodes[i], nodes[j])
materials = [
    (node_mesh, {'name':'Azure signal','baseColorFactor':[0.12,0.52,0.82,1],'metallicFactor':0.3,'roughnessFactor':0.25,'emissiveFactor':[0.06,0.3,0.65]}, 'Neural signal nodes'),
    (gold_mesh, {'name':'Gold nucleus','baseColorFactor':[0.72,0.52,0.2,1],'metallicFactor':0.8,'roughnessFactor':0.22,'emissiveFactor':[0.3,0.16,0.02]}, 'Gold anchor nodes'),
    (links, {'name':'Neural connections','baseColorFactor':[0.03,0.19,0.32,1],'metallicFactor':0.45,'roughnessFactor':0.4}, 'Interconnected neural edges')
]
model = pack_glb(materials, {'provenance':'Original Interstitium Labs procedural geometry','generator':'scripts/build-noah-neural.py','editable':True,'license':'Interstitium Labs project asset; no third-party input','nodes':len(nodes),'edges':len(edges)})
(OUT/'noah-neural.glb').write_bytes(model)
(OUT/'noah-neural.json').write_text(json.dumps({'version':1,'provenance':'original procedural geometry','nodes':nodes,'edges':edges,'loopSeconds':20}, separators=(',',':')), encoding='utf-8')
print(json.dumps({'nodes':len(nodes),'edges':len(edges),'triangles':sum(len(m.indices)//3 for m,_,_ in materials),'glbBytes':len(model)}))
