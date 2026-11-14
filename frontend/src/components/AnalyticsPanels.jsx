import React from 'react'
import { Link } from 'react-router-dom'
import {
  SCORE_COLOR,
  TELEMETRY_HELP,
  TELEMETRY_LABELS,
  TOPIC_STATUS_ORDER,
  activityText,
  formatDate,
  formatPercent,
  relativeDay,
  subjectColor,
  topicStatusInfo
} from '../utils/analytics'

const TONES = {
  emerald: 'bg-emerald-500/10 text-emerald-300 border-emerald-500/25',
  amber: 'bg-amber-500/10 text-amber-300 border-amber-500/25',
  rose: 'bg-rose-500/10 text-rose-300 border-rose-500/25',
  slate: 'bg-slate-800/60 text-slate-300 border-slate-700'
}

export function Panel({ title, subtitle, action, children, className = '' }) {
  return (
    <section className={`glass-panel rounded-3xl p-5 sm:p-6 border border-slate-900 shadow-lg space-y-4 ${className}`}>
      {(title || action) && (
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div className="min-w-0">
            {title && <h2 className="text-base font-bold text-white">{title}</h2>}
            {subtitle && <p className="text-xs text-slate-500 mt-0.5 leading-relaxed">{subtitle}</p>}
          </div>
          {action}
        </div>
      )}
      {children}
    </section>
  )
}

export function StatTile({ label, value, sub, icon, help }) {
  return (
    <div className="glass-panel rounded-3xl p-5 border border-slate-900 shadow-md relative" title={help}>
      <p className="text-[11px] font-semibold uppercase tracking-wider text-slate-500 pr-8">{label}</p>
      <p className="mt-3 text-3xl font-extrabold text-white tabular-nums">{value}</p>
      {sub && <p className="mt-1 text-xs text-slate-400">{sub}</p>}
      {icon && (
        <span className="absolute right-5 top-5 text-xl select-none" aria-hidden="true">
          {icon}
        </span>
      )}
    </div>
  )
}

export function ProgressBar({ percent, color = SCORE_COLOR, label }) {
  const width = Math.max(0, Math.min(100, Number(percent) || 0))
  return (
    <div
      className="w-full bg-slate-900 rounded-full h-2 overflow-hidden"
      role="progressbar"
      aria-valuenow={Math.round(width)}
      aria-valuemin={0}
      aria-valuemax={100}
      aria-label={label}
    >
      <div className="h-2 rounded-full" style={{ width: `${width}%`, background: color }} />
    </div>
  )
}

export function LoadingSkeleton({ blocks = 4 }) {
  return (
    <div className="space-y-6 animate-pulse" aria-busy="true" aria-label="Loading">
      <div className="h-24 bg-slate-800/70 rounded-3xl" />
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {[...Array(blocks)].map((_, i) => (
          <div key={i} className="h-28 bg-slate-800/70 rounded-3xl" />
        ))}
      </div>
      <div className="h-72 bg-slate-800/70 rounded-3xl" />
    </div>
  )
}

export function ErrorState({ message, onRetry }) {
  return (
    <div className="rounded-3xl border border-rose-500/25 bg-rose-500/10 p-6 text-center space-y-3" role="alert">
      <p className="text-sm font-semibold text-rose-200">We could not load your learning data.</p>
      <p className="text-xs text-rose-300/80">{message}</p>
      {onRetry && (
        <button
          type="button"
          onClick={onRetry}
          className="px-4 py-2 rounded-xl bg-slate-900 border border-slate-700 text-xs font-semibold text-slate-200 hover:bg-slate-800"
        >
          Try again
        </button>
      )}
    </div>
  )
}

export function EmptyState({ icon = '📊', title, text, action }) {
  return (
    <div className="flex flex-col items-center justify-center text-center py-10 px-4 space-y-2">
      <div className="text-3xl" aria-hidden="true">
        {icon}
      </div>
      <p className="text-sm font-semibold text-slate-300">{title}</p>
      {text && <p className="text-xs text-slate-500 max-w-sm leading-relaxed">{text}</p>}
      {action}
    </div>
  )
}

