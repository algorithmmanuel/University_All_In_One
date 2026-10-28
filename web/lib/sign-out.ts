/** Revoke the current session when reachable; always remove this browser's token.
 * A failed/offline revoke does not prove server-side invalidation.
 */
export async function signOutLocally(api:string){
  const token=sessionStorage.getItem('educyber_token');
  try{
    if(token)await fetch(api+'/api/v1/auth/logout',{method:'POST',headers:{Authorization:'Bearer '+token},signal:AbortSignal.timeout(5000)});
  }catch{
    // Keep offline sign-out bounded and usable.
  }finally{sessionStorage.removeItem('educyber_token');}
}
