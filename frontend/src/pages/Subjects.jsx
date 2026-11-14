import React, { useEffect, useMemo, useState } from 'react'
import { useLocation } from 'react-router-dom'
import { ArrowRight, BookOpen, CircleCheck, GraduationCap, Search, SearchX, Star, Trophy } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import { GradePicker } from '../components/GradeGate'
import { DifficultyBadge, SubjectIcon } from '../components/learning'
import { subjectVisual } from '../components/visuals'
import {
  Badge,
  Button,
  Callout,
  Card,
  EmptyState,
  INPUT_CLASS,
  PageHeader,
  ProgressBar,
  ProgressRing,
  SegmentedControl,
  Skeleton,
  cx
} from '../components/ui'
import { SUBJECTS, curriculumService } from '../services/curriculumService'

// A lesson is "completed" when the server says so (a quiz passed); "mastered"
// keeps this page's earlier rule of a best score of 80% or more.
const MASTERY_SCORE = 80

function lessonStatus(lesson) {
  if (lesson.completed && lesson.best_score >= MASTERY_SCORE) return 'mastered'
  if (lesson.completed) return 'completed'
  if (lesson.attempts > 0) return 'in_progress'
  return 'not_started'
}

const STATUS_META = {
  mastered: { label: 'Mastered', tone: 'success', action: 'Review' },
  completed: { label: 'Completed', tone: 'mint', action: 'Review' },
  in_progress: { label: 'In progress', tone: 'warning', action: 'Continue' },
  not_started: { label: 'Not started', tone: 'neutral', action: 'Start' }
}

const FILTERS = [
  { value: 'all', label: 'All' },
  { value: 'todo', label: 'To do' },
  { value: 'in_progress', label: 'In progress' },
  { value: 'done', label: 'Completed' }
]

function matchesFilter(status, filter) {
  if (filter === 'all') return true
  if (filter === 'todo') return status === 'not_started'
  if (filter === 'in_progress') return status === 'in_progress'
  return status === 'completed' || status === 'mastered'
}

function allLessons(subject) {
  const list = []
  for (const unit of subject?.units || []) {
    for (const topic of unit.topics) {
      for (const lesson of topic.lessons) list.push({ lesson, topic, unit })
    }
  }
  return list
}

function SubjectCard({ name, data, selected, onSelect }) {
  const visual = subjectVisual(name)
  const lessons = allLessons(data)
  const total = data?.lesson_count ?? lessons.length
  const completed = lessons.filter(({ lesson }) => lesson.completed).length
  const started = data?.lessons_attempted ?? 0
  const percent = total ? (completed / total) * 100 : 0
  return (
    <button
      type="button"
      onClick={onSelect}
      aria-pressed={selected}
      className={cx(
        'group relative flex flex-col gap-4 overflow-hidden rounded-card border bg-surface p-4 text-left shadow-card transition-[border-color,background-color,transform] duration-200 hover:-translate-y-0.5 sm:p-5',
        selected ? 'bg-[#182036]' : 'border-line hover:border-line-strong'
      )}
      style={selected ? { borderColor: visual.ring, boxShadow: `0 0 0 1px ${visual.ring}, 0 14px 34px -18px ${visual.glow}` } : undefined}
    >
      <span
        className={cx('absolute inset-x-0 top-0 h-[2px] transition-opacity duration-200', selected ? 'opacity-100' : 'opacity-0')}
        style={{ background: visual.color }}
        aria-hidden="true"
      />
      <div className="flex items-start justify-between gap-3">
        <SubjectIcon subject={name} size="md" />
        <ProgressRing value={percent} size={44} stroke={4} color={visual.color} label={`${Math.round(percent)}% of ${name} completed`}>
          <span className="text-[11px] font-semibold text-ink">{Math.round(percent)}%</span>
        </ProgressRing>
      </div>
      <div className="space-y-1">
        <p className="font-display text-[15px] font-semibold text-ink sm:text-base">{name}</p>
        <p className="text-xs text-ink-2">
          {total ? (
            <>
              {completed}/{total} passed · {started} started
            </>
          ) : (
            'No lessons yet'
          )}
        </p>
      </div>
    </button>
  )
}

