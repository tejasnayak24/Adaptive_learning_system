import api from "./api";

async function getQuiz(quizId) {
  return api.get(`/quiz/${quizId}`);
}

async function startQuiz(quizId) {
  return api.post(`/quiz/start`, { quiz_id: quizId });
}

async function submitQuiz(payload) {
  // payload expected to match QuizSubmitRequest
  return api.post(`/quiz/submit`, payload);
}

export default { getQuiz, startQuiz, submitQuiz };
