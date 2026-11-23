import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.180.0/build/three.module.js";

const canvas = document.querySelector("#authvanta3DLock");
if (!canvas) throw new Error("AUTHVANTA 3D canvas not found");

const scene = new THREE.Scene();
scene.background = null;

const camera = new THREE.PerspectiveCamera(35, 1, 0.1, 100);
camera.position.set(4.5, 3.8, 8);
camera.lookAt(0, 0.20, 0);

const renderer = new THREE.WebGLRenderer({
    canvas,
    alpha: true,
    antialias: true
});
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.35;

const lock = new THREE.Group();
lock.scale.setScalar(0.88);
scene.add(lock);

/* LIGHTING */
scene.add(new THREE.AmbientLight(0xffffff, 1.8));

const keyLight = new THREE.DirectionalLight(0xffe0bb, 2.5);
keyLight.position.set(-4, 7, 6);
keyLight.castShadow = true;
keyLight.shadow.mapSize.set(2048, 2048);
keyLight.shadow.camera.left = -5;
keyLight.shadow.camera.right = 5;
keyLight.shadow.camera.top = 5;
keyLight.shadow.camera.bottom = -5;
scene.add(keyLight);

const fillLight = new THREE.PointLight(0xffbd78, 18, 12);
fillLight.position.set(4, 2, 4);
scene.add(fillLight);

const rimLight = new THREE.PointLight(0xffd4a0, 14, 10);
rimLight.position.set(-4, 3, -2);
scene.add(rimLight);

/* MATERIALS */
const orangeMetal = new THREE.MeshPhysicalMaterial({
    color: 0xf08a16,
    metalness: 0.72,
    roughness: 0.24,
    clearcoat: 1,
    clearcoatRoughness: 0.16
});

const goldMetal = new THREE.MeshPhysicalMaterial({
    color: 0xe7a84e,
    metalness: 0.88,
    roughness: 0.2,
    clearcoat: 1
});

const darkMetal = new THREE.MeshStandardMaterial({
    color: 0x8e4808,
    metalness: 0.8,
    roughness: 0.3
});

const platformMaterial = new THREE.MeshStandardMaterial({
    color: 0xf4dfc3,
    metalness: 0.12,
    roughness: 0.58
});

/* BEVELLED LOCK BODY */
function roundedShape(width, height, radius) {
    const s = new THREE.Shape();
    const x = -width / 2;
    const y = -height / 2;

    s.moveTo(x + radius, y);
    s.lineTo(x + width - radius, y);
    s.quadraticCurveTo(x + width, y, x + width, y + radius);
    s.lineTo(x + width, y + height - radius);
    s.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
    s.lineTo(x + radius, y + height);
    s.quadraticCurveTo(x, y + height, x, y + height - radius);
    s.lineTo(x, y + radius);
    s.quadraticCurveTo(x, y, x + radius, y);
    return s;
}

const bodyGeometry = new THREE.ExtrudeGeometry(
    roundedShape(2.15, 1.85, 0.2),
    {
        depth: 0.65,
        bevelEnabled: true,
        bevelSegments: 5,
        steps: 1,
        bevelSize: 0.09,
        bevelThickness: 0.09,
        curveSegments: 16
    }
);

bodyGeometry.center();

const body = new THREE.Mesh(bodyGeometry, orangeMetal);
body.position.set(0, -0.45, 0.15);
body.castShadow = true;
body.receiveShadow = true;
lock.add(body);

/* METALLIC SIDE PANEL */
const sideGeometry = new THREE.BoxGeometry(0.035, 1.45, 0.035);
const side = new THREE.Mesh(sideGeometry, goldMetal);
side.position.set(1.05, -0.45, 0.49);
lock.add(side);

/* CURVED METALLIC SHACKLE - DEPTH CENTRED */
/* CURVED METALLIC SHACKLE */
const shacklePoints = [
    new THREE.Vector3(-0.72, 0.35, 0.15),
    new THREE.Vector3(-0.72, 1.15, 0.15),
    new THREE.Vector3(-0.67, 1.75, 0.15),
    new THREE.Vector3(-0.38, 2.05, 0.15),
    new THREE.Vector3(0, 2.13, 0.15),
    new THREE.Vector3(0.38, 2.05, 0.15),
    new THREE.Vector3(0.67, 1.75, 0.15),
    new THREE.Vector3(0.72, 1.15, 0.15),
    new THREE.Vector3(0.72, 0.35, 0.15)
];

const shackleCurve = new THREE.CatmullRomCurve3(shacklePoints);
const shackleGeometry = new THREE.TubeGeometry(shackleCurve, 100, 0.115, 24, false);

const shackle = new THREE.Mesh(shackleGeometry, goldMetal);
shackle.castShadow = true;
lock.add(shackle);

/* INNER SHACKLE HIGHLIGHT */
const innerPoints = shacklePoints.map(p =>
    new THREE.Vector3(p.x, p.y, p.z + 0.025)
);
const innerCurve = new THREE.CatmullRomCurve3(innerPoints);
const innerGeometry = new THREE.TubeGeometry(innerCurve, 100, 0.018, 8, false);

const innerShine = new THREE.Mesh(
    innerGeometry,
    new THREE.MeshBasicMaterial({ color: 0xffe0a3 })
);
lock.add(innerShine);

/* KEYHOLE */
const keyholeMaterial = new THREE.MeshPhysicalMaterial({
    color: 0x75400d,
    metalness: 0.8,
    roughness: 0.2
});

