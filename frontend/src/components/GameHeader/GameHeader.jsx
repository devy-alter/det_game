export default function GameHeader({ state, caseData }) {
  return (
    <header className="gameHeader">
      <div className="brandMark">
        <span className="badge">BPD</span>
        <div><span>BLACKWOOD</span><b>INTERROGATION DIVISION</b></div>
      </div>
      <div className="caseHeaderName"><span>ACTIVE FILE</span><b>{caseData?.title}</b></div>
      <div className="headerStats">
        <div><span>QUESTION</span><b>{String(state.question_count).padStart(2, "0")} / 10</b></div>
        <div><span>ROOM</span><b>04</b></div>
      </div>
    </header>
  );
}
