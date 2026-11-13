import React, { useCallback, useEffect, useMemo, useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { analyticsService } from '../services/analyticsService'
import {
  SUBJECT_ORDER,
  filterTrend,
  formatDate,
  formatPercent,
  trendDirection,
  trendRows,
  weeklyActivity
} from '../utils/analytics'
import {
  ActivityFeed,
  AttentionPanel,
  EmptyState,
  ErrorState,
  LoadingSkeleton,
  Milestones,
  Panel,
  ProgressBar,
  ScoreTrendChart,
  StatTile,
  SubjectPerformance,
  TelemetryBadge,
  TopicPerformance,
  WeeklyActivityChart
} from '../components/AnalyticsPanels'

const DIFFICULTY_TONE = {
  EASY: 'bg-emerald-500/10 text-emerald-300 border-emerald-500/20',
  MEDIUM: 'bg-amber-500/10 text-amber-300 border-amber-500/20',
  HARD: 'bg-rose-500/10 text-rose-300 border-rose-500/20'
}

const selectClass =
  'rounded-xl bg-slate-900 border border-slate-700 px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-indigo-500'

export default function Progress() {
  const location = useLocation()
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [filters, setFilters] = useState({ subject: 'all', from: '', to: '' })
  const [topicSubject, setTopicSubject] = useState('all')
  const [showAllAttempts, setShowAllAttempts] = useState(false)

  const load = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      setSummary(await analyticsService.getSummary())
    } catch (err) {
      setError(err.message || 'Failed to load progress analytics')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    load()
  }, [load])

  useEffect(() => {
    if (!loading && location.hash) {
      document.getElementById(location.hash.slice(1))?.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  }, [loading, location.hash])

  const filtered = useMemo(() => filterTrend(summary?.trend, filters), [summary, filters])
  const rows = useMemo(() => trendRows(filtered), [filtered])
  const allRows = useMemo(() => trendRows(summary?.trend), [summary])
  const direction = useMemo(() => trendDirection(filtered), [filtered])
  const weekly = useMemo(() => weeklyActivity(summary?.trend), [summary])

  if (loading) return <LoadingSkeleton />
  if (error) return <ErrorState message={error} onRetry={load} />

  const o = summary.overview
  const subjectsInTrend = SUBJECT_ORDER.filter((s) => summary.trend.some((p) => p.subject === s))
  const filtering = filters.subject !== 'all' || filters.from || filters.to
  const counts = summary.topic_status_counts
  const attempts = [...summary.trend].reverse()
  const visibleAttempts = showAllAttempts ? attempts : attempts.slice(0, 15)

  return (
    <div className="space-y-6 sm:space-y-8">
      <div className="space-y-1.5">
        <h1 className="font-display text-3xl font-extrabold tracking-tight text-white md:text-4xl">Progress &amp; Analytics</h1>
        <p className="text-slate-400 text-sm leading-relaxed max-w-3xl">
          Everything here comes from your own quiz attempts{summary.student.grade ? ` in Grade ${summary.student.grade}` : ''}.
          A lesson is <strong className="text-slate-200">completed</strong> when you pass one of its quizzes ({summary.definitions.pass_score}% or more).
        </p>
      </div>

      {/* A. Overall */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
        <div className="col-span-2 lg:col-span-1 glass-panel rounded-3xl p-5 border border-slate-900 shadow-md space-y-3">
          <p className="text-[11px] font-semibold uppercase tracking-wider text-slate-500">Curriculum completion</p>
          <p className="text-3xl font-extrabold text-white tabular-nums">{formatPercent(o.completion_percent, '0%')}</p>
          <ProgressBar percent={o.completion_percent} label="Curriculum completion" />
          <p className="text-xs text-slate-400">
            {o.lessons_completed} of {o.lessons_total} lessons completed
          </p>
        </div>
        <StatTile label="Lessons completed" value={o.lessons_completed} sub={`${o.lessons_attempted} started`} icon="📚" />
        <StatTile label="Quiz attempts" value={o.quiz_attempts} sub={o.days_active ? `on ${o.days_active} day${o.days_active === 1 ? '' : 's'}` : 'none yet'} icon="📝" />
        <StatTile
          label="Average accuracy"
          value={formatPercent(o.average_score)}
          sub={o.average_score === null ? 'take a quiz to see it' : `best ${formatPercent(o.best_score)} · all attempts`}
          icon="🎯"
        />
      </div>
      {o.attempts_outside_grade > 0 && (
        <p className="text-xs text-slate-500">
          {o.attempts_outside_grade} of your quiz attempts are from lessons outside Grade {summary.student.grade}. They count in your totals and
          trend, but not in this grade’s subject and topic progress.
        </p>
      )}

      {o.quiz_attempts === 0 ? (
        <Panel>
          <EmptyState
            icon="📈"
            title="No analytics yet"
            text="Your charts, subject and topic performance appear after your first quiz."
            action={
              <Link to="/subjects" className="mt-2 inline-flex px-5 py-2.5 rounded-xl bg-indigo-500 hover:bg-indigo-600 text-white font-semibold text-xs">
                Start your first lesson
              </Link>
            }
          />
        </Panel>
      ) : (
        <>
          {/* D. Trend */}
          <Panel
            title="Quiz scores over time"
            subtitle="Each point is one quiz attempt, oldest on the left. The dashed line is the pass mark."
            action={
              <div className="flex flex-wrap items-end gap-2" role="group" aria-label="Filter quiz scores">
                <label className="text-[10px] text-slate-500 space-y-1">
                  <span className="block">Subject</span>
                  <select className={selectClass} value={filters.subject} onChange={(e) => setFilters({ ...filters, subject: e.target.value })}>
                    <option value="all">All subjects</option>
                    {subjectsInTrend.map((s) => (
                      <option key={s} value={s}>
                        {s}
                      </option>
                    ))}
                  </select>
                </label>
                <label className="text-[10px] text-slate-500 space-y-1">
                  <span className="block">From</span>
                  <input type="date" className={selectClass} value={filters.from} max={filters.to || undefined} onChange={(e) => setFilters({ ...filters, from: e.target.value })} />
                </label>
                <label className="text-[10px] text-slate-500 space-y-1">
                  <span className="block">To</span>
                  <input type="date" className={selectClass} value={filters.to} min={filters.from || undefined} onChange={(e) => setFilters({ ...filters, to: e.target.value })} />
                </label>
                {filtering && (
                  <button
                    type="button"
                    className="px-3 py-2 rounded-xl text-xs font-semibold text-slate-300 hover:text-white"
                    onClick={() => setFilters({ subject: 'all', from: '', to: '' })}
                  >
                    Clear
                  </button>
                )}
              </div>
            }
          >
            {rows.length === 0 ? (
              <EmptyState icon="🔍" title="No quizzes match these filters" text="Try another subject or a wider date range." />
            ) : (
              <>
                <ScoreTrendChart rows={rows} passScore={summary.definitions.pass_score} />
                <p className="text-xs text-slate-400">
                  {rows.length} attempt{rows.length === 1 ? '' : 's'} shown.{' '}
                  {direction
                    ? direction.direction === 'up'
                      ? `Your last 3 scores average ${direction.last}%, up from ${direction.first}% in your first 3 — nice progress!`
                      : direction.direction === 'down'
                        ? `Your last 3 scores average ${direction.last}%, down from ${direction.first}% in your first 3. The topics below show where to revise.`
                        : `Your scores are steady at about ${direction.last}%.`
                    : 'Take at least six quizzes to see whether your scores are rising.'}
                </p>
              </>
            )}
          </Panel>

          {/* B. Subjects */}
          <Panel title="Subject performance" subtitle="Progress counts lessons you have passed. Average score uses every quiz attempt in that subject.">
            <SubjectPerformance subjects={summary.subjects} />
          </Panel>

          {/* C. Topics */}
          <Panel
            title="Topic performance"
            subtitle={`Judged from your last ${summary.definitions.recent_attempts_for_topic_status} quizzes in each topic. A topic needs at least ${summary.definitions.min_attempts_to_evaluate_topic} quizzes before it is rated — untried topics are never marked weak.`}
            action={
              <select className={selectClass} value={topicSubject} onChange={(e) => setTopicSubject(e.target.value)} aria-label="Filter topics by subject">
                <option value="all">All subjects</option>
                {summary.subjects.map((s) => (
                  <option key={s.subject} value={s.subject}>
                    {s.subject}
                  </option>
                ))}
              </select>
            }
          >
            <p className="text-xs text-slate-400">
              {counts.strong} strong · {counts.needs_revision} need revision · {counts.weak} weak · {counts.insufficient_data} need more attempts ·{' '}
              {counts.not_started} not started
            </p>
            <TopicPerformance topics={summary.topics} subject={topicSubject} />
          </Panel>

          {/* E. Attention */}
          <AttentionPanel attention={summary.attention} trendRows={allRows} />

          {/* A. Activity over time + activity history */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6" id="activity">
            <Panel title="Learning activity over time" subtitle="Quiz attempts per week (weeks start on Monday).">
              {weekly.weeks.length ? (
                <WeeklyActivityChart weeks={weekly.weeks} />
              ) : (
                <EmptyState icon="🗓️" title="No dated attempts" />
              )}
              {weekly.undated > 0 && (
                <p className="text-[11px] text-slate-500">{weekly.undated} older attempts have no recorded date and are not shown.</p>
              )}
              <p className="text-xs text-slate-400">
                Active on {o.days_active} day{o.days_active === 1 ? '' : 's'} · current streak {o.current_streak_days} · longest {o.longest_streak_days} (days
                with at least one quiz, UTC).
              </p>
            </Panel>
            <Panel title="Recent activity" subtitle="Quizzes, completed lessons and finished subjects.">
              <ActivityFeed events={summary.activity} limit={12} />
            </Panel>
          </div>

          <Panel title="Milestones" subtitle="Earned from your saved results.">
            <Milestones milestones={summary.milestones} />
          </Panel>

          {/* Attempt log */}
          <section className="glass-panel rounded-3xl border border-slate-900 shadow-lg overflow-hidden">
            <div className="p-5 sm:p-6 border-b border-slate-900">
              <h2 className="text-base font-bold text-white">All quiz attempts</h2>
              <p className="text-xs text-slate-500 mt-0.5">Newest first. Hover a camera label to see what it means.</p>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs border-collapse min-w-[720px]">
                <thead>
                  <tr className="bg-slate-900/50 text-slate-400 font-semibold tracking-wider uppercase border-b border-slate-900">
                    <th className="py-3 px-4">Date</th>
                    <th className="py-3 px-4">Lesson</th>
                    <th className="py-3 px-4">Level</th>
                    <th className="py-3 px-4 text-right">Score</th>
                    <th className="py-3 px-4">Camera</th>
                    <th className="py-3 px-4 text-right">Attention</th>
                    <th className="py-3 px-4 text-right">Time</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-900/80">
                  {visibleAttempts.map((p) => (
                    <tr key={p.progress_id} className="hover:bg-slate-900/20">
                      <td className="py-3 px-4 text-slate-400 whitespace-nowrap">{formatDate(p.at)}</td>
                      <td className="py-3 px-4">
                        <Link to={`/lesson/${p.lesson_id}`} className="font-semibold text-slate-200 hover:text-indigo-300">
                          {p.lesson_title}
                        </Link>
                        <span className="block text-[10px] text-slate-500">
                          {p.subject} · {p.topic}
                          {p.mode !== 'standard' ? ` · ${p.mode}` : ''}
                        </span>
                      </td>
                      <td className="py-3 px-4">
                        <span className={`px-2 py-0.5 rounded border text-[10px] font-bold ${DIFFICULTY_TONE[String(p.difficulty).toUpperCase()] || ''}`}>
                          {p.difficulty}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-right font-semibold text-white tabular-nums">
                        {formatPercent(p.score)} <span className={p.passed ? 'text-emerald-400' : 'text-amber-400'}>{p.passed ? '✓' : '✗'}</span>
                      </td>
                      <td className="py-3 px-4">
                        <TelemetryBadge telemetry={p.telemetry} />
                      </td>
                      <td className="py-3 px-4 text-right tabular-nums text-slate-200">{formatPercent(p.attention)}</td>
                      <td className="py-3 px-4 text-right tabular-nums text-slate-400">{Math.round(p.response_time)}s</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {attempts.length > 15 && (
              <div className="p-4 border-t border-slate-900 text-center">
                <button type="button" className="text-xs font-semibold text-indigo-300 hover:text-indigo-200" onClick={() => setShowAllAttempts((v) => !v)}>
                  {showAllAttempts ? 'Show fewer' : `Show all ${attempts.length} attempts`}
                </button>
              </div>
            )}
          </section>
        </>
      )}
    </div>
  )
}
