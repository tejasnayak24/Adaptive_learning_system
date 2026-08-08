import api from "./api";

async function getRecommendation(payload) {
  // payload must match RecommendationRequest schema
  return api.post(`/rl/recommend`, payload);
}

export default { getRecommendation };
