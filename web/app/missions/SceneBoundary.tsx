'use client';
import {Component,type ReactNode} from 'react';

/** A device/driver failure must not prevent completing the lightweight mission. */
export default class SceneBoundary extends Component<{children:ReactNode},{failed:boolean}>{
  state={failed:false};
  static getDerivedStateFromError(){return {failed:true};}
  render(){
    return this.state.failed?<p role="status">3D is unavailable on this device. Switch to the 2D workstation to continue the same mission.</p>:this.props.children;
  }
}
