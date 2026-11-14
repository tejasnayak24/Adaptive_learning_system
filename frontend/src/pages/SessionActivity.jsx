import React, { useCallback, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../services/api'
import { formatDate } from '../utils/analytics'
import { EmptyState, ErrorState, LoadingSkeleton, Panel } from '../components/AnalyticsPanels'

/*
 * Session activity: a factual summary of what was measured during the
 * student's own quizzes -- tab-switch incidents, unverified periods and
 * multiple-face episodes. No score, probability or verdict.
 */

const STATUS_TONE = {
  submitted: 'text-emerald-300 border-emerald-500/30 bg-emerald-500/10',
  terminated: 'text-rose-300 border-rose-500/30 bg-rose-500/10',
  abandoned: 'text-slate-300 border-slate-600 bg-slate-800/60',
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

function clock(value) {
  return formatDate(value, { withTime: true })
}

function seconds(value) {
  if (value === null || value === undefined) return null
  return value < 60 ? `${value.toFixed(1)} s` : `${Math.floor(value / 60)} min ${Math.round(value % 60)} s`
}

function Tile({ label, value, hint }) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-4">
      <p className="text-[11px] font-semibold uppercase tracking-wider text-slate-500">{label}</p>
      <p className="mt-1 text-2xl font-extrabold text-white">{value}</p>
      {hint && <p className="mt-1 text-[11px] text-slate-500">{hint}</p>}
    </div>
  )
}

function AttemptCard({ attempt }) {
  const tone = STATUS_TONE[attempt.status] || 'text-indigo-300 border-indigo-500/30 bg-indigo-500/10'
  const timeline = [
    ...attempt.incidents.map((i) => ({
      at: i.at,
      title: INCIDENT_KIND[i.kind] || 'Quiz page hidden',
      detail: [
        i.away_seconds !== null && i.away_seconds !== undefined
          ? `Time away (measured by the browser): ${seconds(i.away_seconds)}`
          : 'Time away: not measured',
        i.unverified ? 'Return not confirmed in time (unverified period)' : null,
        i.result,
      ].filter(Boolean),
      tone: i.kind === 'page_reloaded' ? 'slate' : 'amber',
    })),
    ...attempt.multiple_face_episodes.map((e) => ({
      at: e.started_at,
      title: 'More than one face visible',
      detail: [
        e.ongoing ? 'Still visible at the time of this report' : `Duration: ${seconds(e.seconds) ?? 'not measured'}`,
        e.peak_face_count ? `Most faces seen at once: ${e.peak_face_count}` : null,
      ].filter(Boolean),
      tone: 'sky',
    })),
  ].sort((a, b) => String(a.at).localeCompare(String(b.at)))

  return (
    <li className="rounded-2xl border border-slate-800 bg-slate-900/30 p-4 space-y-3">
      <div className="flex flex-wrap items-start justify-between gap-2">
        <div className="min-w-0">
          <p className="text-sm font-bold text-white truncate">{attempt.quiz_title || 'Quiz'}</p>
          <p className="text-xs text-slate-400">
            {attempt.lesson_title ? `${attempt.lesson_title} · ` : ''}
            Started {clock(attempt.started_at)}
            {attempt.ended_at ? ` · ended ${clock(attempt.ended_at)}` : ''}
          </p>
        </div>
        <span className={`shrink-0 rounded-full border px-2.5 py-0.5 text-[11px] font-bold ${tone}`}>
          {STATUS_LABEL[attempt.status] || attempt.status}
        </span>
      </div>

      <p className="text-xs text-slate-300">{attempt.outcome}</p>

      <div className="flex flex-wrap gap-x-4 gap-y-1 text-[11px] text-slate-400">
        <span>Tab-switch incidents: <strong className="text-slate-200">{attempt.tab_switch_incidents}</strong></span>
        <span>Multiple-face episodes: <strong className="text-slate-200">{attempt.multiple_face_episodes.length}</strong></span>
        {attempt.unverified_periods.length > 0 && (
          <span>Unverified periods: <strong className="text-slate-200">{attempt.unverified_periods.length}</strong></span>
        )}
        {attempt.reports_delayed_by_network > 0 && (
          <span>Reports delayed by the network: <strong className="text-slate-200">{attempt.reports_delayed_by_network}</strong></span>
        )}
        {attempt.window_focus_changes > 0 && (
          <span title="Diagnostic only: never counted as a tab switch">
            Window focus changes (diagnostic): <strong className="text-slate-200">{attempt.window_focus_changes}</strong>
          </span>
        )}
      </div>

      {timeline.length > 0 ? (
        <ol className="space-y-2 border-l border-slate-800 pl-4">
          {timeline.map((item, index) => (
            <li key={index} className="relative">
              <span
                className={`absolute -left-[21px] top-1.5 h-2.5 w-2.5 rounded-full ${
                  item.tone === 'amber' ? 'bg-amber-400' : item.tone === 'sky' ? 'bg-sky-400' : 'bg-slate-500'
                }`}
                aria-hidden="true"
              />
              <p className="text-xs font-semibold text-slate-200">
                {clock(item.at)} · {item.title}
              </p>
              {item.detail.map((line, i) => (
                <p key={i} className="text-[11px] text-slate-400">{line}</p>
              ))}
            </li>
          ))}
        </ol>
      ) : (
        <p className="text-[11px] text-slate-500">No tab switches or multiple-face episodes were recorded.</p>
      )}
    </li>
  )
}

