'use client';
import {ThreeEvent} from '@react-three/fiber';
export const ARTIFACT_POSITIONS:[number,number,number][]=[[-3,1.82,-.6],[0,1.82,-1.2],[3,1.82,-.6]];
export default function EvidenceObjects({inspected,onInspect}:{inspected:number[];onInspect:(index:number)=>void}){
 const colors=['#f59e64','#5ac8f5','#d7b7ff'];
 return <group>{ARTIFACT_POSITIONS.map((position,i)=><group key={i} position={position}>
  <mesh onClick={(event:ThreeEvent<MouseEvent>)=>{event.stopPropagation();onInspect(i);}} onPointerOver={e=>{e.stopPropagation();document.body.style.cursor='pointer';}} onPointerOut={()=>{document.body.style.cursor='auto';}}>
   <boxGeometry args={[.6,.42,.1]}/><meshStandardMaterial color={inspected.includes(i)?'#205d4f':colors[i]} emissive={inspected.includes(i)?'#2dd4bf':colors[i]} emissiveIntensity={.42}/>
  </mesh>
  <mesh position={[0,.32,0]}><boxGeometry args={[.14,.08,.08]}/><meshStandardMaterial color={inspected.includes(i)?'#40e0aa':'#ffcc70'} emissive={inspected.includes(i)?'#40e0aa':'#ffcc70'} emissiveIntensity={.7}/></mesh>
 </group>)}</group>;
}