function StatusNode({ status, position }) {
  if (status === 'mastered' || status === 'completed') {
    return (
      <span
        className={cx(
          'relative z-10 grid h-8 w-8 shrink-0 place-items-center rounded-full ring-1 ring-inset',
          status === 'mastered' ? 'bg-success/15 text-success ring-success/35' : 'bg-mint-500/15 text-mint-300 ring-mint-500/35'
        )}
      >
        {status === 'mastered' ? <Star size={15} aria-hidden="true" /> : <CircleCheck size={16} aria-hidden="true" />}
      </span>
    )
  }
  if (status === 'in_progress') {
    return (
      <span className="relative z-10 grid h-8 w-8 shrink-0 place-items-center rounded-full bg-warning/10 text-[12px] font-semibold text-warning ring-1 ring-inset ring-warning/40">
        {position}
      </span>
    )
  }
  return (
    <span className="relative z-10 grid h-8 w-8 shrink-0 place-items-center rounded-full bg-deep text-[12px] font-semibold text-ink-2 ring-1 ring-inset ring-line-strong">
      {position}
    </span>
  )
}

function LessonRow({ lesson, subject, last, highlight }) {
  const status = lessonStatus(lesson)
  const meta = STATUS_META[status]
  return (
    <li className="relative">
      {!last && <span className="absolute bottom-0 left-[15.5px] top-10 w-px bg-line-strong/70" aria-hidden="true" />}
      <div
        className={cx(
          'flex flex-col gap-3 rounded-xl px-2 py-3 transition-colors duration-150 hover:bg-white/[0.02] sm:flex-row sm:items-center sm:gap-4',
          highlight && 'bg-brand-500/[0.05] ring-1 ring-inset ring-brand-500/25 hover:bg-brand-500/[0.07]'
        )}
      >
        <div className="flex min-w-0 flex-1 items-start gap-3.5 sm:items-center">
          <StatusNode status={status} position={lesson.position} />
          <div className="min-w-0 flex-1 space-y-1">
            <div className="flex flex-wrap items-center gap-2">
              <p className="text-sm font-medium text-ink">{lesson.title}</p>
              {highlight && (
                <Badge tone="brand" size="sm">
                  Next up
                </Badge>
              )}
            </div>
            <p className="flex flex-wrap items-center gap-x-2 gap-y-1 text-xs text-ink-2">
              <span className={cx(status === 'not_started' ? 'text-ink-2' : '')}>{meta.label}</span>
              {lesson.attempts > 0 && (
                <>
                  <span aria-hidden="true">·</span>
                  <span>
                    Best <span className="font-semibold text-ink">{Math.round(lesson.best_score)}%</span> in {lesson.attempts} attempt
                    {lesson.attempts === 1 ? '' : 's'}
                  </span>
                </>
              )}
            </p>
          </div>
        </div>
        <div className="flex items-center justify-between gap-3 pl-[46px] sm:justify-end sm:pl-0">
          <div className="hidden items-center gap-1.5 md:flex" aria-label="Quiz levels">
            {lesson.quizzes.map((quiz) => (
              <DifficultyBadge key={quiz.id} difficulty={quiz.difficulty} size="sm" />
            ))}
          </div>
          <p className="text-xs text-ink-2 md:hidden">
            {lesson.quizzes.length} quiz level{lesson.quizzes.length === 1 ? '' : 's'}
          </p>
          <Button
            to={`/lesson/${lesson.id}`}
            state={{ subject }}
            size="sm"
            variant={highlight || status === 'in_progress' ? 'primary' : 'secondary'}
            iconRight={ArrowRight}
          >
            {meta.action}
            <span className="sr-only"> {lesson.title}</span>
          </Button>
        </div>
      </div>
    </li>
  )
}

function SubjectsSkeleton() {
  return (
    <div className="space-y-8" aria-busy="true" aria-label="Loading your curriculum" role="status">
      <div className="space-y-3">
        <Skeleton className="h-4 w-28" />
        <Skeleton className="h-9 w-72" />
        <Skeleton className="h-4 w-full max-w-xl" />
      </div>
      <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
        {[0, 1, 2, 3].map((i) => (
          <Skeleton key={i} className="h-36 rounded-card" />
        ))}
      </div>
      <Skeleton className="h-80 rounded-card" />
    </div>
  )
}

