import React, { useEffect, useState } from 'react'
import { useParams, useNavigate, Link, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { quizService } from '../services/quizService'
import { lessonService } from '../services/lessonService'
import { progressService } from '../services/progressService'
import { rlService } from '../services/rlService'

export default function QuizView() {
  const { id } = useParams()
  const { user } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  const [loading, setLoading] = useState(true)
  const [submitLoading, setSubmitLoading] = useState(false)
  const [error, setError] = useState('')

  const [quiz, setQuiz] = useState(null)
  const [lesson, setLesson] = useState(null)
  const [questions, setQuestions] = useState([])
  const [progressHistory, setProgressHistory] = useState([])
  const [allLessons, setAllLessons] = useState([])

  const [currentQuestionIdx, setCurrentQuestionIdx] = useState(0)
  const [selectedAnswers, setSelectedAnswers] = useState({})
  const [hintsRevealed, setHintsRevealed] = useState({})
  const [hintsCount, setHintsCount] = useState(0)
  const [secondsElapsed, setSecondsElapsed] = useState(0)

  const [isFinished, setIsFinished] = useState(false)
  const [results, setResults] = useState(null)
  const [rlRecommendation, setRlRecommendation] = useState(null)

  const resetQuizTelemetry = async () => {
    try {
      const studentId = user?.id ?? user?.sub

      if (!studentId) {
        console.warn(
          'No student ID available for telemetry reset.'
        )
        return
      }

      await fetch(
        `/api/attention/${studentId}/reset`,
        {
          method: 'POST',
        }
      )
    } catch (err) {
      console.error(
        'Failed to reset quiz telemetry:',
        err
      )
    }
  }

  useEffect(() => {
    async function loadQuizData() {
      try {
        setError('')

        await resetQuizTelemetry()

        const quizRes = await quizService.getQuiz(id)

        if (!quizRes.success) {
          throw new Error('Could not load quiz details')
        }

        const quizData = quizRes.data.quiz
        const questionsList = quizRes.data.questions || []

        setQuiz(quizData)
        setQuestions(questionsList)

        const lessonRes = await lessonService.getLesson(
          quizData.lesson_id
        )

        if (lessonRes.success) {
          setLesson(lessonRes.data)
        } else {
          throw new Error('Could not load lesson details')
        }

        try {
          const allLessonsRes =
            await lessonService.getLessons()

          if (allLessonsRes.success) {
            setAllLessons(allLessonsRes.data || [])
          }
        } catch (lessonListError) {
          console.warn(
            'Could not load all lessons:',
            lessonListError
          )
          setAllLessons([])
        }

        try {
          const studentId = user?.id ?? user?.sub

          if (studentId) {
            const progressRes =
              await progressService.getStudentProgress(
                studentId
              )

            if (progressRes.success) {
              setProgressHistory(
                progressRes.data || []
              )
            }
          }
        } catch (progressError) {
          console.warn(
            'Progress could not be loaded:',
            progressError
          )

          setProgressHistory([])
        }
      } catch (err) {
        console.error(
          'Quiz initialization error:',
          err
        )

        setError(
          err.message ||
            'Failed to initialize quiz'
        )
      } finally {
        setLoading(false)
      }
    }

    loadQuizData()
  }, [id, user?.id, user?.sub])

  useEffect(() => {
    if (loading || isFinished) {
      return
    }

    const timer = setInterval(() => {
      setSecondsElapsed((previous) => previous + 1)
    }, 1000)

    return () => clearInterval(timer)
  }, [loading, isFinished])

  if (loading) {
    return (
      <div className="flex h-[70vh] items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="h-10 w-10 animate-spin rounded-full border-4 border-teal-500/20 border-t-teal-500" />

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

        <h3 className="text-xl font-bold text-white">
          Assessment Error
        </h3>

        <p className="text-sm text-slate-400">
          {error ||
            'Failed to load quiz metadata.'}
        </p>

        <Link
          to="/subjects"
          className="inline-flex px-5 py-2.5 rounded-xl bg-indigo-500 text-white font-semibold text-xs"
        >
          Return to Curriculum
        </Link>
      </div>
    )
  }

  if (!questions.length) {
    return (
      <div className="max-w-md mx-auto space-y-6 text-center py-12">
        <div className="text-5xl">⚠️</div>

        <h3 className="text-xl font-bold text-white">
          No Questions Found
        </h3>

        <p className="text-sm text-slate-400">
          This quiz does not contain any questions.
        </p>

        <Link
          to={`/lesson/${lesson.id}`}
          className="inline-flex px-5 py-2.5 rounded-xl bg-indigo-500 text-white font-semibold text-xs"
        >
          Return to Lesson
        </Link>
      </div>
    )
  }

  const currentQuestion =
    questions[currentQuestionIdx]

  /*
   * IMPORTANT:
   * Keep this at component scope.
   *
   * It is used by both:
   * - handleSubmitQuiz()
   * - the Results screen
   *
   * This prevents the "resolvedSubject is not defined"
   * blank-page error.
   */
  const resolvedSubject =
    location.state?.subject ||
    quiz.subject ||
    lesson.subject ||
    'Science'

  const handleSelectOption = (option) => {
    setSelectedAnswers((previous) => ({
      ...previous,
      [currentQuestion.id]: option
    }))
  }

  const handleRevealHint = () => {
    if (!hintsRevealed[currentQuestion.id]) {
      setHintsRevealed((previous) => ({
        ...previous,
        [currentQuestion.id]: true
      }))

      setHintsCount(
        (previous) => previous + 1
      )
    }
  }

  const handleNext = () => {
    if (
      currentQuestionIdx <
      questions.length - 1
    ) {
      setCurrentQuestionIdx(
        (previous) => previous + 1
      )
    }
  }

  const handlePrev = () => {
    if (currentQuestionIdx > 0) {
      setCurrentQuestionIdx(
        (previous) => previous - 1
      )
    }
  }

  const getLatestTelemetry = async () => {
    try {
      const studentId = user?.id ?? user?.sub

      if (!studentId) {
        console.warn(
          'No student ID available for telemetry.'
        )

        return null
      }

      console.log(
        'Fetching facial telemetry for student:',
        studentId
      )

      const response = await fetch(
        `/api/attention/${studentId}`
      )

      if (!response.ok) {
        console.warn(
          'Telemetry request failed:',
          response.status
        )

        return null
      }

      const data = await response.json()

      console.log(
        'Facial telemetry response:',
        data
      )

      if (!data.success) {
        return null
      }

      return data.data
    } catch (err) {
      console.error(
        'Failed to fetch facial telemetry:',
        err
      )

      return null
    }
  }

  const handleSubmitQuiz = async () => {
    if (submitLoading) {
      return
    }

    const unansweredQuestions =
      questions.filter(
        (question) =>
          selectedAnswers[question.id] ===
          undefined
      )

    if (unansweredQuestions.length > 0) {
      alert(
        'Please answer all questions before submitting the quiz.'
      )

      return
    }

    const studentId = user?.id ?? user?.sub

    if (!studentId) {
      alert(
        'Student session could not be identified. Please log in again.'
      )

      return
    }

    let correctCount = 0

    questions.forEach((question) => {
      if (
        selectedAnswers[question.id] ===
        question.correct_answer
      ) {
        correctCount += 1
      }
    })

    const finalScore = Math.round(
      (correctCount / questions.length) * 100
    )

    setSubmitLoading(true)

    try {
      /*
       * Read telemetry at submission.
       *
       * The backend should return:
       *
       * attention_score
       * yawning
       * yawning_observed
       * looking_away
       * looking_away_observed
       *
       * We prefer the "_observed" values because they
       * remember whether the event happened at ANY
       * point during the quiz.
       */
      const telemetry =
        await getLatestTelemetry()

      console.log(
        'FINAL TELEMETRY USED FOR QUIZ:',
        telemetry
      )

      const currentAttention = telemetry?.attention_score

      const currentYawning =
        telemetry?.yawning_observed ??
        telemetry?.yawning ??
        false

      const currentLookingAway =
        telemetry?.looking_away_observed ??
        telemetry?.looking_away ??
        false

      console.log(
        'FINAL YAWNING STATE:',
        currentYawning
      )

      console.log(
        'FINAL LOOKING AWAY STATE:',
        currentLookingAway
      )

      /*
       * 1. Save quiz result to PostgreSQL.
       */
      const submitRes =
        await quizService.submitQuiz({
          studentId,
          lessonId: lesson.id,
          quizScore: finalScore,
          responseTime: secondsElapsed,
          attentionScore: currentAttention,
          difficulty: quiz.difficulty
        })

      if (!submitRes?.success) {
        throw new Error(
          'Failed to save assessment progress logs'
        )
      }

      /*
       * 2. Build updated progress history.
       */
      const updatedProgressHistory = [
        ...progressHistory,
        submitRes.data
      ]

      const sortedHistory = [
        ...updatedProgressHistory
      ].sort(
        (a, b) =>
          (b.id ?? 0) - (a.id ?? 0)
      )

      const previousAttempt =
        sortedHistory[1] || {
          quiz_score: 0
        }

      const completedLessonsCount =
        new Set(
          updatedProgressHistory
            .filter(
              (progress) =>
                progress.completed
            )
            .map(
              (progress) =>
                progress.lesson_id
            )
        ).size

      const attemptsCount =
        updatedProgressHistory.filter(
          (progress) =>
            progress.lesson_id ===
            lesson.id
        ).length

      /*
       * 3. Ask the RL engine for a recommendation.
       */
      let rlRes = null

      try {
        const payload = {
          subject: resolvedSubject,
          topic:
            lesson.topic ||
            lesson.title ||
            quiz.title,
          lesson:
            lesson.title ||
            quiz.title,

          previous_quiz_score:
            Math.round(
              Number(
                previousAttempt.quiz_score || 0
              )
            ),

          current_quiz_score:
            finalScore,

          difficulty:
            quiz.difficulty,

          response_time:
            Number(secondsElapsed),

          hints_used:
            Number(hintsCount),

          lesson_attempts:
            Number(attemptsCount),

          completed_lessons:
            Number(
              completedLessonsCount
            ),

          /*
           * Persistent telemetry.
           */
          yawning:
            Boolean(currentYawning),

          looking_away:
            Boolean(currentLookingAway)
        }

        if (
          currentAttention !== null
        ) {
          payload.attention_score =
            Number(currentAttention)
        }

        console.log(
          'RL recommendation payload:',
          payload
        )

        rlRes =
          await rlService.getRecommendation(
            payload
          )

        console.log(
          'RL recommendation response:',
          rlRes
        )
      } catch (rlError) {
        console.error(
          'RL recommendation failed:',
          rlError
        )

        /*
         * Do NOT crash the results page if RL fails.
         */
        rlRes = {
          error:
            'Unable to get an adaptive recommendation: Telemetry is offline.'
        }
      }

      /*
       * 4. Store result state.
       */
      setResults({
        score: finalScore,
        correctCount,
        totalQuestions:
          questions.length,
        timeTaken:
          secondsElapsed,

        attentionUsed:
          currentAttention,

        /*
         * IMPORTANT:
         * This is the persistent observed value,
         * not just the latest frame.
         */
        yawned:
          Boolean(currentYawning),

        lookedAway:
          Boolean(currentLookingAway)
      })

      setRlRecommendation(rlRes)
      setIsFinished(true)
    } catch (err) {
      console.error(
        'Quiz submission error:',
        err
      )

      alert(
        err.message ||
          'Error occurred during grading submission'
      )
    } finally {
      setSubmitLoading(false)
    }
  }

  const getQuizOfDifficulty = (
    difficulty
  ) => {
    /*
     * lesson.quizzes may not exist depending on
     * the backend response, so never call .find()
     * directly on it.
     */
    const lessonQuizzes =
      Array.isArray(lesson.quizzes)
        ? lesson.quizzes
        : []

    const target =
      lessonQuizzes.find(
        (quizItem) =>
          String(
            quizItem.difficulty || ''
          ).toLowerCase() ===
          difficulty.toLowerCase()
      )

    return target || null
  }

  const renderNextStepsButton = () => {
    if (!rlRecommendation) {
      return null
    }

    if (rlRecommendation.error) {
      return (
        <Link
          to="/subjects"
          className="px-6 py-3 rounded-xl bg-slate-900 border border-slate-700 hover:bg-slate-800 text-slate-200 font-bold text-sm"
        >
          Back to Subjects
        </Link>
      )
    }

    const action =
      rlRecommendation.action

    if (
      action ===
      'INCREASE_DIFFICULTY'
    ) {
      const currentDifficulty =
        String(
          quiz.difficulty
        ).toUpperCase()

      const nextDifficulty =
        currentDifficulty === 'EASY'
          ? 'Medium'
          : currentDifficulty ===
              'MEDIUM'
            ? 'Hard'
            : null

      if (!nextDifficulty) {
        return (
          <Link
            to="/subjects"
            className="px-6 py-3 rounded-xl bg-emerald-500 hover:bg-emerald-600 text-white font-bold text-sm"
          >
            Continue Learning →
          </Link>
        )
      }

      const targetQuiz =
        getQuizOfDifficulty(
          nextDifficulty
        )

      return (
        <button
          onClick={() => {
            if (targetQuiz?.id) {
              navigate(
                `/quiz/${targetQuiz.id}`
              )
            } else {
              alert(
                `No ${nextDifficulty} quiz is available for this lesson yet.`
              )
            }
          }}
          className="px-6 py-3 rounded-xl bg-indigo-500 hover:bg-indigo-600 text-white font-bold text-sm shadow-md shadow-indigo-500/20 transition-all"
        >
          Calibrate to{' '}
          {nextDifficulty} Quiz →
        </button>
      )
    }

    if (
      action ===
      'DECREASE_DIFFICULTY'
    ) {
      const currentDifficulty =
        String(
          quiz.difficulty
        ).toUpperCase()

      const previousDifficulty =
        currentDifficulty === 'HARD'
          ? 'Medium'
          : currentDifficulty ===
              'MEDIUM'
            ? 'Easy'
            : null

      if (!previousDifficulty) {
        return (
          <Link
            to={`/lesson/${lesson.id}`}
            className="px-6 py-3 rounded-xl bg-slate-900 border border-slate-700 text-slate-200 font-bold text-sm"
          >
            Review Lesson
          </Link>
        )
      }

      const targetQuiz =
        getQuizOfDifficulty(
          previousDifficulty
        )

      return (
        <button
          onClick={() => {
            if (targetQuiz?.id) {
              navigate(
                `/quiz/${targetQuiz.id}`
              )
            } else {
              alert(
                `No ${previousDifficulty} quiz is available for this lesson yet.`
              )
            }
          }}
          className="px-6 py-3 rounded-xl bg-amber-500 hover:bg-amber-600 text-white font-bold text-sm shadow-md shadow-amber-500/20 transition-all"
        >
          Return to{' '}
          {previousDifficulty} Quiz →
        </button>
      )
    }

    /*
     * For low scores, the recommendation is now
     * REPEAT_LESSON, which is the preferred behavior.
     */
    if (
      action ===
      'REPEAT_LESSON'
    ) {
      return (
        <button
          onClick={() =>
            navigate(
              `/lesson/${lesson.id}`
            )
          }
          className="px-6 py-3 rounded-xl bg-slate-900 border border-slate-700 hover:bg-slate-800 text-slate-200 font-bold text-sm transition-all"
        >
          Review Lesson Material →
        </button>
      )
    }

    if (
      action ===
      'NEXT_LESSON'
    ) {
      const sortedLessons =
        [...allLessons].sort(
          (a, b) =>
            (a.id ?? 0) -
            (b.id ?? 0)
        )

      const currentIndex =
        sortedLessons.findIndex(
          (item) =>
            item.id === lesson.id
        )

      const nextLesson =
        currentIndex !== -1 &&
        currentIndex <
          sortedLessons.length - 1
          ? sortedLessons[
              currentIndex + 1
            ]
          : null

      if (!nextLesson) {
        return (
          <Link
            to="/subjects"
            className="px-6 py-3 rounded-xl bg-emerald-500 hover:bg-emerald-600 text-white font-bold text-sm"
          >
            Back to Subjects →
          </Link>
        )
      }

      return (
        <button
          onClick={() =>
            navigate(
              `/lesson/${nextLesson.id}`
            )
          }
          className="px-6 py-3 rounded-xl bg-emerald-500 hover:bg-emerald-600 text-white font-bold text-sm shadow-md shadow-emerald-500/20 transition-all"
        >
          Advance to Next Lesson →
        </button>
      )
    }

    if (
      action ===
      'FOCUS_RECOVERY'
    ) {
      return (
        <button
          onClick={() => {
            alert(
              'Aegis Coach Break:\n\nTake a 30-second breathing break. Look away from the screen, take a deep breath in, and slowly breathe out. When ready, continue learning.'
            )

            navigate('/subjects')
          }}
          className="px-6 py-3 rounded-xl bg-sky-500 hover:bg-sky-600 text-white font-bold text-sm shadow-md shadow-sky-500/20 transition-all"
        >
          Start Focus Recovery →
        </button>
      )
    }

    return (
      <Link
        to="/subjects"
        className="px-6 py-3 rounded-xl bg-slate-900 border border-slate-700 hover:bg-slate-800 text-slate-200 font-bold text-sm"
      >
        Back to Subjects
      </Link>
    )
  }

  /*
   * RESULTS SCREEN
   */
  if (isFinished && results) {
    return (
      <div className="max-w-4xl mx-auto space-y-8 animate-fade-in">
        <div className="relative overflow-hidden rounded-3xl border border-slate-800 bg-gradient-to-br from-indigo-950/30 via-slate-900/40 to-slate-950 p-8 shadow-xl text-center">
          <div className="absolute top-0 left-1/2 -translate-x-1/2 h-36 w-36 bg-indigo-500/10 blur-3xl pointer-events-none" />

          <div className="space-y-4">
            <span className="inline-flex px-3 py-1 rounded-lg bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 text-xs font-bold uppercase tracking-wider">
              Assessment Results
            </span>

            <h1 className="text-4xl font-display font-extrabold text-white">
              Quiz score:{' '}
              <span className="bg-gradient-to-r from-indigo-400 to-teal-300 bg-clip-text text-transparent">
                {results.score}%
              </span>
            </h1>

            <p className="text-sm text-slate-400 max-w-md mx-auto">
              You correctly answered{' '}
              {results.correctCount}{' '}
              out of{' '}
              {results.totalQuestions}{' '}
              questions at{' '}
              <span className="text-white font-semibold">
                {quiz.difficulty}
              </span>{' '}
              difficulty level.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="glass-panel rounded-3xl p-6 border border-slate-900 shadow-md space-y-4">
            <h3 className="text-sm font-bold uppercase tracking-wider text-slate-500">
              Speed & Hints
            </h3>

            <div className="space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">
                  Response time
                </span>

                <span className="font-semibold text-white">
                  {results.timeTaken}{' '}
                  seconds
                </span>
              </div>

              <div className="flex justify-between text-sm">
                <span className="text-slate-400">
                  Hints used
                </span>

                <span className="font-semibold text-white">
                  {hintsCount} hints
                </span>
              </div>

              <div className="flex justify-between text-sm">
                <span className="text-slate-400">
                  Tempo score
                </span>

                <span className="font-semibold text-teal-400">
                  {results.timeTaken <
                  questions.length *
                    15
                    ? 'Fast'
                    : results.timeTaken <
                        questions.length *
                          35
                      ? 'Moderate'
                      : 'Steady'}
                </span>
              </div>
            </div>
          </div>

          <div className="glass-panel rounded-3xl p-6 border border-slate-900 shadow-md space-y-4">
            <h3 className="text-sm font-bold uppercase tracking-wider text-slate-500">
              Attention Telemetry
            </h3>

            <div className="space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">
                  Average attention
                </span>

                <span className="font-semibold text-white">
                  {results.attentionUsed !==
                  null
                    ? `${Math.round(
                        results.attentionUsed *
                          100
                      )}%`
                    : 'Unavailable'}
                </span>
              </div>

              <div className="flex justify-between text-sm">
                <span className="text-slate-400">
                  Yawning observed
                </span>

                <span
                  className={`font-semibold ${
                    results.yawned
                      ? 'text-amber-400'
                      : 'text-slate-400'
                  }`}
                >
                  {results.yawned
                    ? 'Yes'
                    : 'No'}
                </span>
              </div>

              <div className="flex justify-between text-sm">
                <span className="text-slate-400">
                  Gaze stability
                </span>

                <span
                  className={`font-semibold ${
                    results.lookedAway
                      ? 'text-amber-400'
                      : 'text-slate-400'
                  }`}
                >
                  {results.lookedAway
                    ? 'Looking away'
                    : 'Stable'}
                </span>
              </div>
            </div>
          </div>

          <div className="glass-panel rounded-3xl p-6 border border-slate-900 shadow-md space-y-4">
            <h3 className="text-sm font-bold uppercase tracking-wider text-slate-500">
              Grading Log
            </h3>

            <div className="space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">
                  Subject
                </span>

                <span className="font-semibold text-white">
                  {resolvedSubject}
                </span>
              </div>

              <div className="flex justify-between text-sm">
                <span className="text-slate-400">
                  Topic
                </span>

                <span className="font-semibold text-white truncate max-w-[120px] inline-block">
                  {lesson.topic ||
                    lesson.title}
                </span>
              </div>

              <div className="flex justify-between text-sm">
                <span className="text-slate-400">
                  Sync status
                </span>

                <span className="font-semibold text-emerald-400">
                  PostgreSQL saved
                </span>
              </div>
            </div>
          </div>
        </div>

        {rlRecommendation?.error ? (
          <div className="glass-panel rounded-3xl p-8 border border-slate-900 shadow-xl space-y-6 text-center">
            <p className="text-sm font-semibold text-rose-400">
              {rlRecommendation.error}
            </p>

            <p className="text-xs text-slate-500">
              The reinforcement learning engine could not resolve a recommendation.
            </p>

            <Link
              to="/subjects"
              className="inline-flex px-6 py-3 rounded-xl bg-slate-900 border border-slate-700 hover:bg-slate-800 text-slate-200 font-bold text-sm"
            >
              Back to Subjects
            </Link>
          </div>
        ) : (
          rlRecommendation && (
            <div className="glass-panel rounded-3xl p-8 border border-slate-900 shadow-xl space-y-6 relative overflow-hidden">
              <div className="absolute top-0 right-0 h-40 w-40 bg-teal-500/5 blur-3xl pointer-events-none" />

              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-800/80 pb-4">
                <div>
                  <h3 className="text-xl font-bold text-white flex items-center gap-2">
                    <span className="text-teal-400">
                      ✦
                    </span>

                    Reinforcement Learning Policy Decision
                  </h3>

                  <p className="text-xs text-slate-500 mt-1">
                    Generated by our Q-Learning Agent mapping student engagement metrics to target content difficulty
                  </p>
                </div>

                <div className="shrink-0 flex items-center gap-2 bg-slate-900 border border-slate-800 rounded-2xl px-4 py-2">
                  <span className="text-slate-500 text-[10px] uppercase font-bold tracking-wide">
                    CONFIDENCE
                  </span>

                  <span className="text-teal-400 font-extrabold text-sm">
                    {Math.round(
                      Number(
                        rlRecommendation.confidence ??
                          0
                      ) * 100
                    )}
                    %
                  </span>
                </div>
              </div>

              <div className="space-y-4">
                <div className="flex flex-col gap-1.5">
                  <span className="text-[10px] font-semibold text-indigo-400 uppercase tracking-wider">
                    Suggested Pedagogical Action
                  </span>

                  <span className="text-2xl font-extrabold text-white">
                    {String(
                      rlRecommendation.action ||
                        'CONTINUE'
                    ).replace(
                      /_/g,
                      ' '
                    )}
                  </span>
                </div>

                <div className="flex flex-col gap-1">
                  <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider">
                    Coach Justification
                  </span>

                  <p className="text-sm text-slate-300 italic leading-relaxed">
                    "
                    {rlRecommendation.explanation ||
                      'Adaptive recommendation generated from your learning activity.'}
                    "
                  </p>
                </div>
              </div>

              <div className="border-t border-slate-800/80 pt-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                <span className="text-xs text-slate-400">
                  Aegis adapted the curriculum sequence. Click the button to advance:
                </span>

                <div className="flex items-center gap-3">
                  {renderNextStepsButton()}
                </div>
              </div>
            </div>
          )
        )}
      </div>
    )
  }

  const progressPercent = Math.round(
    ((currentQuestionIdx + 1) /
      questions.length) *
      100
  )

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div>
        <Link
          to={`/lesson/${lesson.id}`}
          className="inline-flex items-center gap-1 text-xs font-semibold uppercase tracking-wider text-slate-500 hover:text-slate-300 transition-colors"
        >
          ← Abort to Lesson
        </Link>
      </div>

      <div className="glass-panel rounded-3xl p-6 border border-slate-900 shadow-md space-y-4">
        <div className="flex items-center justify-between text-xs">
          <div className="flex items-center gap-2">
            <span className="px-2 py-0.5 text-[9px] font-extrabold uppercase bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 rounded">
              {quiz.difficulty} Level
            </span>

            <span className="text-slate-600">
              •
            </span>

            <span className="font-semibold text-slate-300 truncate max-w-[150px] inline-block">
              {quiz.title}
            </span>
          </div>

          <div className="flex items-center gap-4 text-slate-400 font-medium">
            <span>
              Question{' '}
              {currentQuestionIdx +
                1}{' '}
              of {questions.length}
            </span>

            <span>
              Time:{' '}
              <span className="text-white font-semibold font-mono">
                {secondsElapsed}s
              </span>
            </span>
          </div>
        </div>

        <div className="w-full bg-slate-950 rounded-full h-2 overflow-hidden">
          <div
            className="bg-gradient-to-r from-indigo-500 to-teal-400 h-2 rounded-full transition-all duration-300"
            style={{
              width: `${progressPercent}%`
            }}
          />
        </div>
      </div>

      <div className="glass-panel rounded-3xl p-8 border border-slate-900 shadow-lg space-y-8 min-h-[300px] flex flex-col justify-between">
        <div className="space-y-6">
          <h2 className="text-lg md:text-xl font-bold text-white leading-relaxed">
            {currentQuestion.question}
          </h2>

          <div className="grid grid-cols-1 gap-4">
            {['A', 'B', 'C', 'D'].map(
              (letter) => {
                const optionText =
                  currentQuestion[
                    `option_${letter.toLowerCase()}`
                  ]

                const isSelected =
                  selectedAnswers[
                    currentQuestion.id
                  ] === letter

                return (
                  <button
                    key={letter}
                    onClick={() =>
                      handleSelectOption(
                        letter
                      )
                    }
                    className={`w-full flex items-center gap-4 text-left p-4 rounded-2xl border transition-all duration-200 ${
                      isSelected
                        ? 'bg-indigo-500/10 border-indigo-500 text-white shadow-inner font-medium'
                        : 'bg-slate-900/30 border-slate-800/80 hover:border-slate-700/60 text-slate-300'
                    }`}
                  >
                    <span
                      className={`flex h-7 w-7 shrink-0 items-center justify-center rounded-xl text-xs font-bold border transition-colors ${
                        isSelected
                          ? 'bg-indigo-500 border-indigo-500 text-white'
                          : 'bg-slate-950 border-slate-800 text-slate-500'
                      }`}
                    >
                      {letter}
                    </span>

                    <span className="text-sm">
                      {optionText}
                    </span>
                  </button>
                )
              }
            )}
          </div>
        </div>

        <div className="border-t border-slate-800/80 pt-6 flex items-center justify-between gap-4">
          <div>
            {hintsRevealed[
              currentQuestion.id
            ] ? (
              <div className="text-xs text-indigo-400 leading-relaxed font-medium">
                💡 Hint: Review the core reading sections matching the topic of{' '}
                {lesson.topic}.
              </div>
            ) : (
              <button
                onClick={
                  handleRevealHint
                }
                className="text-xs font-semibold text-slate-500 hover:text-slate-300 transition-colors flex items-center gap-1"
              >
                💡 Need a hint?
              </button>
            )}
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={handlePrev}
              disabled={
                currentQuestionIdx === 0
              }
              className="px-4 py-2 rounded-xl bg-slate-950 hover:bg-slate-900 border border-slate-800 text-xs font-semibold text-slate-400 hover:text-slate-200 disabled:opacity-30 disabled:cursor-not-allowed transition-all"
            >
              Previous
            </button>

            {currentQuestionIdx <
            questions.length - 1 ? (
              <button
                onClick={handleNext}
                className="px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-xs font-semibold text-slate-200 hover:text-white transition-all"
              >
                Next
              </button>
            ) : (
              <button
                onClick={
                  handleSubmitQuiz
                }
                disabled={
                  submitLoading ||
                  Object.keys(
                    selectedAnswers
                  ).length <
                    questions.length
                }
                className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-indigo-500 to-indigo-600 hover:from-indigo-600 hover:to-indigo-700 text-xs font-bold text-white shadow-md shadow-indigo-500/20 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
              >
                {submitLoading
                  ? 'Grading...'
                  : 'Submit quiz'}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}