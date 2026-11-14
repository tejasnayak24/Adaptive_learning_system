import React, { useCallback, useEffect, useRef, useState } from 'react'
import { useParams, useNavigate, useLocation } from 'react-router-dom'
import {
  ArrowLeft,
  ArrowRight,
  BookOpen,
  Camera,
  CircleCheck,
  CircleX,
  ClipboardCheck,
  Clock,
  Coffee,
  Lightbulb,
  ListChecks,
  Send,
  Sparkles,
  Timer,
  TriangleAlert
} from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import { useMonitoring } from '../context/MonitoringContext'
import { quizService } from '../services/quizService'
import { lessonService } from '../services/lessonService'
import { telemetryService } from '../services/telemetryService'
import { useLeaveGuard, useQuizIntegrity } from '../hooks/useQuizIntegrity'
import { scrollBehavior } from '../hooks/useReducedMotion'
import {
  AttemptEndedPanel,
  CheckingOverlay,
  CooldownPanel,
  IntegrityRulesBanner,
  LeaveQuizModal,
  SaveStatus,
  StrikeWarningModal,
  formatClock
} from '../components/QuizIntegrity'
import { ActionIcon, DifficultyBadge, SubjectChip } from '../components/learning'
import { actionIcon } from '../components/visuals'
import { Badge, Button, Callout, Card, EmptyState, ErrorState, Modal, ProgressBar, ProgressRing, SectionHeader, Spinner, Tooltip, cx } from '../components/ui'

const OPEN_STATUSES = ['in_progress', 'away', 'unverified']
import {
  CONFIDENCE_NOTE,
  POLICY_LABELS,
  actionInfo,
  resolveNextStep
} from '../utils/recommendationActions'

