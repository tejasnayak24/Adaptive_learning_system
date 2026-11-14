import React, { useId } from 'react'
import { Link } from 'react-router-dom'
import { BookOpen, CalendarClock, ChevronRight, Compass, Medal, Trophy } from 'lucide-react'
import { Badge, Button, Card, EmptyState, ProgressBar, SectionHeader, cx } from './ui'
import { SubjectChip, SubjectIcon, TopicStatusBadge, TrendBadge } from './learning'
import { TOPIC_STATUS_ORDER, activityText, formatDate, formatPercent, relativeDay, topicStatusInfo } from '../utils/analytics'
import { TONE_SOFT, activityVisual, subjectVisual } from './visuals'

export { DifficultyBadge, SubjectChip, SubjectIcon, TelemetryBadge, TopicStatusBadge, TrendBadge } from './learning'

/** A titled card section. */
export function Panel({ title, subtitle, action, icon, id, padding = 'md', className, children }) {
  const headingId = useId()
  return (
    <Card
      as="section"
      padding={padding}
      id={id}
      aria-labelledby={title ? headingId : undefined}
      className={cx('scroll-mt-24 space-y-5', className)}
    >
      {(title || action) && <SectionHeader id={headingId} title={title} description={subtitle} action={action} icon={icon} />}
      {children}
    </Card>
  )
}

// ---------------------------------------------------------------- subjects

export function SubjectPerformance({ subjects, compact = false, trends }) {
  if (!subjects?.length) {
    return <EmptyState icon={BookOpen} title="No subjects yet" text="Choose your grade to see your subjects." compact />
  }

  if (compact) {
    return (
      <ul className="-mx-2 divide-y divide-line/70">
        {subjects.map((s) => (
          <li key={s.subject}>
            <Link
              to="/subjects"
              state={{ subject: s.subject }}
              className="group flex items-center gap-3.5 rounded-xl px-2 py-3 transition-colors hover:bg-white/[0.025]"
            >
              <SubjectIcon subject={s.subject} size="sm" />
              <div className="min-w-0 flex-1 space-y-2">
                <div className="flex items-baseline justify-between gap-3">
                  <p className="truncate text-sm font-medium text-ink">{s.subject}</p>
                  <p className="shrink-0 text-xs text-ink-2">
                    {s.completed ? (
                      <span className="font-semibold text-success">Complete</span>
                    ) : (
                      <span className="font-semibold text-ink">{formatPercent(s.progress_percent, '0%')}</span>
                    )}{' '}
                    · {s.lessons_completed}/{s.lessons_total} lessons
                  </p>
                </div>
                <ProgressBar value={s.progress_percent} color={subjectVisual(s.subject).color} size="sm" label={`${s.subject} progress`} />
              </div>
              <ChevronRight
                size={16}
                className="shrink-0 text-ink-3 transition-transform duration-200 group-hover:translate-x-0.5"
                aria-hidden="true"
              />
            </Link>
          </li>
        ))}
      </ul>
    )
  }

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
      {subjects.map((s) => (
        <Link
          key={s.subject}
          to="/subjects"
          state={{ subject: s.subject }}
          className="group flex flex-col rounded-card border border-line bg-deep/60 p-4 transition-[border-color,background-color] duration-200 hover:border-line-strong hover:bg-deep"
        >
          <div className="flex items-start gap-2.5">
            <SubjectIcon subject={s.subject} size="sm" />
            <div className="min-w-0 space-y-1.5">
              <p className="text-sm font-semibold leading-tight text-ink">{s.subject}</p>
              {s.completed ? (
                <Badge tone="success" icon={Trophy} size="sm">
                  Complete
                </Badge>
              ) : (
                <TrendBadge trend={trends?.[s.subject]} />
              )}
            </div>
          </div>
          <div className="mt-4 flex items-baseline justify-between gap-2">
            <p className="text-2xl font-semibold text-ink">{formatPercent(s.progress_percent, '0%')}</p>
            <p className="text-xs text-ink-2">
              {s.lessons_completed}/{s.lessons_total} lessons passed
            </p>
          </div>
          <ProgressBar
            className="mt-2"
            value={s.progress_percent}
            color={subjectVisual(s.subject).color}
            size="sm"
            label={`${s.subject} progress`}
          />
          <dl className="mt-4 grid grid-cols-2 gap-3 text-xs">
            <div>
              <dt className="text-ink-2">Quizzes</dt>
              <dd className="mt-0.5 font-semibold text-ink tabular-nums">{s.quiz_attempts}</dd>
            </div>
            <div>
              <dt className="text-ink-2">Average score</dt>
              <dd className="mt-0.5 font-semibold text-ink">{formatPercent(s.average_score, 'No quizzes')}</dd>
            </div>
          </dl>
          <p className="mt-auto pt-3 text-[11px] text-ink-2">
            {s.last_activity_at ? `Last studied ${relativeDay(s.last_activity_at)}` : 'Not started yet'}
          </p>
        </Link>
      ))}
    </div>
  )
}

// ------------------------------------------------------------------ topics

function topicAction(topic) {
  const revise = topic.status === 'weak' || topic.status === 'needs_revision'
  const target = revise ? topic.revise_lesson : topic.next_lesson
  const lessonId = target?.lesson_id || topic.first_lesson_id
  const label = revise ? 'Revise' : topic.status === 'not_started' ? 'Start' : topic.next_lesson ? 'Continue' : 'Review'
  return { lessonId, label, revise }
}

