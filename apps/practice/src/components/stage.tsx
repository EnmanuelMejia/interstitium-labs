import { useEffect, useRef } from "react";
import type { BufferGeometry, Material, Object3D, Vector3 } from "three";
import type { SceneId } from "@/lib/paths";

type StageProps = {
  scene: SceneId;
  signal: number;
  label: string;
  /** 0–1 stall point. Pipeline packets stop here until the studio clears. */
  hold?: number | null;
};

type Mover = { obj: Object3D; base: Vector3; phase: number; hot: boolean; scale: number };
type Orbit = { obj: Object3D; base: number; speed: number };

export function Stage({ scene, signal, label, hold = null }: StageProps) {
  const host = useRef<HTMLDivElement>(null);
  const signalRef = useRef(signal);
  const holdRef = useRef<number | null>(hold);
  signalRef.current = signal;
  holdRef.current = hold;

  useEffect(() => {
    const el = host.current;
    if (!el) return;
    let disposed = false;
    let cleanup = () => {};

    void import("three").then((THREE) => {
      if (disposed || !host.current) return;
      const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
      renderer.setPixelRatio(Math.min(2, window.devicePixelRatio || 1));
      renderer.setClearColor(0x000000, 0);
      renderer.toneMapping = THREE.ACESFilmicToneMapping;
      renderer.toneMappingExposure = 1.08;
      const width = el.clientWidth || 320;
      const height = el.clientHeight || 280;
      renderer.setSize(width, height);
      renderer.domElement.style.position = "absolute";
      renderer.domElement.style.inset = "0";
      renderer.domElement.style.display = "block";
      renderer.domElement.style.width = "100%";
      renderer.domElement.style.height = "100%";
      el.appendChild(renderer.domElement);

      const scene3 = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(42, width / height, 0.1, 80);
      scene3.add(new THREE.AmbientLight(0xeceae4, 0.38));
      const key = new THREE.DirectionalLight(0xf3efe4, 1.45);
      key.position.set(4, 6, 5);
      scene3.add(key);
      const rim = new THREE.DirectionalLight(0x3c9fbe, 0.55);
      rim.position.set(-5, 1, -3);
      scene3.add(rim);
      const goldLight = new THREE.PointLight(0xc6a36a, 6, 12);
      goldLight.position.set(0.4, 0.2, 1.6);
      scene3.add(goldLight);

      const bone = new THREE.MeshStandardMaterial({ color: 0xe8e2d4, roughness: 0.42, metalness: 0.22 });
      const gold = new THREE.MeshStandardMaterial({
        color: 0xc6a36a,
        roughness: 0.32,
        metalness: 0.72,
        emissive: 0x3a2a12,
        emissiveIntensity: 0.35,
      });
      const cyan = new THREE.MeshStandardMaterial({
        color: 0x3c9fbe,
        roughness: 0.28,
        metalness: 0.45,
        emissive: 0x0c3a48,
        emissiveIntensity: 0.8,
      });
      const dim = new THREE.MeshStandardMaterial({ color: 0x3a403c, roughness: 0.7, metalness: 0.08 });
      const hotMat = new THREE.MeshStandardMaterial({
        color: 0xd08b82,
        roughness: 0.4,
        metalness: 0.2,
        emissive: 0x000000,
      });
      const ink = new THREE.MeshStandardMaterial({ color: 0x102028, roughness: 0.5, metalness: 0.1 });
      const lineMat = new THREE.LineBasicMaterial({ color: 0xc6a36a });
      const creamLine = new THREE.LineBasicMaterial({ color: 0xeceae4 });
      const geos: BufferGeometry[] = [];
      const mats: Material[] = [bone, gold, cyan, dim, hotMat, ink, lineMat, creamLine];
      const movers: Mover[] = [];
      const orbits: Orbit[] = [];
      const track = (geo: BufferGeometry) => {
        geos.push(geo);
        return geo;
      };

      const placeSigil = (x: number, y: number, z: number, scale: number, hot: boolean, phase: number) => {
        const group = new THREE.Group();
        const ring = new THREE.Mesh(track(new THREE.TorusGeometry(1.52, 0.018, 8, 72)), bone);
        group.add(ring);
        const dot = track(new THREE.SphereGeometry(0.055, 12, 10));
        for (const [dx, dy] of [
          [0, 1.52],
          [1.52, 0],
          [0, -1.52],
          [-1.52, 0],
        ] as const) {
          const mark = new THREE.Mesh(dot, bone);
          mark.position.set(dx, dy, 0);
          group.add(mark);
        }
        const tri = new THREE.LineLoop(
          track(
            new THREE.BufferGeometry().setFromPoints([
              new THREE.Vector3(0, 0.98, 0.02),
              new THREE.Vector3(0.82, -0.5, 0.02),
              new THREE.Vector3(-0.82, -0.5, 0.02),
            ]),
          ),
          lineMat,
        );
        group.add(tri);
        const bar = track(new THREE.BoxGeometry(0.16, 0.92, 0.08));
        const stem = new THREE.Mesh(bar, gold);
        stem.position.set(-0.28, 0.08, 0.06);
        group.add(stem);
        const footGeo = track(new THREE.BoxGeometry(0.46, 0.16, 0.08));
        const upright = new THREE.Mesh(bar, gold);
        upright.position.set(0.22, 0.18, 0.06);
        const foot = new THREE.Mesh(footGeo, gold);
        foot.position.set(0.37, -0.2, 0.06);
        group.add(upright, foot);
        const nucleus = new THREE.Mesh(track(new THREE.SphereGeometry(0.16, 24, 16)), gold);
        const pupil = new THREE.Mesh(track(new THREE.SphereGeometry(0.07, 16, 12)), ink);
        pupil.position.z = 0.1;
        group.add(nucleus, pupil);
        const tilts = [-0.42, 0.6, 1.4];
        const speeds = [0.35, -0.22, 0.16];
        tilts.forEach((tilt, i) => {
          const orbit = new THREE.Mesh(track(new THREE.TorusGeometry(1.05 - i * 0.08, 0.012, 6, 80)), cyan);
          orbit.scale.set(1.15, 0.42, 1);
          orbit.rotation.x = 0.55 + i * 0.35;
          orbit.rotation.z = tilt;
          group.add(orbit);
          orbits.push({ obj: orbit, base: tilt, speed: speeds[i] });
        });
        group.position.set(x, y, z);
        group.scale.setScalar(scale);
        scene3.add(group);
        movers.push({ obj: group, base: group.position.clone(), phase, hot, scale });
      };

      if (scene === "cluster") {
        placeSigil(0, 0, 0, 0.7, true, 0);
        for (let i = 0; i < 6; i++) {
          const a = (i / 6) * Math.PI * 2;
          placeSigil(Math.cos(a) * 2.15, (i % 2) * 0.35 - 0.1, Math.sin(a) * 2.15, 0.32, i === 3, i);
        }
      } else if (scene === "pipeline") {
        for (let i = 0; i < 4; i++) placeSigil(-2.25 + i * 1.5, 0, 0, 0.42, i === 2, i);
        const packet = new THREE.Mesh(track(new THREE.SphereGeometry(0.12, 16, 12)), hotMat);
        packet.position.set(-2.4, 0.7, 0.35);
        scene3.add(packet);
        movers.push({ obj: packet, base: packet.position.clone(), phase: 99, hot: true, scale: 1 });
      } else if (scene === "packets") {
        placeSigil(0, 0, 0, 0.85, true, 0);
        const speck = track(new THREE.SphereGeometry(0.06, 10, 8));
        for (let i = 0; i < 28; i++) {
          const mesh = new THREE.Mesh(speck, i % 7 === 0 ? hotMat : i % 2 === 0 ? gold : dim);
          const a = i * 0.7;
          const rad = 1.15 + (i % 4) * 0.38;
          mesh.position.set(Math.cos(a) * rad, ((i % 5) - 2) * 0.22, Math.sin(a) * rad * 0.55);
          scene3.add(mesh);
          movers.push({ obj: mesh, base: mesh.position.clone(), phase: i * 0.2, hot: i % 7 === 0, scale: 1 });
        }
      } else if (scene === "cloud") {
        placeSigil(0, 0, 0, 0.72, true, 0);
        const slab = track(new THREE.TorusGeometry(1.7, 0.015, 6, 64));
        for (let i = 0; i < 3; i++) {
          const mesh = new THREE.Mesh(slab, i === 1 ? cyan : dim);
          mesh.rotation.x = Math.PI / 2.2;
          mesh.position.y = i * 0.7 - 0.7;
          scene3.add(mesh);
          orbits.push({ obj: mesh, base: mesh.rotation.z, speed: 0.12 * (i % 2 === 0 ? 1 : -1) });
          movers.push({ obj: mesh, base: mesh.position.clone(), phase: i, hot: i === 2, scale: 1 });
        }
      } else if (scene === "nodes") {
        placeSigil(0, 0, 0, 0.62, false, 0);
        const sph = track(new THREE.SphereGeometry(0.14, 16, 12));
        for (let i = 0; i < 6; i++) {
          const a = (i / 6) * Math.PI * 2;
          const mesh = new THREE.Mesh(sph, i === 4 ? hotMat : gold);
          mesh.position.set(Math.cos(a) * 1.85, Math.sin(i) * 0.28, Math.sin(a) * 1.85);
          scene3.add(mesh);
          movers.push({ obj: mesh, base: mesh.position.clone(), phase: i, hot: i === 4, scale: 1 });
          const g = track(new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(0, 0, 0), mesh.position.clone()]));
          scene3.add(new THREE.Line(g, creamLine));
        }
      } else if (scene === "detector") {
        placeSigil(0, 0, 0, 1.05, true, 0);
        const scan = new THREE.Mesh(track(new THREE.TorusGeometry(2.05, 0.02, 8, 80)), hotMat);
        scan.rotation.x = 1.15;
        scene3.add(scan);
        orbits.push({ obj: scan, base: 0, speed: 0.45 });
      } else {
        placeSigil(0, 0, 0, scene === "monas" ? 1.25 : 1.1, true, 0);
        if (scene === "lattice") {
          const cell = track(new THREE.SphereGeometry(0.08, 10, 8));
          for (let i = 0; i < 8; i++) {
            const a = (i / 8) * Math.PI * 2;
            const mesh = new THREE.Mesh(cell, i % 2 === 0 ? dim : bone);
            mesh.position.set(Math.cos(a) * 2.3, (i % 3) * 0.35 - 0.3, Math.sin(a) * 2.3);
            scene3.add(mesh);
            movers.push({ obj: mesh, base: mesh.position.clone(), phase: i, hot: false, scale: 1 });
          }
        }
      }

      let yaw = 0.5;
      let pitch = 0.38;
      let dragging = false;
      let lx = 0;
      let ly = 0;
      const down = (e: PointerEvent) => {
        dragging = true;
        lx = e.clientX;
        ly = e.clientY;
        el.setPointerCapture(e.pointerId);
      };
      const move = (e: PointerEvent) => {
        if (!dragging) return;
        yaw += (e.clientX - lx) * 0.007;
        pitch = Math.max(0.05, Math.min(1.15, pitch + (e.clientY - ly) * 0.005));
        lx = e.clientX;
        ly = e.clientY;
      };
      const up = () => {
        dragging = false;
      };
      el.addEventListener("pointerdown", down);
      el.addEventListener("pointermove", move);
      el.addEventListener("pointerup", up);
      el.addEventListener("pointercancel", up);

      let frame = 0;
      const tick = (t: number) => {
        frame = requestAnimationFrame(tick);
        const s = signalRef.current;
        const holdNow = holdRef.current;
        if (!reduced && !dragging) yaw += 0.003;
        const radius = scene === "pipeline" || scene === "cluster" ? 7.4 : 5.6;
        camera.position.set(Math.sin(yaw) * radius, 1.1 + pitch * 2.1, Math.cos(yaw) * radius);
        camera.lookAt(0, 0.05, 0);
        const time = t * 0.001;
        hotMat.emissive.setHex(holdNow == null ? 0x000000 : 0x3a221c);
        if (!reduced) {
          for (const o of orbits) o.obj.rotation.z = o.base + time * o.speed * (0.65 + s);
        }
        for (const m of movers) {
          if (m.phase === 99) {
            const cap = holdNow == null ? 1 : Math.max(0.12, Math.min(0.9, holdNow));
            const travel = (time * (0.35 + s)) % 1;
            const along = holdNow == null ? travel : Math.min(travel, cap);
            m.obj.position.x = -2.4 + along * 4.8;
            m.obj.position.y = 0.7 + Math.sin(time * 3) * 0.08;
            m.obj.visible = holdNow == null ? s < 0.92 || travel < 0.62 : true;
            continue;
          }
          const spread = m.hot ? 0.15 + s * 0.85 : 0.04;
          const stall = holdNow == null ? 0 : holdNow;
          m.obj.position.x = m.base.x * (1 + (m.hot ? s * 0.35 + stall * 0.2 : 0));
          m.obj.position.y = m.base.y + Math.sin(time * 1.4 + m.phase) * spread * 0.25;
          m.obj.position.z = m.base.z * (1 + (m.hot ? s * 0.35 : 0));
          const sc = m.hot ? 1 + s * 0.28 + (holdNow == null ? 0 : 0.1) : 1;
          m.obj.scale.setScalar(m.scale * sc);
        }
        renderer.render(scene3, camera);
      };
      frame = requestAnimationFrame(tick);

      const resize = () => {
        const w = el.clientWidth || 320;
        const h = el.clientHeight || 280;
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
        renderer.setSize(w, h);
      };
      const ro = new ResizeObserver(resize);
      ro.observe(el);

      cleanup = () => {
        cancelAnimationFrame(frame);
        ro.disconnect();
        el.removeEventListener("pointerdown", down);
        el.removeEventListener("pointermove", move);
        el.removeEventListener("pointerup", up);
        el.removeEventListener("pointercancel", up);
        geos.forEach((g) => g.dispose());
        mats.forEach((m) => m.dispose());
        renderer.dispose();
        renderer.domElement.remove();
      };
    });

    return () => {
      disposed = true;
      cleanup();
    };
  }, [scene]);

  return (
    <figure className="overflow-hidden rounded-xl border border-line bg-surface">
      <div ref={host} className="stage-well relative h-72 w-full touch-none sm:h-96" aria-label={label}>
        <svg viewBox="0 0 64 64" className="pointer-events-none absolute top-1/2 left-1/2 size-44 -translate-x-1/2 -translate-y-1/2 opacity-50 sm:size-56" aria-hidden>
          <circle cx="32" cy="32" r="23" fill="none" stroke="#eceae4" strokeWidth="1.4" />
          <circle cx="32" cy="9" r="1.3" fill="#eceae4" />
          <circle cx="55" cy="32" r="1.3" fill="#eceae4" />
          <circle cx="32" cy="55" r="1.3" fill="#eceae4" />
          <circle cx="9" cy="32" r="1.3" fill="#eceae4" />
          <path d="M32 16.2 45.6 43.6H18.4Z" fill="none" stroke="#c6a36a" strokeWidth="1.4" />
          <rect x="22.6" y="21.6" width="4.6" height="21.4" fill="#c6a36a" />
          <path d="M35.2 21.6h4.6v15.2h8.6v4.4H35.2Z" fill="#c6a36a" />
          <g fill="none" stroke="#3c9fbe" strokeWidth="1.2">
            <ellipse cx="32" cy="33" rx="13.4" ry="5.3" transform="rotate(-24 32 33)" />
            <ellipse cx="32" cy="33" rx="12" ry="4.7" transform="rotate(34 32 33)" />
            <ellipse cx="32" cy="33" rx="10.6" ry="4.1" transform="rotate(80 32 33)" />
          </g>
          <circle cx="32" cy="33" r="3.2" fill="#c6a36a" />
          <circle cx="32" cy="33" r="1.4" fill="#102028" />
        </svg>
      </div>
      <figcaption className="border-t border-line px-4 py-3 text-sm text-muted">{label} Drag to orbit.</figcaption>
    </figure>
  );
}
