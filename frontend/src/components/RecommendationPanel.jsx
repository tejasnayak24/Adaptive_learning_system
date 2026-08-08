import { useEffect, useState } from "react";
import recommendationService from "../services/recommendationService";
import { useAuth } from "../context/AuthContext";

function RecommendationPanel({ recommendation }) {
  const { user } = useAuth();
  const [rec, setRec] = useState(recommendation ?? null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (recommendation) {
      setRec(recommendation);
      return;
    }

    // Try to fetch latest recommendation for user if endpoint exists
    let mounted = true;
    const fetchLatest = async () => {
      if (!user) return;
      setLoading(true);
      try {
        const candidates = ["/rl/latest", "/rl/recommendation", "/rl/recent"];
        for (const p of candidates) {
          try {
            const r = await recommendationService.getRecommendation({ _probe: true, _path: p });
            const data = r?.data ?? r;
            if (data) {
              if (mounted) setRec(data);
              break;
            }
          } catch (e) {
            // try next
          }
        }
      } catch (e) {
        if (mounted) setError(e.message || "Failed to load recommendation");
      } finally {
        if (mounted) setLoading(false);
      }
    };
    fetchLatest();
    return () => (mounted = false);
  }, [user, recommendation]);

  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-md p-6">Loading recommendation...</div>
    );
  }

  if (!rec) {
    return (
      <div className="bg-white rounded-xl shadow-md p-6">
        <h2 className="text-2xl font-bold mb-6">AI Recommendation</h2>
        <p className="text-gray-500">No recommendation yet. Take a quiz to get a recommendation.</p>
      </div>
    );
  }

  const action = rec.action ?? rec.data?.action ?? JSON.stringify(rec?.action ?? rec?.data ?? "");
  const confidence = rec.confidence ?? rec.data?.confidence;
  const explanation = rec.explanation ?? rec.data?.explanation ?? rec.data?.reason;

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <h2 className="text-2xl font-bold mb-6">AI Recommendation</h2>
      <div className="space-y-4">
        <div className="border rounded-lg p-4">
          <h3 className="font-semibold text-lg">{action}</h3>
          {confidence !== undefined && <p className="text-gray-500">Confidence: {confidence}</p>}
          {explanation && <p className="text-gray-500 mt-2">{explanation}</p>}
        </div>
      </div>
    </div>
  );
}

export default RecommendationPanel;