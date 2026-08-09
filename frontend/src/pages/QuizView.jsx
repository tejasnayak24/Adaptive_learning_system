import React, { useEffect, useState } from 'react'
import { useParams, useNavigate, Link, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { quizService } from '../services/quizService'
import { lessonService } from '../services/lessonService'
import { progressService } from '../services/progressService'
import { rlService } from '../services/rlService'

export default function QuizView() {
  const { id } = useParams() // Quiz ID
  const { user } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  // Loading & error states
  const [loading, setLoading] = useState(true)
  const [submitLoading, setSubmitLoading] = useState(false)
  const [error, setError] = useState('')

  // Core quiz content
  const [quiz, setQuiz] = useState(null)
  const [lesson, setLesson] = useState(null)
  const [questions, setQuestions] = useState([])
  const [progressHistory, setProgressHistory] = useState([])

  // Quiz execution states
  const [allLessons, setAllLessons] = useState([])
  const [currentQuestionIdx, setCurrentQuestionIdx] = useState(0)
  const [selectedAnswers, setSelectedAnswers] = useState({})
  const [hintsRevealed, setHintsRevealed] = useState({})
  const [hintsCount, setHintsCount] = useState(0)
  const [secondsElapsed, setSecondsElapsed] = useState(0)

  // Quiz submission & results states
  const [isFinished, setIsFinished] = useState(false)
  const [results, setResults] = useState(null)
  const [rlRecommendation, setRlRecommendation] = useState(null)

  // Load quiz details, associated lesson, and student progress logs
  useEffect(() => {
    async function loadQuizData() {
      try {
        setError('')
        // Use GET /quiz/{quizId} to fetch quiz questions and metadata
        const quizRes = await quizService.getQuiz(id)
        if (!quizRes.success) {
          throw new Error('Could not load quiz details')
        }
        
        const quizData = quizRes.data.quiz
        const questionsList = quizRes.data.questions
        setQuiz(quizData)
        setQuestions(questionsList)

        // Load the lesson to get subject, topic info
        const lessonRes = await lessonService.getLesson(quizData.lesson_id)
        if (lessonRes.success) {
          setLesson(lessonRes.data)
        }

        // Load all lessons to determine next sequential lesson
        const allLessonsRes = await lessonService.getLessons()
        if (allLessonsRes.success) {
          setAllLessons(allLessonsRes.data)
        }

        // Load overall progress history to compute historical inputs for RL
        const progressRes = await progressService.getStudentProgress(user.id)
        if (progressRes.success) {
          setProgressHistory(progressRes.data)
        }
      } catch (err) {
        setError(err.message || 'Failed to initialize quiz')
      } finally {
        setLoading(false)
      }
    }
    loadQuizData()
  }, [id, user.id])

  // Timer effect
  useEffect(() => {
    if (loading || isFinished) return
    const timer = setInterval(() => {
      setSecondsElapsed((prev) => prev + 1)
    }, 1000)
    return () => clearInterval(timer)
  }, [loading, isFinished])

  if (loading) {
    return (
      <div className="flex h-[70vh] items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="h-10 w-10 animate-spin rounded-full border-4 border-teal-500/20 border-t-teal-500"></div>
          <p className="text-sm font-semibold tracking-wider text-slate-400 animate-pulse font-display uppercase">
            Downloading Assessment Questions...
          </p>
        </div>
      </div>
    )
  }

  if (error || !quiz || !lesson) {
    return (
      <div className="max-w-md mx-auto space-y-6 text-center py-12">
        <div className="text-5xl">⚠️</div>
        <h3 className="text-xl font-bold text-white">Assessment Error</h3>
        <p className="text-sm text-slate-400">{error || 'Failed to load quiz metadata.'}</p>
        <Link to="/subjects" className="inline-flex px-5 py-2.5 rounded-xl bg-indigo-500 text-white font-semibold text-xs transition-colors">
          Return to Curriculum
        </Link>
      </div>
    )
  }

  const currentQuestion = questions[currentQuestionIdx]

  const handleSelectOption = (opt) => {
    setSelectedAnswers({
      ...selectedAnswers,
      [currentQuestion.id]: opt
    })
  }

  const handleRevealHint = () => {
    if (!hintsRevealed[currentQuestion.id]) {
      setHintsRevealed({
        ...hintsRevealed,
        [currentQuestion.id]: true
      })
      setHintsCount(prev => prev + 1)
    }
  }

  const handleNext = () => {
    if (currentQuestionIdx < questions.length - 1) {
      setCurrentQuestionIdx(currentQuestionIdx + 1)
    }
  }

  const handlePrev = () => {
    if (currentQuestionIdx > 0) {
      setCurrentQuestionIdx(currentQuestionIdx - 1)
    }
  }

  const handleSubmitQuiz = async () => {
    // Grade the quiz using backend correctness contract
    let correctCount = 0
    questions.forEach((q) => {
      const selected = selectedAnswers[q.id]
      if (selected === q.correct_answer) {
        correctCount++
      }
    })

    const finalScore = Math.round((correctCount / questions.length) * 100)
    
    // Calculate actual historical average attention score from past attempts
    const hasHistory = progressHistory && progressHistory.length > 0
    const historicalAttention = hasHistory
      ? progressHistory.reduce((sum, p) => sum + p.attention_score, 0) / progressHistory.length
      : null

    // Resolve subject dynamically from backend data
    const resolvedSubject = location.state?.subject || quiz.subject || lesson.subject || undefined

    setSubmitLoading(true)
    try {
      // 1. Submit quiz results to backend to save student progress
      const submitRes = await quizService.submitQuiz({
        studentId: user.id,
        lessonId: lesson.id,
        quizScore: finalScore,
        responseTime: secondsElapsed,
        attentionScore: historicalAttention !== null ? historicalAttention : undefined,
        difficulty: quiz.difficulty
      })

      if (!submitRes.success) {
        throw new Error('Failed to save assessment progress logs')
      }

      // Compute context variables for the RL recommender based on updated history
      const updatedProgressHistory = [...progressHistory, submitRes.data]
      const sortedHistory = [...updatedProgressHistory].sort((a, b) => b.id - a.id)
      
      const previousAttempt = sortedHistory[1] || { quiz_score: 0 }
      const completedLessonsCount = new Set(
        updatedProgressHistory.filter(p => p.completed).map(p => p.lesson_id)
      ).size
      const attemptsCount = updatedProgressHistory.filter(p => p.lesson_id === lesson.id).length

      // 2. Fetch the adaptive recommendation from the RL engine
      let rlRes = null
      try {
        const payload = {
          subject: resolvedSubject,
          topic: lesson.topic,
          lesson: lesson.title,
          previous_quiz_score: Math.round(previousAttempt.quiz_score),
          current_quiz_score: finalScore,
          difficulty: quiz.difficulty,
          response_time: secondsElapsed,
          hints_used: hintsCount,
          lesson_attempts: attemptsCount,
          completed_lessons: completedLessonsCount
        }

        if (historicalAttention !== null) {
          payload.attention_score = historicalAttention
        }

        rlRes = await rlService.getRecommendation(payload)
      } catch (rlErr) {
        console.error('RL recommendation failed:', rlErr)
        rlRes = { error: 'Unable to get an adaptive recommendation: Telemetry is offline.' }
      }

      setResults({
        score: finalScore,
        correctCount,
        totalQuestions: questions.length,
        timeTaken: secondsElapsed,
        attentionUsed: null,
        yawned: null,
        lookedAway: null
      })
      setRlRecommendation(rlRes)
      setIsFinished(true)
    } catch (err) {
      alert(err.message || 'Error occurred during grading submission')
    } finally {
      setSubmitLoading(false)
    }
  }

  // Next steps router mapping for the RL action buttons on Results Screen
  const renderNextStepsButton = () => {
    if (!rlRecommendation) return null

    const action = rlRecommendation.action
    const explanation = rlRecommendation.explanation

    // Determine the target quiz difficulty progression
    const getQuizOfDifficulty = (diff) => {
      return lesson.quizzes.find(q => q.difficulty.toLowerCase() === diff.toLowerCase())
    }

    if (action === 'INCREASE_DIFFICULTY') {
      const nextDiff = quiz.difficulty.toUpperCase() === 'EASY' ? 'Medium' : 'Hard'
      const targetQuiz = getQuizOfDifficulty(nextDiff)
      return (
        <button
          onClick={() => {
            if (targetQuiz) navigate(`/quiz/${targetQuiz.id}`)
            else navigate('/subjects')
          }}
          className="px-6 py-3 rounded-xl bg-indigo-500 hover:bg-indigo-600 text-white font-bold text-sm shadow-md shadow-indigo-500/20 active:scale-[0.98] transform transition-all"
        >
          Calibrate to {nextDiff} Quiz &rarr;
        </button>
      )
    }

    if (action === 'DECREASE_DIFFICULTY') {
      const prevDiff = quiz.difficulty.toUpperCase() === 'HARD' ? 'Medium' : 'Easy'
      const targetQuiz = getQuizOfDifficulty(prevDiff)
      return (
        <button
          onClick={() => {
            if (targetQuiz) navigate(`/quiz/${targetQuiz.id}`)
            else navigate('/subjects')
          }}
          className="px-6 py-3 rounded-xl bg-amber-500 hover:bg-amber-600 text-white font-bold text-sm shadow-md shadow-amber-500/20 active:scale-[0.98] transform transition-all"
        >
          Return to {prevDiff} Quiz &rarr;
        </button>
      )
    }

    if (action === 'REPEAT_LESSON') {
      return (
        <button
          onClick={() => navigate(`/lesson/${lesson.id}`)}
          className="px-6 py-3 rounded-xl bg-slate-900 border border-slate-700 hover:bg-slate-800 text-slate-200 font-bold text-sm active:scale-[0.98] transform transition-all"
        >
          Review Lesson Material &rarr;
        </button>
      )
    }

    if (action === 'NEXT_LESSON') {
      // Find the next sequential lesson
      const sortedLessons = [...allLessons].sort((a, b) => a.id - b.id)
      const currentIdx = sortedLessons.findIndex(l => l.id === lesson.id)
      const nextLesson = currentIdx !== -1 && currentIdx < sortedLessons.length - 1 ? sortedLessons[currentIdx + 1] : null

      if (nextLesson) {
        return (
          <button
            onClick={() => navigate(`/lesson/${nextLesson.id}`)}
            className="px-6 py-3 rounded-xl bg-emerald-500 hover:bg-emerald-600 text-white font-bold text-sm shadow-md shadow-emerald-500/20 active:scale-[0.98] transform transition-all"
          >
            Advance to Next Lesson: {nextLesson.title} &rarr;
          </button>
        )
      }

      return (
        <button
          onClick={() => navigate('/subjects')}
          className="px-6 py-3 rounded-xl bg-emerald-500 hover:bg-emerald-600 text-white font-bold text-sm shadow-md shadow-emerald-500/20 active:scale-[0.98] transform transition-all"
        >
          Curriculum Complete! Back to Subjects &rarr;
        </button>
      )
    }

    if (action === 'FOCUS_RECOVERY') {
      return (
        <button
          onClick={() => {
            // Display standard breathe alert / relaxation guide modal then route back
            alert('Aegis Coach Break:\n\nTake a 30-second breathing break. Let your eyes focus away from the screen, take a deep breath in... and let it out. When ready, go back to study topics.')
            navigate('/subjects')
          }}
          className="px-6 py-3 rounded-xl bg-sky-500 hover:bg-sky-600 text-white font-bold text-sm shadow-md shadow-sky-500/20 active:scale-[0.98] transform transition-all"
        >
          Open Focus Recovery break &rarr;
        </button>
      )
    }

    // Default fallback to curriculum subjects
    return (
      <Link
        to="/subjects"
        className="px-6 py-3 rounded-xl bg-slate-900 border border-slate-700 hover:bg-slate-800 text-slate-200 font-bold text-sm active:scale-[0.98] transform transition-all inline-block"
      >
        Back to Subjects
      </Link>
    )
  }

  // 1. Render Results Page
  if (isFinished && results) {
    return (
      <div className="max-w-4xl mx-auto space-y-8 animate-fade-in">
        {/* Results Banner */}
        <div className="relative overflow-hidden rounded-3xl border border-slate-800 bg-gradient-to-br from-indigo-950/30 via-slate-900/40 to-slate-950 p-8 shadow-xl text-center">
          <div className="absolute top-0 left-1/2 -translate-x-1/2 h-36 w-36 bg-indigo-500/10 blur-3xl pointer-events-none"></div>
          <div className="space-y-4">
            <span className="inline-flex px-3 py-1 rounded-lg bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 text-xs font-bold uppercase tracking-wider">
              Assessment Results
            </span>
            <h1 className="text-4xl font-display font-extrabold text-white">
              Quiz score: <span className="bg-gradient-to-r from-indigo-400 to-teal-300 bg-clip-text text-transparent">{results.score}%</span>
            </h1>
            <p className="text-sm text-slate-400 max-w-md mx-auto">
              You correctly answered {results.correctCount} out of {results.totalQuestions} questions at <span className="text-white font-semibold">{quiz.difficulty}</span> difficulty level.
            </p>
          </div>
        </div>

        {/* Breakdown details */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Performance breakdown card */}
          <div className="glass-panel rounded-3xl p-6 border border-slate-900 shadow-md space-y-4">
            <h3 className="text-sm font-bold uppercase tracking-wider text-slate-500">Speed & Hints</h3>
            <div className="space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Response time</span>
                <span className="font-semibold text-white">{results.timeTaken} seconds</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Hints used</span>
                <span className="font-semibold text-white">{hintsCount} hints</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Tempo score</span>
                <span className="font-semibold text-teal-400">
                  {results.timeTaken < questions.length * 15 ? 'Fast' : results.timeTaken < questions.length * 35 ? 'Moderate' : 'Steady'}
                </span>
              </div>
            </div>
          </div>

          {/* Attention telemetry card */}
          <div className="glass-panel rounded-3xl p-6 border border-slate-900 shadow-md space-y-4">
            <h3 className="text-sm font-bold uppercase tracking-wider text-slate-500">Attention Telemetry</h3>
            <div className="space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Average attention</span>
                <span className="font-semibold text-slate-400">Unavailable</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Yawning observed</span>
                <span className="font-semibold text-slate-400">Unavailable</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Gaze stability</span>
                <span className="font-semibold text-slate-400">Unavailable</span>
              </div>
            </div>
          </div>

          {/* Calibrator details card */}
          <div className="glass-panel rounded-3xl p-6 border border-slate-900 shadow-md space-y-4">
            <h3 className="text-sm font-bold uppercase tracking-wider text-slate-500">Grading Log</h3>
            <div className="space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Subject</span>
                <span className="font-semibold text-white">Science</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Topic</span>
                <span className="font-semibold text-white truncate max-w-[120px] inline-block">{lesson.topic}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Sync status</span>
                <span className="font-semibold text-emerald-400">PostgreSQL saved</span>
              </div>
            </div>
          </div>
        </div>

        {/* AI Reinforcement Learning Recommendation Card */}
        {rlRecommendation && rlRecommendation.error ? (
          <div className="glass-panel rounded-3xl p-8 border border-slate-900 shadow-xl space-y-6 text-center">
            <p className="text-sm font-semibold text-rose-400">
              {rlRecommendation.error}
            </p>
            <p className="text-xs text-slate-500">
              The reinforcement learning engine could not resolve a recommendation.
            </p>
            <div className="pt-2">
              <Link
                to="/subjects"
                className="px-6 py-3 rounded-xl bg-slate-900 border border-slate-700 hover:bg-slate-800 text-slate-200 font-bold text-sm"
              >
                Back to Subjects
              </Link>
            </div>
          </div>
        ) : rlRecommendation && (
          <div className="glass-panel rounded-3xl p-8 border border-slate-900 shadow-xl space-y-6 relative overflow-hidden">
            <div className="absolute top-0 right-0 h-40 w-40 bg-teal-500/5 blur-3xl pointer-events-none"></div>
            
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-800/80 pb-4">
              <div>
                <h3 className="text-xl font-bold text-white flex items-center gap-2">
                  <span className="text-teal-400">✦</span> Reinforcement Learning Policy Decision
                </h3>
                <p className="text-xs text-slate-500 mt-1">
                  Generated by our Q-Learning Agent mapping student engagement metrics to target content difficulty
                </p>
              </div>

              <div className="shrink-0 flex items-center gap-2 bg-slate-900 border border-slate-800 rounded-2xl px-4 py-2">
                <span className="text-slate-500 text-[10px] uppercase font-bold tracking-wide">CONFIDENCE</span>
                <span className="text-teal-400 font-extrabold text-sm">{Math.round(rlRecommendation.confidence * 100)}%</span>
              </div>
            </div>

            <div className="space-y-4">
              {/* Action Banner */}
              <div className="flex flex-col gap-1.5">
                <span className="text-[10px] font-semibold text-indigo-400 uppercase tracking-wider">Suggested Pedagogical Action</span>
                <span className="text-2xl font-extrabold text-white bg-gradient-to-r from-indigo-300 to-indigo-100 bg-clip-text text-transparent">
                  {rlRecommendation.action.replace(/_/g, ' ')}
                </span>
              </div>

              {/* Justification text */}
              <div className="flex flex-col gap-1">
                <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider">Coach Justification</span>
                <p className="text-sm text-slate-300 italic leading-relaxed">
                  "{rlRecommendation.explanation}"
                </p>
              </div>
            </div>

            {/* CTA action buttons */}
            <div className="border-t border-slate-800/80 pt-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <span className="text-xs text-slate-400">
                Aegis adapted the curriculum sequence. Click the button to advance:
              </span>
              <div className="flex items-center gap-3">
                {renderNextStepsButton()}
              </div>
            </div>
          </div>
        )}
      </div>
    )
  }

  // 2. Render Quiz In-Progress Screen
  const hasSelected = selectedAnswers[currentQuestion.id] !== undefined
  const progressPercent = Math.round(((currentQuestionIdx + 1) / questions.length) * 100)

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      {/* Navigation Breadcrumb */}
      <div>
        <Link 
          to={`/lesson/${lesson.id}`} 
          className="inline-flex items-center gap-1 text-xs font-semibold uppercase tracking-wider text-slate-500 hover:text-slate-300 transition-colors"
        >
          &larr; Abort to Lesson
        </Link>
      </div>

      {/* Progress header */}
      <div className="glass-panel rounded-3xl p-6 border border-slate-900 shadow-md space-y-4">
        <div className="flex items-center justify-between text-xs">
          <div className="flex items-center gap-2">
            <span className="px-2 py-0.5 text-[9px] font-extrabold uppercase bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 rounded">
              {quiz.difficulty} Level
            </span>
            <span className="text-slate-600">&bull;</span>
            <span className="font-semibold text-slate-300 truncate max-w-[150px] inline-block">{quiz.title}</span>
          </div>
          
          <div className="flex items-center gap-4 text-slate-400 font-medium">
            <span>Question {currentQuestionIdx + 1} of {questions.length}</span>
            <span>Time: <span className="text-white font-semibold font-mono">{secondsElapsed}s</span></span>
          </div>
        </div>

        <div className="w-full bg-slate-950 rounded-full h-2 overflow-hidden">
          <div 
            className="bg-gradient-to-r from-indigo-500 to-teal-400 h-2 rounded-full transition-all duration-300"
            style={{ width: `${progressPercent}%` }}
          ></div>
        </div>
      </div>

      {/* Question Panel */}
      <div className="glass-panel rounded-3xl p-8 border border-slate-900 shadow-lg space-y-8 min-h-[300px] flex flex-col justify-between">
        <div className="space-y-6">
          <h2 className="text-lg md:text-xl font-bold text-white leading-relaxed">
            {currentQuestion.question}
          </h2>

          {/* Answer option choices */}
          <div className="grid grid-cols-1 gap-4">
            {['A', 'B', 'C', 'D'].map((letter) => {
              const optText = currentQuestion[`option_${letter.toLowerCase()}`]
              const isSelected = selectedAnswers[currentQuestion.id] === letter
              
              return (
                <button
                  key={letter}
                  onClick={() => handleSelectOption(letter)}
                  className={`w-full flex items-center gap-4 text-left p-4 rounded-2xl border transition-all duration-200 ${
                    isSelected 
                      ? 'bg-indigo-500/10 border-indigo-500 text-white shadow-inner font-medium' 
                      : 'bg-slate-900/30 border-slate-800/80 hover:border-slate-700/60 text-slate-300'
                  }`}
                >
                  <span className={`flex h-7 w-7 shrink-0 items-center justify-center rounded-xl text-xs font-bold border transition-colors ${
                    isSelected 
                      ? 'bg-indigo-500 border-indigo-500 text-white' 
                      : 'bg-slate-950 border-slate-800 text-slate-500'
                  }`}>
                    {letter}
                  </span>
                  <span className="text-sm">{optText}</span>
                </button>
              )
            })}
          </div>
        </div>

        {/* Hint button details */}
        <div className="border-t border-slate-800/80 pt-6 flex items-center justify-between gap-4">
          <div>
            {hintsRevealed[currentQuestion.id] ? (
              <div className="text-xs text-indigo-400 leading-relaxed font-medium">
                💡 Hint: Review the core reading sections matching the topic of {lesson.topic}.
              </div>
            ) : (
              <button
                onClick={handleRevealHint}
                className="text-xs font-semibold text-slate-500 hover:text-slate-300 transition-colors flex items-center gap-1"
              >
                💡 Need a hint?
              </button>
            )}
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={handlePrev}
              disabled={currentQuestionIdx === 0}
              className="px-4 py-2 rounded-xl bg-slate-950 hover:bg-slate-900 border border-slate-800 text-xs font-semibold text-slate-400 hover:text-slate-200 disabled:opacity-30 disabled:cursor-not-allowed transition-all"
            >
              Previous
            </button>

            {currentQuestionIdx < questions.length - 1 ? (
              <button
                onClick={handleNext}
                className="px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-xs font-semibold text-slate-200 hover:text-white transition-all"
              >
                Next
              </button>
            ) : (
              <button
                onClick={handleSubmitQuiz}
                disabled={submitLoading || Object.keys(selectedAnswers).length < questions.length}
                className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-indigo-500 to-indigo-600 hover:from-indigo-600 hover:to-indigo-700 text-xs font-bold text-white shadow-md shadow-indigo-500/20 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
              >
                {submitLoading ? 'Grading...' : 'Submit quiz'}
              </button>
            )}
          </div>
        </div>

      </div>
    </div>
  )
}
