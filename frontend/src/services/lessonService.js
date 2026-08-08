import api from "./api";

async function getAllLessons() {
  // Try common endpoints until one works
  const candidates = ["/lessons", "/lesson", "/api/lessons"];
  for (const path of candidates) {
    try {
      const res = await api.get(path);
      // Normalize response shapes: { data: [...] } or [...] or { lessons: [...] }
      if (Array.isArray(res)) return res;
      if (Array.isArray(res?.data)) return res.data;
      if (Array.isArray(res?.lessons)) return res.lessons;
    } catch (e) {
      // try next
    }
  }
  throw new Error("Failed to fetch lessons from backend");
}

async function getLessonById(id) {
  const candidates = [`/lesson/${id}`, `/lessons/${id}`, `/api/lesson/${id}`];
  for (const path of candidates) {
    try {
      const res = await api.get(path);
      if (res?.data) return res.data;
      if (res) return res;
    } catch (e) {
      // try next
    }
  }
  throw new Error("Failed to fetch lesson");
}

export default { getAllLessons, getLessonById };
