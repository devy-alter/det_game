import { useEffect, useRef } from "react";
import * as THREE from "three";

function moodFor(confidence, pressure) {
  if (pressure === "critical" || confidence <= 18) return "breaking";
  if (pressure === "high" || confidence <= 42) return "tense";
  if (pressure === "medium" || confidence <= 68) return "uneasy";
  if (pressure === "thinking") return "thinking";
  if (pressure === "answering") return "alert";
  return "composed";
}

function mat(color, roughness = 0.65, metalness = 0) {
  return new THREE.MeshStandardMaterial({ color, roughness, metalness });
}

function roundedShape(width, height, depth, radius = 0.12) {
  const shape = new THREE.Shape();
  const x = -width / 2;
  const y = -height / 2;
  shape.moveTo(x + radius, y);
  shape.lineTo(x + width - radius, y);
  shape.quadraticCurveTo(x + width, y, x + width, y + radius);
  shape.lineTo(x + width, y + height - radius);
  shape.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
  shape.lineTo(x + radius, y + height);
  shape.quadraticCurveTo(x, y + height, x, y + height - radius);
  shape.lineTo(x, y + radius);
  shape.quadraticCurveTo(x, y, x + radius, y);
  const geometry = new THREE.ExtrudeGeometry(shape, { depth, bevelEnabled: true, bevelSegments: 3, bevelSize: radius * .35, bevelThickness: radius * .35 });
  geometry.center();
  return geometry;
}

function createCharacter(scene) {
  const root = new THREE.Group();
  root.position.set(0, -1.55, 0);
  scene.add(root);

  const chair = new THREE.Mesh(new THREE.CylinderGeometry(1.3, 1.45, .16, 32), mat(0x16110e, .95));
  chair.position.set(0, .15, -.15);
  chair.scale.z = .7;
  root.add(chair);

  const torso = new THREE.Group();
  torso.position.y = 1.25;
  root.add(torso);
  const jacket = new THREE.Mesh(new THREE.CapsuleGeometry(.86, 1.7, 6, 18), mat(0x1b1a18, .88));
  jacket.scale.set(1, 1, .72);
  torso.add(jacket);

  const shirt = new THREE.Mesh(roundedShape(.82, 1.2, .14, .09), mat(0xd7d0c4, .8));
  shirt.position.set(0, .47, .62);
  shirt.rotation.z = Math.PI;
  torso.add(shirt);

  const tie = new THREE.Mesh(new THREE.BoxGeometry(.12, .72, .06), mat(0x29211e, .6));
  tie.position.set(0, .2, .71);
  torso.add(tie);

  const armL = new THREE.Group();
  const armR = new THREE.Group();
  armL.position.set(-.72, .85, .06); armR.position.set(.72, .85, .06);
  torso.add(armL, armR);
  const armGeo = new THREE.CapsuleGeometry(.19, .95, 5, 10);
  const armLMesh = new THREE.Mesh(armGeo, mat(0x1b1a18, .88));
  const armRMesh = armLMesh.clone();
  armL.add(armLMesh); armR.add(armRMesh);
  const handGeo = new THREE.SphereGeometry(.16, 12, 8);
  const handL = new THREE.Mesh(handGeo, mat(0xa36d56, .9));
  const handR = handL.clone();
  handL.position.set(0, -.66, .03); handR.position.set(0, -.66, .03);
  armL.add(handL); armR.add(handR);

  const neck = new THREE.Mesh(new THREE.CylinderGeometry(.22, .25, .42, 16), mat(0xa36d56, .92));
  neck.position.set(0, 2.16, 0);
  root.add(neck);

  const head = new THREE.Group();
  head.position.set(0, 3.05, .02);
  root.add(head);
  const skin = mat(0xb77b60, .92);
  const face = new THREE.Mesh(new THREE.SphereGeometry(.83, 28, 22), skin);
  face.scale.set(.84, 1, .78);
  head.add(face);
  const earGeo = new THREE.SphereGeometry(.14, 12, 8);
  const earL = new THREE.Mesh(earGeo, skin); const earR = earL.clone();
  earL.position.set(-.72, .04, -.02); earR.position.set(.72, .04, -.02); head.add(earL, earR);

  const hair = new THREE.Mesh(new THREE.SphereGeometry(.87, 24, 16, 0, Math.PI * 2, 0, Math.PI * .56), mat(0x171312, .95));
  hair.scale.set(.95, .78, .88); hair.position.y = .38; head.add(hair);

  const eyeWhite = mat(0xe8e2db, .45);
  const pupilMat = mat(0x161311, .4);
  const eyeL = new THREE.Mesh(new THREE.SphereGeometry(.13, 16, 10), eyeWhite);
  const eyeR = eyeL.clone(); eyeL.position.set(-.28, .08, .72); eyeR.position.set(.28, .08, .72);
  head.add(eyeL, eyeR);
  const pupilL = new THREE.Mesh(new THREE.SphereGeometry(.055, 10, 8), pupilMat);
  const pupilR = pupilL.clone(); pupilL.position.set(-.28, .08, .82); pupilR.position.set(.28, .08, .82); head.add(pupilL, pupilR);

  const browL = new THREE.Mesh(new THREE.BoxGeometry(.29, .055, .08), mat(0x34211c, .95));
  const browR = browL.clone(); browL.position.set(-.29, .28, .71); browR.position.set(.29, .28, .71); head.add(browL, browR);

  const nose = new THREE.Mesh(new THREE.SphereGeometry(.11, 12, 8), skin);
  nose.scale.set(.8, 1.2, 1.1); nose.position.set(0, -.02, .79); head.add(nose);
  const mouth = new THREE.Group(); mouth.position.set(0, -.34, .72); head.add(mouth);
  const lipTop = new THREE.Mesh(new THREE.BoxGeometry(.24, .035, .045), mat(0x6b3832, .8));
  const lipBottom = new THREE.Mesh(new THREE.BoxGeometry(.20, .035, .045), mat(0x7a443b, .8));
  lipTop.position.y = .025; lipBottom.position.y = -.025; mouth.add(lipTop, lipBottom);

  return { root, torso, armL, armR, head, eyeL, eyeR, pupilL, pupilR, browL, browR, mouth, key: null };
}

