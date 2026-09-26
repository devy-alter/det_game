export default function GameOverModal({ state, onRestart }) {
  if (state.status === "active") return null;
  const win = state.status === "won";
  return (
    <div className="modalBackdrop">
      <div className={`caseOutcome ${win ? "win" : "loss"}`}>
        <span className="outcomeKicker">CASE {win ? "CRACKED" : "CLOSED"}</span>
        <h2>{win ? "CONFESSION\nSECURED" : "THE STORY HELD"}</h2>
        <p>{win ? "The suspect's defence finally collapsed under the weight of your interrogation." : "Ten questions are gone. The suspect kept enough of the story intact to avoid a confession."}</p>
        <div className="outcomeStats">
          <div><span>COMPOSURE</span><b>{state.confidence}%</b></div>
          <div><span>CASE PRESSURE</span><b>{state.confession_progress}%</b></div>
          <div><span>QUESTIONS</span><b>{state.question_count}/10</b></div>
        </div>
        <button onClick={onRestart}>REOPEN CASE</button>
      </div>
    </div>
  );
}
