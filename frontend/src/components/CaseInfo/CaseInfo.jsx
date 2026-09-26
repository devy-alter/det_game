export default function CaseInfo({ caseData }) {
  if (!caseData) return null;
  return (
    <aside className="caseFile">
      <div className="fileStamp">CASE FILE</div>
      <div className="fileHeader">
        <div><span>FILE ID</span><b>{caseData.id.toUpperCase()}</b></div>
        <div><span>CLASS</span><b>{caseData.difficulty.toUpperCase()}</b></div>
      </div>
      <div className="fileTitle">
        <span>ACTIVE INVESTIGATION</span>
        <h2>{caseData.title}</h2>
        <p>{caseData.description}</p>
      </div>
      <div className="fileFacts">
        <div><span>VICTIM</span><b>{caseData.crime.victim}</b></div>
        <div><span>SCENE</span><b>{caseData.crime.location}</b></div>
        <div><span>EST. TIME</span><b>{caseData.crime.time}</b></div>
        <div><span>SUSPECT</span><b>{caseData.suspect.name}</b><small>{caseData.suspect.occupation}</small></div>
      </div>
      <div className="fileAlibi">
        <span>STATEMENT ON RECORD</span>
        <p>“{caseData.alibi_claim}”</p>
      </div>
      <div className="evidenceHeading"><span>KNOWN EVIDENCE</span><b>{caseData.evidence.length.toString().padStart(2, "0")}</b></div>
      <div className="evidenceList">
        {caseData.evidence.map((e) => (
          <article className="evidenceCard" key={e.id}>
            <div className="evidenceMeta"><span>{e.id.toUpperCase()}</span><b>{e.strength}/10</b></div>
            <h3>{e.name}</h3>
            <p>{e.description}</p>
          </article>
        ))}
      </div>
      <div className="fileFooter"><span>CONFIDENTIAL</span><span>DO NOT DISTRIBUTE</span></div>
    </aside>
  );
}
