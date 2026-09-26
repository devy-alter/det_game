import { api, API_BASE } from "./api";

export const getGamesCases = () => api("/cases");
export const startGame = (case_id) => api("/game/start", { method: "POST", body: JSON.stringify({ case_id }) });
export const getGame = (id) => api(`/game/${id}`);
export const restartGame = (id) => api(`/game/${id}/restart`, { method: "POST" });

export async function askQuestionStream(id, question, onEvent) {
  const response = await fetch(`${API_BASE}/game/${id}/question`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "text/event-stream" },
    body: JSON.stringify({ question }),
  });

  if (!response.ok) {
    const data = await response.json().catch(() => ({ detail: `Request failed (${response.status})` }));
    throw new Error(data.detail || `Request failed (${response.status})`);
  }
  if (!response.body) throw new Error("Streaming is not supported by this browser");

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const chunks = buffer.split("\n\n");
    buffer = chunks.pop() || "";
    for (const chunk of chunks) {
      const line = chunk.split("\n").find((item) => item.startsWith("data: "));
      if (!line) continue;
      const event = JSON.parse(line.slice(6));
      onEvent(event);
      if (event.type === "error") throw new Error(event.message);
    }
  }
}
