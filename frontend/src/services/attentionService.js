import api from "./api";

// Provides access to facial-analysis/attention data from backend
async function getLatestAttention(studentId) {
  // Try common endpoints
  const candidates = [`/attention`, `/integration/attention`, `/attention/${studentId}`];
  for (const path of candidates) {
    try {
      const res = await api.get(path);
      if (res?.data) return res.data;
      return res;
    } catch (e) {
      // try next
    }
  }
  throw new Error("No attention data available from backend");
}

export default { getLatestAttention };
