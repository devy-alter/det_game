import { useState } from "react";

export default function DetectiveInput({ onAsk, disabled, remaining }) {
  const [q, setQ] = useState("");

  function submit(e) {
    e.preventDefault();
    const text = q.trim();
    if (!text || disabled || remaining <= 0) return;
    onAsk(text);
    setQ("");
  }

  return (
    <form className="questionConsole" onSubmit={submit}>
      <div className="consoleLabel"><span>DETECTIVE</span><b>QUESTION THE SUBJECT</b></div>
      <textarea value={q} disabled={disabled} onChange={(e) => setQ(e.target.value)} placeholder="Ask the question that makes the story impossible to maintain..." rows="3" maxLength="1000" />
      <div className="consoleFooter"><span>ENTER TO SUBMIT · SHIFT + ENTER FOR NEW LINE</span><button disabled={disabled || !q.trim() || remaining <= 0}>{disabled ? "LISTENING" : "SUBMIT QUESTION"}</button></div>
    </form>
  );
}
