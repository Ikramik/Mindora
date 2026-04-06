import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { useRef } from 'react';
import * as THREE from 'three';

//Temporary 3D object
function PlaceholderBrain() {
  const meshRef = useRef<THREE.Mesh>(null!);

// This hook runs on every frame, rotating the mesh slowly
  useFrame(() => {
    if (meshRef.current) {
      meshRef.current.rotation.x += 0.01;
      meshRef.current.rotation.y += 0.01;
    }
  });
  return (
    <mesh ref={meshRef}>
      <boxGeometry args={[2, 2, 2]}/>
      <meshStandardMaterial color="#5a0a0a" wireframe={true} />
    </mesh>
  );
}

function App() {
  return (
    // The Canvas needs a fixed height to show up on the screen
    <div style={{ height: '100vh', width: '100vw', backgroundColor: '#ffffff'}}>
    <Canvas> 
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 10]} intensity={1} />
      <PlaceholderBrain />
      <OrbitControls />
    </Canvas>
    </div>
  );
}
export default App;