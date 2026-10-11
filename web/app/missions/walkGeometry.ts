/** Approximate collision geometry for the procedural SOC room. */
export type Point={x:number;z:number};
export const PLAYER_RADIUS=.22;
export const SPAWN:Point={x:0,z:2.7};
export const DESKS:readonly {x:number;z:number;halfWidth:number;halfDepth:number}[]=[
 {x:-3,z:-.6,halfWidth:.9,halfDepth:.55},
 {x:0,z:-1.2,halfWidth:.9,halfDepth:.55},
 {x:3,z:-.6,halfWidth:.9,halfDepth:.55},
];
export const STATIONS:readonly {id:'briefing'|'evidence'|'decision';x:number;z:number}[]=[
 {id:'briefing',x:-3,z:-.6},
 {id:'evidence',x:0,z:-1.2},
 {id:'decision',x:3,z:-.6},
];
export function canWalk(x:number,z:number):boolean{
 if(!Number.isFinite(x)||!Number.isFinite(z))return false;
 if(x < -5.45+PLAYER_RADIUS || x > 5.45-PLAYER_RADIUS || z < -2.95+PLAYER_RADIUS || z > 3.25-PLAYER_RADIUS)return false;
 return DESKS.every(d=>Math.abs(x-d.x)>=d.halfWidth+PLAYER_RADIUS || Math.abs(z-d.z)>=d.halfDepth+PLAYER_RADIUS);
}
export function nearbyStation(x:number,z:number,maxDistance=1.8){
 let nearest:typeof STATIONS[number]|undefined;
 let best=maxDistance*maxDistance;
 for(const s of STATIONS){const dist=(x-s.x)**2+(z-s.z)**2;if(dist<best){nearest=s;best=dist;}}
 return nearest?.id??null;
}
