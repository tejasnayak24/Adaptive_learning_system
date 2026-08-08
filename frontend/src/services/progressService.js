import api from "./api";

async function getStudentProgress(studentId) {
  return api.get(`/progress/${studentId}`);
}

async function getLessonProgress(studentId, lessonId) {
  return api.get(`/progress/${studentId}/${lessonId}`);
}

async function updateProgress(progressId, body) {
  return api.put(`/progress/${progressId}`, body);
}

export default { getStudentProgress, getLessonProgress, updateProgress };
