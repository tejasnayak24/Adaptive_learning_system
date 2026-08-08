import { useEffect, useState } from "react";
import attentionService from "../services/attentionService";

function AttentionWidget({ studentId }) {
  const [attention, setAttention] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    attentionService
      .getLatestAttention(studentId)
      .then((res) => {
        // backend may return normalized 0.0-1.0 or percentage
        let val = res?.attention_score ?? res?.score ?? res?.value ?? res;
        if (val == null) throw new Error("No attention value");
        if (typeof val === "number") {
          if (val <= 1.0) val = Math.round(val * 100);
          else val = Math.round(val);
        }
        if (mounted) setAttention(val);
      })
      .catch((err) => mounted && setError(err.message || "Failed to load"))
      .finally(() => mounted && setLoading(false));

    return () => (mounted = false);
  }, [studentId]);

  const display = loading ? "--" : error ? "N/A" : `${attention}%`;

  return (
    <div className="bg-white rounded-xl shadow-md p-6">

      <h2 className="text-2xl font-bold mb-6">AI Attention Monitor</h2>

      <div className="flex justify-center">

        <div className="relative w-44 h-44">

          <svg className="w-44 h-44 rotate-[-90deg]">

            <circle cx="88" cy="88" r="70" stroke="#E5E7EB" strokeWidth="12" fill="none" />

            <circle
              cx="88"
              cy="88"
              r="70"
              stroke="#2563EB"
              strokeWidth="12"
              fill="none"
              strokeDasharray={440}
              strokeDashoffset={
                loading || error || attention == null ? 440 : 440 - (440 * Math.min(Math.max(attention, 0), 100)) / 100
              }
              strokeLinecap="round"
            />

          </svg>

          <div className="absolute inset-0 flex flex-col justify-center items-center">

            <h1 className="text-4xl font-bold">{display}</h1>

            <p className="text-gray-500">Focus</p>

          </div>

        </div>

      </div>

      <p className="text-center text-gray-600 mt-6">{error ? error : "Current attention level"}</p>

    </div>
  );
}

export default AttentionWidget;