export function TopicPerformance({ topics, subject = 'all' }) {
  const visible = (topics || []).filter((t) => subject === 'all' || t.subject === subject)
  if (!visible.length) {
    return <EmptyState icon={Compass} title="No topics to show" text="Topics appear once your grade is chosen." compact />
  }
  const groups = TOPIC_STATUS_ORDER.map((status) => ({
    status,
    items: visible.filter((t) => t.status === status)
  })).filter((group) => group.items.length)

  return (
    <div className="space-y-6">
      {groups.map(({ status, items }) => (
        <div key={status} className="space-y-3">
          <div className="flex flex-wrap items-center gap-x-3 gap-y-1.5">
            <TopicStatusBadge status={status} />
            <span className="text-xs text-ink-2">
              {items.length} topic{items.length === 1 ? '' : 's'} · {topicStatusInfo(status).help}
            </span>
          </div>
          <ul className="grid grid-cols-1 gap-2.5 lg:grid-cols-2">
            {items.map((t) => {
              const action = topicAction(t)
              return (
                <li
                  key={t.topic_id}
                  className="flex items-center justify-between gap-3 rounded-xl border border-line bg-deep/60 px-4 py-3 transition-colors hover:border-line-strong"
                >
                  <div className="min-w-0 space-y-1">
                    <p className="truncate text-sm font-medium text-ink">{t.topic}</p>
                    <p className="flex min-w-0 flex-wrap items-center gap-x-2 gap-y-0.5 text-xs text-ink-2">
                      <SubjectChip subject={t.subject} />
                      <span aria-hidden="true">·</span>
                      <span>
                        {t.lessons_completed}/{t.lessons_total} lessons
                      </span>
                      <span aria-hidden="true">·</span>
                      <span>
                        {t.quiz_attempts === 0
                          ? 'no quizzes yet'
                          : `${t.quiz_attempts} quiz${t.quiz_attempts === 1 ? '' : 'zes'}, recent avg ${formatPercent(t.recent_average)}`}
                      </span>
                    </p>
                  </div>
                  {action.lessonId && (
                    <Button
                      to={`/lesson/${action.lessonId}`}
                      size="xs"
                      variant={action.revise ? 'secondary' : 'ghost'}
                      iconRight={ChevronRight}
                    >
                      {action.label}
                      <span className="sr-only"> {t.topic}</span>
                    </Button>
                  )}
                </li>
              )
            })}
          </ul>
        </div>
      ))}
    </div>
  )
}

// ---------------------------------------------------------------- activity

export function ActivityFeed({ events, limit = 10 }) {
  const items = (events || []).slice(0, limit)
  if (!items.length) {
    return (
      <EmptyState icon={CalendarClock} title="No activity yet" text="Your quizzes and completed lessons will appear here." compact />
    )
  }
  return (
    <ol className="relative space-y-1">
      {items.map((event, index) => {
        const text = activityText(event)
        const visual = activityVisual(event)
        const Icon = visual.icon
        const to = event.lesson_id ? `/lesson/${event.lesson_id}` : '/subjects'
        const last = index === items.length - 1
        return (
          <li key={`${event.type}-${event.progress_id}-${index}`} className="relative">
            {!last && <span className="absolute bottom-[-6px] left-[21.5px] top-11 w-px bg-line" aria-hidden="true" />}
            <Link to={to} className="group flex items-start gap-3 rounded-xl p-1.5 pr-2 transition-colors hover:bg-white/[0.025]">
              <span className={cx('relative grid h-8 w-8 shrink-0 place-items-center rounded-lg ring-1 ring-inset', TONE_SOFT[visual.tone])}>
                <Icon size={16} aria-hidden="true" />
              </span>
              <span className="min-w-0 flex-1 pt-0.5">
                <span className="block truncate text-sm text-ink">{text.title}</span>
                <span className="block truncate text-xs text-ink-2">{text.detail}</span>
              </span>
              <span className="shrink-0 pt-1 text-[11px] text-ink-2">{relativeDay(event.at)}</span>
            </Link>
          </li>
        )
      })}
    </ol>
  )
}

export function Milestones({ milestones }) {
  if (!milestones?.length) {
    return (
      <EmptyState
        icon={Medal}
        title="No milestones yet"
        text="Milestones are earned from your real results: your first quiz, completed lessons and finished subjects."
        compact
      />
    )
  }
  return (
    <ol className="grid grid-cols-1 gap-3 sm:grid-cols-2">
      {milestones.map((m) => (
        <li key={m.key} className="flex items-center gap-3 rounded-xl border border-line bg-deep/60 px-3.5 py-3">
          <span className="grid h-9 w-9 shrink-0 place-items-center rounded-lg bg-brand-500/[0.12] text-brand-300 ring-1 ring-inset ring-brand-500/25">
            <Medal size={17} aria-hidden="true" />
          </span>
          <span className="min-w-0">
            <span className="block truncate text-sm font-medium text-ink">{m.title}</span>
            <span className="block text-xs text-ink-2">{formatDate(m.at)}</span>
          </span>
        </li>
      ))}
    </ol>
  )
}
