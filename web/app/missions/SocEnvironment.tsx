'use client';
/** Lightweight procedural SOC scenery. All displays are fictional, non-sensitive data. */
const alertBars=[.7,.38,.92,.53,.8,.25,.61,.44];
function WallPanel({x,y,accent}:{x:number;y:number;accent:string}){
 return <group position={[x,y,-3.05]}>
  <mesh><boxGeometry args={[2.35,1.15,.12]}/><meshStandardMaterial color="#081321" metalness={.25} roughness={.55}/></mesh>
  <mesh position={[0,0,.068]}><planeGeometry args={[2.16,.98]}/><meshStandardMaterial color="#102a3a" emissive="#0a4b52" emissiveIntensity={.17}/></mesh>
  {alertBars.map((h,i)=><mesh key={i} position={[-.89+i*.25,-.24+h*.29,.077]}>
   <boxGeometry args={[.13,h*.58,.012]}/><meshBasicMaterial color={i===2||i===4?accent:'#3e9dba'}/>
  </mesh>)}
  <mesh position={[0,.37,.08]}><boxGeometry args={[1.83,.035,.015]}/><meshBasicMaterial color={accent}/></mesh>
 </group>;
}
function ServerRack({x}:{x:number}){
 return <group position={[x,1,-2.55]}>
  <mesh><boxGeometry args={[.82,2,.62]}/><meshStandardMaterial color="#111b2a" metalness={.6} roughness={.45}/></mesh>
  {Array.from({length:7},(_,i)=><group key={i} position={[0,.76-i*.245,.32]}>
   <mesh><boxGeometry args={[.68,.17,.015]}/><meshStandardMaterial color="#243a4c"/></mesh>
   <mesh position={[-.23,0,.018]}><boxGeometry args={[.06,.035,.012]}/><meshBasicMaterial color={i===4?'#e6ae57':'#49d7b1'}/></mesh>
   <mesh position={[-.12,0,.018]}><boxGeometry args={[.06,.035,.012]}/><meshBasicMaterial color="#2f7b98"/></mesh>
  </group>)}
 </group>;
}
function FloorGuides(){
 return <group>
  {[-4.5,-1.5,1.5,4.5].map(x=><mesh key={x} position={[x,-.006,1.25]}>
   <boxGeometry args={[.035,.008,3.5]}/><meshBasicMaterial color="#1b6371"/></mesh>)}
  {[-1.4,.2,1.8,3.4].map(z=><mesh key={z} position={[0,-.004,z]}>
   <boxGeometry args={[10,.008,.025]}/><meshBasicMaterial color="#164b60"/></mesh>)}
 </group>;
}
export default function SocEnvironment({quality}:{quality:'standard'|'low'}){
 return <group>
  <mesh position={[0,3.6,-3.1]}><boxGeometry args={[11,.25,.2]}/><meshStandardMaterial color="#233a50"/></mesh>
  <mesh position={[-5.8,1.8,0]}><boxGeometry args={[.15,3.6,6.5]}/><meshStandardMaterial color="#132b3e"/></mesh>
  <mesh position={[5.8,1.8,0]}><boxGeometry args={[.15,3.6,6.5]}/><meshStandardMaterial color="#132b3e"/></mesh>
  <WallPanel x={-2.55} y={2.15} accent="#f2b96c"/>
  <WallPanel x={0} y={2.15} accent="#54dfba"/>
  <WallPanel x={2.55} y={2.15} accent="#e17e78"/>
  <ServerRack x={-4.85}/><ServerRack x={4.85}/>
  <FloorGuides/>
  {quality==='standard'&&<>
   <pointLight position={[-4,2.7,1]} intensity={12} distance={6} color="#40a8c4"/>
   <pointLight position={[4,2.7,1]} intensity={12} distance={6} color="#48d7af"/>
  </>}
 </group>;
}
