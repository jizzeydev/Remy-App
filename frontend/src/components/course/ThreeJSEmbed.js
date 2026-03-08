import { useRef, useState, Suspense } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Grid, Text } from '@react-three/drei';
import * as THREE from 'three';

// Rotating mesh component
const RotatingMesh = ({ geometry, color = '#0891b2', wireframe = false, rotation = true }) => {
  const meshRef = useRef();
  
  useFrame((state, delta) => {
    if (rotation && meshRef.current) {
      meshRef.current.rotation.x += delta * 0.2;
      meshRef.current.rotation.y += delta * 0.3;
    }
  });

  const getGeometry = () => {
    switch (geometry) {
      case 'box':
        return <boxGeometry args={[2, 2, 2]} />;
      case 'sphere':
        return <sphereGeometry args={[1.5, 32, 32]} />;
      case 'torus':
        return <torusGeometry args={[1, 0.4, 16, 100]} />;
      case 'cone':
        return <coneGeometry args={[1, 2, 32]} />;
      case 'cylinder':
        return <cylinderGeometry args={[1, 1, 2, 32]} />;
      case 'torusKnot':
        return <torusKnotGeometry args={[1, 0.3, 100, 16]} />;
      case 'dodecahedron':
        return <dodecahedronGeometry args={[1.5]} />;
      case 'icosahedron':
        return <icosahedronGeometry args={[1.5]} />;
      case 'octahedron':
        return <octahedronGeometry args={[1.5]} />;
      case 'tetrahedron':
        return <tetrahedronGeometry args={[1.5]} />;
      default:
        return <boxGeometry args={[2, 2, 2]} />;
    }
  };

  return (
    <mesh ref={meshRef}>
      {getGeometry()}
      <meshStandardMaterial 
        color={color} 
        wireframe={wireframe}
        metalness={0.3}
        roughness={0.4}
      />
    </mesh>
  );
};

// 3D Function surface
const FunctionSurface = ({ func = 'sin', color = '#0891b2' }) => {
  const meshRef = useRef();
  
  // Create geometry based on function
  const createSurfaceGeometry = () => {
    const size = 4;
    const segments = 50;
    const geometry = new THREE.PlaneGeometry(size, size, segments, segments);
    const positions = geometry.attributes.position;
    
    for (let i = 0; i < positions.count; i++) {
      const x = positions.getX(i);
      const y = positions.getY(i);
      let z = 0;
      
      switch (func) {
        case 'sin':
          z = Math.sin(Math.sqrt(x * x + y * y) * 2) * 0.5;
          break;
        case 'cos':
          z = Math.cos(x) * Math.cos(y) * 0.5;
          break;
        case 'saddle':
          z = (x * x - y * y) * 0.2;
          break;
        case 'paraboloid':
          z = (x * x + y * y) * 0.15;
          break;
        case 'wave':
          z = Math.sin(x * 2) * Math.cos(y * 2) * 0.5;
          break;
        default:
          z = Math.sin(x) * Math.cos(y) * 0.5;
      }
      
      positions.setZ(i, z);
    }
    
    geometry.computeVertexNormals();
    return geometry;
  };

  useFrame((state, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.z += delta * 0.1;
    }
  });

  return (
    <mesh ref={meshRef} rotation={[-Math.PI / 4, 0, 0]} geometry={createSurfaceGeometry()}>
      <meshStandardMaterial 
        color={color}
        side={THREE.DoubleSide}
        metalness={0.2}
        roughness={0.6}
      />
    </mesh>
  );
};

// Vector visualization
const VectorArrow = ({ start = [0, 0, 0], end = [1, 1, 1], color = '#ef4444' }) => {
  const direction = new THREE.Vector3(...end).sub(new THREE.Vector3(...start));
  const length = direction.length();
  direction.normalize();
  
  const arrowHelper = new THREE.ArrowHelper(
    direction,
    new THREE.Vector3(...start),
    length,
    color,
    length * 0.2,
    length * 0.1
  );
  
  return <primitive object={arrowHelper} />;
};

