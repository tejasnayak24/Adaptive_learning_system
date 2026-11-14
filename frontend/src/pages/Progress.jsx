import React, { useCallback, useEffect, useMemo, useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import {
  ArrowRight,
  BookCheck,
  CalendarClock,
  ChartLine,
  CircleCheck,
  CircleDot,
  ClipboardList,
  Eye,
  Flame,
  Funnel,
  GraduationCap,
  Medal,
  Target,
  X
} from 'lucide-react'
import { analyticsService } from '../services/analyticsService'
import {
  ATTENTION_COLOR,
  SCORE_COLOR,
  SUBJECT_ORDER,
  TELEMETRY_HELP,
  TELEMETRY_LABELS,
  attentionSummary,
  filterTrend,
  formatDate,
  formatPercent,
  observationText,
  topicStatusInfo,
  trendDirection,
  trendRows,
  weeklyActivity
} from '../utils/analytics'
import {
  AttentionTrendChart,
  ChartCard,
  ScoreTrendChart,
  SubjectScoreChart,
  TOPIC_STATUS_KEYS,
  TopicStatusChart,
  TopicStatusLegend,
  WeeklyActivityChart,
  topicStatusRows
} from '../components/AnalyticsCharts'
import { ActivityFeed, Milestones, Panel, SubjectPerformance, TopicPerformance } from '../components/AnalyticsPanels'
import { DifficultyBadge, SubjectChip, TelemetryBadge } from '../components/learning'
import { TELEMETRY_VISUALS } from '../components/visuals'
import {
  Badge,
  Button,
  Card,
  DataTable,
  EmptyState,
  ErrorState,
  INPUT_CLASS,
  PageHeader,
  PageSkeleton,
  ProgressBar,
  SegmentedControl,
  SelectField,
  StatCard,
  cx
} from '../components/ui'
import { scrollBehavior } from '../hooks/useReducedMotion'

const PRESETS = [
  { value: 'all', label: 'All time' },
  { value: '7', label: '7 days' },
  { value: '30', label: '30 days' },
  { value: '90', label: '90 days' }
]

function isoDate(date) {
  const pad = (n) => String(n).padStart(2, '0')
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`
}

/** From-date for "the last N days" (including today), local time. */
function presetFrom(days) {
  const date = new Date()
  date.setDate(date.getDate() - (Number(days) - 1))
  return isoDate(date)
}

const STATUS_TEXT = {
  ok: 'text-success',
  limited: 'text-warning',
  none: 'text-ink-2'
}

export default function Progress() {
  const location = useLocation()
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [filters, setFilters] = useState({ subject: 'all', from: '', to: '' })
  const [preset, setPreset] = useState('all')
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
      document.getElementById(location.hash.slice(1))?.scrollIntoView({ behavior: scrollBehavior(), block: 'start' })
    }
  }, [loading, location.hash])

  // The filter row scopes every chart and table in "Quiz history".
  const filtered = useMemo(() => filterTrend(summary?.trend, filters), [summary, filters])
  const rows = useMemo(() => trendRows(filtered), [filtered])
  const direction = useMemo(() => trendDirection(filtered), [filtered])
  const weekly = useMemo(() => weeklyActivity(filtered), [filtered])
  const attentionRows = useMemo(() => rows.filter((r) => r.attention !== null && r.attention !== undefined), [rows])
  // Per-subject first-3 vs last-3 comparison (all attempts in that subject).
  const subjectTrends = useMemo(
    () => Object.fromEntries(SUBJECT_ORDER.map((s) => [s, trendDirection((summary?.trend || []).filter((p) => p.subject === s))])),
    [summary]
  )

  if (loading) return <PageSkeleton label="Loading your progress" />
  if (error) return <ErrorState message={error} onRetry={load} />

  const o = summary.overview
  const subjectsInTrend = SUBJECT_ORDER.filter((s) => summary.trend.some((p) => p.subject === s))
  const filtering = filters.subject !== 'all' || filters.from || filters.to
  const counts = summary.topic_status_counts
  const attempts = [...filtered].reverse()
  const visibleAttempts = showAllAttempts ? attempts : attempts.slice(0, 15)
  const attention = summary.attention
  const attentionInfo = attentionSummary(attention)

  const choosePreset = (value) => {
    setPreset(value)
    setFilters((current) => ({ ...current, from: value === 'all' ? '' : presetFrom(value), to: '' }))
  }
  const setDate = (key, value) => {
    setPreset('custom')
    setFilters((current) => ({ ...current, [key]: value }))
  }
  const clearFilters = () => {
    setPreset('all')
    setFilters({ subject: 'all', from: '', to: '' })
  }

  const trendSentence = direction
    ? direction.direction === 'up'
      ? `Your last 3 scores average ${direction.last}%, up from ${direction.first}% in your first 3 — nice progress!`
      : direction.direction === 'down'
        ? `Your last 3 scores average ${direction.last}%, down from ${direction.first}% in your first 3. The topics below show where to revise.`
        : `Your scores are steady at about ${direction.last}%.`
    : 'Take at least six quizzes to see whether your scores are rising.'

  const attemptColumns = [
    {
      key: 'lesson',
      header: 'Lesson',
      primary: true,
      render: (p) => (
        <div className="min-w-0">
          <Link to={`/lesson/${p.lesson_id}`} className="font-medium text-ink transition-colors hover:text-brand-300">
            {p.lesson_title}
          </Link>
          <span className="mt-0.5 flex flex-wrap items-center gap-x-1.5 text-xs text-ink-2">
            <SubjectChip subject={p.subject} /> · {p.topic}
            {p.mode !== 'standard' ? ` · ${p.mode}` : ''}
          </span>
        </div>
      )
    },
    { key: 'date', header: 'Date', render: (p) => <span className="whitespace-nowrap text-ink-2">{formatDate(p.at)}</span> },
    { key: 'level', header: 'Level', render: (p) => <DifficultyBadge difficulty={p.difficulty} size="sm" /> },
    {
      key: 'score',
      header: 'Score',
      align: 'right',
      render: (p) => (
        <span className="inline-flex items-center justify-end gap-1.5 font-semibold text-ink">
          {formatPercent(p.score)}
          {p.passed ? (
            <CircleCheck size={14} className="text-success" aria-label="passed" />
          ) : (
            <CircleDot size={14} className="text-warning" aria-label="not passed" />
          )}
        </span>
      )
    },
    { key: 'camera', header: 'Camera', render: (p) => <TelemetryBadge telemetry={p.telemetry} /> },
    { key: 'attention', header: 'Attention', align: 'right', render: (p) => formatPercent(p.attention) },
    { key: 'time', header: 'Time', align: 'right', render: (p) => <span className="text-ink-2">{Math.round(p.response_time)}s</span> }
  ]

  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="Insights"
        title="Progress & Analytics"
        description={
          <>
            Everything here comes from your own quiz attempts{summary.student.grade ? ` in Grade ${summary.student.grade}` : ''}. A lesson is{' '}
            <strong className="font-semibold text-ink">completed</strong> when you pass one of its quizzes ({summary.definitions.pass_score}% or more).
          </>
        }
        meta={
          summary.student.grade && (
            <Badge tone="brand" icon={GraduationCap}>
              Grade {summary.student.grade}
            </Badge>
          )
        }
      />

      {/* Overview */}
      <div className="grid grid-cols-2 gap-3 sm:gap-4 xl:grid-cols-4">
        <StatCard label="Curriculum completion" value={formatPercent(o.completion_percent, '0%')} icon={Target} tone="brand">
          <ProgressBar value={o.completion_percent} tone="gradient" size="sm" className="mt-3" label="Curriculum completion" />
          <p className="mt-2 text-xs text-ink-2">
            {o.lessons_completed} of {o.lessons_total} lessons completed
          </p>
        </StatCard>
        <StatCard label="Lessons completed" value={o.lessons_completed} sub={`${o.lessons_attempted} started`} icon={BookCheck} tone="mint" />
        <StatCard
          label="Quiz attempts"
          value={o.quiz_attempts}
          sub={o.days_active ? `on ${o.days_active} day${o.days_active === 1 ? '' : 's'}` : 'none yet'}
          icon={ClipboardList}
          tone="info"
        />
        <StatCard
          label="Average accuracy"
          value={formatPercent(o.average_score)}
          sub={o.average_score === null ? 'take a quiz to see it' : `best ${formatPercent(o.best_score)} · all attempts`}
          icon={Flame}
          tone="warning"
        />
      </div>
      {o.attempts_outside_grade > 0 && (
        <p className="-mt-4 text-xs text-ink-2">
          {o.attempts_outside_grade} of your quiz attempts are from lessons outside Grade {summary.student.grade}. They count in your totals and trend,
          but not in this grade’s subject and topic progress.
        </p>
      )}

      {o.quiz_attempts === 0 ? (
        <Card>
          <EmptyState
            icon={ChartLine}
            title="No analytics yet"
            text="Your charts, subject and topic performance appear after your first quiz."
            action={
              <Button to="/subjects" iconRight={ArrowRight}>
                Start your first lesson
              </Button>
            }
          />
        </Card>
      ) : (
        <>
          {/* Quiz history: one filter row scopes everything in this section */}
          <section aria-labelledby="history-heading" className="space-y-4">
            <div className="flex flex-col gap-3 lg:flex-row lg:items-end lg:justify-between">
              <div>
                <h2 id="history-heading" className="font-display text-xl font-semibold tracking-tight text-ink">
                  Quiz history
                </h2>
                <p className="mt-1 text-[13px] text-ink-2">The filters apply to every chart and table in this section.</p>
              </div>
            </div>
            <Card padding="sm" className="flex flex-col gap-3 xl:flex-row xl:items-end" role="group" aria-label="Filter quiz history">
              <span className="hidden h-9 items-center gap-1.5 text-xs font-medium text-ink-2 xl:inline-flex">
                <Funnel size={14} aria-hidden="true" />
                Filters
              </span>
              <SelectField
                label="Subject"
                size="sm"
                className="xl:w-48"
                value={filters.subject}
                onChange={(e) => setFilters({ ...filters, subject: e.target.value })}
              >
                <option value="all">All subjects</option>
                {subjectsInTrend.map((s) => (
                  <option key={s} value={s}>
                    {s}
                  </option>
                ))}
              </SelectField>
              <div className="space-y-1.5">
                <p className="text-[13px] font-medium text-ink-2">Period</p>
                <SegmentedControl label="Period" size="sm" value={preset} onChange={choosePreset} options={PRESETS} />
              </div>
              <div className="grid grid-cols-2 gap-3 sm:flex sm:items-end">
                <label className="space-y-1.5">
                  <span className="block text-[13px] font-medium text-ink-2">From</span>
                  <input
                    type="date"
                    className={cx(INPUT_CLASS, 'h-9 px-3 text-[13px]')}
                    value={filters.from}
                    max={filters.to || undefined}
                    onChange={(e) => setDate('from', e.target.value)}
                  />
                </label>
                <label className="space-y-1.5">
                  <span className="block text-[13px] font-medium text-ink-2">To</span>
                  <input
                    type="date"
                    className={cx(INPUT_CLASS, 'h-9 px-3 text-[13px]')}
                    value={filters.to}
                    min={filters.from || undefined}
                    onChange={(e) => setDate('to', e.target.value)}
                  />
                </label>
              </div>
              {filtering && (
                <Button variant="ghost" size="sm" icon={X} onClick={clearFilters} className="self-start xl:self-end">
                  Clear
                </Button>
              )}
              <p className="text-xs text-ink-2 xl:ml-auto xl:pb-2">
                {rows.length} of {summary.trend.length} attempt{summary.trend.length === 1 ? '' : 's'}
              </p>
            </Card>

            {rows.length === 0 ? (
              <Card>
                <EmptyState
                  icon={Funnel}
                  title="No quizzes match these filters"
                  text="Try another subject or a wider date range."
                  action={
                    <Button variant="secondary" size="sm" onClick={clearFilters}>
                      Clear filters
                    </Button>
                  }
                />
              </Card>
            ) : (
              <>
                <ChartCard
                  title="Quiz scores over time"
                  description="Each point is one quiz attempt, oldest on the left. The dashed line is the pass mark."
                  table={{
                    rowKey: (r) => r.n,
                    rows,
                    columns: [
                      { key: 'label', header: 'Attempt', primary: true },
                      { key: 'at', header: 'Date', render: (r) => formatDate(r.at) },
                      { key: 'lesson', header: 'Lesson' },
                      { key: 'subject', header: 'Subject' },
                      { key: 'score', header: 'Score', align: 'right', render: (r) => formatPercent(r.score) }
                    ]
                  }}
                >
                  <ScoreTrendChart rows={rows} passScore={summary.definitions.pass_score} />
                  <p className="flex items-start gap-2 text-[13px] leading-relaxed text-ink-2">
                    <span className="mt-[7px] h-[2px] w-3 shrink-0 rounded-full" style={{ background: SCORE_COLOR }} aria-hidden="true" />
                    <span>
                      {rows.length} attempt{rows.length === 1 ? '' : 's'} shown. {trendSentence}
                    </span>
                  </p>
                </ChartCard>

                <div className="grid grid-cols-1 gap-6 xl:grid-cols-2">
                  <ChartCard
                    title="Learning activity by week"
                    description="Quiz attempts per week (weeks start on Monday)."
                    table={{
                      rowKey: (w) => w.week,
                      rows: weekly.weeks,
                      columns: [
                        {
                          key: 'week',
                          header: 'Week of',
                          primary: true,
                          render: (w) => new Date(`${w.week}T00:00:00`).toLocaleDateString(undefined, { day: 'numeric', month: 'short', year: 'numeric' })
                        },
                        { key: 'attempts', header: 'Quiz attempts', align: 'right' }
                      ]
                    }}
                  >
                    {weekly.weeks.length ? <WeeklyActivityChart weeks={weekly.weeks} /> : <EmptyState icon={CalendarClock} title="No dated attempts" compact />}
                    {weekly.undated > 0 && <p className="text-[11px] text-ink-2">{weekly.undated} older attempts have no recorded date and are not shown.</p>}
                    <p className="text-xs text-ink-2">
                      Active on {o.days_active} day{o.days_active === 1 ? '' : 's'} · current streak {o.current_streak_days} · longest {o.longest_streak_days}{' '}
                      (days with at least one quiz, UTC).
                    </p>
                  </ChartCard>

                  <ChartCard
                    title="Focus during quizzes"
                    description="The camera agent measures attention while you take a quiz. Aegis stores one average per quiz, not a recording."
                    table={
                      attentionRows.length
                        ? {
                            rowKey: (r) => r.n,
                            rows: attentionRows,
                            columns: [
                              { key: 'label', header: 'Attempt', primary: true },
                              { key: 'lesson', header: 'Lesson' },
                              { key: 'attention', header: 'Attention', align: 'right', render: (r) => formatPercent(r.attention) }
                            ]
                          }
                        : undefined
                    }
                  >
                    <p className={cx('flex items-start gap-2 text-[13px] leading-relaxed', STATUS_TEXT[attentionInfo.level])}>
                      <Eye size={15} className="mt-0.5 shrink-0" aria-hidden="true" />
                      {attentionInfo.message}
                    </p>
                    {attentionRows.length >= 2 ? (
                      <AttentionTrendChart rows={attentionRows} />
                    ) : (
                      <p className="rounded-xl border border-dashed border-line-strong px-4 py-6 text-center text-xs text-ink-2">
                        The attention trend appears once at least two quizzes in this selection have a camera measurement.
                      </p>
                    )}
                    {attention && attention.attempts_total > 0 && (
                      <dl className="grid grid-cols-2 gap-2.5">
                        <div className="rounded-lg bg-deep/70 p-3 ring-1 ring-inset ring-line">
                          <dt className="text-[11px] text-ink-2">Average attention</dt>
                          <dd className="mt-1 flex items-center gap-1.5 text-sm font-semibold text-ink">
                            <span className="h-[2px] w-3 rounded-full" style={{ background: ATTENTION_COLOR }} aria-hidden="true" />
                            {formatPercent(attention.average_attention)}
                          </dd>
                        </div>
                        <div className="rounded-lg bg-deep/70 p-3 ring-1 ring-inset ring-line">
                          <dt className="text-[11px] text-ink-2">Yawning seen in</dt>
                          <dd className="mt-1 text-sm font-semibold text-ink">{observationText(attention.yawning)}</dd>
                        </div>
                        <div className="rounded-lg bg-deep/70 p-3 ring-1 ring-inset ring-line">
                          <dt className="text-[11px] text-ink-2">Looking away seen in</dt>
                          <dd className="mt-1 text-sm font-semibold text-ink">{observationText(attention.looking_away)}</dd>
                        </div>
                        <div className="rounded-lg bg-deep/70 p-3 ring-1 ring-inset ring-line">
                          <dt className="text-[11px] text-ink-2">Drowsiness seen in</dt>
                          <dd className="mt-1 text-sm font-semibold text-ink">{observationText(attention.drowsiness)}</dd>
                        </div>
                      </dl>
                    )}
                    {attention?.by_subject?.length > 1 && (
                      <ul className="grid grid-cols-1 gap-2 text-xs sm:grid-cols-2">
                        {attention.by_subject.map((s) => (
                          <li key={s.subject} className="flex items-center justify-between gap-2 rounded-lg border border-line px-3 py-2">
                            <SubjectChip subject={s.subject} className="text-ink-2" />
                            <span className="font-semibold text-ink">
                              {formatPercent(s.average_attention)} <span className="font-normal text-ink-2">({s.measured_attempts})</span>
                            </span>
                          </li>
                        ))}
                      </ul>
                    )}
                    <p className="text-[11px] leading-relaxed text-ink-2">Averages cover all your measured quizzes, not only this selection.</p>
                  </ChartCard>
                </div>

                <Card as="section" padding="none" aria-labelledby="attempts-heading" className="overflow-hidden">
                  <div className="flex flex-col gap-3 border-b border-line px-5 py-4 sm:flex-row sm:items-center sm:justify-between sm:px-6">
                    <div>
                      <h3 id="attempts-heading" className="font-display text-[17px] font-semibold tracking-tight text-ink">
                        All quiz attempts
                      </h3>
                      <p className="mt-0.5 text-[13px] text-ink-2">Newest first.</p>
                    </div>
                    <ul className="flex flex-wrap gap-x-4 gap-y-1 text-[11px] text-ink-2" aria-label="Camera labels">
                      {Object.keys(TELEMETRY_LABELS).map((key) => {
                        const Icon = TELEMETRY_VISUALS[key].icon
                        return (
                          <li key={key} className="flex max-w-[16rem] items-start gap-1.5" title={TELEMETRY_HELP[key]}>
                            <Icon size={13} className="mt-px shrink-0" aria-hidden="true" />
                            <span>
                              <span className="font-medium text-ink">{TELEMETRY_LABELS[key]}</span>
                            </span>
                          </li>
                        )
                      })}
                    </ul>
                  </div>
                  <div className="p-3 sm:p-2">
                    <DataTable caption="All quiz attempts" columns={attemptColumns} rows={visibleAttempts} rowKey={(p) => p.progress_id} minWidth={760} />
                  </div>
                  {attempts.length > 15 && (
                    <div className="border-t border-line p-3 text-center">
                      <Button variant="ghost" size="sm" onClick={() => setShowAllAttempts((v) => !v)}>
                        {showAllAttempts ? 'Show fewer' : `Show all ${attempts.length} attempts`}
                      </Button>
                    </div>
                  )}
                </Card>
              </>
            )}
          </section>

          {/* Where you stand */}
          <section aria-labelledby="standing-heading" className="space-y-4">
            <div>
              <h2 id="standing-heading" className="font-display text-xl font-semibold tracking-tight text-ink">
                Where you stand
              </h2>
              <p className="mt-1 text-[13px] text-ink-2">Your current standing in each subject and topic, from all your attempts.</p>
            </div>

            <ChartCard
              title="Subject performance"
              description="Average quiz score per subject (bars) against the pass mark. Progress counts lessons you have passed."
              table={{
                rowKey: (s) => s.subject,
                rows: summary.subjects,
                columns: [
                  { key: 'subject', header: 'Subject', primary: true },
                  { key: 'average_score', header: 'Average score', align: 'right', render: (s) => formatPercent(s.average_score, 'No quizzes') },
                  { key: 'quiz_attempts', header: 'Quizzes', align: 'right' },
                  { key: 'lessons', header: 'Lessons passed', align: 'right', render: (s) => `${s.lessons_completed}/${s.lessons_total}` },
                  { key: 'progress', header: 'Progress', align: 'right', render: (s) => formatPercent(s.progress_percent, '0%') }
                ]
              }}
            >
              <SubjectScoreChart subjects={summary.subjects} passScore={summary.definitions.pass_score} />
              <SubjectPerformance subjects={summary.subjects} trends={subjectTrends} />
              <p className="text-[11px] leading-relaxed text-ink-2">
                Improving, stable and needs revision compare your first three and last three quizzes in a subject (six quizzes needed).
              </p>
            </ChartCard>

            <ChartCard
              title="Topic performance"
              description={`Judged from your last ${summary.definitions.recent_attempts_for_topic_status} quizzes in each topic. A topic needs at least ${summary.definitions.min_attempts_to_evaluate_topic} quizzes before it is rated — untried topics are never marked weak.`}
              legend={<TopicStatusLegend />}
              table={{
                rowKey: (r) => r.subject,
                rows: topicStatusRows(summary.topics),
                columns: [
                  { key: 'subject', header: 'Subject', primary: true },
                  ...TOPIC_STATUS_KEYS.map((key) => ({ key, header: topicStatusInfo(key).label, align: 'right' }))
                ]
              }}
            >
              <TopicStatusChart topics={summary.topics} />
              <div className="flex flex-col gap-3 border-t border-line pt-5 md:flex-row md:items-center md:justify-between">
                <p className="text-xs text-ink-2">
                  {counts.strong} strong · {counts.needs_revision} need revision · {counts.weak} weak · {counts.insufficient_data} need more attempts ·{' '}
                  {counts.not_started} not started
                </p>
                <SegmentedControl
                  label="Show topics for"
                  size="sm"
                  value={topicSubject}
                  onChange={setTopicSubject}
                  options={[{ value: 'all', label: 'All' }, ...summary.subjects.map((s) => ({ value: s.subject, label: s.subject }))]}
                />
              </div>
              <TopicPerformance topics={summary.topics} subject={topicSubject} />
            </ChartCard>
          </section>

          <div className="grid grid-cols-1 gap-6 xl:grid-cols-2">
            <Panel title="Milestones" subtitle="Earned from your saved results." icon={Medal}>
              <Milestones milestones={summary.milestones} />
            </Panel>
            <Panel id="activity" title="Recent activity" subtitle="Quizzes, completed lessons and finished subjects." icon={CalendarClock}>
              <ActivityFeed events={summary.activity} limit={12} />
            </Panel>
          </div>
        </>
      )}
    </div>
  )
}
