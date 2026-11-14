import React, { useCallback, useEffect, useMemo, useState } from 'react'
import {
  ArrowRight,
  CircleCheck,
  CircleDot,
  CirclePause,
  ClipboardList,
  EyeOff,
  Info,
  LockKeyhole,
  OctagonX,
  RotateCw,
  ShieldCheck,
  Users,
  WifiOff
} from 'lucide-react'
import api from '../services/api'
import { formatDate } from '../utils/analytics'
import { Panel } from '../components/AnalyticsPanels'
import { TONE_SOFT } from '../components/visuals'
import { Badge, Button, Callout, Card, EmptyState, ErrorState, PageHeader, PageSkeleton, SegmentedControl, StatCard, cx } from '../components/ui'

/*
 * Session activity: a factual summary of what was measured during the
 * student's own quizzes -- tab-switch incidents, unverified periods and
 * multiple-face episodes. No score, probability or verdict.
 */

const STATUS_BADGE = {
  submitted: { tone: 'success', icon: CircleCheck },
  terminated: { tone: 'danger', icon: OctagonX },
  abandoned: { tone: 'neutral', icon: CirclePause },
  in_progress: { tone: 'info', icon: CircleDot },
  away: { tone: 'info', icon: CircleDot },
  unverified: { tone: 'warning', icon: CircleDot },
}

const STATUS_LABEL = {
  submitted: 'Graded',
  terminated: 'Ended, not graded',
  abandoned: 'Closed, not graded',
  in_progress: 'In progress',
  away: 'In progress',
  unverified: 'Waiting for confirmation',
}

const INCIDENT_KIND = {
  page_hidden: 'Quiz page hidden',
  page_closed_or_reloaded: 'Quiz page closed or reloaded',
  page_reloaded: 'Quiz page reloaded',
}

const FILTERS = [
  { value: 'all', label: 'All' },
  { value: 'graded', label: 'Graded' },
  { value: 'ended', label: 'Ended or closed' },
  { value: 'events', label: 'With events' },
]

function matchesFilter(attempt, filter) {
  if (filter === 'graded') return attempt.status === 'submitted'
  if (filter === 'ended') return attempt.status === 'terminated' || attempt.status === 'abandoned'
  if (filter === 'events') return attempt.tab_switch_incidents > 0 || attempt.multiple_face_episodes.length > 0
  return true
}

function clock(value) {
  return formatDate(value, { withTime: true })
}

function seconds(value) {
  if (value === null || value === undefined) return null
  return value < 60 ? `${value.toFixed(1)} s` : `${Math.floor(value / 60)} min ${Math.round(value % 60)} s`
}

function TimelineItem({ item, last }) {
  const Icon = item.icon
  return (
    <li className="relative flex gap-3.5">
      {!last && <span className="absolute bottom-[-12px] left-[15px] top-9 w-px bg-line" aria-hidden="true" />}
      <span className={cx('relative grid h-8 w-8 shrink-0 place-items-center rounded-lg ring-1 ring-inset', TONE_SOFT[item.tone])}>
        <Icon size={15} aria-hidden="true" />
      </span>
      <div className="min-w-0 pb-1 pt-1">
        <p className="text-[13px] font-semibold text-ink">
          {item.title} <span className="font-normal text-ink-2">· {clock(item.at)}</span>
        </p>
        {item.detail.map((line, i) => (
          <p key={i} className="mt-0.5 text-xs leading-relaxed text-ink-2">
            {line}
          </p>
        ))}
      </div>
    </li>
  )
}

