export const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000/api";
export async function api(path, options={}){
  const r=await fetch(`${API_BASE}${path}`,{headers:{"Content-Type":"application/json",...(options.headers||{})},...options});
  const data=await r.json().catch(()=>({detail:"Invalid server response"}));
  if(!r.ok) throw new Error(data.detail || `Request failed (${r.status})`);
  return data;
}