export default function Subjects() {
  const { user } = useAuth()
  const [curriculum, setCurriculum] = useState(null)
  const location = useLocation()
  // Analytics pages link here with the subject to open.
  const [selectedSubject, setSelectedSubject] = useState(
    SUBJECTS.includes(location.state?.subject) ? location.state.subject : SUBJECTS[0]
  )
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [changingGrade, setChangingGrade] = useState(false)
  const [query, setQuery] = useState('')
  const [filter, setFilter] = useState('all')

  useEffect(() => {
    let cancelled = false
    async function load() {
      setLoading(true)
      setError('')
      try {
        const res = await curriculumService.getCurriculum()
        if (!cancelled) setCurriculum(res.data)
      } catch (err) {
        if (!cancelled) setError(err.message || 'Failed to load your curriculum')
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    load()
    return () => {
      cancelled = true
    }
  }, [user?.grade])

  const subjects = useMemo(() => curriculum?.subjects || [], [curriculum])
  const subject = subjects.find((s) => s.subject === selectedSubject)
  const lessons = useMemo(() => allLessons(subject), [subject])
  const nextUp = lessons.find(({ lesson }) => !lesson.completed) || null

  const counts = useMemo(() => {
    const result = { all: lessons.length, todo: 0, in_progress: 0, done: 0 }
    for (const { lesson } of lessons) {
      const status = lessonStatus(lesson)
      if (matchesFilter(status, 'todo')) result.todo += 1
      if (matchesFilter(status, 'in_progress')) result.in_progress += 1
      if (matchesFilter(status, 'done')) result.done += 1
    }
    return result
  }, [lessons])

  const needle = query.trim().toLowerCase()
  const visibleUnits = useMemo(() => {
    if (!subject) return []
    return subject.units
      .map((unit) => ({
        ...unit,
        topics: unit.topics
          .map((topic) => ({
            ...topic,
            lessons: topic.lessons.filter(
              (lesson) =>
                matchesFilter(lessonStatus(lesson), filter) &&
                (!needle || lesson.title.toLowerCase().includes(needle) || topic.title.toLowerCase().includes(needle))
            )
          }))
          .filter((topic) => topic.lessons.length)
      }))
      .filter((unit) => unit.topics.length)
  }, [subject, filter, needle])

  if (changingGrade) {
    return (
      <div className="space-y-4">
        <GradePicker
          current={user?.grade}
          title="Change your grade"
          subtitle="Your previous quiz results are kept. You will see the lessons for the grade you choose."
          onPicked={() => setChangingGrade(false)}
        />
        <div className="text-center">
          <Button variant="ghost" size="sm" onClick={() => setChangingGrade(false)}>
            Cancel
          </Button>
        </div>
      </div>
    )
  }

  if (loading) return <SubjectsSkeleton />

  const grade = curriculum?.grade ?? user?.grade

  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="My Learning"
        title={grade ? `Grade ${grade} curriculum` : 'Your curriculum'}
        description="Lessons organised by subject, unit and topic. Each lesson has explanations, worked examples and Easy, Medium and Hard quizzes. A lesson is completed when you pass one of its quizzes."
        actions={
          (user?.role || 'student') === 'student' && (
            <Button variant="secondary" size="sm" icon={GraduationCap} onClick={() => setChangingGrade(true)}>
              Grade {user?.grade} · Change
            </Button>
          )
        }
      />

      {error && (
        <Callout tone="danger" role="alert">
          {error}
        </Callout>
      )}

      <div className="grid grid-cols-2 gap-3 lg:grid-cols-4 lg:gap-4" role="group" aria-label="Subjects">
        {SUBJECTS.map((name) => (
          <SubjectCard
            key={name}
            name={name}
            data={subjects.find((s) => s.subject === name)}
            selected={selectedSubject === name}
            onSelect={() => setSelectedSubject(name)}
          />
        ))}
      </div>

      {!subject ? (
        <Card>
          <EmptyState
            icon={BookOpen}
            title="No lessons yet"
            text={`No ${selectedSubject} lessons are available for your grade. Ask your teacher to import the curriculum.`}
          />
        </Card>
      ) : (
        <div className="space-y-6">
          {nextUp ? (
            <Card padding="sm" className="relative overflow-hidden sm:p-5">
              <div
                className="pointer-events-none absolute -right-10 -top-16 h-40 w-40 rounded-full blur-3xl"
                style={{ background: subjectVisual(selectedSubject).glow }}
                aria-hidden="true"
              />
              <div className="relative flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <div className="flex min-w-0 items-center gap-4">
                  <SubjectIcon subject={selectedSubject} size="lg" />
                  <div className="min-w-0 space-y-1">
                    <p className="text-xs font-medium text-ink-2">Next up in {selectedSubject}</p>
                    <p className="truncate font-display text-lg font-semibold text-ink">{nextUp.lesson.title}</p>
                    <p className="truncate text-xs text-ink-2">
                      {nextUp.unit.title} · {nextUp.topic.title}
                    </p>
                  </div>
                </div>
                <Button to={`/lesson/${nextUp.lesson.id}`} state={{ subject: selectedSubject }} iconRight={ArrowRight} className="shrink-0">
                  {nextUp.lesson.attempts > 0 ? 'Continue lesson' : 'Start lesson'}
                </Button>
              </div>
            </Card>
          ) : (
            <Callout tone="success" icon={Trophy} title={`Every ${selectedSubject} lesson is completed`}>
              You can still review any lesson and retake its quizzes.
            </Callout>
          )}

          <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
            <div className="relative w-full md:max-w-xs">
              <Search size={16} className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-ink-3" aria-hidden="true" />
              <input
                type="search"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder={`Search ${selectedSubject} lessons`}
                aria-label={`Search ${selectedSubject} lessons`}
                className={cx(INPUT_CLASS, 'h-10 pl-9 pr-3')}
              />
            </div>
            <SegmentedControl
              label="Filter lessons by status"
              value={filter}
              onChange={setFilter}
              options={FILTERS.map((option) => ({ ...option, count: counts[option.value] }))}
            />
          </div>

          {visibleUnits.length === 0 ? (
            <Card>
              <EmptyState
                icon={SearchX}
                title="No lessons match"
                text="Try a different search or show all lessons."
                action={
                  <Button
                    variant="secondary"
                    size="sm"
                    onClick={() => {
                      setQuery('')
                      setFilter('all')
                    }}
                  >
                    Clear filters
                  </Button>
                }
              />
            </Card>
          ) : (
            <div className="space-y-5">
              {visibleUnits.map((unit) => {
                const fullUnit = subject.units.find((u) => u.id === unit.id)
                const unitLessons = fullUnit.topics.flatMap((t) => t.lessons)
                const unitDone = unitLessons.filter((l) => l.completed).length
                return (
                  <Card as="section" key={unit.id} padding="none" aria-label={unit.title}>
                    <header className="flex flex-col gap-3 border-b border-line px-5 py-4 sm:flex-row sm:items-center sm:justify-between sm:px-6">
                      <div className="min-w-0">
                        <p className="text-xs font-medium text-ink-2">Unit</p>
                        <h2 className="font-display text-lg font-semibold tracking-tight text-ink">{unit.title}</h2>
                      </div>
                      <div className="flex items-center gap-3 sm:w-56">
                        <ProgressBar
                          value={unitLessons.length ? (unitDone / unitLessons.length) * 100 : 0}
                          color={subjectVisual(selectedSubject).color}
                          size="sm"
                          label={`${unit.title} progress`}
                        />
                        <span className="shrink-0 text-xs text-ink-2">
                          <span className="font-semibold text-ink">{unitDone}</span>/{unitLessons.length} passed
                        </span>
                      </div>
                    </header>
                    <div className="divide-y divide-line/60">
                      {unit.topics.map((topic) => (
                        <div key={topic.id} className="px-3 py-4 sm:px-4">
                          <div className="px-2 pb-2">
                            <h3 className="text-sm font-semibold text-ink">{topic.title}</h3>
                            {topic.description && <p className="mt-0.5 text-xs leading-relaxed text-ink-2">{topic.description}</p>}
                          </div>
                          <ol className="space-y-0.5">
                            {topic.lessons.map((lesson, index) => (
                              <LessonRow
                                key={lesson.id}
                                lesson={lesson}
                                subject={selectedSubject}
                                last={index === topic.lessons.length - 1}
                                highlight={nextUp?.lesson.id === lesson.id}
                              />
                            ))}
                          </ol>
                        </div>
                      ))}
                    </div>
                  </Card>
                )
              })}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