export default function SessionActivity() {
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [report, setReport] = useState(null)

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

  if (loading) return <LoadingSkeleton blocks={4} />
  if (error) return <ErrorState message={error} onRetry={load} />

  const totals = report?.totals || {}
  const attempts = report?.attempts || []

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <div className="space-y-1">
        <h1 className="text-2xl font-display font-extrabold text-white">Session activity</h1>
        <p className="text-sm text-slate-400">
          What was measured during your recent quizzes. This is a factual record, not a judgement: it contains no score
          and does not say that anything was wrong.
        </p>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <Tile label="Tab-switch incidents" value={totals.tab_switch_incidents ?? 0} hint={`${totals.reloads ?? 0} page reload${totals.reloads === 1 ? '' : 's'} (not counted)`} />
        <Tile
          label="Quizzes ended or closed"
          value={(totals.attempts_terminated ?? 0) + (totals.attempts_abandoned ?? 0)}
          hint={`${totals.attempts_terminated ?? 0} ended · ${totals.attempts_abandoned ?? 0} closed · not graded`}
        />
        <Tile
          label="Multiple-face episodes"
          value={totals.multiple_face_episodes ?? 0}
          hint={totals.multiple_face_seconds ? `${seconds(totals.multiple_face_seconds)} in total` : null}
        />
        <Tile
          label="Unverified periods"
          value={totals.unverified_periods ?? 0}
          hint={`${totals.reports_delayed_by_network ?? 0} report${totals.reports_delayed_by_network === 1 ? '' : 's'} delayed by the network`}
        />
      </div>

      <Panel title="Recent quizzes" subtitle={`${attempts.length} most recent attempts, newest first`}>
        {attempts.length === 0 ? (
          <EmptyState
            icon="🗂️"
            title="No quiz attempts yet"
            text="Your activity appears here after you start a quiz."
            action={<Link to="/subjects" className="text-xs font-semibold text-indigo-300">Go to my lessons →</Link>}
          />
        ) : (
          <ul className="space-y-3">
            {attempts.map((attempt) => (
              <AttemptCard key={attempt.attempt_id} attempt={attempt} />
            ))}
          </ul>
        )}
      </Panel>

      <Panel title="How these are measured">
        <ul className="list-disc pl-5 space-y-1 text-xs text-slate-400">
          {(report?.notes || []).map((note, i) => (
            <li key={i}>{note}</li>
          ))}
          <li>Only event times and numbers are stored. Webcam images and video are never stored or sent.</li>
        </ul>
      </Panel>
    </div>
  )
}