function AttemptCard({ attempt }) {
  const badge = STATUS_BADGE[attempt.status] || { tone: 'brand', icon: CircleDot }
  const timeline = [
    ...attempt.incidents.map((i) => ({
      at: i.at,
      title: INCIDENT_KIND[i.kind] || 'Quiz page hidden',
      icon: i.kind === 'page_hidden' ? EyeOff : RotateCw,
      detail: [
        i.away_seconds !== null && i.away_seconds !== undefined
          ? `Time away (measured by the browser): ${seconds(i.away_seconds)}`
          : 'Time away: not measured',
        i.unverified ? 'Return not confirmed in time (unverified period)' : null,
        i.result,
      ].filter(Boolean),
      tone: i.kind === 'page_reloaded' ? 'neutral' : 'warning',
    })),
    ...attempt.multiple_face_episodes.map((e) => ({
      at: e.started_at,
      title: 'More than one face visible',
      icon: Users,
      detail: [
        e.ongoing ? 'Still visible at the time of this report' : `Duration: ${seconds(e.seconds) ?? 'not measured'}`,
        e.peak_face_count ? `Most faces seen at once: ${e.peak_face_count}` : null,
      ].filter(Boolean),
      tone: 'info',
    })),
  ].sort((a, b) => String(a.at).localeCompare(String(b.at)))

  const counters = [
    { label: 'Tab-switch incidents', value: attempt.tab_switch_incidents, icon: EyeOff },
    { label: 'Multiple-face episodes', value: attempt.multiple_face_episodes.length, icon: Users },
    attempt.unverified_periods.length > 0 && { label: 'Unverified periods', value: attempt.unverified_periods.length, icon: LockKeyhole },
    attempt.reports_delayed_by_network > 0 && { label: 'Reports delayed by the network', value: attempt.reports_delayed_by_network, icon: WifiOff },
    attempt.window_focus_changes > 0 && {
      label: 'Window focus changes (diagnostic)',
      value: attempt.window_focus_changes,
      icon: Info,
      title: 'Diagnostic only: never counted as a tab switch',
    },
  ].filter(Boolean)

  return (
    <li className="rounded-card border border-line bg-deep/60 p-4 sm:p-5">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div className="min-w-0 space-y-1">
          <p className="truncate font-display text-[15px] font-semibold text-ink">{attempt.quiz_title || 'Quiz'}</p>
          <p className="text-xs leading-relaxed text-ink-2">
            {attempt.lesson_title ? `${attempt.lesson_title} · ` : ''}
            Started {clock(attempt.started_at)}
            {attempt.ended_at ? ` · ended ${clock(attempt.ended_at)}` : ''}
          </p>
        </div>
        <Badge tone={badge.tone} icon={badge.icon} className="self-start">
          {STATUS_LABEL[attempt.status] || attempt.status}
        </Badge>
      </div>

      {attempt.outcome && <p className="mt-3 text-[13px] leading-relaxed text-ink">{attempt.outcome}</p>}

      <ul className="mt-3 flex flex-wrap gap-2">
        {counters.map(({ label, value, icon: Icon, title }) => (
          <li
            key={label}
            title={title}
            className="inline-flex items-center gap-1.5 rounded-md border border-line-strong bg-white/[0.02] px-2 py-1 text-[11px] text-ink-2"
          >
            <Icon size={12} aria-hidden="true" />
            {label}: <strong className="font-semibold text-ink">{value}</strong>
          </li>
        ))}
      </ul>

      {timeline.length > 0 ? (
        <ol className="mt-4 space-y-3 border-t border-line pt-4">
          {timeline.map((item, index) => (
            <TimelineItem key={index} item={item} last={index === timeline.length - 1} />
          ))}
        </ol>
      ) : (
        <p className="mt-4 flex items-center gap-2 border-t border-line pt-4 text-xs text-ink-2">
          <CircleCheck size={14} className="text-success" aria-hidden="true" />
          No tab switches or multiple-face episodes were recorded.
        </p>
      )}
    </li>
  )
}

