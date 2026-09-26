export default function QuestionCounter({ remaining }) {
  return <div className="counterBlock"><span>QUESTIONS LEFT</span><b>{String(remaining).padStart(2, "0")}</b></div>;
}
