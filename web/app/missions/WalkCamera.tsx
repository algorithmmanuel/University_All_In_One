'use client';
import {useEffect,useRef} from 'react';
import {useFrame,useThree} from '@react-three/fiber';
import {canWalk,nearbyStation,SPAWN} from './walkGeometry';
type Station='briefing'|'evidence'|'decision';
type Props={enabled:boolean;onInteract:(station:Station)=>void;onNearby:(station:Station|null)=>void};
export default function WalkCamera({enabled,onInteract,onNearby}:Props){
 const {camera,gl}=useThree();
 const keys=useRef(new Set<string>());
 const yaw=useRef(0);
 const pitch=useRef(-.08);
 const dragging=useRef(false);
 const interact=useRef(onInteract);
 const nearby=useRef(onNearby);
 interact.current=onInteract;nearby.current=onNearby;
 useEffect(()=>{
  if(!enabled)return;
  const canvas=gl.domElement;
  const previousTabIndex=canvas.getAttribute('tabindex');
  canvas.tabIndex=0;
  camera.position.set(SPAWN.x,1.7,SPAWN.z);
  yaw.current=0;pitch.current=-.08;
  const down=(e:KeyboardEvent)=>{
   if(document.activeElement!==canvas||e.repeat&&e.key.toLowerCase()==='e')return;
   const key=e.key.toLowerCase();
   if(['w','a','s','d','arrowup','arrowdown','arrowleft','arrowright','e'].includes(key))e.preventDefault();
   if(key==='e'){const id=nearbyStation(camera.position.x,camera.position.z);if(id)interact.current(id);}
   else keys.current.add(key);
  };
  const up=(e:KeyboardEvent)=>keys.current.delete(e.key.toLowerCase());
  const move=(e:PointerEvent)=>{
   if(!dragging.current)return;
   yaw.current-=e.movementX*.004;
   pitch.current=Math.max(-.9,Math.min(.9,pitch.current-e.movementY*.003));
  };
  const pointerDown=(e:PointerEvent)=>{if(e.button===0){dragging.current=true;canvas.focus();}};
  const pointerUp=()=>{dragging.current=false;};
  const blur=()=>{keys.current.clear();dragging.current=false;};
  canvas.addEventListener('keydown',down);canvas.addEventListener('keyup',up);
  canvas.addEventListener('pointerdown',pointerDown);canvas.addEventListener('pointermove',move);
  window.addEventListener('pointerup',pointerUp);window.addEventListener('blur',blur);
  return()=>{
   blur();nearby.current(null);
   canvas.removeEventListener('keydown',down);canvas.removeEventListener('keyup',up);
   canvas.removeEventListener('pointerdown',pointerDown);canvas.removeEventListener('pointermove',move);
   window.removeEventListener('pointerup',pointerUp);window.removeEventListener('blur',blur);
   if(previousTabIndex===null)canvas.removeAttribute('tabindex');else canvas.setAttribute('tabindex',previousTabIndex);
  };
 },[enabled,camera,gl]);
 const lastNearby=useRef<Station|null>(null);
 useFrame((_,delta)=>{
  if(!enabled)return;
  const k=keys.current;
  const f=Number(k.has('w')||k.has('arrowup'))-Number(k.has('s')||k.has('arrowdown'));
  const strafe=Number(k.has('d')||k.has('arrowright'))-Number(k.has('a')||k.has('arrowleft'));
  const norm=Math.hypot(f,strafe)||1;
  const speed=Math.min(delta,.05)*2.5;
  const dx=(Math.cos(yaw.current)*strafe-Math.sin(yaw.current)*f)/norm*speed;
  const dz=(-Math.cos(yaw.current)*f-Math.sin(yaw.current)*strafe)/norm*speed;
  if(canWalk(camera.position.x+dx,camera.position.z))camera.position.x+=dx;
  if(canWalk(camera.position.x,camera.position.z+dz))camera.position.z+=dz;
  camera.rotation.order='YXZ';
  camera.rotation.set(pitch.current,yaw.current,0);
  const id=nearbyStation(camera.position.x,camera.position.z);
  if(id!==lastNearby.current){lastNearby.current=id;nearby.current(id);}
 });
 return null;
}