export default function SuspectPresence({ confidence, pressure = "low", name }) {
  const mountRef = useRef(null);
  const stateRef = useRef(moodFor(confidence, pressure));
  const mood = moodFor(confidence, pressure);
  stateRef.current = mood;

  useEffect(() => {
    const mount = mountRef.current;
    if (!mount) return undefined;
    let renderer;
    try { renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true }); } catch {
      mount.innerHTML = '<div class="threeFallback">3D VIEW UNAVAILABLE<br/>ENABLE WEBGL TO VIEW SUBJECT</div>';
      return undefined;
    }

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(30, Math.max(1, mount.clientWidth) / Math.max(1, mount.clientHeight), .1, 100);
    camera.position.set(0, 1.55, 8.5); camera.lookAt(0, 1.8, 0);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.8));
    renderer.setSize(mount.clientWidth, mount.clientHeight, false);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    mount.appendChild(renderer.domElement);

    scene.add(new THREE.HemisphereLight(0x9e7659, 0x080706, 1.1));
    const key = new THREE.SpotLight(0xffd1a1, 24, 16, Math.PI / 5.5, .75, 1.5);
    key.position.set(-2.1, 6.5, 3.2); key.castShadow = true; scene.add(key);
    const fill = new THREE.PointLight(0x7a3b22, 5.5, 9); fill.position.set(2.8, 3.5, -2); scene.add(fill);

    const floor = new THREE.Mesh(new THREE.PlaneGeometry(14, 10), mat(0x070605, 1));
    floor.rotation.x = -Math.PI / 2; floor.position.y = 0; floor.receiveShadow = true; scene.add(floor);

    const model = createCharacter(scene); model.key = key;
    const clock = new THREE.Clock();
    let raf = 0;
    let lastBlink = 0;

    const animate = () => {
      raf = requestAnimationFrame(animate);
      const t = clock.getElapsedTime();
      const current = stateRef.current;
      const nervous = current === "tense" || current === "breaking";
      const alert = current === "alert" || current === "thinking";
      const headTilt = current === "breaking" ? .13 : current === "tense" ? .075 : current === "uneasy" ? .04 : current === "thinking" ? -.07 : 0;
      const headTurn = current === "thinking" ? -.12 : current === "breaking" ? .05 : 0;
      model.head.rotation.z = THREE.MathUtils.lerp(model.head.rotation.z, headTilt, .08);
      model.head.rotation.y = THREE.MathUtils.lerp(model.head.rotation.y, headTurn, .08);
      model.torso.rotation.z = THREE.MathUtils.lerp(model.torso.rotation.z, nervous ? .02 : 0, .06);
      model.torso.position.x = Math.sin(t * 2.1) * (nervous ? .018 : .005);
      model.armL.rotation.z = THREE.MathUtils.lerp(model.armL.rotation.z, nervous ? -.035 : alert ? -.015 : 0, .06);
      model.armR.rotation.z = THREE.MathUtils.lerp(model.armR.rotation.z, nervous ? .035 : alert ? .015 : 0, .06);
      const breath = 1 + Math.sin(t * 1.7) * (current === "breaking" ? .018 : nervous ? .011 : .006);
      model.torso.scale.y = THREE.MathUtils.lerp(model.torso.scale.y, breath, .08);
      const brow = current === "breaking" ? .12 : current === "tense" ? .07 : current === "uneasy" ? .035 : current === "thinking" ? .02 : 0;
      model.browL.rotation.z = THREE.MathUtils.lerp(model.browL.rotation.z, -brow, .08);
      model.browR.rotation.z = THREE.MathUtils.lerp(model.browR.rotation.z, brow, .08);
      const pupilX = current === "thinking" ? -.035 : current === "breaking" ? .025 : Math.sin(t * .6) * .018;
      model.pupilL.position.x = THREE.MathUtils.lerp(model.pupilL.position.x, -.28 + pupilX, .1);
      model.pupilR.position.x = THREE.MathUtils.lerp(model.pupilR.position.x, .28 + pupilX, .1);
      if (t - lastBlink > 2.1 + Math.random() * 2) { lastBlink = t; }
      const blinkProgress = t - lastBlink;
      const blink = blinkProgress < .12 ? Math.sin((blinkProgress / .12) * Math.PI) : 0;
      const eyeScale = 1 - blink * .92;
      model.eyeL.scale.y = eyeScale; model.eyeR.scale.y = eyeScale;
      model.pupilL.scale.y = eyeScale; model.pupilR.scale.y = eyeScale;
      const mouthY = current === "breaking" ? -.01 : current === "tense" ? -.003 : 0;
      model.mouth.scale.y = THREE.MathUtils.lerp(model.mouth.scale.y, 1 + mouthY * -10, .08);
      key.intensity = THREE.MathUtils.lerp(key.intensity, current === "breaking" ? 13 : current === "tense" ? 17 : 23, .05);
      renderer.render(scene, camera);
    };
    animate();

    const resize = () => {
      const w = Math.max(1, mount.clientWidth), h = Math.max(1, mount.clientHeight);
      camera.aspect = w / h; camera.updateProjectionMatrix(); renderer.setSize(w, h, false);
    };
    const ro = new ResizeObserver(resize); ro.observe(mount); resize();

    return () => {
      cancelAnimationFrame(raf); ro.disconnect(); renderer.dispose();
      scene.traverse((obj) => { if (obj.geometry) obj.geometry.dispose(); if (obj.material) Array.isArray(obj.material) ? obj.material.forEach((m) => m.dispose()) : obj.material.dispose(); });
      if (renderer.domElement.parentNode === mount) mount.removeChild(renderer.domElement);
    };
  }, []);

  return (
    <aside className="suspectStage">
      <div className="suspectLabel"><span>SUBJECT</span><b>{name || "UNKNOWN"}</b></div>
      <div className="threeStage" ref={mountRef} />
      <div className="suspectReadout"><div><span>COMPOSURE</span><b>{confidence}%</b></div><div><span>BEHAVIOUR</span><b>{mood.toUpperCase()}</b></div></div>
    </aside>
  );
}
