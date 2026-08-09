import api from './api'

export const rlService = {
  async getRecommendation(data) {
    // Ensures numerical fields are integers/floats as enforced by Pydantic schemas
    const payload = {
      subject: data.subject,
      topic: data.topic,
      lesson: data.lesson,
      previous_quiz_score: data.previous_quiz_score !== undefined ? Math.round(data.previous_quiz_score) : undefined,
      current_quiz_score: data.current_quiz_score !== undefined ? Math.round(data.current_quiz_score) : undefined,
      difficulty: data.difficulty ? data.difficulty.toUpperCase() : undefined, // Norm to EASY/MEDIUM/HARD
      response_time: data.response_time !== undefined ? parseFloat(data.response_time) : undefined,
      hints_used: data.hints_used !== undefined ? parseInt(data.hints_used, 10) : undefined,
      lesson_attempts: data.lesson_attempts !== undefined ? parseInt(data.lesson_attempts, 10) : undefined,
      completed_lessons: data.completed_lessons !== undefined ? parseInt(data.completed_lessons, 10) : undefined
    }

    if (data.attention_score !== undefined && data.attention_score !== null) {
      payload.attention_score = parseFloat(data.attention_score)
    }

    if (data.yawning !== undefined && data.yawning !== null) {
      payload.yawning = data.yawning
    }

    if (data.looking_away !== undefined && data.looking_away !== null) {
      payload.looking_away = data.looking_away
    }

    return await api.post('/rl/recommend', payload)
  }
}

