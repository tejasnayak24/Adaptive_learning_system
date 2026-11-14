import React, { useEffect, useState } from 'react'
import { Link, useParams, useLocation } from 'react-router-dom'
import { ArrowLeft, ArrowRight, BookOpen, CircleCheck, CircleDot, ClipboardCheck, ShieldCheck, Timer, Trophy } from 'lucide-react'
import { actionInfo } from '../utils/recommendationActions'
import LessonMaterial, { materialOutline } from '../components/LessonMaterial'
import { DifficultyBadge, SubjectIcon } from '../components/learning'
import { actionIcon, subjectVisual } from '../components/visuals'
import { Badge, Breadcrumbs, Button, Callout, Card, ErrorState, PageSkeleton, ProgressBar, SectionHeader, Tooltip } from '../components/ui'
import { scrollBehavior } from '../hooks/useReducedMotion'
import { useAuth } from '../context/AuthContext'
import { curriculumService } from '../services/curriculumService'
import { lessonService } from '../services/lessonService'
import { progressService } from '../services/progressService'

function findLessonStanding(curriculum, lessonId) {
  for (const subject of curriculum?.subjects || []) {
    for (const unit of subject.units) {
      for (const topic of unit.topics) {
        const match = topic.lessons.find((l) => l.id === lessonId)
        if (match) return { completed: match.completed, best_score: match.best_score, attempts: match.attempts }
      }
    }
  }
  return null
}