const keyCircle = new THREE.Mesh(
    new THREE.CylinderGeometry(0.19, 0.19, 0.055, 48),
    goldMetal
);
keyCircle.rotation.x = Math.PI / 2;
keyCircle.position.set(0, -0.35, 0.55);
lock.add(keyCircle);

const keyStem = new THREE.Mesh(
    new THREE.CylinderGeometry(0.065, 0.085, 0.38, 32),
    keyholeMaterial
);
keyStem.position.set(0, -0.59, 0.59);
lock.add(keyStem);

const keyTip = new THREE.Mesh(
    new THREE.SphereGeometry(0.085, 24, 24),
    keyholeMaterial
);
keyTip.scale.set(1, 0.65, 0.5);
keyTip.position.set(0, -0.78, 0.59);
lock.add(keyTip);

/* FLOATING ISOMETRIC PLATFORM */
const platformGeometry = new THREE.BoxGeometry(4.4, 0.24, 3.3);
const platform = new THREE.Mesh(platformGeometry, platformMaterial);
platform.position.set(0, -1.55, 0);
platform.rotation.y = -0.12;
platform.castShadow = true;
platform.receiveShadow = true;
lock.add(platform);

/* PLATFORM EDGE */
const edge = new THREE.Mesh(
    new THREE.BoxGeometry(4.43, 0.07, 3.33),
    goldMetal
);
edge.position.set(0, -1.69, 0);
edge.rotation.y = -0.12;
lock.add(edge);

/* PLATFORM DOTS REMOVED */

/* FLOATING PARTICLES REMOVED */
/* AMBER SECURITY AURA — SOFT GLOWING CIRCLES */
const glowCanvas = document.createElement("canvas");
glowCanvas.width = 128;
glowCanvas.height = 128;

const glowContext = glowCanvas.getContext("2d");
const glowGradient = glowContext.createRadialGradient(64, 64, 2, 64, 64, 62);

glowGradient.addColorStop(0, "rgba(255, 205, 115, 1)");
glowGradient.addColorStop(0.16, "rgba(255, 157, 40, 0.85)");
glowGradient.addColorStop(0.42, "rgba(255, 145, 25, 0.35)");
glowGradient.addColorStop(1, "rgba(255, 145, 25, 0)");

glowContext.fillStyle = glowGradient;
glowContext.fillRect(0, 0, 128, 128);

const glowTexture = new THREE.CanvasTexture(glowCanvas);

const glowGroup = new THREE.Group();
lock.add(glowGroup);



for (let i = 0; i < 26; i++) {
    const angle = (i / 26) * Math.PI * 2;
    const radius = 1.65 + Math.random() * 0.55;

    const material = new THREE.SpriteMaterial({
        map: glowTexture,
        color: i % 3 === 0 ? 0xffbd63 : 0xffa12b,
        transparent: true,
        opacity: 0.12 + Math.random() * 0.08,
        blending: THREE.AdditiveBlending,
        depthWrite: false,
        depthTest: false
    });

    const sprite = new THREE.Sprite(material);
    const size = 0.07 + Math.random() * 0.05;

    sprite.scale.set(size, size, 1);
    sprite.position.set(
        Math.cos(angle) * radius,
        0.45 + Math.sin(angle) * 1.35,
        0.65 + Math.random() * 0.35
    );

    glowGroup.add(sprite);
}

/* A few larger, subtle ambient glow circles */
for (let i = 0; i < 5; i++) {
    const material = new THREE.SpriteMaterial({
        map: glowTexture,
        color: 0xffa12b,
        transparent: true,
        opacity: 0.12,
        blending: THREE.AdditiveBlending,
        depthWrite: false,
        depthTest: false
    });

    const sprite = new THREE.Sprite(material);
    sprite.scale.set(0.65, 0.65, 1);

    const angle = (i / 5) * Math.PI * 2;
    sprite.position.set(
        Math.cos(angle) * 2.05,
        0.35 + Math.sin(angle) * 1.6,
        0.1
    );

    glowGroup.add(sprite);
}


/* FLOOR SHADOW REMOVED: prevents oversized hard shadow */

/* THEME SUPPORT */
function updateTheme() {
    const dark = document.documentElement.dataset.theme === "dark";

    platformMaterial.color.set(dark ? 0x33271a : 0xf3d6ad);
    scene.fog = new THREE.Fog(
        dark ? 0x191713 : 0xfaf7f1,
        12,
        24
    );
    keyLight.intensity = dark ? 3.3 : 4;
    fillLight.intensity = dark ? 55 : 45;
}

updateTheme();

const observer = new MutationObserver(updateTheme);
observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ["data-theme"]
});


/* SECURITY SHIELD REMOVED */
/* RESPONSIVE RENDERING */
function resize() {
    const width = canvas.clientWidth;
    const height = canvas.clientHeight;
    if (!width || !height) return;

    camera.aspect = width / height;
    camera.position.x = width < 450 ? 4.5 : 4.5;
    camera.position.y = width < 450 ? 3.8 : 3.8;
    camera.lookAt(0, 0.20, 0);
    camera.updateProjectionMatrix();
    renderer.setSize(width, height, false);
}

const resizeObserver = new ResizeObserver(resize);
resizeObserver.observe(canvas);
resize();

/* ANIMATION */
const clock = new THREE.Clock();

function animate() {
    requestAnimationFrame(animate);

    const t = clock.getElapsedTime();
    lock.position.y = Math.sin(t * 0.65) * 0.045;

    /* Smooth, slow rotation of the complete lock assembly */
    lock.rotation.y = Math.sin(t * 0.35) * (Math.PI / 2);
    lock.rotation.x = 0;
    lock.rotation.z = 0;

    renderer.render(scene, camera);
}

animate();















