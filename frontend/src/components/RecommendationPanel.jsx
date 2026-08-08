import { useEffect, useState } from "react";
import recommendationService from "../services/recommendationService";
import { useAuth } from "../context/AuthContext";

function RecommendationPanel() {
  const { user } = useAuth();
  const [rec, setRec] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!user) return;
    // No automatic call without context; the UI should get rec after quiz submission.
    // Keep this component ready to display `rec` when provided via props or global state.
  }, [user]);

  if (!rec) {
    return (
      <div className="bg-white rounded-xl shadow-md p-6">
        <h2 className="text-2xl font-bold mb-6">AI Recommendation</h2>
        <p className="text-gray-500">No recommendation yet. Take a quiz to get a recommendation.</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <h2 className="text-2xl font-bold mb-6">AI Recommendation</h2>
      <div className="space-y-4">
        <div className="border rounded-lg p-4">
          <h3 className="font-semibold text-lg">{rec.action}</h3>
          <p className="text-gray-500">Confidence: {rec.confidence}</p>
          <p className="text-gray-500 mt-2">{rec.explanation}</p>
        </div>
      </div>
    </div>
  );
}

export default RecommendationPanel;