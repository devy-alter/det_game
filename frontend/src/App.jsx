import { useEffect, useMemo, useState } from "react";
import { getGamesCases } from "./services/gameApi";
import { useGame } from "./hooks/useGame";
import CaseSelection from "./components/CaseSelection/CaseSelection";
import GameHeader from "./components/GameHeader/GameHeader";
import CaseInfo from "./components/CaseInfo/CaseInfo";
import ConfidenceMeter from "./components/Confidence/ConfidenceMeter";
import QuestionCounter from "./components/QuestionCounter/QuestionCounter";
import ChatHistory from "./components/Interrogation/ChatHistory";
import DetectiveInput from "./components/Interrogation/DetectiveInput";
import GameOverModal from "./components/Modals/GameOverModal";
import SuspectPresence from "./components/SuspectPresence/SuspectPresence";

export default function App() {
  const [cases, setCases] = useState([]);
  const [sceneState, setSceneState] = useState("idle");
  const game = useGame();

  useEffect(() => {
    let mounted = true;
    getGamesCases()
      .then((data) => mounted && setCases(data))
      .catch((e) => mounted && game.setError?.(e.message));
    return () => { mounted = false; };
  }, []);

  const latest = game.state?.history?.at(-1);
  const pressure = latest?.room_pressure || "low";
  const reaction = useMemo(() => {
    if (sceneState === "thinking") return "thinking";
    if (sceneState === "answering") return "answering";
    if (pressure === "critical") return "critical";
    if (pressure === "high") return "tense";
    if (pressure === "medium") return "uneasy";
    return "composed";
  }, [sceneState, pressure]);

  async function ask(question) {
    setSceneState("answering");
    try {
      const result = await game.ask(question, {
        onDone: () => setSceneState("thinking"),
      });
      if (result) setSceneState(result.status === "active" ? "idle" : "broken");
    } finally {
      window.setTimeout(() => setSceneState("idle"), 700);
    }
  }

  if (!game.state) {
    return (
      <main className="menuScene">
        <div className="menuAtmosphere" />
        <header className="menuHeader">
          <span>BLACKWOOD POLICE DEPARTMENT</span>
          <span>CASE DIVISION / LIVE INTERROGATION</span>
        </header>
        <section className="menuHero">
          <div className="eyebrow">INTERROGATION SIMULATION</div>
          <h1>Read the room.<br /><em>Break the lie.</em></h1>
          <p>Ten questions. One suspect. Every answer changes the pressure in the room. Build a contradiction, expose the story, and force the confession.</p>
        </section>
        <div className="caseSelectionHeader">
          <div><span>CASE ARCHIVE</span><b>{cases.length.toString().padStart(2, "0")} ACTIVE FILES</b></div>
          <small>SELECT A CASE TO ENTER THE ROOM</small>
        </div>
        <CaseSelection cases={cases} onStart={(id) => game.start(id, cases)} loading={game.loading} />
        {game.error && <div className="error menuError">{game.error}</div>}
      </main>
    );
  }

  const cd = game.caseData || cases.find((c) => c.id === game.state.case_id);
  const history = game.state.history || [];

  return (
    <main className={`interrogationScene room_${reaction}`}>
      <div className="roomAmbient" />
      <div className="roomCeilingLight" />
      <div className="roomNoise" />
      <GameHeader state={game.state} caseData={cd} />

      <div className="interrogationLayout">
        <CaseInfo caseData={cd} />

        <section className="interrogationCore">
          <div className="roomPlate">
            <div><span>INTERVIEW ROOM 04</span><b>ACTIVE RECORDING</b></div>
            <div><span>CASE {cd?.id?.toUpperCase()}</span><b>{game.state.question_count.toString().padStart(2, "0")} / 10</b></div>
          </div>

          <div className="pressureStrip">
            <ConfidenceMeter value={game.state.confidence} label="SUSPECT COMPOSURE" />
            <ConfidenceMeter value={game.state.confession_progress} label="CASE PRESSURE" variant="pressure" />
            <QuestionCounter remaining={game.state.questions_remaining} />
          </div>

          <div className="theater">
            <div className="theaterBackdrop" />
            <div className="theaterTable" />
            <div className="dialogueColumn">
              <div className="dialogueHeader">
                <span>INTERROGATION RECORD</span>
                <span>{history.length ? `${history.length} EXCHANGES` : "RECORDING STARTING"}</span>
              </div>

              <div className="dialogueHistory">
                <ChatHistory history={history} />
              </div>

              <div className="liveExchange">
                <div className="liveRule"><span>{latest ? `QUESTION ${String(latest.question_number).padStart(2, "0")}` : "OPENING"}</span><b>{sceneState === "answering" ? "THE ROOM IS LISTENING" : sceneState === "thinking" ? "THE SUSPECT IS THINKING" : "INTERROGATION LIVE"}</b></div>
                {latest ? (
                  <div className="exchangeText">
                    <div className="detectiveLine"><span>DETECTIVE</span><p>{latest.detective_question}</p></div>
                    <div className="suspectLine"><span>ETHAN COLE</span><p>{latest.suspect_response || "..."}</p></div>
                  </div>
                ) : (
                  <div className="openingLine"><span>YOUR FIRST QUESTION</span><p>The suspect is in the room. Start with something that makes the story difficult to maintain.</p></div>
                )}
              </div>

              <DetectiveInput disabled={game.loading || game.state.status !== "active"} remaining={game.state.questions_remaining} onAsk={ask} />
              {game.error && <div className="error roomError">{game.error}</div>}
            </div>

            <SuspectPresence confidence={game.state.confidence} pressure={reaction} name={cd?.suspect?.name} />
          </div>
        </section>
      </div>

      <GameOverModal state={game.state} onRestart={() => { game.restart(); setSceneState("idle"); }} />
    </main>
  );
}
