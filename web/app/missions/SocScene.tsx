'use client';
import {Canvas, ThreeEvent, useFrame, useThree} from '@react-three/fiber';
import {useEffect,useRef} from 'react';
import * as THREE from 'three';
import {useState} from 'react';
import styles from './soc-scene.module.css';
import SocEnvironment from './SocEnvironment';
import WalkCamera from './WalkCamera';
import EvidenceObjects from './EvidenceObjects';

type Station='briefing'|'evidence'|'decision';
type Props={stage:number;active:Station;onSelect:(station:Station)=>void;evidence:string[];onInspect:(index:number)=>void;inspected:number[]};
const stations:{id:Station;name:string;position:[number,number,number];color:string}[]=[
  {id:'briefing',name:'Command briefing',position:[-3,0,-0.6],color:'#27b7d6'},
  {id:'evidence',name:'Evidence terminal',position:[0,0,-1.2],color:'#54dfba'},
  {id:'decision',name:'Incident desk',position:[3,0,-0.6],color:'#f3bd63'}
];
function CameraNavigator({target}:{target:[number,number,number]}){
 const {camera}=useThree();
 const destination=useRef(new THREE.Vector3(...target));
 useEffect(()=>{destination.current.set(...target);},[target]);
 useFrame((_,delta)=>{
   camera.position.lerp(destination.current,1-Math.exp(-3*delta));
   camera.lookAt(0,1,-1.3);
 });
 return null;
}
function Console({position,color,active,onClick}:{position:[number,number,number];color:string;active:boolean;onClick:(e:ThreeEvent<MouseEvent>)=>void}){
 return <group position={position} onClick={onClick}>
   <mesh position={[0,.55,0]}><boxGeometry args={[1.75,.16,.9]}/><meshStandardMaterial color="#273d53"/></mesh>
   <mesh position={[0,1.2,-.28]} rotation={[-.12,0,0]}>
     <boxGeometry args={[1.55,.88,.12]}/><meshStandardMaterial color="#0b1626" metalness={.4} roughness={.3}/>
   </mesh>
   <mesh position={[0,1.2,-.205]} rotation={[-.12,0,0]}>
     <planeGeometry args={[1.37,.7]}/><meshStandardMaterial color={color} emissive={color} emissiveIntensity={active?.6:.22}/>
   </mesh>
   <mesh position={[0,.15,.35]}><boxGeometry args={[.8,.27,.65]}/><meshStandardMaterial color="#15293e"/></mesh>
   <mesh position={[0,.72,.17]}><boxGeometry args={[.9,.03,.3]}/><meshStandardMaterial color="#0b1626"/></mesh>
   {active&&<pointLight position={[0,1.7,0]} intensity={2.2} color={color} distance={3}/>}
 </group>;
}
export default function SocScene({stage,active,onSelect,evidence,onInspect,inspected}:Props){
 const [quality,setQuality]=useState<'standard'|'low'>('standard');
 const [view,setView]=useState(0);
 const [walk,setWalk]=useState(false);
 const [nearby,setNearby]=useState<{kind:'artifact';index:number}|{kind:'station';id:Station}|null>(null);
 const [artifact,setArtifact]=useState<number|null>(null);
 const inspectedCount=inspected.filter(i=>i>=0&&i<evidence.length).length;
 function inspectArtifact(i:number){if(i<0||i>=evidence.length)return;setArtifact(i);onInspect(i);onSelect('evidence');}
 const signal=stage===0?'PRIVILEGED LOGIN ALERT':stage===1?'UNRECOGNIZED DEVICE':'CONTAINMENT REVIEW';
 const views:[number,number,number][]=[[0,4.4,9],[-3,2.5,4],[0,2.8,3.6],[3,2.5,4]];
 function navigate(index:number){setArtifact(null);setWalk(false);setView(index);if(index>0)onSelect(stations[index-1].id);}
 useEffect(()=>{const handle=(e:KeyboardEvent)=>{if(e.altKey||e.ctrlKey||e.metaKey||['INPUT','TEXTAREA','SELECT'].includes((e.target as HTMLElement)?.tagName))return;if(walk)return;if(e.key==='ArrowLeft'||e.key==='a'){setView(v=>(v+3)%4);}if(e.key==='ArrowRight'||e.key==='d'){setView(v=>(v+1)%4);}};window.addEventListener('keydown',handle);return()=>window.removeEventListener('keydown',handle);},[walk]);
 return <section className={styles.shell} aria-label="Interactive 3D security operations centre">
  <div className={styles.heading}><div><strong>EDUCYBER · SOC SIMULATION</strong><p>Operation Firewall · Stage {stage+1} · {signal} · Fictional training environment</p></div>
   <button type="button" onClick={()=>setQuality(q=>q==='standard'?'low':'standard')}>Graphics: {quality}</button></div>
  <div className={styles.viewport}>
   <Canvas camera={{position:[0,4.4,9],fov:48}} dpr={quality==='low'?1:[1,1.5]} gl={{antialias:quality==='standard',powerPreference:'low-power'}} fallback={<p>3D rendering is unavailable. Use the 2D workstation below.</p>}>
    {!walk&&<CameraNavigator target={views[view]}/>}
    <WalkCamera enabled={walk} onTarget={setNearby} onInspect={inspectArtifact} onInteract={id=>{onSelect(id);setWalk(false);setView(stations.findIndex(s=>s.id===id)+1);}}/>
    <color attach="background" args={['#071321']}/>
    <ambientLight intensity={1.6}/>
    {quality==='standard'&&<pointLight position={[0,5,2]} intensity={55} color="#8ad7ed"/>}
    <mesh position={[0,-.12,0]}><boxGeometry args={[12,.2,7]}/><meshStandardMaterial color="#12253a"/></mesh>
    <SocEnvironment quality={quality}/>
    <mesh position={[0,2,-3.3]}><boxGeometry args={[12,4,.16]}/><meshStandardMaterial color="#162d43"/></mesh>
    <mesh position={[0,2.9,-3.19]}><boxGeometry args={[9,.12,.05]}/><meshStandardMaterial color="#38c6b0" emissive="#38c6b0" emissiveIntensity={.45}/></mesh>
    <EvidenceObjects inspected={inspected} onInspect={inspectArtifact}/>
    {stations.map(s=><Console key={s.id} position={s.position} color={s.color} active={active===s.id}
      onClick={e=>{e.stopPropagation();onSelect(s.id);setWalk(false);setView(stations.findIndex(x=>x.id===s.id)+1);}}/>)}
   </Canvas>
  </div>
  <div className={styles.controls} aria-label="Stage evidence objects">{evidence.map((item,i)=><button key={stage+'-'+i} type="button" className={artifact===i?styles.selected:styles.station} aria-pressed={artifact===i} onClick={()=>{setWalk(false);setView(2);inspectArtifact(i);}}>Inspect artifact {i+1}{inspected.includes(i)?' ✓':''}</button>)}</div>
  {artifact!==null&&evidence[artifact]&&<div className={styles.help} role="status"><strong>Evidence terminal · Artifact {artifact+1}</strong><p>{evidence[artifact]}</p><p>This is a fictional case artifact. It is also available in the Evidence Locker.</p><button type="button" className={styles.station} onClick={()=>setArtifact(null)}>Close evidence detail</button></div>}
  <p className={styles.help} role="status"><strong>INVESTIGATION HUD · {inspectedCount}/{evidence.length} artifacts inspected</strong>{walk&&<span> · {nearby?.kind==='artifact'?`Near artifact ${nearby.index+1}: press E to inspect, Shift+E for workstation.`:'Move toward a glowing marker; click the scene to focus, then press E near evidence.'}</span>}</p>}
  <div className={styles.controls}>
   <button type="button" className={walk?styles.selected:styles.station} onClick={()=>setWalk(v=>!v)}>{walk?"Exit walking mode":"Walk around (WASD)"}</button>
   <button type="button" className={!walk&&view===0?styles.selected:styles.station} onClick={()=>navigate(0)}>Overview</button>
   {stations.map(s=><button key={s.id} type="button" aria-pressed={active===s.id} className={active===s.id?styles.selected:styles.station} onClick={()=>navigate(stations.findIndex(x=>x.id===s.id)+1)}>{s.name} →</button>)}
  </div>
  <p className={styles.help}>Walk mode: click the scene to focus, use W/A/S/D to move, hold left mouse button and drag to look, and press E near evidence to inspect or Shift+E to open its workstation. Movement keys are ignored while typing outside the scene. Use Exit walking mode to return to guided views. Navigate guided views with buttons or arrow keys. Select a glowing workstation to focus on it. Click a small glowing evidence marker above a workstation to inspect it, or use the Inspect artifact buttons as an accessible alternative. Investigations and scoring continue in the secure mission workspace below. No live systems are connected.</p>
 </section>;
}