/** A labelled value row on the results screen. */
function ResultRow({ label, children, tone }) {
  return (
    <div className="flex items-center justify-between gap-3 py-2.5 text-sm">
      <dt className="text-ink-2">{label}</dt>
      <dd className={cx('text-right font-medium', tone || 'text-ink')}>{children}</dd>
    </div>
  )
}

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

  // Presentation only: the submit confirmation and inline messages that
  // replace browser alert() pop-ups (same checks, same wording).
  const [confirmOpen, setConfirmOpen] = useState(false)
  const [notice, setNotice] = useState('')

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

  // When the results replace the quiz, start at the top so the score is
  // the first thing the student sees (presentation only).
  useEffect(() => {
    if (isFinished) window.scrollTo({ top: 0, behavior: scrollBehavior() })
  }, [isFinished])

  if (loading) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <div className="flex flex-col items-center gap-4 text-center">
          <span className="grid h-14 w-14 place-items-center rounded-2xl border border-line-strong bg-raised shadow-card">
            <Spinner size={24} label="Preparing your quiz" />
          </span>
          <div className="space-y-1">
            <p className="font-display text-base font-semibold text-ink">Preparing your quiz…</p>
            <p className="text-[13px] text-ink-2">Loading the questions and your saved answers.</p>
          </div>
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
      <div className="space-y-4 py-8">
        <ErrorState title="This quiz could not be loaded" message={error || 'Failed to load quiz metadata.'} />
        <div className="text-center">
          <Button to="/subjects" variant="secondary" icon={BookOpen}>
            Return to My Learning
          </Button>
        </div>
      </div>
    )
  }

  if (!questions.length) {
    return (
      <Card className="mx-auto max-w-lg">
        <EmptyState
          icon={TriangleAlert}
          title="No questions found"
          text="This quiz does not contain any questions."
          action={
            <Button to={`/lesson/${lesson.id}`} variant="secondary" icon={ArrowLeft}>
              Return to lesson
            </Button>
          }
        />
      </Card>
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

  // Jump straight to a question from the navigator (same as pressing
  // Previous/Next repeatedly; answers and grading are unaffected).
  const handleJump = (index) => {
    if (index >= 0 && index < questions.length) {
      setCurrentQuestionIdx(index)
    }
  }

  const handleSubmitQuiz = async () => {
    if (submitLoading) {
      return
    }

    setNotice('')

    const unansweredQuestions =
      questions.filter(
        (question) =>
          selectedAnswers[question.id] ===
          undefined
      )

    if (unansweredQuestions.length > 0) {
      setNotice(
        'Please answer all questions before submitting the quiz.'
      )

      return
    }

    if (!studentId) {
      setNotice(
        'Student session could not be identified. Please log in again.'
      )

      return
    }

    if (!monitoringVerified || !monitoring.sessionId) {
      setNotice('Camera monitoring must be active to submit the quiz.')
      return
    }

    if (!attempt?.id || locked) {
      setNotice('Your quiz is being checked. Please wait a moment and try again.')
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

      setNotice(
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
      document.getElementById('answer-review')?.scrollIntoView({ behavior: scrollBehavior() })
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
        <Button to="/subjects" variant="secondary" icon={BookOpen}>
          Back to My Learning
        </Button>
      )
    }

    if (!nextStep || nextStep.kind === 'unknown') {
      return (
        <Badge tone="warning" icon={TriangleAlert}>
          {actionInfo(rlRecommendation.action).label}
        </Badge>
      )
    }

    return (
      <Button onClick={() => performNextStep(nextStep)} size="lg" wrap icon={actionIcon(rlRecommendation.action)}>
        {nextStep.label}
      </Button>
    )
  }

  const renderBreakPanel = () => {
    if (breakSecondsLeft === null) return null
    const done = breakSecondsLeft <= 0
    return (
      <div className="space-y-4 rounded-card border border-info/30 bg-info/[0.06] p-5" role="status" aria-live="polite">
        <div className="flex items-center gap-4">
          <ProgressRing value={done ? 100 : ((60 - breakSecondsLeft) / 60) * 100} size={56} stroke={5} color="#6cb4f8" label="Break progress">
            {done ? <CircleCheck size={20} className="text-info" aria-hidden="true" /> : <Coffee size={20} className="text-info" aria-hidden="true" />}
          </ProgressRing>
          <div className="space-y-1">
            <p className="text-sm font-semibold text-ink">
              {done ? 'Break complete. Welcome back.' : `Focus-recovery break: ${breakSecondsLeft}s`}
            </p>
            <p className="text-[13px] leading-relaxed text-ink-2">
              Look away from the screen at something far away, blink slowly, and take a few deep breaths. Stretch your shoulders. Continue when
              you feel alert.
            </p>
          </div>
        </div>
        <div className="flex flex-wrap gap-2.5">
          <Button to={`/lesson/${lesson.id}`} size="sm" iconRight={ArrowRight}>
            Continue learning
          </Button>
          {!done && (
            <Button onClick={() => setBreakSecondsLeft(null)} size="sm" variant="secondary">
              Skip break
            </Button>
          )}
        </div>
      </div>
    )
  }

  /*
   * RESULTS SCREEN
   */
  if (isFinished && results) {
    const tempo =
      results.timeTaken < questions.length * 15
        ? 'Fast'
        : results.timeTaken < questions.length * 35
          ? 'Moderate'
          : 'Steady'
    const observed = (value, yes, no) => (value === null || value === undefined ? 'Unknown' : value ? yes : no)
    const recommendationInfo = rlRecommendation && !rlRecommendation.error ? actionInfo(rlRecommendation.action) : null
    const strength = Math.round(Number(rlRecommendation?.confidence ?? 0) * 100)

    return (
      <div className="mx-auto max-w-[960px] space-y-6">
        {/* Score */}
        <Card padding="lg" className="relative overflow-hidden">
          <div className="pointer-events-none absolute -left-24 -top-24 h-64 w-64 rounded-full bg-brand-500/[0.12] blur-3xl" aria-hidden="true" />
          <div className="pointer-events-none absolute -bottom-24 right-0 h-56 w-56 rounded-full bg-mint-500/[0.08] blur-3xl" aria-hidden="true" />
          <div className="relative flex flex-col items-center gap-8 text-center md:flex-row md:text-left">
            <ProgressRing value={results.score} size={172} stroke={12} label={`Quiz score ${results.score}%`}>
              <span>
                <span className="block text-[42px] font-semibold leading-none tracking-tight text-ink">{results.score}%</span>
                <span className="mt-1.5 block text-xs font-medium text-ink-2">quiz score</span>
              </span>
            </ProgressRing>
            <div className="min-w-0 flex-1 space-y-4">
              <Badge tone="brand" icon={ClipboardCheck}>
                Assessment results
              </Badge>
              <h1 className="font-display text-[28px] font-semibold leading-tight tracking-tight text-ink sm:text-[32px]">
                {results.correctCount} of {results.totalQuestions} correct
              </h1>
              <p className="text-sm leading-relaxed text-ink-2">
                You correctly answered {results.correctCount} out of {results.totalQuestions} questions at{' '}
                <span className="font-semibold text-ink">{quiz.difficulty}</span> difficulty level.
              </p>
              <div className="flex flex-wrap justify-center gap-2 md:justify-start">
                <DifficultyBadge difficulty={quiz.difficulty} />
                <Badge icon={Clock}>{formatClock(results.timeTaken)}</Badge>
                <Badge icon={Lightbulb}>
                  {hintsCount} {hintsCount === 1 ? 'hint' : 'hints'}
                </Badge>
                <Badge>
                  <SubjectChip subject={resolvedSubject} />
                </Badge>
              </div>
            </div>
          </div>
        </Card>

        {results.mode && results.mode !== 'standard' && (
          <Callout tone="brand" icon={results.mode === 'challenge' ? Timer : results.mode === 'hints' ? Lightbulb : ListChecks}>
            <span className="font-medium text-ink">
              {results.mode === 'challenge'
                ? results.timeTaken <= results.challengeTarget
                  ? `Quick challenge complete: ${results.timeTaken}s, within the ${results.challengeTarget}s target.`
                  : `Quick challenge: ${results.timeTaken}s, ${results.timeTaken - results.challengeTarget}s over the ${results.challengeTarget}s target. Try again to beat it.`
                : results.mode === 'hints'
                  ? `Retry with hints: you used ${hintsCount} hint(s).`
                  : 'Practice attempt recorded.'}
            </span>
          </Callout>
        )}

        {/* AI coach decision */}
        {rlRecommendation?.error ? (
          <Card padding="lg" className="space-y-4 text-center">
            <span className="mx-auto grid h-12 w-12 place-items-center rounded-2xl bg-warning/[0.12] text-warning ring-1 ring-inset ring-warning/25">
              <Camera size={22} aria-hidden="true" />
            </span>
            <p className="mx-auto max-w-md font-display text-base font-semibold text-ink">{rlRecommendation.error}</p>
            <p className="mx-auto max-w-md text-[13px] leading-relaxed text-ink-2">
              {rlRecommendation.telemetryUnavailable
                ? 'Your quiz result was saved. Start the Aegis camera agent before your next attempt to receive adaptive recommendations.'
                : 'The recommendation engine could not resolve a recommendation.'}
            </p>
            <div className="flex justify-center">{renderNextStepsButton()}</div>
          </Card>
        ) : (
          rlRecommendation && (
            <Card as="section" padding="lg" aria-labelledby="coach-decision" className="relative space-y-6 overflow-hidden">
              <div className="pointer-events-none absolute -right-16 -top-20 h-56 w-56 rounded-full bg-brand-500/[0.08] blur-3xl" aria-hidden="true" />
              <SectionHeader
                id="coach-decision"
                icon={Sparkles}
                title="Your AI coach's next step"
                description="Generated by the Aegis adaptive policy from your quiz performance and camera engagement metrics."
              />
              <div className="relative flex flex-col gap-4 rounded-xl border border-brand-500/25 bg-brand-500/[0.06] p-5 sm:flex-row sm:items-start">
                <span className="grid h-12 w-12 shrink-0 place-items-center rounded-xl bg-brand-500/[0.15] text-brand-200 ring-1 ring-inset ring-brand-500/30">
                  <ActionIcon action={rlRecommendation.action} size={22} />
                </span>
                <div className="min-w-0 space-y-1.5">
                  <p className="text-xs font-medium text-brand-300">Suggested pedagogical action</p>
                  <p className="font-display text-xl font-semibold text-ink">{recommendationInfo.label}</p>
                  <p className="text-sm leading-relaxed text-ink-2">{recommendationInfo.description}</p>
                  {rlRecommendation.policy && (
                    <p className="text-xs text-ink-2">Decided by: {POLICY_LABELS[rlRecommendation.policy] || rlRecommendation.policy}</p>
                  )}
                </div>
              </div>

              <figure className="relative space-y-2">
                <figcaption className="text-xs font-medium text-ink-2">Why the coach chose this</figcaption>
                <blockquote className="rounded-xl border border-line bg-deep/60 px-4 py-3.5 text-sm italic leading-relaxed text-ink">
                  “{rlRecommendation.explanation || 'Adaptive recommendation generated from your learning activity.'}”
                </blockquote>
              </figure>

              <div className="relative space-y-2">
                <div className="flex items-center justify-between text-xs">
                  <Tooltip content={CONFIDENCE_NOTE} align="start">
                    <span tabIndex={0} className="cursor-help rounded text-ink-2 underline decoration-line-strong decoration-dotted underline-offset-4">
                      Decision strength
                    </span>
                  </Tooltip>
                  <span className="font-semibold text-mint-300">{strength}%</span>
                </div>
                <ProgressBar value={strength} tone="mint" size="sm" label="Decision strength" />
                <p className="text-[11px] text-ink-2">How clearly this step beat the others. It is not a probability.</p>
              </div>

              <div className="relative flex flex-col gap-3 border-t border-line pt-5 sm:flex-row sm:items-center sm:justify-between">
                <span className="text-sm text-ink-2">Your recommended next step:</span>
                <div className="flex items-center gap-3">{renderNextStepsButton()}</div>
              </div>

              {renderBreakPanel()}
            </Card>
          )
        )}

        {/* Details */}
        <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
          <Card>
            <h3 className="font-display text-[15px] font-semibold text-ink">Speed &amp; hints</h3>
            <dl className="mt-2 divide-y divide-line/70">
              <ResultRow label="Response time">{results.timeTaken} seconds</ResultRow>
              <ResultRow label="Hints used">
                {hintsCount} {hintsCount === 1 ? 'hint' : 'hints'}
              </ResultRow>
              <ResultRow label="Tempo score" tone="text-mint-300">
                {tempo}
              </ResultRow>
            </dl>
          </Card>
          <Card>
            <h3 className="font-display text-[15px] font-semibold text-ink">Attention telemetry</h3>
            <dl className="mt-2 divide-y divide-line/70">
              <ResultRow label="Average attention">
                {results.attentionUsed !== null && results.attentionUsed !== undefined
                  ? `${Math.round(results.attentionUsed * 100)}%`
                  : 'Unavailable (no camera data)'}
              </ResultRow>
              <ResultRow label="Yawning observed" tone={results.yawned ? 'text-warning' : 'text-ink-2'}>
                {observed(results.yawned, 'Yes', 'No')}
              </ResultRow>
              <ResultRow label="Gaze stability" tone={results.lookedAway ? 'text-warning' : 'text-ink-2'}>
                {observed(results.lookedAway, 'Looking away', 'Stable')}
              </ResultRow>
              <ResultRow label="Possible drowsiness" tone={results.drowsy ? 'text-warning' : 'text-ink-2'}>
                {observed(results.drowsy, 'Observed', 'Not observed')}
              </ResultRow>
            </dl>
          </Card>
          <Card>
            <h3 className="font-display text-[15px] font-semibold text-ink">Grading log</h3>
            <dl className="mt-2 divide-y divide-line/70">
              <ResultRow label="Subject">{resolvedSubject}</ResultRow>
              <ResultRow label="Topic">
                <span className="inline-block max-w-[150px] truncate align-bottom">{lesson.topic || lesson.title}</span>
              </ResultRow>
              <ResultRow label="Sync status" tone="text-success">
                <span className="inline-flex items-center gap-1.5">
                  <CircleCheck size={14} aria-hidden="true" />
                  Saved by the server
                </span>
              </ResultRow>
            </dl>
          </Card>
        </div>

        {/* Answer review (correct answers are shown only after grading) */}
        {Array.isArray(results.review) && results.review.length > 0 && (
          <Card as="section" id="answer-review" aria-labelledby="answer-review-title" className="scroll-mt-24 space-y-5">
            <SectionHeader
              id="answer-review-title"
              icon={ListChecks}
              title="Answer review"
              description={`${results.correctCount} correct · ${results.totalQuestions - results.correctCount} to review`}
            />
            <ol className="space-y-3">
              {results.review.map((item, index) => {
                const question = questions.find((q) => q.id === item.question_id)
                const optionText = (letter) => (question ? question[`option_${String(letter).toLowerCase()}`] : '')

                return (
                  <li
                    key={item.question_id}
                    className={cx(
                      'flex gap-3 rounded-xl border p-4',
                      item.is_correct ? 'border-success/25 bg-success/[0.04]' : 'border-danger/25 bg-danger/[0.04]'
                    )}
                  >
                    {item.is_correct ? (
                      <CircleCheck size={19} className="mt-0.5 shrink-0 text-success" aria-hidden="true" />
                    ) : (
                      <CircleX size={19} className="mt-0.5 shrink-0 text-danger" aria-hidden="true" />
                    )}
                    <div className="min-w-0 space-y-1.5">
                      <p className="text-sm font-medium leading-relaxed text-ink">
                        {index + 1}. {question?.question}
                      </p>
                      <p className={cx('text-[13px]', item.is_correct ? 'text-success' : 'text-danger')}>
                        {item.is_correct ? 'Correct' : 'Incorrect'} — your answer: {item.selected_answer}. {optionText(item.selected_answer)}
                      </p>
                      {!item.is_correct && (
                        <p className="text-[13px] text-ink-2">
                          Correct answer: {item.correct_answer}. {optionText(item.correct_answer)}
                        </p>
                      )}
                      {item.explanation && (
                        <p className="text-[13px] leading-relaxed text-ink-2">
                          <span className="font-semibold text-brand-300">Why: </span>
                          {item.explanation}
                        </p>
                      )}
                    </div>
                  </li>
                )
              })}
            </ol>
          </Card>
        )}
      </div>
    )
  }

  const answeredCount = questions.filter((question) => selectedAnswers[question.id] !== undefined).length
  const isLastQuestion = currentQuestionIdx === questions.length - 1
  const challengeTarget = questions.length * CHALLENGE_SECONDS_PER_QUESTION
  const overTarget = attemptMode === 'challenge' && secondsElapsed > challengeTarget
  // The same conditions that always disabled the submit button.
  const submitDisabled =
    submitLoading || locked || !monitoringVerified || Object.keys(selectedAnswers).length < questions.length

  const openSubmitConfirm = () => {
    setNotice('')
    setConfirmOpen(true)
  }
  const confirmSubmit = () => {
    setConfirmOpen(false)
    handleSubmitQuiz()
  }

  const modeBanner = {
    practice: 'Practice attempt recommended by your coach: focus on the questions you missed last time.',
    hints: 'Retry with hints: press the hint button on any question you are unsure about.',
    challenge: `Quick challenge: answer all ${questions.length} questions within ${questions.length * CHALLENGE_SECONDS_PER_QUESTION} seconds.`
  }[attemptMode]

  const timer = (
    <span className="inline-flex items-center gap-1.5 text-sm font-medium tabular-nums text-ink">
      <Clock size={15} className="text-ink-2" aria-hidden="true" />
      <span>{formatClock(secondsElapsed)}</span>
      {attemptMode === 'challenge' && (
        <span className={cx('text-xs font-medium', overTarget ? 'text-danger' : 'text-mint-300')}>/ target {formatClock(challengeTarget)}</span>
      )}
    </span>
  )

  return (
    <div className="mx-auto max-w-[1080px] space-y-5">
      <StrikeWarningModal open={warningOpen && attemptOpen} onClose={() => setWarningOpen(false)} />
      <LeaveQuizModal pending={leaveGuard.pending} onConfirm={leaveGuard.confirm} onCancel={leaveGuard.cancel} />
      <Modal
        open={confirmOpen && attemptOpen}
        onClose={() => setConfirmOpen(false)}
        icon={Send}
        title="Submit your answers?"
        description="Your quiz is graded straight away, and the answers cannot be changed afterwards."
        footer={
          <>
            <Button variant="secondary" onClick={() => setConfirmOpen(false)}>
              Keep reviewing
            </Button>
            <Button onClick={confirmSubmit} disabled={submitDisabled} icon={Send} autoFocus>
              Submit answers
            </Button>
          </>
        }
      >
        <dl className="grid grid-cols-3 gap-2 rounded-xl border border-line bg-deep/60 p-3 text-center">
          <div>
            <dt className="text-[11px] text-ink-2">Answered</dt>
            <dd className="mt-0.5 text-sm font-semibold text-ink">
              {answeredCount}/{questions.length}
            </dd>
          </div>
          <div>
            <dt className="text-[11px] text-ink-2">Hints used</dt>
            <dd className="mt-0.5 text-sm font-semibold text-ink">{hintsCount}</dd>
          </div>
          <div>
            <dt className="text-[11px] text-ink-2">Time</dt>
            <dd className="mt-0.5 text-sm font-semibold text-ink">{formatClock(secondsElapsed)}</dd>
          </div>
        </dl>
        {locked && <p className="mt-3 text-xs text-warning">Your quiz is being checked. Please wait a moment.</p>}
      </Modal>

      <div className="flex flex-wrap items-center justify-between gap-3">
        <Button to={`/lesson/${lesson.id}`} variant="ghost" size="sm" icon={ArrowLeft} className="-ml-2">
          Abort to Lesson
        </Button>
        <SaveStatus state={saveState} />
      </div>

      {attempt?.protected && <IntegrityRulesBanner strikes={attempt.strikes} />}

      {modeBanner && (
        <Callout tone="brand" icon={attemptMode === 'challenge' ? Timer : attemptMode === 'hints' ? Lightbulb : ListChecks}>
          <span className="font-medium text-ink">{modeBanner}</span>
        </Callout>
      )}

      <div className="grid items-start gap-5 lg:grid-cols-[minmax(0,1fr)_288px]">
        <div className="min-w-0 space-y-4">
          <Card padding="none" className="relative">
            {locked && <CheckingOverlay connection={integrity.connection} status={attempt?.status} />}

            <div className="border-b border-line px-5 pb-4 pt-5 sm:px-7">
              <div className="flex flex-wrap items-center justify-between gap-3">
                <p className="text-sm text-ink-2">
                  Question <span className="font-semibold text-ink">{currentQuestionIdx + 1}</span> of {questions.length}
                </p>
                <div className="flex items-center gap-3">
                  <span className="lg:hidden">{timer}</span>
                  <DifficultyBadge difficulty={quiz.difficulty} size="sm" />
                </div>
              </div>
              <ProgressBar
                value={(answeredCount / questions.length) * 100}
                tone="gradient"
                size="xs"
                className="mt-3.5"
                label={`${answeredCount} of ${questions.length} questions answered`}
              />
            </div>

            <div className="space-y-6 px-5 py-6 sm:px-7 sm:py-8">
              <h2 id="quiz-question" className="font-display text-[20px] font-semibold leading-snug text-ink sm:text-[22px]">
                {currentQuestion.question}
              </h2>

              <div role="radiogroup" aria-labelledby="quiz-question" className="grid gap-3">
                {['A', 'B', 'C', 'D'].map((letter) => {
                  const optionText = currentQuestion[`option_${letter.toLowerCase()}`]
                  const isSelected = selectedAnswers[currentQuestion.id] === letter

                  return (
                    <button
                      key={letter}
                      type="button"
                      role="radio"
                      aria-checked={isSelected}
                      disabled={locked}
                      onClick={() => handleSelectOption(letter)}
                      className={cx(
                        'group flex w-full items-center gap-4 rounded-xl border p-3.5 text-left transition-[border-color,background-color,box-shadow] duration-150 disabled:cursor-not-allowed sm:p-4',
                        isSelected
                          ? 'border-brand-500/70 bg-brand-500/[0.1] shadow-[0_0_0_1px_rgb(136_117_255/0.45)]'
                          : 'border-line-strong bg-deep/60 hover:border-[#3a4664] hover:bg-white/[0.025]'
                      )}
                    >
                      <span
                        className={cx(
                          'grid h-8 w-8 shrink-0 place-items-center rounded-lg text-[13px] font-semibold transition-colors duration-150',
                          isSelected ? 'bg-brand-600 text-white shadow-button' : 'bg-raised text-ink-2 ring-1 ring-inset ring-line-strong group-hover:text-ink'
                        )}
                      >
                        {letter}
                      </span>
                      <span className="formula flex-1 text-[15px] leading-relaxed text-ink">{optionText}</span>
                      <CircleCheck
                        size={19}
                        className={cx('shrink-0 text-brand-300 transition-opacity duration-150', isSelected ? 'opacity-100' : 'opacity-0')}
                        aria-hidden="true"
                      />
                    </button>
                  )
                })}
              </div>

              <div>
                {hintsRevealed[currentQuestion.id] ? (
                  <Callout tone="brand" icon={Lightbulb} title="Hint">
                    {currentQuestion.hint || `Review the lesson section on ${lesson.topic}.`}
                  </Callout>
                ) : (
                  <Button variant="ghost" size="sm" icon={Lightbulb} onClick={handleRevealHint} disabled={locked} className="-ml-2">
                    Need a hint?
                  </Button>
                )}
              </div>
            </div>

            <div className="flex items-center justify-between gap-3 border-t border-line px-5 py-4 sm:px-7">
              <Button variant="secondary" icon={ArrowLeft} onClick={handlePrev} disabled={currentQuestionIdx === 0}>
                Previous
              </Button>
              {!isLastQuestion ? (
                <Button onClick={handleNext} iconRight={ArrowRight}>
                  Next
                </Button>
              ) : (
                <Button onClick={openSubmitConfirm} disabled={submitDisabled} loading={submitLoading} icon={submitLoading ? undefined : Send}>
                  {submitLoading ? 'Grading...' : 'Submit quiz'}
                </Button>
              )}
            </div>
          </Card>

          {notice && (
            <Callout tone="warning" role="alert">
              {notice}
            </Callout>
          )}
        </div>

        <aside aria-label="Quiz overview" className="space-y-4 lg:sticky lg:top-24">
          <Card padding="sm" className="space-y-4 sm:p-5">
            <div className="space-y-1">
              <p className="line-clamp-2 text-xs text-ink-2">
                {resolvedSubject} · {lesson.title}
              </p>
              <p className="font-display text-[15px] font-semibold leading-snug text-ink">{quiz.title}</p>
            </div>
            <dl className="grid grid-cols-2 gap-2.5">
              <div className="rounded-lg bg-deep/70 p-3 ring-1 ring-inset ring-line">
                <dt className="text-[11px] text-ink-2">Time</dt>
                <dd className="mt-1 text-sm font-semibold tabular-nums text-ink">{formatClock(secondsElapsed)}</dd>
              </div>
              <div className="rounded-lg bg-deep/70 p-3 ring-1 ring-inset ring-line">
                <dt className="text-[11px] text-ink-2">Answered</dt>
                <dd className="mt-1 text-sm font-semibold tabular-nums text-ink">
                  {answeredCount}/{questions.length}
                </dd>
              </div>
              <div className="rounded-lg bg-deep/70 p-3 ring-1 ring-inset ring-line">
                <dt className="text-[11px] text-ink-2">Hints used</dt>
                <dd className="mt-1 text-sm font-semibold tabular-nums text-ink">{hintsCount}</dd>
              </div>
              <div className="rounded-lg bg-deep/70 p-3 ring-1 ring-inset ring-line">
                <dt className="text-[11px] text-ink-2">{attemptMode === 'challenge' ? 'Target' : 'Camera'}</dt>
                <dd className={cx('mt-1 text-sm font-semibold tabular-nums', attemptMode === 'challenge' ? (overTarget ? 'text-danger' : 'text-mint-300') : monitoringVerified ? 'text-success' : 'text-warning')}>
                  {attemptMode === 'challenge' ? formatClock(challengeTarget) : monitoringVerified ? 'Verified' : 'Paused'}
                </dd>
              </div>
            </dl>
            {!monitoringVerified && <p className="text-xs leading-relaxed text-warning">The timer pauses while camera monitoring is interrupted.</p>}
          </Card>

          <Card padding="sm" className="space-y-3.5 sm:p-5">
            <p className="text-sm font-semibold text-ink">Questions</p>
            <ol className="grid grid-cols-5 gap-2">
              {questions.map((question, index) => {
                const answered = selectedAnswers[question.id] !== undefined
                const current = index === currentQuestionIdx
                return (
                  <li key={question.id}>
                    <button
                      type="button"
                      onClick={() => handleJump(index)}
                      disabled={locked}
                      aria-current={current ? 'step' : undefined}
                      aria-label={`Question ${index + 1}, ${answered ? 'answered' : 'not answered'}${hintsRevealed[question.id] ? ', hint used' : ''}`}
                      className={cx(
                        'relative grid h-10 w-full place-items-center rounded-lg text-[13px] font-semibold tabular-nums transition-[background-color,color,box-shadow] duration-150 disabled:cursor-not-allowed disabled:opacity-60',
                        current
                          ? 'bg-brand-600 text-white shadow-button'
                          : answered
                            ? 'bg-brand-500/[0.14] text-brand-200 ring-1 ring-inset ring-brand-500/30 hover:bg-brand-500/20'
                            : 'bg-deep text-ink-2 ring-1 ring-inset ring-line-strong hover:text-ink'
                      )}
                    >
                      {index + 1}
                      {hintsRevealed[question.id] && (
                        <span className="absolute right-1 top-1 h-1.5 w-1.5 rounded-full bg-warning" aria-hidden="true" />
                      )}
                    </button>
                  </li>
                )
              })}
            </ol>
            <ul className="flex flex-wrap gap-x-3 gap-y-1.5 text-[11px] text-ink-2">
              <li className="flex items-center gap-1.5">
                <span className="h-2.5 w-2.5 rounded-[3px] bg-brand-500/40 ring-1 ring-inset ring-brand-500/40" aria-hidden="true" />
                Answered
              </li>
              <li className="flex items-center gap-1.5">
                <span className="h-2.5 w-2.5 rounded-[3px] bg-deep ring-1 ring-inset ring-line-strong" aria-hidden="true" />
                Not answered
              </li>
              <li className="flex items-center gap-1.5">
                <span className="h-1.5 w-1.5 rounded-full bg-warning" aria-hidden="true" />
                Hint used
              </li>
            </ul>
            <Button variant="secondary" size="sm" fullWidth icon={Send} onClick={openSubmitConfirm} disabled={submitDisabled}>
              Review and submit
            </Button>
          </Card>
        </aside>
      </div>
    </div>
  )
}
