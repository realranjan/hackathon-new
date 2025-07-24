
import React, { useRef, useEffect, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Html } from '@react-three/drei';
import * as THREE from 'three';

// Mock supply chain data with 3D coordinates
const supplyChainData = [
  {
    id: 'rotterdam',
    name: 'Rotterdam Port',
    country: 'Netherlands',
    position: [0.08, 0.91, 0.4] as [number, number, number], // 3D position on sphere
    status: 'disrupted',
    risk: 'high',
    shipments: 156,
    description: 'Port Strike Active - 48 hours'
  },
  {
    id: 'hongkong',
    name: 'Hong Kong Port',
    country: 'China',
    position: [2.0, 0.4, -0.9] as [number, number, number],
    status: 'operational',
    risk: 'medium',
    shipments: 234,
    description: 'Weather Warning - Typhoon approaching'
  },
  {
    id: 'losangeles',
    name: 'Port of Los Angeles',
    country: 'USA',
    position: [-2.0, 0.6, 0.2] as [number, number, number],
    status: 'operational',
    risk: 'low',
    shipments: 189,
    description: 'Normal Operations'
  },
  {
    id: 'singapore',
    name: 'Singapore Port',
    country: 'Singapore',
    position: [1.8, 0.1, -0.8] as [number, number, number],
    status: 'warning',
    risk: 'medium',
    shipments: 167,
    description: 'Container Backlog'
  },
  {
    id: 'dubai',
    name: 'Jebel Ali Port',
    country: 'UAE',
    position: [1.0, 0.5, -0.3] as [number, number, number],
    status: 'operational',
    risk: 'low',
    shipments: 134,
    description: 'Optimal Conditions'
  }
];

const statusColors = {
  operational: '#22c55e',
  warning: '#f59e0b',
  disrupted: '#ef4444'
};

// Simplified Supply Chain Point Component
const SupplyPoint = ({ data, onClick }: { data: any, onClick: (data: any) => void }) => {
  const meshRef = useRef<THREE.Mesh>(null);
  const [hovered, setHovered] = useState(false);

  useFrame(() => {
    if (meshRef.current) {
      meshRef.current.scale.setScalar(hovered ? 1.2 : 1);
      meshRef.current.rotation.y += 0.01;
    }
  });

  const color = statusColors[data.status as keyof typeof statusColors];

  return (
    <group position={data.position}>
      <mesh
        ref={meshRef}
        onClick={() => onClick(data)}
        onPointerOver={() => setHovered(true)}
        onPointerOut={() => setHovered(false)}
      >
        <sphereGeometry args={[0.05, 16, 16]} />
        <meshStandardMaterial 
          color={color} 
          emissive={color}
          emissiveIntensity={0.3}
        />
      </mesh>
      
      {/* Pulsing ring effect */}
      <mesh>
        <ringGeometry args={[0.08, 0.12, 32]} />
        <meshBasicMaterial 
          color={color} 
          transparent 
          opacity={0.3}
          side={THREE.DoubleSide}
        />
      </mesh>
      
      {hovered && (
        <Html distanceFactor={10} position={[0, 0.15, 0]}>
          <div className="bg-background/90 backdrop-blur-sm rounded-lg p-3 text-xs whitespace-nowrap border border-border shadow-lg">
            <div className="font-semibold text-foreground">{data.name}</div>
            <div className="text-muted-foreground">{data.country}</div>
            <div className="flex items-center space-x-2 mt-1">
              <div 
                className="w-2 h-2 rounded-full" 
                style={{ backgroundColor: color }}
              />
              <span className="text-xs">{data.shipments} shipments</span>
            </div>
            <div className="text-xs text-muted-foreground mt-1">{data.description}</div>
          </div>
        </Html>
      )}
    </group>
  );
};

// Earth Globe Component
const EarthGlobe = ({ onPointClick }: { onPointClick: (data: any) => void }) => {
  const earthRef = useRef<THREE.Mesh>(null);
  const cloudsRef = useRef<THREE.Mesh>(null);

  useFrame(() => {
    if (earthRef.current) {
      earthRef.current.rotation.y += 0.002;
    }
    if (cloudsRef.current) {
      cloudsRef.current.rotation.y += 0.003;
    }
  });

  return (
    <group>
      {/* Earth Sphere */}
      <mesh ref={earthRef}>
        <sphereGeometry args={[2, 64, 64]} />
        <meshStandardMaterial 
          color="#1e40af"
          roughness={0.8}
          metalness={0.1}
        />
      </mesh>
      
      {/* Cloud Layer */}
      <mesh ref={cloudsRef}>
        <sphereGeometry args={[2.05, 64, 64]} />
        <meshStandardMaterial 
          color="#ffffff"
          transparent
          opacity={0.1}
          roughness={1}
        />
      </mesh>
      
      {/* Supply Chain Points */}
      {supplyChainData.map((point) => (
        <SupplyPoint 
          key={point.id} 
          data={point} 
          onClick={onPointClick}
        />
      ))}
    </group>
  );
};

const Globe3D = ({ onPointClick }: { onPointClick: (data: any) => void }) => {
  return (
    <div className="w-full h-full">
      <Canvas camera={{ position: [0, 0, 5], fov: 75 }}>
        {/* Lighting */}
        <ambientLight intensity={0.4} />
        <directionalLight position={[5, 5, 5]} intensity={1} />
        <pointLight position={[-5, -5, -5]} intensity={0.5} />
        
        {/* Earth and Supply Chain */}
        <EarthGlobe onPointClick={onPointClick} />
        
        {/* Controls */}
        <OrbitControls 
          enableZoom={true}
          enablePan={false}
          enableRotate={true}
          autoRotate={true}
          autoRotateSpeed={0.5}
        />
      </Canvas>
    </div>
  );
};

export default Globe3D;