export default function SessionActivity() {
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [report, setReport] = useState(null)
  const [filter, setFilter] = useState('all')

  const load = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      const response = await api.get('/integrity/report', { params: { limit: 20 } })
      setReport(response.data)
    } catch (err) {
      setError(err.message || 'Could not load your session activity')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    load()
  }, [load])

  const attempts = useMemo(() => report?.attempts || [], [report])
  const visible = useMemo(() => attempts.filter((a) => matchesFilter(a, filter)), [attempts, filter])

  if (loading) return <PageSkeleton label="Loading your session activity" />
  if (error) return <ErrorState message={error} onRetry={load} />

  const totals = report?.totals || {}
  const counts = Object.fromEntries(FILTERS.map((f) => [f.value, attempts.filter((a) => matchesFilter(a, f.value)).length]))

  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="Insights"
        title="Session Activity"
        description="What was measured during your recent quizzes. This is a factual record, not a judgement: it contains no score and does not say that anything was wrong."
        meta={
          <Badge tone="mint" icon={ShieldCheck}>
            Only your own records
          </Badge>
        }
      />

      <div className="grid grid-cols-2 gap-3 sm:gap-4 xl:grid-cols-4">
        <StatCard
          label="Tab-switch incidents"
          value={totals.tab_switch_incidents ?? 0}
          sub={`including ${totals.reloads ?? 0} confirmed page reload${totals.reloads === 1 ? '' : 's'}`}
          icon={EyeOff}
          tone="warning"
        />
        <StatCard
          label="Quizzes ended or closed"
          value={(totals.attempts_terminated ?? 0) + (totals.attempts_abandoned ?? 0)}
          sub={`${totals.attempts_terminated ?? 0} ended · ${totals.attempts_abandoned ?? 0} closed · not graded`}
          icon={OctagonX}
          tone="neutral"
        />
        <StatCard
          label="Multiple-face episodes"
          value={totals.multiple_face_episodes ?? 0}
          sub={totals.multiple_face_seconds ? `${seconds(totals.multiple_face_seconds)} in total` : 'none recorded'}
          icon={Users}
          tone="info"
        />
        <StatCard
          label="Unverified periods"
          value={totals.unverified_periods ?? 0}
          sub={`${totals.reports_delayed_by_network ?? 0} report${totals.reports_delayed_by_network === 1 ? '' : 's'} delayed by the network`}
          icon={LockKeyhole}
          tone="neutral"
        />
      </div>

      <Panel
        title="Recent quizzes"
        subtitle={`${attempts.length} most recent attempts, newest first`}
        icon={ClipboardList}
        action={
          attempts.length > 0 && (
            <SegmentedControl
              label="Filter quizzes"
              size="sm"
              value={filter}
              onChange={setFilter}
              options={FILTERS.map((f) => ({ ...f, count: counts[f.value] }))}
            />
          )
        }
      >
        {attempts.length === 0 ? (
          <EmptyState
            icon={ClipboardList}
            title="No quiz attempts yet"
            text="Your activity appears here after you start a quiz."
            action={
              <Button to="/subjects" variant="secondary" iconRight={ArrowRight}>
                Go to my lessons
              </Button>
            }
          />
        ) : visible.length === 0 ? (
          <EmptyState icon={ClipboardList} title="No quizzes match this filter" compact />
        ) : (
          <ul className="space-y-3">
            {visible.map((attempt) => (
              <AttemptCard key={attempt.attempt_id} attempt={attempt} />
            ))}
          </ul>
        )}
      </Panel>

      <Card as="section" aria-labelledby="measured-heading" className="space-y-4">
        <h2 id="measured-heading" className="flex items-center gap-2 font-display text-[17px] font-semibold tracking-tight text-ink">
          <Info size={18} className="text-brand-400" aria-hidden="true" />
          How these are measured
        </h2>
        <ul className="space-y-2">
          {(report?.notes || []).map((note, i) => (
            <li key={i} className="flex gap-3 text-[13px] leading-relaxed text-ink-2">
              <span className="mt-[8px] h-1.5 w-1.5 shrink-0 rounded-full bg-ink-3" aria-hidden="true" />
              <span>{note}</span>
            </li>
          ))}
        </ul>
        <Callout tone="mint" icon={ShieldCheck}>
          Only event times and numbers are stored. Webcam images and video are never stored or sent.
        </Callout>
      </Card>
    </div>
  )
}
