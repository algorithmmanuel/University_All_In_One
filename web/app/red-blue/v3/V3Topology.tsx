"use client";
import styles from "./V3Topology.module.css";

type VisibleAsset = {
  id:string; name:string; kind:string; isolated?:boolean;
  knowledge?:string; value?:number; business_value?:number|null;
};
const position: Record<string,{x:number;y:number}> = {
  teller:{x:130,y:88},
  gateway:{x:130,y:286},
  identity:{x:445,y:88},
  ledger:{x:755,y:160},
  bureau:{x:755,y:315},
};

/** Purely visual: nodes and arrows derive solely from already seat-filtered data. */
export default function V3Topology({assets,connections,side}:{
  assets:VisibleAsset[];
  connections:{source:string;target:string}[];
  side:"red"|"blue";
}) {
  const known = new Map(assets.map(a=>[a.id,a]));
  const edges = connections.filter(e=>known.has(e.source)&&known.has(e.target));
  return (
    <section className={styles.frame} aria-label="Observed network topology">
      <p className={styles.note}>Known directed trust paths only. Open an asset card below to inspect evidence and controls.</p>
      <svg viewBox="0 0 950 430" role="img"
        aria-label={side==="red"?"Partial discovered Red network":"Blue owned institutional network"}
        preserveAspectRatio="xMidYMid meet">
        <defs>
          <marker id="v3-arrow" markerWidth="8" markerHeight="8" refX="6" refY="3"
            orient="auto" markerUnits="strokeWidth">
            <path d="M0,0 L0,6 L7,3 z" fill="#7abebf"/>
          </marker>
        </defs>
        {edges.map((e,i)=>{
          const a=position[e.source],b=position[e.target];
          if(!a||!b)return null;
          const mid=(a.x+b.x)/2;
          return <path key={i} d={"M"+(a.x+90)+","+a.y+" H"+mid+
            " V"+b.y+" H"+(b.x-92)}
            fill="none" stroke="#7abebf" strokeWidth="3"
            markerEnd="url(#v3-arrow)" strokeLinejoin="round"/>;
        })}
        {assets.map(asset=>{
          const p=position[asset.id];
          if(!p)return null;
          const colour=side==="red"?"#983f56":asset.isolated?"#825b3d":"#14576c";
          const short=asset.name.length>24?asset.name.slice(0,23)+"…":asset.name;
          return <g key={asset.id}>
            <rect x={p.x-90} y={p.y-36} width="180" height="72" rx="12"
              fill={colour} stroke={side==="red"?"#ffadbd":"#78dbe2"} strokeWidth="2"/>
            <text x={p.x} y={p.y-9} textAnchor="middle"
              fontSize="14" fontWeight="700" fill="#f6f9fa">{short}</text>
            <text x={p.x} y={p.y+16} textAnchor="middle"
              fontSize="12" fill="#cfe4ec">
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