// Scene component
const Scene = ({ config }) => {
  const { type, geometry, func, color, wireframe, vectors } = config;
  
  return (
    <>
      <ambientLight intensity={0.5} />
      <directionalLight position={[5, 5, 5]} intensity={1} />
      <pointLight position={[-5, -5, -5]} intensity={0.5} />
      
      {type === 'geometry' && (
        <RotatingMesh 
          geometry={geometry || 'box'} 
          color={color || '#0891b2'}
          wireframe={wireframe}
        />
      )}
      
      {type === 'surface' && (
        <FunctionSurface func={func || 'sin'} color={color || '#0891b2'} />
      )}
      
      {type === 'vectors' && vectors && vectors.map((v, i) => (
        <VectorArrow 
          key={i}
          start={v.start || [0, 0, 0]}
          end={v.end || [1, 1, 1]}
          color={v.color || ['#ef4444', '#22c55e', '#3b82f6'][i % 3]}
        />
      ))}
      
      <Grid args={[10, 10]} position={[0, -2, 0]} cellColor="#94a3b8" sectionColor="#64748b" />
      <OrbitControls enableDamping dampingFactor={0.05} />
    </>
  );
};

const ThreeJSEmbed = ({ config: configStr, height = 400 }) => {
  const [error, setError] = useState(null);
  
  // Parse config string
  const parseConfig = (str) => {
    try {
      // Try JSON first
      return JSON.parse(str);
    } catch {
      // Parse simple format: type=geometry;shape=sphere;color=#ff0000
      const parts = str.split(';').reduce((acc, part) => {
        const [key, value] = part.split('=').map(s => s.trim());
        if (key && value) {
          try {
            acc[key] = JSON.parse(value);
          } catch {
            acc[key] = value;
          }
        }
        return acc;
      }, {});
      
      return {
        type: parts.type || 'geometry',
        geometry: parts.shape || parts.geometry || 'box',
        func: parts.func || 'sin',
        color: parts.color || '#0891b2',
        wireframe: parts.wireframe === 'true' || parts.wireframe === true,
        vectors: parts.vectors
      };
    }
  };

  let config;
  try {
    config = parseConfig(configStr);
  } catch (err) {
    return (
      <div className="my-6 p-4 bg-red-50 text-red-600 rounded-lg">
        Error en configuración 3D: {err.message}
      </div>
    );
  }

  if (!configStr) return null;

  return (
    <div className="my-6">
      <div className="bg-slate-50 rounded-lg p-3 border border-slate-200">
        <div className="flex items-center gap-2 mb-2 text-sm text-slate-600">
          <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M12 2L2 7l10 5 10-5-10-5z" strokeWidth="2"/>
            <path d="M2 17l10 5 10-5" strokeWidth="2"/>
            <path d="M2 12l10 5 10-5" strokeWidth="2"/>
          </svg>
          <span className="font-medium">Visualización 3D</span>
          <span className="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded">Three.js</span>
        </div>
        
        {error ? (
          <div className="text-red-500 text-sm p-4 bg-red-50 rounded">
            {error}
          </div>
        ) : (
          <div 
            style={{ width: '100%', height: `${height}px` }}
            className="rounded-lg overflow-hidden bg-gradient-to-b from-slate-900 to-slate-800"
          >
            <Canvas camera={{ position: [4, 3, 4], fov: 50 }}>
              <Suspense fallback={null}>
                <Scene config={config} />
              </Suspense>
            </Canvas>
          </div>
        )}
        
        <div className="mt-2 text-xs text-slate-500">
          <span>💡 Tip: Arrastra para rotar, scroll para zoom, click derecho para mover</span>
        </div>
      </div>
    </div>
  );
};

export default ThreeJSEmbed;
