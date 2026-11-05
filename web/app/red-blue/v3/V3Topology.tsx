"use client";
import styles from "./V3Topology.module.css";

type VisibleAsset = {
  id:string; name:string; kind:string; isolated?:boolean;
  knowledge?:string; value?:number; business_value?:number|null;
};

/** Visual graph uses only seat-filtered asset/edge inputs, never a hidden ID map. */
export default function V3Topology({assets,connections,side}:{
  assets:VisibleAsset[];
  connections:{source:string;target:string}[];
  side:"red"|"blue";
}) {
  const known = new Map(assets.map((asset,i)=>[
    asset.id,{asset,x:120+(i%4)*235,y:95+Math.floor(i/4)*145},
  ]));
  const edges = connections.filter(edge=>known.has(edge.source)&&known.has(edge.target));
  const height=Math.max(245,Math.ceil(assets.length/4)*145+70);
  return (
    <section className={styles.frame} aria-label="Observed network topology">
      <p className={styles.note}>Known directed trust paths only. Open an asset card below to inspect its evidence and controls.</p>
      <svg viewBox={"0 0 950 "+height} role="img"
        aria-label={side==="red"?"Partial discovered Red network":"Blue owned institutional network"}
        preserveAspectRatio="xMidYMid meet">
        <defs>
          <marker id="v3-arrow" markerWidth="8" markerHeight="8" refX="6" refY="3"
            orient="auto" markerUnits="strokeWidth">
            <path d="M0,0 L0,6 L7,3 z" fill="#7abebf"/>
          </marker>
        </defs>
        {edges.map((edge,i)=>{
          const a=known.get(edge.source),b=known.get(edge.target);
          if(!a||!b)return null;
          const mid=(a.x+b.x)/2;
          const d=Math.abs(a.x-b.x)<3
            ? "M"+a.x+","+(a.y+37)+" V"+(b.y-42)
            : "M"+(a.x+90)+","+a.y+" H"+mid+" V"+b.y+" H"+(b.x-94);
          return <path key={i} d={d} fill="none" stroke="#7abebf"
            strokeWidth="2.5" strokeOpacity=".7" markerEnd="url(#v3-arrow)"
            strokeLinejoin="round"/>;
        })}
        {assets.map(asset=>{
          const p=known.get(asset.id);
          if(!p)return null;
          const colour=side==="red"?"#983f56":asset.isolated?"#825b3d":"#14576c";
          const short=asset.name.length>24?asset.name.slice(0,23)+"…":asset.name;
          return <g key={asset.id}>
            <rect x={p.x-90} y={p.y-36} width="180" height="72" rx="12"
              fill={colour} stroke={side==="red"?"#ffadbd":"#78dbe2"} strokeWidth="2"/>
            <text x={p.x} y={p.y-9} textAnchor="middle" fontSize="14"
              fontWeight="700" fill="#f6f9fa">{short}</text>
            <text x={p.x} y={p.y+16} textAnchor="middle" fontSize="12" fill="#cfe4ec">
              {side==="blue" ? (asset.isolated?"Isolated":"Business value "+asset.value)
                : asset.knowledge || "Discovered"}
            </text>
          </g>;
        })}
      </svg>
      <p className={styles.note}>
        {assets.length} known assets · {edges.length} known directed connections.
        {side==="red"?" Additional assets may remain undiscovered.":""}
      </p>
    </section>
  );
}
