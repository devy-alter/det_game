import { useState } from "react";
import { askQuestionStream, restartGame, startGame } from "../services/gameApi";

export function useGame() {
  const [state, setState] = useState(null);
  const [caseData, setCaseData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function start(caseId, cases) {
    setError("");
    setLoading(true);
    try {
      const next = await startGame(caseId);
      setState(next);
      setCaseData(cases.find((c) => c.id === caseId) || null);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  async function ask(question, { onDone } = {}) {
    if (!state) return null;
    setError("");
    setLoading(true);
    let finalState = null;
    try {
      await askQuestionStream(state.game_id, question, (event) => {
        if (event.type === "suspect_start") {
          setState((prev) => ({
            ...prev,
            pending_question: event.question_number,
            history: [...prev.history, {
              question_number: event.question_number,
              detective_question: event.detective_question,
              suspect_response: "",
              pending: true,
              room_pressure: prev.history.at(-1)?.room_pressure || "low",
            }],
          }));
        }
        if (event.type === "suspect_chunk") {
          setState((prev) => ({
            ...prev,
            history: prev.history.map((item) => item.question_number === event.question_number ? { ...item, suspect_response: item.suspect_response + event.text } : item),
          }));
        }
        if (event.type === "suspect_done") {
          setState((prev) => ({
            ...prev,
            history: prev.history.map((item) => item.question_number === event.question_number ? { ...item, suspect_response: event.suspect_response } : item),
          }));
          onDone?.();
        }
        if (event.type === "state") {
          finalState = event;
          setState((prev) => {
            const history = prev.history.map((item) => item.question_number === event.question_number ? {
              ...item,
              pending: false,
              confidence_after: event.confidence,
              progress_after: event.confession_progress,
              room_pressure: event.room_pressure,
            } : item);
            return { ...prev, ...event, history, pending_question: null };
          });
        }
      });
      return finalState;
    } catch (e) {
      setError(e.message);
      setState((prev) => prev ? { ...prev, history: prev.history.filter((item) => !item.pending) } : prev);
      return null;
    } finally {
      setLoading(false);
    }
  }

  async function restart() {
    if (!state) return;
    setError("");
    setLoading(true);
    try {
      const next = await restartGame(state.game_id);
      setState(next);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return { state, caseData, loading, error, start, ask, restart, setError };
}
