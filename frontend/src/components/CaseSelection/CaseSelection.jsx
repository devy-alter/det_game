export default function CaseSelection({ cases, onStart, loading }) {
  if (!cases.length) return <div className="emptyCases">No case files are available. Start the backend and verify the case directory.</div>;
  return (
    <div className="caseGrid">
      {cases.map((c, index) => (
        <button className="archiveFile" key={c.id} onClick={() => onStart(c.id)} disabled={loading}>
          <div className="archiveTop"><span>FILE {String(index + 1).padStart(2, "0")}</span><b>{c.difficulty.toUpperCase()}</b></div>
          <div className="archiveRule" />
          <div className="archiveType">{c.crime.type.toUpperCase()}</div>
          <h3>{c.title}</h3>
          <p>{c.description}</p>
          <div className="archiveBottom"><span>{c.crime.location}</span><b>{loading ? "OPENING..." : "OPEN FILE"}</b></div>
        </button>
      ))}
    </div>
  );
}
