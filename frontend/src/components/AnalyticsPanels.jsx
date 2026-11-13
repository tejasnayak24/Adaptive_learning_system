import React from 'react'
import { Link } from 'react-router-dom'
import {
  Bar,
  BarChart,
  CartesianGrid,
  Line,
  LineChart,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from 'recharts'
import {
  ATTENTION_COLOR,
  SCORE_COLOR,
  TELEMETRY_HELP,
  TELEMETRY_LABELS,
  TOPIC_STATUS_ORDER,
  activityText,
  attentionSummary,
  formatDate,
  formatPercent,
  observationText,
  relativeDay,
  subjectColor,
  topicStatusInfo
} from '../utils/analytics'

const AXIS = { stroke: '#475569', fontSize: 11, tickLine: false }
const GRID = { strokeDasharray: '3 3', stroke: '#1e293b', vertical: false }

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

// ------------------------------------------------------------------ charts

function ChartTooltip({ active, payload, kind }) {
  if (!active || !payload?.length) return null
  const row = payload[0].payload
  return (
    <div className="rounded-xl border border-slate-700 bg-slate-950/95 px-3 py-2 text-xs shadow-xl space-y-0.5 max-w-[240px]">
      {kind === 'week' ? (
        <>
          <p className="font-semibold text-white">Week of {formatDate(row.week)}</p>
          <p className="text-slate-300">
            {row.attempts} quiz attempt{row.attempts === 1 ? '' : 's'}
          </p>
        </>
      ) : (
        <>
          <p className="font-semibold text-white">
            Attempt {row.label} · {kind === 'attention' ? `${formatPercent(row.attention)} attention` : formatPercent(row.score)}
          </p>
          <p className="text-slate-300 truncate">{row.lesson}</p>
          <p className="text-slate-500">
            {row.subject} · {String(row.difficulty || '').toLowerCase()}
            {row.mode && row.mode !== 'standard' ? ` · ${row.mode}` : ''}
          </p>
          <p className="text-slate-500">{formatDate(row.at, { withTime: true })}</p>
        </>
      )}
    </div>
  )
}

export function ScoreTrendChart({ rows, passScore = 50, height = 260 }) {
  return (
    <div style={{ height }} role="img" aria-label="Line chart of quiz scores by attempt">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={rows} margin={{ top: 8, right: 12, left: -18, bottom: 0 }}>
          <CartesianGrid {...GRID} />
          <XAxis dataKey="label" {...AXIS} minTickGap={16} />
          <YAxis {...AXIS} domain={[0, 100]} ticks={[0, 25, 50, 75, 100]} unit="%" />
          <ReferenceLine
            y={passScore}
            stroke="#64748b"
            strokeDasharray="4 4"
            label={{ value: `Pass ${passScore}%`, position: 'insideTopRight', fill: '#94a3b8', fontSize: 10 }}
          />
          <Tooltip content={<ChartTooltip kind="score" />} cursor={{ stroke: '#334155' }} />
          <Line
            type="monotone"
            dataKey="score"
            name="Quiz score"
            stroke={SCORE_COLOR}
            strokeWidth={2}
            dot={{ r: 4, strokeWidth: 2, stroke: '#07090e', fill: SCORE_COLOR }}
            activeDot={{ r: 6 }}
            isAnimationActive={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

export function WeeklyActivityChart({ weeks, height = 200 }) {
  return (
    <div style={{ height }} role="img" aria-label="Bar chart of quiz attempts per week">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={weeks} margin={{ top: 8, right: 12, left: -24, bottom: 0 }}>
          <CartesianGrid {...GRID} />
          <XAxis
            dataKey="week"
            {...AXIS}
            minTickGap={12}
            tickFormatter={(w) => new Date(`${w}T00:00:00`).toLocaleDateString(undefined, { day: 'numeric', month: 'short' })}
          />
          <YAxis {...AXIS} allowDecimals={false} />
          <Tooltip content={<ChartTooltip kind="week" />} cursor={{ fill: '#1e293b55' }} />
          <Bar dataKey="attempts" name="Quiz attempts" fill={SCORE_COLOR} radius={[4, 4, 0, 0]} maxBarSize={36} isAnimationActive={false} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

// --------------------------------------------------------------- attention

export function AttentionPanel({ attention, trendRows }) {
  const summary = attentionSummary(attention)
  const measuredRows = (trendRows || []).filter((r) => r.attention !== null && r.attention !== undefined)

  return (
    <Panel
      title="Focus during quizzes (camera)"
      subtitle="The camera agent measures attention while you take a quiz. Aegis stores one average per quiz, not a continuous recording, so these figures describe your quizzes only."
    >
      <p
        className={`rounded-2xl border px-4 py-3 text-xs leading-relaxed ${
          summary.level === 'ok' ? TONES.emerald : summary.level === 'limited' ? TONES.amber : TONES.slate
        }`}
      >
        {summary.message}
      </p>

      {attention && attention.attempts_total > 0 && (
        <>
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
            <MiniStat
              label="Average attention"
              value={formatPercent(attention.average_attention)}
              note={attention.measured_attempts ? `${attention.measured_attempts} measured quizzes` : 'no measurements'}
            />
            <MiniStat label="Yawning seen in" value={observationText(attention.yawning)} />
            <MiniStat label="Looking away seen in" value={observationText(attention.looking_away)} />
            <MiniStat label="Drowsiness seen in" value={observationText(attention.drowsiness)} />
          </div>

          <div className="flex flex-wrap gap-2 text-[11px]">
            <span className="inline-flex items-center gap-1.5">
              <TelemetryBadge telemetry="measured" />
              <span className="text-slate-400 tabular-nums">{attention.measured_attempts}</span>
            </span>
            <span className="inline-flex items-center gap-1.5">
              <TelemetryBadge telemetry="unavailable" />
              <span className="text-slate-400 tabular-nums">{attention.unavailable_attempts}</span>
            </span>
            {attention.not_monitored_attempts > 0 && (
              <span className="inline-flex items-center gap-1.5">
                <TelemetryBadge telemetry="not_monitored" />
                <span className="text-slate-400 tabular-nums">{attention.not_monitored_attempts}</span>
              </span>
            )}
          </div>
          {attention.unavailable_attempts > 0 && (
            <p className="text-[11px] text-slate-500 leading-relaxed">{TELEMETRY_HELP.unavailable}</p>
          )}

          {measuredRows.length >= 2 ? (
            <div style={{ height: 200 }} role="img" aria-label="Line chart of attention per measured quiz">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={measuredRows} margin={{ top: 8, right: 12, left: -18, bottom: 0 }}>
                  <CartesianGrid {...GRID} />
                  <XAxis dataKey="label" {...AXIS} minTickGap={16} />
                  <YAxis {...AXIS} domain={[0, 100]} ticks={[0, 50, 100]} unit="%" />
                  <Tooltip content={<ChartTooltip kind="attention" />} cursor={{ stroke: '#334155' }} />
                  <Line
                    type="monotone"
                    dataKey="attention"
                    name="Attention"
                    stroke={ATTENTION_COLOR}
                    strokeWidth={2}
                    dot={{ r: 4, strokeWidth: 2, stroke: '#07090e', fill: ATTENTION_COLOR }}
                    isAnimationActive={false}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <p className="text-xs text-slate-500">
              The attention trend appears once at least two quizzes have a camera measurement. Quiz numbers match the score trend above.
            </p>
          )}

          {attention.by_subject?.length > 1 && (
            <ul className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
              {attention.by_subject.map((s) => (
                <li key={s.subject} className="flex justify-between rounded-xl bg-slate-900/40 border border-slate-800 px-3 py-2">
                  <span className="text-slate-300">{s.subject}</span>
                  <span className="text-slate-200 font-semibold tabular-nums">
                    {formatPercent(s.average_attention)}{' '}
                    <span className="text-slate-500 font-normal">({s.measured_attempts})</span>
                  </span>
                </li>
              ))}
            </ul>
          )}
        </>
      )}
    </Panel>
  )
}

function MiniStat({ label, value, note }) {
  return (
    <div className="rounded-2xl bg-slate-900/40 border border-slate-800 p-3">
      <p className="text-[10px] font-semibold uppercase tracking-wider text-slate-500">{label}</p>
      <p className="mt-1 text-sm font-bold text-white">{value}</p>
      {note && <p className="text-[10px] text-slate-500">{note}</p>}
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