export function StatusBadge({ status }) {
  const info = topicStatusInfo(status)
  return (
    <span
      className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full border text-[10px] font-bold ${TONES[info.tone]}`}
      title={info.help}
    >
      <span aria-hidden="true">{info.icon}</span>
      {info.label}
    </span>
  )
}

export function TelemetryBadge({ telemetry }) {
  const tone = telemetry === 'measured' ? 'emerald' : telemetry === 'unavailable' ? 'amber' : 'slate'
  return (
    <span
      className={`inline-flex px-2 py-0.5 rounded-full border text-[10px] font-semibold ${TONES[tone]}`}
      title={TELEMETRY_HELP[telemetry]}
    >
      {TELEMETRY_LABELS[telemetry] || telemetry}
    </span>
  )
}

// ---------------------------------------------------------------- subjects

export function SubjectPerformance({ subjects, compact = false }) {
  if (!subjects?.length) {
    return <EmptyState icon="📚" title="No subjects yet" text="Choose your grade to see your subjects." />
  }
  return (
    <div className={`grid grid-cols-1 ${compact ? 'sm:grid-cols-2' : 'md:grid-cols-2 xl:grid-cols-4'} gap-4`}>
      {subjects.map((s) => (
        <Link
          key={s.subject}
          to="/subjects"
          state={{ subject: s.subject }}
          className="block rounded-2xl bg-slate-900/40 border border-slate-800 hover:border-slate-600 p-4 space-y-3 transition-colors"
        >
          <div className="flex items-center justify-between gap-2">
            <span className="flex items-center gap-2 text-sm font-bold text-white">
              <span className="h-2.5 w-2.5 rounded-full shrink-0" style={{ background: subjectColor(s.subject) }} aria-hidden="true" />
              {s.subject}
            </span>
            {s.completed ? (
              <span className="text-[10px] font-bold text-emerald-300">🏆 Complete</span>
            ) : (
              <span className="text-xs font-bold text-slate-300 tabular-nums">{formatPercent(s.progress_percent)}</span>
            )}
          </div>
          <ProgressBar percent={s.progress_percent} color={subjectColor(s.subject)} label={`${s.subject} progress`} />
          <dl className="grid grid-cols-3 gap-2 text-[11px]">
            <div>
              <dt className="text-slate-500">Lessons</dt>
              <dd className="font-semibold text-slate-200 tabular-nums">
                {s.lessons_completed}/{s.lessons_total}
              </dd>
            </div>
            <div>
              <dt className="text-slate-500">Quizzes</dt>
              <dd className="font-semibold text-slate-200 tabular-nums">{s.quiz_attempts}</dd>
            </div>
            <div>
              <dt className="text-slate-500">Avg score</dt>
              <dd className="font-semibold text-slate-200 tabular-nums">{formatPercent(s.average_score, 'No quizzes')}</dd>
            </div>
          </dl>
          {!compact && (
            <p className="text-[10px] text-slate-500">
              {s.last_activity_at ? `Last studied ${relativeDay(s.last_activity_at)}` : 'Not started yet'}
            </p>
          )}
        </Link>
      ))}
    </div>
  )
}

// ------------------------------------------------------------------ topics

export function TopicPerformance({ topics, subject = 'all' }) {
  const visible = (topics || []).filter((t) => subject === 'all' || t.subject === subject)
  if (!visible.length) {
    return <EmptyState icon="🧭" title="No topics to show" text="Topics appear once your grade is chosen." />
  }
  const groups = TOPIC_STATUS_ORDER.map((status) => ({
    status,
    items: visible.filter((t) => t.status === status)
  })).filter((g) => g.items.length)

  return (
    <div className="space-y-5">
      {groups.map(({ status, items }) => (
        <div key={status} className="space-y-2">
          <div className="flex items-center gap-2">
            <StatusBadge status={status} />
            <span className="text-[11px] text-slate-500">
              {items.length} topic{items.length === 1 ? '' : 's'} · {topicStatusInfo(status).help}
            </span>
          </div>
          <ul className="grid grid-cols-1 lg:grid-cols-2 gap-2">
            {items.map((t) => {
              const target = t.status === 'weak' || t.status === 'needs_revision' ? t.revise_lesson : t.next_lesson
              const lessonId = target?.lesson_id || t.first_lesson_id
              return (
                <li
                  key={t.topic_id}
                  className="flex items-center justify-between gap-3 rounded-2xl bg-slate-900/40 border border-slate-800 px-4 py-3"
                >
                  <div className="min-w-0">
                    <p className="text-sm font-semibold text-slate-100 truncate">{t.topic}</p>
                    <p className="text-[11px] text-slate-500 truncate">
                      <span style={{ color: subjectColor(t.subject) }} aria-hidden="true">
                        ●{' '}
                      </span>
                      {t.subject} · {t.lessons_completed}/{t.lessons_total} lessons ·{' '}
                      {t.quiz_attempts === 0
                        ? 'no quizzes yet'
                        : `${t.quiz_attempts} quiz${t.quiz_attempts === 1 ? '' : 'zes'}, recent avg ${formatPercent(t.recent_average)}`}
                    </p>
                  </div>
                  {lessonId && (
                    <Link
                      to={`/lesson/${lessonId}`}
                      className="shrink-0 px-3 py-1.5 text-[11px] font-semibold rounded-lg bg-slate-900 border border-slate-700 text-slate-200 hover:bg-indigo-600 hover:border-indigo-600"
                    >
                      {t.status === 'weak' || t.status === 'needs_revision'
                        ? 'Revise'
                        : t.status === 'not_started'
                          ? 'Start'
                          : t.next_lesson
                            ? 'Continue'
                            : 'Review'}
                    </Link>
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
    return <EmptyState icon="🗓️" title="No activity yet" text="Your quizzes and completed lessons will appear here." />
  }
  return (
    <ol className="space-y-2">
      {items.map((event, index) => {
        const text = activityText(event)
        const to = event.lesson_id ? `/lesson/${event.lesson_id}` : '/subjects'
        return (
          <li key={`${event.type}-${event.progress_id}-${index}`}>
            <Link
              to={to}
              className="flex items-start gap-3 rounded-2xl px-3 py-2.5 hover:bg-slate-900/50 transition-colors"
            >
              <span className="text-lg leading-none mt-0.5" aria-hidden="true">
                {text.icon}
              </span>
              <span className="min-w-0 flex-1">
                <span className="block text-sm text-slate-100 truncate">{text.title}</span>
                <span className="block text-[11px] text-slate-500 truncate">{text.detail}</span>
              </span>
              <span className="shrink-0 text-[10px] text-slate-500 mt-1">{relativeDay(event.at)}</span>
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
      <p className="text-xs text-slate-500">
        Milestones are earned from your real results — your first quiz, completed lessons and finished subjects.
      </p>
    )
  }
  return (
    <ul className="flex flex-wrap gap-2">
      {milestones.map((m) => (
        <li
          key={m.key}
          className="inline-flex items-center gap-2 rounded-full border border-indigo-500/25 bg-indigo-500/10 px-3 py-1.5 text-xs text-indigo-200"
          title={formatDate(m.at)}
        >
          <span aria-hidden="true">🏅</span>
          {m.title}
          <span className="text-[10px] text-indigo-300/70">{formatDate(m.at)}</span>
        </li>
      ))}
    </ul>
  )
}