export default function LessonDetail() {
  const { id } = useParams()
  const { user } = useAuth()
  const location = useLocation()
  const [lesson, setLesson] = useState(null)
  const [lessonProgress, setLessonProgress] = useState([])
  const [standing, setStanding] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function loadLessonData() {
      try {
        const lessonRes = await lessonService.getLesson(id)

        if (lessonRes.success) {
          setLesson(lessonRes.data)
        }
      } catch (err) {
        setError(err.message || 'Failed to load lesson content')
        setLoading(false)
        return
      }

      try {
        const studentId = user?.id

        if (studentId) {
          const progressRes = await progressService.getStudentProgress(studentId)

          if (progressRes.success) {
            const filtered = progressRes.data.filter((p) => p.lesson_id === parseInt(id, 10))
            setLessonProgress(filtered)
          }
        }
      } catch (err) {
        console.warn('Progress could not be loaded:', err)
      } finally {
        setLoading(false)
      }
    }

    loadLessonData()
  }, [id, user?.id])

  // Completion as the server defines it (one of the lesson's quizzes
  // passed), read from the curriculum tree. Optional: only adds a badge.
  useEffect(() => {
    if (!lesson?.id || !lesson.subject) return undefined
    let cancelled = false
    curriculumService
      .getCurriculum(lesson.subject)
      .then((res) => {
        if (!cancelled) setStanding(findLessonStanding(res.data, lesson.id))
      })
      .catch(() => {})
    return () => {
      cancelled = true
    }
  }, [lesson?.id, lesson?.subject])

  const focusSection = {
    SHOW_WORKED_EXAMPLE: 'worked-examples',
    SHOW_REAL_WORLD_APPLICATION: 'real-world'
  }[location.state?.recommendedAction]

  useEffect(() => {
    if (!lesson || !focusSection) return
    const timer = setTimeout(() => {
      document.getElementById(focusSection)?.scrollIntoView({ behavior: scrollBehavior(), block: 'start' })
    }, 300)
    return () => clearTimeout(timer)
  }, [lesson, focusSection])

  if (loading) {
    return <PageSkeleton variant="reading" label="Loading lesson" />
  }

  if (error || !lesson) {
    return (
      <div className="space-y-6">
        <Button to="/subjects" variant="ghost" size="sm" icon={ArrowLeft}>
          Back to My Learning
        </Button>
        <ErrorState title="Error loading lesson" message={error || 'Lesson not found'} />
      </div>
    )
  }

  // Extract quizzes associated with this lesson
  const quizzes = lesson.quizzes || []

  const getQuizByDifficulty = (diff) => {
    return quizzes.find((q) => q.difficulty.toLowerCase() === diff.toLowerCase())
  }

  const subject = lesson.subject || location.state?.subject || ''
  const navigation = lesson.navigation
  const topicTitle = lesson.curriculum_topic?.title || lesson.topic
  const outline = materialOutline(lesson.material)

  // Guidance when the student arrives here because of a recommendation.
  const recommendedAction = location.state?.recommendedAction
  const recommendationGuide = {
    REPEAT_LESSON: 'Read the lesson again slowly. Note the key terms and try to explain each paragraph in your own words before retaking a quiz.',
    SHOW_REAL_WORLD_APPLICATION: 'Read the highlighted “In the real world” section and think of one more example from your own life before retaking a quiz.',
    SHOW_WORKED_EXAMPLE: 'Work through the highlighted worked examples step by step, then try the practice exercises before retaking a quiz.',
    NEXT_LESSON: 'You are ready for this lesson. Start with the Easy quiz after reading.',
    SKIP_TO_ADVANCED_TOPIC: 'You skipped ahead because of strong results. Start with the Medium or Hard quiz after reading.',
    INCREASE_DIFFICULTY: 'Choose the next harder quiz below.',
    DECREASE_DIFFICULTY: 'Choose an easier quiz below to rebuild confidence.',
    PRACTICE_QUIZ: 'Retake a quiz below for practice.',
    PROVIDE_HINT: 'Retake a quiz below and use the hint button on questions you are unsure about.',
    QUICK_CHALLENGE: 'Pick a quiz below and try to finish it quickly.',
    FOCUS_RECOVERY: 'Take a short break before continuing.'
  }[recommendedAction]

  const attempted = standing ? standing.attempts > 0 : lessonProgress.length > 0
  const scrollToPart = (partId) => document.getElementById(partId)?.scrollIntoView({ behavior: scrollBehavior(), block: 'start' })

  return (
    <div className="mx-auto max-w-[860px] space-y-10">
      {/* Lesson header */}
      <header className="space-y-5">
        <Breadcrumbs
          items={[
            { label: 'My Learning', to: '/subjects', state: { subject } },
            ...(subject ? [{ label: subject, to: '/subjects', state: { subject } }] : []),
            ...(lesson.unit ? [{ label: lesson.unit.title }] : []),
            ...(topicTitle ? [{ label: topicTitle }] : [])
          ]}
        />

        <div className="flex flex-wrap items-center gap-2">
          {subject && (
            <span className="inline-flex items-center gap-2 rounded-lg border border-line-strong bg-white/[0.03] py-1 pl-1 pr-2.5 text-xs font-medium text-ink">
              <SubjectIcon subject={subject} size="xs" />
              {subject}
            </span>
          )}
          {lesson.grade && <Badge>Grade {lesson.grade}</Badge>}
          {standing?.completed ? (
            <Badge tone="success" icon={CircleCheck}>
              Completed · best {Math.round(standing.best_score)}%
            </Badge>
          ) : attempted ? (
            <Badge tone="warning" icon={CircleDot}>
              In progress
            </Badge>
          ) : null}
        </div>

        <h1 className="font-display text-[30px] font-semibold leading-[1.12] tracking-tight text-ink sm:text-[38px]">{lesson.title}</h1>
        {lesson.curriculum_topic?.description && (
          <p className="max-w-2xl text-[15px] leading-relaxed text-ink-2">{lesson.curriculum_topic.description}</p>
        )}

        {navigation && (
          <div className="flex max-w-md items-center gap-3">
            <ProgressBar
              value={((navigation.index + 1) / navigation.total) * 100}
              color={subjectVisual(subject).color}
              size="xs"
              label={`Lesson ${navigation.index + 1} of ${navigation.total}`}
            />
            <span className="shrink-0 text-xs text-ink-2">
              Lesson {navigation.index + 1} of {navigation.total}
            </span>
          </div>
        )}

        {outline.length > 0 && (
          <nav aria-label="In this lesson" className="flex flex-wrap gap-2 border-t border-line pt-5">
            {outline.map((part) => (
              <button
                key={part.id}
                type="button"
                onClick={() => scrollToPart(part.id)}
                className="inline-flex h-8 items-center gap-1.5 rounded-lg border border-line bg-surface px-3 text-xs font-medium text-ink-2 transition-colors hover:border-line-strong hover:text-ink"
              >
                {part.label}
                {part.count !== undefined && <span className="tabular-nums text-ink-3">{part.count}</span>}
              </button>
            ))}
          </nav>
        )}
      </header>

      {recommendationGuide && (
        <Callout tone="mint" icon={actionIcon(recommendedAction)} title={`Coach recommendation: ${actionInfo(recommendedAction).label}`}>
          {recommendationGuide}
        </Callout>
      )}

      {/* Reading pane */}
      {lesson.material ? (
        <article>
          <LessonMaterial material={lesson.material} highlight={focusSection} />
        </article>
      ) : (
        <article className="reading space-y-4">
          {lesson.content.split('\n\n').map((paragraph, index) => (
            <p key={index}>{paragraph}</p>
          ))}
        </article>
      )}

      {/* Assessments */}
      <Card as="section" padding="lg" aria-labelledby="lesson-quizzes" className="space-y-6">
        <SectionHeader
          id="lesson-quizzes"
          icon={ClipboardCheck}
          title="Check your understanding"
          description="Choose a quiz level. Your result updates your progress, and your AI coach suggests the next step."
        />
        <div className="grid grid-cols-1 gap-3 md:grid-cols-3">
          {['Easy', 'Medium', 'Hard'].map((diff) => {
            const quiz = getQuizByDifficulty(diff)
            const levelRows = lessonProgress.filter((p) => p.difficulty.toLowerCase() === diff.toLowerCase())
            const attemptsCount = levelRows.length
            const bestAttempt = [...levelRows].sort((a, b) => b.quiz_score - a.quiz_score)[0]

            return (
              <div key={diff} className="flex flex-col rounded-xl border border-line bg-deep/60 p-4 transition-colors hover:border-line-strong">
                <DifficultyBadge difficulty={diff} className="self-start" />
                <p className="mt-4 text-2xl font-semibold text-ink">{attemptsCount === 0 ? '—' : `${Math.round(bestAttempt.quiz_score)}%`}</p>
                <p className="mt-0.5 text-xs text-ink-2">
                  {attemptsCount === 0 ? 'No attempts yet' : `Best of ${attemptsCount} attempt${attemptsCount === 1 ? '' : 's'}`}
                </p>
                {quiz ? (
                  <div className="mt-5 flex gap-2">
                    <Button to={`/quiz/${quiz.id}`} state={{ subject, attempt: Date.now() }} size="sm" iconRight={ArrowRight} className="flex-1">
                      Take quiz
                    </Button>
                    <Tooltip content="Timed challenge: 30 seconds per question" align="end">
                      <Button
                        to={`/quiz/${quiz.id}`}
                        state={{ subject, attempt: Date.now(), mode: 'challenge' }}
                        size="sm"
                        variant="secondary"
                        icon={Timer}
                        aria-label={`${diff} quiz as a timed challenge, 30 seconds per question`}
                      >
                        Challenge
                      </Button>
                    </Tooltip>
                  </div>
                ) : (
                  <Button size="sm" variant="secondary" disabled className="mt-5 w-full">
                    Unavailable
                  </Button>
                )}
              </div>
            )
          })}
        </div>
        <p className="flex items-start gap-2 text-xs leading-relaxed text-ink-2">
          <ShieldCheck size={15} className="mt-px shrink-0 text-ink-3" aria-hidden="true" />
          Quizzes are protected: keep the quiz page open until you submit. Hints stay available, and camera monitoring must be on.
        </p>
      </Card>

      {navigation && (
        <nav aria-label="Lesson navigation" className="grid grid-cols-1 gap-3 sm:grid-cols-2">
          {navigation.previous ? (
            <Link
              to={`/lesson/${navigation.previous.id}`}
              className="group rounded-card border border-line bg-surface p-4 shadow-card transition-colors hover:border-line-strong"
            >
              <span className="flex items-center gap-1.5 text-xs font-medium text-ink-2">
                <ArrowLeft size={14} className="transition-transform group-hover:-translate-x-0.5" aria-hidden="true" />
                Previous lesson
              </span>
              <span className="mt-1.5 block truncate text-sm font-medium text-ink">{navigation.previous.title}</span>
            </Link>
          ) : (
            <span className="hidden sm:block" />
          )}
          {navigation.next ? (
            <Link
              to={`/lesson/${navigation.next.id}`}
              className="group rounded-card border border-brand-500/30 bg-brand-500/[0.06] p-4 text-right shadow-card transition-colors hover:border-brand-500/50 hover:bg-brand-500/[0.09]"
            >
              <span className="flex items-center justify-end gap-1.5 text-xs font-medium text-brand-300">
                Next lesson
                <ArrowRight size={14} className="transition-transform group-hover:translate-x-0.5" aria-hidden="true" />
              </span>
              <span className="mt-1.5 block truncate text-sm font-medium text-ink">{navigation.next.title}</span>
            </Link>
          ) : (
            <Link
              to="/subjects"
              className="group flex items-center justify-end gap-3 rounded-card border border-success/30 bg-success/[0.06] p-4 text-right shadow-card transition-colors hover:border-success/50"
            >
              <span>
                <span className="flex items-center justify-end gap-1.5 text-xs font-medium text-success">
                  <Trophy size={14} aria-hidden="true" />
                  Last lesson in this subject
                </span>
                <span className="mt-1.5 block text-sm font-medium text-ink">Back to My Learning</span>
              </span>
              <BookOpen size={18} className="shrink-0 text-ink-2" aria-hidden="true" />
            </Link>
          )}
        </nav>
      )}
    </div>
  )
}
