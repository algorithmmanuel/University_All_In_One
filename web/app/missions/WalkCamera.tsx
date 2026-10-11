'use client';
import {useEffect,useRef} from 'react';
import {useFrame,useThree} from '@react-three/fiber';
export default function WalkCamera({enabled}:{enabled:boolean}){
 const {camera}=useThree();
 const keys=useRef(new Set<string>());
 useEffect(()=>{
  if(!enabled)return;
  camera.position.set(0,1.7,2.7);
  const down=(e:KeyboardEvent)=>{if(['w','a','s','d'].includes(e.key.toLowerCase()))keys.current.add(e.key.toLowerCase());};
  const up=(e:KeyboardEvent)=>keys.current.delete(e.key.toLowerCase());
  window.addEventListener('keydown',down);window.addEventListener('keyup',up);
  return()=>{keys.current.clear();window.removeEventListener('keydown',down);window.removeEventListener('keyup',up);};
 },[enabled,camera]);
 useFrame((_,delta)=>{
  if(!enabled)return;
  const k=keys.current;
  const dx=(Number(k.has('d'))-Number(k.has('a')))*delta*2;
  const dz=(Number(k.has('s'))-Number(k.has('w')))*delta*2;
  camera.position.x=Math.max(-5,Math.min(5,camera.position.x+dx));
  camera.position.z=Math.max(.9,Math.min(3,camera.position.z+dz));
  camera.lookAt(camera.position.x,1.3,-2);
 });
 return null;
}
