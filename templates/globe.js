const scene = new THREE.Scene();

// Create a camera
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 5;

// Create a WebGL renderer
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById('globe-container').appendChild(renderer.domElement);

// Create a globe
const geometry = new THREE.SphereGeometry(2, 32, 32);
const texture = new THREE.TextureLoader().load('path/to/your/globe/texture.jpg');
const material = new THREE.MeshBasicMaterial({ map: texture });
const globe = new THREE.Mesh(geometry, material);
scene.add(globe);

// Function to add static markers
function addStaticMarker(location) {
    const marker = new THREE.Mesh(new THREE.SphereGeometry(0.03, 8, 8), new THREE.MeshBasicMaterial({ color: 0x00ff00 }));
    marker.position.set(location.x, location.y, location.z);
    scene.add(marker);
}

// Add static markers for demonstration purposes
addStaticMarker({ x: 0.5, y: 0.2, z: 2 }); // Example marker 1
addStaticMarker({ x: -0.5, y: -0.2, z: 2 }); // Example marker 2

// Function to animate the globe
function animate() {
    requestAnimationFrame(animate);
    globe.rotation.y += 0.005;
    renderer.render(scene, camera);
}
animate();