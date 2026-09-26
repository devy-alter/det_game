import { useEffect, useRef } from "react";

export default function ChatHistory({ history }) {
  const ref = useRef(null);

  useEffect(() => {
    if (ref.current) ref.current.scrollTop = ref.current.scrollHeight;
  }, [history.length, history.at(-1)?.suspect_response]);

  return (
    <div className="historyRail" ref={ref}>
      {history.length <= 1 && <div className="historyEmpty">{history.length ? "CURRENT EXCHANGE HELD BELOW" : "NO PRIOR EXCHANGES / START RECORDING"}</div>}
      {history.slice(0, -1).map((h) => (
        <article className={`historyTurn ${h.pending ? "isPending" : ""}`} key={h.question_number}>
          <div className="historyQuestion"><span>Q{String(h.question_number).padStart(2, "0")}</span><p>{h.detective_question}</p></div>
          <div className="historyAnswer"><span>R</span><p>{h.suspect_response || "..."}</p></div>
        </article>
      ))}
    </div>
  );
}
