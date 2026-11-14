import React, { useCallback, useEffect, useRef, useState } from 'react'
import { useParams, useNavigate, Link, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useMonitoring } from '../context/MonitoringContext'
import { quizService } from '../services/quizService'
import { lessonService } from '../services/lessonService'
import { telemetryService } from '../services/telemetryService'
import { useLeaveGuard, useQuizIntegrity } from '../hooks/useQuizIntegrity'
import {
  AttemptEndedPanel,
  CheckingOverlay,
  CooldownPanel,
  IntegrityRulesBanner,
  LeaveQuizModal,
  SaveStatus,
  StrikeWarningModal
} from '../components/QuizIntegrity'

const OPEN_STATUSES = ['in_progress', 'away', 'unverified']
import {
  CONFIDENCE_NOTE,
  POLICY_LABELS,
  actionInfo,
  resolveNextStep
} from '../utils/recommendationActions'

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
  const [allLessons, setAllLessons] = useState([])

  const [currentQuestionIdx, setCurrentQuestionIdx] = useState(0)
  const [selectedAnswers, setSelectedAnswers] = useState({})
  const [hintsRevealed, setHintsRevealed] = useState({})
  const [hintsCount, setHintsCount] = useState(0)
  const [secondsElapsed, setSecondsElapsed] = useState(0)

  const [isFinished, setIsFinished] = useState(false)
  const [results, setResults] = useState(null)
  const [rlRecommendation, setRlRecommendation] = useState(null)
  const [breakSecondsLeft, setBreakSecondsLeft] = useState(null)

  // Server-side attempt (tab-switch rule). The server decides its state.
  const [attempt, setAttempt] = useState(null)
  const [cooldown, setCooldown] = useState(null)
  const [warningOpen, setWarningOpen] = useState(false)
  const [saveState, setSaveState] = useState(null)
  const strikesSeen = useRef(0)

  const studentId = user?.id
  // How this attempt is taken: standard, practice, hints or challenge
  // (set by a recommended next step). Recorded with the attempt.
  const attemptMode = ['practice', 'hints', 'challenge'].includes(location.state?.mode)
    ? location.state.mode
    : 'standard'
  const CHALLENGE_SECONDS_PER_QUESTION = 30
  const monitoring = useMonitoring()
  const monitoringVerified = monitoring.verified

  // In-progress answers survive a reload or a camera interruption. Only
  // answers, position, elapsed time and hints are stored -- never tokens.
  const draftKey = studentId ? `aegis.quizDraft.${studentId}.${id}` : null
  const [draftLoaded, setDraftLoaded] = useState(false)

  const attemptOpen = Boolean(attempt && OPEN_STATUSES.includes(attempt.status) && !isFinished)
  const protectedOpen = attemptOpen && Boolean(attempt?.protected)
  const attemptEnded = Boolean(attempt && ['terminated', 'abandoned'].includes(attempt.status))

  const clearDraft = useCallback(() => {
    try {
      if (draftKey) sessionStorage.removeItem(draftKey)
    } catch {
      // ignore
    }
  }, [draftKey])

  // Every server decision about the attempt arrives here.
  const applyAttemptView = useCallback(
    (view) => {
      if (!view) return
      setAttempt((previous) => ({ ...(previous || {}), ...view }))
      if (OPEN_STATUSES.includes(view.status) && view.strikes > strikesSeen.current) {
        setWarningOpen(true)
      }
      strikesSeen.current = view.strikes ?? strikesSeen.current
      if (['terminated', 'abandoned'].includes(view.status)) {
        setWarningOpen(false)
        clearDraft()
      }
    },
    [clearDraft]
  )

  const integrity = useQuizIntegrity({
    attemptId: attempt?.id,
    active: protectedOpen,
    initialStatus: attempt?.status,
    onView: applyAttemptView,
    // The quiz page went away without a confirmed departure (e.g. sign-out).
    onUnmountOpen: () => {
      if (attempt?.id) quizService.abandonAttempt(attempt.id, { keepalive: true }).catch(() => {})
    }
  })

  const leaveGuard = useLeaveGuard({
    active: attemptOpen,
    navigate,
    onLeave: async () => {
      if (!attempt?.id) return
      const view = await quizService.abandonAttempt(attempt.id).catch(() => null)
      integrity.endReporting()
      if (view) applyAttemptView(view)
    }
  })

  const locked = Boolean(attemptOpen && (integrity.checking || attempt?.status !== 'in_progress'))

  const retakeQuiz = () => {
    navigate(location.pathname, {
      state: { ...(location.state || {}), attempt: Date.now() }
    })
  }

  const resetQuizTelemetry = async () => {
    try {
      if (!studentId) {
        return
      }

      // Start a fresh aggregation window for this attempt.
      await telemetryService.resetSession(studentId)
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

        // Start a server-side attempt, or resume the open one (reload).
        let quizRes
        try {
          quizRes = await quizService.startAttempt({
            quizId: id,
            mode: attemptMode,
            monitoringSessionId: monitoring.sessionId
          })
        } catch (startError) {
          if (startError.status === 429) {
            const meta = await quizService.getQuiz(id).catch(() => null)
            setCooldown({
              retryAfter: startError.detail?.retry_after_seconds ?? 300,
              lessonId: meta?.data?.quiz?.lesson_id ?? null,
              // e.g. after a confirmed reload that ended the quiz
              endReason: startError.detail?.previous_attempt?.end_reason ?? null
            })
            return
          }
          throw startError
        }

        if (!quizRes.success) {
          throw new Error('Could not load quiz details')
        }

        const view = quizRes.data.attempt
        strikesSeen.current = view.strikes
        setAttempt(view)

        // In-progress answers: the server copy, unless this device holds
        // newer unsaved ones for the same attempt (e.g. saved while offline).
        let restored = null
        try {
          restored = draftKey ? JSON.parse(sessionStorage.getItem(draftKey) || 'null') : null
        } catch {
          restored = null
        }
        if (restored && restored.attemptId !== view.id) restored = null
        const serverDraft = view.draft_state || null

        if (restored) {
          setSelectedAnswers(restored.answers || {})
          setCurrentQuestionIdx(restored.index || 0)
          setSecondsElapsed(restored.seconds || 0)
          setHintsRevealed(restored.hintsRevealed || {})
          setHintsCount(restored.hints || 0)
        } else if (quizRes.data.resumed) {
          setSelectedAnswers(view.answers || {})
          setCurrentQuestionIdx(serverDraft?.index || 0)
          setSecondsElapsed(serverDraft?.seconds || 0)
          setHintsRevealed(serverDraft?.hintsRevealed || {})
          setHintsCount(serverDraft?.hints || 0)
        }
        if (!quizRes.data.resumed) {
          // New attempt: start a fresh camera-measurement window.
          await resetQuizTelemetry()
        }
        setDraftLoaded(true)

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
    // Runs once per quiz and student. draftKey is derived from them, and
    // resetQuizTelemetry is recreated every render; listing it would restart
    // the quiz (and its camera window) on every re-render.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id, studentId])

  // The quiz timer only runs while camera monitoring is verified; any
  // interruption pauses it.
  useEffect(() => {
    if (loading || isFinished || !monitoringVerified) {
      return
    }

    const timer = setInterval(() => {
      setSecondsElapsed((previous) => previous + 1)
    }, 1000)

    return () => clearInterval(timer)
  }, [loading, isFinished, monitoringVerified])

  useEffect(() => {
    if (!draftKey || !draftLoaded || isFinished) return
    try {
      sessionStorage.setItem(
        draftKey,
        JSON.stringify({
          attemptId: attempt?.id,
          answers: selectedAnswers,
          index: currentQuestionIdx,
          seconds: secondsElapsed,
          hintsRevealed,
          hints: hintsCount,
        })
      )
    } catch {
      // Storage unavailable: answers still live in memory.
    }
  }, [draftKey, draftLoaded, isFinished, attempt?.id, selectedAnswers, currentQuestionIdx, secondsElapsed, hintsRevealed, hintsCount])

  // Save answers on the server as the student works (debounced), so they
  // survive a reload and are kept if the attempt ends without grading.
  const latestDraft = useRef(null)
  useEffect(() => {
    latestDraft.current = {
      answers: selectedAnswers,
      draft: { index: currentQuestionIdx, seconds: secondsElapsed, hintsRevealed, hints: hintsCount }
    }
  })
  useEffect(() => {
    if (!attempt?.id || !attemptOpen || !draftLoaded) return undefined
    const timer = setTimeout(async () => {
      setSaveState('saving')
      try {
        await quizService.saveAnswers(attempt.id, latestDraft.current.answers, latestDraft.current.draft)
        setSaveState('saved')
      } catch (saveError) {
        if (saveError.status === 409 && saveError.detail?.attempt) {
          applyAttemptView(saveError.detail.attempt)
          setSaveState(null)
        } else {
          setSaveState(saveError.status ? null : 'offline')
        }
      }
    }, 800)
    return () => clearTimeout(timer)
    // Saved when answers, position or hints change (not on every timer tick).
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [attempt?.id, attemptOpen, draftLoaded, selectedAnswers, currentQuestionIdx, hintsRevealed, hintsCount])

  // Leaving the page: save the latest answers at once (keepalive survives
  // a closed or reloaded tab).
  useEffect(() => {
    if (!attempt?.id || !attemptOpen) return undefined
    const saveNow = () => {
      if (document.visibilityState !== 'hidden' || !latestDraft.current) return
      quizService
        .saveAnswers(attempt.id, latestDraft.current.answers, latestDraft.current.draft, { keepalive: true })
        .catch(() => {})
    }
    document.addEventListener('visibilitychange', saveNow)
    return () => document.removeEventListener('visibilitychange', saveNow)
  }, [attempt?.id, attemptOpen])

  // Focus-recovery break countdown (recommended by the RL engine).
  useEffect(() => {
    if (breakSecondsLeft === null || breakSecondsLeft <= 0) return
    const timer = setTimeout(() => setBreakSecondsLeft((left) => left - 1), 1000)
    return () => clearTimeout(timer)
  }, [breakSecondsLeft])

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

  if (cooldown) {
    return <CooldownPanel retryAfterSeconds={cooldown.retryAfter} lessonId={cooldown.lessonId} endReason={cooldown.endReason} onRetake={retakeQuiz} />
  }

  if (attemptEnded && !isFinished) {
    return <AttemptEndedPanel attempt={attempt} lessonId={lesson?.id ?? quiz?.lesson_id} onRetake={retakeQuiz} />
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

    if (!studentId) {
      alert(
        'Student session could not be identified. Please log in again.'
      )

      return
    }

    if (!monitoringVerified || !monitoring.sessionId) {
      alert('Camera monitoring must be active to submit the quiz.')
      return
    }

    if (!attempt?.id || locked) {
      alert('Your quiz is being checked. Please wait a moment and try again.')
      return
    }

    setSubmitLoading(true)

    try {
      /*
       * The server grades the selected answers, takes the camera
       * measurements its paired agent reported for this monitored session,
       * stores the attempt and generates the adaptive recommendation.
       */
      const submitRes = await quizService.submitQuiz({
        quizId: quiz.id,
        attemptId: attempt.id,
        monitoringSessionId: monitoring.sessionId,
        answers: selectedAnswers,
        responseTime: secondsElapsed,
        hintsUsed: hintsCount,
        mode: attemptMode
      })

      if (!submitRes?.success) {
        throw new Error(
          'Failed to save assessment progress logs'
        )
      }

      const { grading, progress, recommendation, recommendation_status: recommendationStatus } =
        submitRes.data

      clearDraft()
      integrity.endReporting()
      if (submitRes.data.attempt) applyAttemptView(submitRes.data.attempt)

      let rlRes
      if (recommendation) {
        rlRes = recommendation
      } else if (recommendationStatus === 'telemetry_unavailable') {
        rlRes = {
          error:
            'Camera telemetry was unavailable for this attempt, so no adaptive recommendation was generated.',
          telemetryUnavailable: true
        }
      } else {
        rlRes = {
          error: 'The recommendation engine could not produce a recommendation for this attempt.'
        }
      }

      setResults({
        score: Math.round(grading.score),
        correctCount: grading.correct_count,
        totalQuestions: grading.total_questions,
        review: grading.results,
        mode: attemptMode,
        challengeTarget:
          attemptMode === 'challenge' ? questions.length * CHALLENGE_SECONDS_PER_QUESTION : null,
        timeTaken:
          secondsElapsed,

        // Measured by the camera agent; null = no measurement (not zero attention)
        attentionUsed: progress.attention_score,

        // Observed at any point during the attempt; null = unknown.
        yawned: progress.yawning,
        lookedAway: progress.looking_away,
        drowsy: progress.drowsy
      })

      setRlRecommendation(rlRes)
      setIsFinished(true)
    } catch (err) {
      console.error(
        'Quiz submission error:',
        err
      )

      if (err.status === 409 && err.detail?.attempt) {
        // The server's view of the attempt (e.g. return not yet confirmed,
        // or the attempt ended) replaces a generic error.
        applyAttemptView(err.detail.attempt)
        integrity.flush()
      }

      alert(
        err.message ||
          'Error occurred during grading submission'
      )
    } finally {
      setSubmitLoading(false)
    }
  }


  // Every one of the RL engine's 11 actions maps to a concrete next step
  // (utils/recommendationActions.js); nothing falls back to a generic button.
  const nextStep =
    rlRecommendation && !rlRecommendation.error
      ? resolveNextStep(rlRecommendation.action, {
          lessonId: lesson.id,
          quizId: quiz.id,
          difficulty: quiz.difficulty,
          lessonQuizzes: Array.isArray(lesson.quizzes) ? lesson.quizzes : [],
          navigation: lesson.navigation,
          lessons: allLessons,
          onResults: true
        })
      : null

  const performNextStep = (step) => {
    if (step.kind === 'navigate') {
      navigate(step.to, { state: { ...(step.state || {}), subject: resolvedSubject } })
    } else if (step.kind === 'retry') {
      // A new `attempt` remounts the quiz page with a fresh attempt.
      navigate(step.to, {
        state: {
          subject: resolvedSubject,
          attempt: Date.now(),
          mode: step.mode,
          recommendedAction: rlRecommendation?.action
        }
      })
    } else if (step.kind === 'review') {
      document.getElementById('answer-review')?.scrollIntoView({ behavior: 'smooth' })
    } else if (step.kind === 'break') {
      setBreakSecondsLeft(60)
    }
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

    if (!nextStep || nextStep.kind === 'unknown') {
      return (
        <span className="text-xs font-semibold text-amber-400">
          {actionInfo(rlRecommendation.action).label}
        </span>
      )
    }

    return (
      <button
        onClick={() => performNextStep(nextStep)}
        className="px-6 py-3 rounded-xl bg-indigo-500 hover:bg-indigo-600 text-white font-bold text-sm shadow-md shadow-indigo-500/20 transition-all"
      >
        {nextStep.label}
      </button>
    )
  }

  const renderBreakPanel = () => {
    if (breakSecondsLeft === null) return null
    const done = breakSecondsLeft <= 0
    return (
      <div className="rounded-2xl border border-sky-500/30 bg-sky-500/5 p-5 space-y-3">
        <p className="text-sm font-bold text-sky-300">
          {done ? 'Break complete. Welcome back.' : `Focus-recovery break: ${breakSecondsLeft}s`}
        </p>
        <p className="text-xs text-slate-300 leading-relaxed">
          Look away from the screen at something far away, blink slowly, and take a few deep
          breaths. Stretch your shoulders. Continue when you feel alert.
        </p>
        <div className="flex gap-3">
          <Link
            to={`/lesson/${lesson.id}`}
            className="px-4 py-2 rounded-xl bg-sky-500 hover:bg-sky-600 text-white font-bold text-xs"
          >
            Continue learning →
          </Link>
          {!done && (
            <button
              onClick={() => setBreakSecondsLeft(null)}
              className="px-4 py-2 rounded-xl border border-slate-700 text-slate-300 text-xs font-semibold"
            >
              Skip break
            </button>
          )}
        </div>
      </div>
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
                  {hintsCount} {hintsCount === 1 ? 'hint' : 'hints'}
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
                  {results.attentionUsed !== null &&
                  results.attentionUsed !== undefined
                    ? `${Math.round(
                        results.attentionUsed *
                          100
                      )}%`
                    : 'Unavailable (no camera data)'}
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
                  {results.yawned === null ||
                  results.yawned === undefined
                    ? 'Unknown'
                    : results.yawned
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
                  {results.lookedAway === null ||
                  results.lookedAway === undefined
                    ? 'Unknown'
                    : results.lookedAway
                      ? 'Looking away'
                      : 'Stable'}
                </span>
              </div>

              <div className="flex justify-between text-sm">
                <span className="text-slate-400">
                  Possible drowsiness
                </span>

                <span
                  className={`font-semibold ${
                    results.drowsy ? 'text-amber-400' : 'text-slate-400'
                  }`}
                >
                  {results.drowsy === null || results.drowsy === undefined
                    ? 'Unknown'
                    : results.drowsy
                      ? 'Observed'
                      : 'Not observed'}
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
                  Saved by the server
                </span>
              </div>
            </div>
          </div>
        </div>

        {results.mode && results.mode !== 'standard' && (
          <div className="rounded-2xl border border-indigo-500/30 bg-indigo-500/5 px-4 py-3 text-xs font-semibold text-indigo-300">
            {results.mode === 'challenge'
              ? results.timeTaken <= results.challengeTarget
                ? `Quick challenge complete: ${results.timeTaken}s, within the ${results.challengeTarget}s target.`
                : `Quick challenge: ${results.timeTaken}s, ${results.timeTaken - results.challengeTarget}s over the ${results.challengeTarget}s target. Try again to beat it.`
              : results.mode === 'hints'
                ? `Retry with hints: you used ${hintsCount} hint(s).`
                : 'Practice attempt recorded.'}
          </div>
        )}

        {Array.isArray(results.review) && results.review.length > 0 && (
          <div id="answer-review" className="glass-panel rounded-3xl p-6 border border-slate-900 shadow-md space-y-4">
            <h3 className="text-sm font-bold uppercase tracking-wider text-slate-500">
              Answer Review
            </h3>

            <ol className="space-y-3">
              {results.review.map((item, index) => {
                const question = questions.find((q) => q.id === item.question_id)
                const optionText = (letter) =>
                  question ? question[`option_${String(letter).toLowerCase()}`] : ''

                return (
                  <li
                    key={item.question_id}
                    className={`rounded-2xl border p-4 text-sm ${
                      item.is_correct
                        ? 'border-emerald-500/20 bg-emerald-500/5'
                        : 'border-rose-500/20 bg-rose-500/5'
                    }`}
                  >
                    <p className="font-semibold text-slate-200">
                      {index + 1}. {question?.question}
                    </p>
                    <p className={`mt-1 text-xs ${item.is_correct ? 'text-emerald-400' : 'text-rose-400'}`}>
                      {item.is_correct ? '✓ Correct' : '✗ Incorrect'} — your answer: {item.selected_answer}. {optionText(item.selected_answer)}
                    </p>
                    {!item.is_correct && (
                      <p className="mt-1 text-xs text-slate-400">
                        Correct answer: {item.correct_answer}. {optionText(item.correct_answer)}
                      </p>
                    )}
                    {item.explanation && (
                      <p className="mt-2 text-xs text-slate-300 leading-relaxed">
                        <span className="font-semibold text-indigo-300">Why: </span>
                        {item.explanation}
                      </p>
                    )}
                  </li>
                )
              })}
            </ol>
          </div>
        )}

        {rlRecommendation?.error ? (
          <div className="glass-panel rounded-3xl p-8 border border-slate-900 shadow-xl space-y-6 text-center">
            <p className="text-sm font-semibold text-rose-400">
              {rlRecommendation.error}
            </p>

            <p className="text-xs text-slate-500">
              {rlRecommendation.telemetryUnavailable
                ? 'Your quiz result was saved. Start the Aegis camera agent before your next attempt to receive adaptive recommendations.'
                : 'The recommendation engine could not resolve a recommendation.'}
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
                    Generated by the Aegis adaptive policy from your quiz performance and camera engagement metrics
                  </p>
                </div>

                <div
                  className="shrink-0 flex items-center gap-2 bg-slate-900 border border-slate-800 rounded-2xl px-4 py-2"
                  title={CONFIDENCE_NOTE}
                >
                  <span className="text-slate-500 text-[10px] uppercase font-bold tracking-wide">
                    DECISION STRENGTH
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
                    {actionInfo(rlRecommendation.action).icon}{' '}
                    {actionInfo(rlRecommendation.action).label}
                  </span>

                  <span className="text-xs text-slate-400">
                    {actionInfo(rlRecommendation.action).description}
                  </span>

                  {rlRecommendation.policy && (
                    <span className="text-[10px] text-slate-500">
                      Decided by: {POLICY_LABELS[rlRecommendation.policy] || rlRecommendation.policy}
                    </span>
                  )}
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
                  Your recommended next step:
                </span>

                <div className="flex items-center gap-3">
                  {renderNextStepsButton()}
                </div>
              </div>

              {renderBreakPanel()}
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

  const modeBanner = {
    practice: 'Practice attempt recommended by your coach: focus on the questions you missed last time.',
    hints: 'Retry with hints: press the hint button on any question you are unsure about.',
    challenge: `Quick challenge: answer all ${questions.length} questions within ${questions.length * CHALLENGE_SECONDS_PER_QUESTION} seconds.`
  }[attemptMode]

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <StrikeWarningModal open={warningOpen && attemptOpen} onClose={() => setWarningOpen(false)} />
      <LeaveQuizModal pending={leaveGuard.pending} onConfirm={leaveGuard.confirm} onCancel={leaveGuard.cancel} />

      {attempt?.protected && <IntegrityRulesBanner strikes={attempt.strikes} />}

      {modeBanner && (
        <div className="rounded-2xl border border-indigo-500/30 bg-indigo-500/5 px-4 py-3 text-xs font-semibold text-indigo-300">
          {modeBanner}
        </div>
      )}

      <div>
        <Link
          to={`/lesson/${lesson.id}`}
          className="inline-flex items-center gap-1 text-xs font-semibold uppercase tracking-wider text-slate-500 hover:text-slate-300 transition-colors"
        >
          ← Abort to Lesson
        </Link>
        <span className="float-right">
          <SaveStatus state={saveState} />
        </span>
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
                {attemptMode === 'challenge' && (
                  <span
                    className={`ml-2 ${
                      secondsElapsed > questions.length * CHALLENGE_SECONDS_PER_QUESTION
                        ? 'text-rose-400'
                        : 'text-teal-400'
                    }`}
                  >
                    / target {questions.length * CHALLENGE_SECONDS_PER_QUESTION}s
                  </span>
                )}
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

      <div className="relative glass-panel rounded-3xl p-8 border border-slate-900 shadow-lg space-y-8 min-h-[300px] flex flex-col justify-between">
        {locked && <CheckingOverlay connection={integrity.connection} status={attempt?.status} />}
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
                    disabled={locked}
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
                💡 Hint:{' '}
                {currentQuestion.hint ||
                  `Review the lesson section on ${lesson.topic}.`}
              </div>
            ) : (
              <button
                onClick={
                  handleRevealHint
                }
                disabled={locked}
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
                  locked ||
                  !monitoringVerified ||
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