export default function ConfidenceMeter({ value, label, variant = "confidence" }) {
  const tone = value <= 20 ? "critical" : value <= 45 ? "danger" : value <= 70 ? "warn" : "safe";
  return (
    <div className={`meterBlock ${variant} tone_${tone}`}>
      <div className="meterTop"><span>{label}</span><b>{value}%</b></div>
      <div className="meterTrack"><div style={{ width: `${value}%` }} /></div>
    </div>
  );
}
