import api from './api'

export const rlService = {
  async getRecommendation(data) {
    // Ensures numerical fields are integers/floats as enforced by Pydantic schemas
    const payload = {
      subject: data.subject,
      topic: data.topic,
      lesson: data.lesson,
      previous_quiz_score: Math.round(data.previous_quiz_score),
      current_quiz_score: Math.round(data.current_quiz_score),
      attention_score: parseFloat(data.attention_score),
      yawning: !!data.yawning,
      looking_away: !!data.looking_away,
      difficulty: data.difficulty.toUpperCase(), // Norm to EASY/MEDIUM/HARD
      response_time: parseFloat(data.response_time),
      hints_used: parseInt(data.hints_used, 10) || 0,
      lesson_attempts: parseInt(data.lesson_attempts, 10),
      completed_lessons: parseInt(data.completed_lessons, 10)
    }
    return await api.post('/rl/recommend', payload)
  }
}
