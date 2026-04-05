import React, { useEffect, useRef } from "react";
import * as THREE from "three";

export default function InfoPhyzx3DRenderer({ state }) {
  const mountRef = useRef(null);
  const sceneRef = useRef(null);
  const meshRef = useRef(null);
  const rendererRef = useRef(null);
  const cameraRef = useRef(null);

  useEffect(() => {
    const width = mountRef.current.clientWidth;
    const height = 300;

    const scene = new THREE.Scene();
    sceneRef.current = scene;

    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    camera.position.set(0, 20, 30);
    camera.lookAt(0, 0, 0);
    cameraRef.current = camera;

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(width, height);
    rendererRef.current = renderer;
    mountRef.current.appendChild(renderer.domElement);

    const light = new THREE.DirectionalLight(0xffffff, 1);
    light.position.set(10, 20, 10);
    scene.add(light);

    const grid = new THREE.GridHelper(20, 20);
    scene.add(grid);

    const geometry = new THREE.PlaneGeometry(20, 20, 20, 20);
    geometry.rotateX(-Math.PI / 2);
    const material = new THREE.MeshStandardMaterial({
      color: 0x3366ff,
      wireframe: false,
      side: THREE.DoubleSide
    });
    const mesh = new THREE.Mesh(geometry, material);
    meshRef.current = mesh;
    scene.add(mesh);

    const animate = () => {
      requestAnimationFrame(animate);
      renderer.render(scene, camera);
    };
    animate();

    return () => {
      mountRef.current.removeChild(renderer.domElement);
      renderer.dispose();
    };
  }, []);

  useEffect(() => {
    if (!state || !meshRef.current) return;

    const values = Object.values(state);
    if (!values.length) return;

    const geom = meshRef.current.geometry;
    const pos = geom.attributes.position;
    const count = pos.count;

    const min = Math.min(...values);
    const max = Math.max(...values);
    const range = max - min || 1;

    for (let i = 0; i < count; i++) {
      const v = values[i % values.length];
      const t = (v - min) / range;
      pos.setY(i, t * 5.0); // height scale
    }
    pos.needsUpdate = true;
    geom.computeVertexNormals();
  }, [state]);

  return (
    <div
      ref={mountRef}
      style={{ width: "100%", height: "300px", marginTop: "20px" }}
    />
  );
}
