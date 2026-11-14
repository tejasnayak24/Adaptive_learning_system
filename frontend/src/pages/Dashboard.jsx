import React, { useCallback, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { analyticsService } from '../services/analyticsService'
import { rlService } from '../services/rlService'
import { CONFIDENCE_NOTE, POLICY_LABELS, actionInfo } from '../utils/recommendationActions'
import { continueTarget, formatPercent, relativeDay } from '../utils/analytics'
import {
  ActivityFeed,
  ErrorState,
  LoadingSkeleton,
  Panel,
  ProgressBar,
  StatTile,
  SubjectPerformance,
  TelemetryBadge
} from '../components/AnalyticsPanels'

function greeting() {
  const hour = new Date().getHours()
  if (hour < 12) return 'Good morning'
  if (hour < 17) return 'Good afternoon'
  return 'Good evening'
}

export default function Dashboard() {
  const { user } = useAuth()
  const [summary, setSummary] = useState(null)
  const [coach, setCoach] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const load = useCallback(async () => {
    setError('')
    try {
      const [data, latest] = await Promise.all([
        analyticsService.getSummary(),
        // The coach card is optional: a failure there must not hide the dashboard.
        rlService.getLatest().catch(() => null)
      ])
      setSummary(data)
      setCoach(latest)
    } catch (err) {
      setError(err.message || 'Failed to load the dashboard')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    load()
  }, [load, user?.grade])

  useEffect(() => {
    const onFocus = () => load()
    window.addEventListener('focus', onFocus)
    return () => window.removeEventListener('focus', onFocus)
  }, [load])

  if (loading) return <LoadingSkeleton blocks={5} />
  if (error && !summary) return <ErrorState message={error} onRetry={load} />

  const o = summary.overview
  const latest = o.latest_activity
  const next = continueTarget(summary)
  const recommendation = coach?.status === 'available' ? coach.recommendation : null
  const coachAttempt = coach?.attempt

  return (
    <div className="space-y-6 sm:space-y-8">
      {/* Greeting */}
      <div className="relative overflow-hidden rounded-3xl border border-slate-800 bg-gradient-to-r from-indigo-950/40 via-slate-900/40 to-slate-950 p-6 sm:p-8 shadow-2xl">
        <div className="absolute top-0 right-0 h-40 w-40 bg-indigo-500/10 blur-3xl pointer-events-none" />
        <div className="relative z-10 space-y-2">
          <div className="flex flex-wrap items-center gap-2">
            {summary.student.grade && (
              <span className="px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 rounded-lg">
                Grade {summary.student.grade}
              </span>
            )}
            {o.current_streak_days > 1 && (
              <span
                className="px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider bg-amber-500/10 text-amber-300 border border-amber-500/20 rounded-lg"
                title="Consecutive days (UTC) with at least one quiz submitted"
              >
                🔥 {o.current_streak_days}-day streak
              </span>
            )}
          </div>
          <h1 className="font-display text-3xl md:text-4xl font-extrabold tracking-tight text-white">
            {greeting()},{' '}
            <span className="bg-gradient-to-r from-indigo-400 to-teal-300 bg-clip-text text-transparent">
              {summary.student.name}
            </span>
            !
          </h1>
          <p className="text-slate-400 max-w-2xl text-sm leading-relaxed">
            {o.quiz_attempts === 0
              ? 'Welcome to Aegis! Open a lesson, read it, then take its quiz. Your progress and your AI coach start working after your first quiz.'
              : `You have completed ${o.lessons_completed} of ${o.lessons_total} lessons in your grade. A lesson counts as completed when you pass one of its quizzes (${summary.definitions.pass_score}% or more).`}
          </p>
        </div>
      </div>

      {error && (
        <div className="rounded-2xl border border-amber-500/20 bg-amber-500/10 px-4 py-3 text-xs text-amber-200">
          Showing your last loaded data — refresh failed: {error}
        </div>
      )}

      {/* Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-5 gap-3 sm:gap-4">
        <div className="col-span-2 lg:col-span-1 glass-panel rounded-3xl p-5 border border-slate-900 shadow-md space-y-3">
          <p className="text-[11px] font-semibold uppercase tracking-wider text-slate-500">Curriculum completion</p>
          <p className="text-3xl font-extrabold text-white tabular-nums">{formatPercent(o.completion_percent, '0%')}</p>
          <ProgressBar percent={o.completion_percent} label="Curriculum completion" />
        </div>
        <StatTile label="Lessons completed" value={`${o.lessons_completed}/${o.lessons_total}`} sub={`${o.lessons_attempted} started`} icon="📚" />
        <StatTile label="Quiz attempts" value={o.quiz_attempts} sub={o.days_active ? `on ${o.days_active} day${o.days_active === 1 ? '' : 's'}` : 'none yet'} icon="📝" />
        <StatTile
          label="Average score"
          value={formatPercent(o.average_score)}
          sub={o.average_score === null ? 'take a quiz to see it' : `best ${formatPercent(o.best_score)}`}
          icon="🎯"
        />
        <StatTile label="Subjects" value={o.subjects_available} sub={summary.student.grade ? `in Grade ${summary.student.grade}` : 'choose a grade'} icon="🧭" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          {/* Continue + latest activity */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="glass-panel rounded-3xl p-5 border border-slate-900 shadow-lg flex flex-col justify-between gap-4">
              <div className="space-y-1.5">
                <span className="inline-flex px-2.5 py-1 text-[10px] font-semibold uppercase tracking-wider bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 rounded-lg">
                  Continue learning
                </span>
                {next ? (
                  <>
                    <h3 className="text-lg font-bold text-white">{next.lesson_title}</h3>
                    <p className="text-xs text-slate-400">
                      {next.subject} · {next.topic}
                    </p>
                  </>
                ) : (
                  <p className="text-sm text-slate-300">
                    {o.lessons_total > 0 ? '🏆 Every lesson in your grade is completed!' : 'Choose your grade to start.'}
                  </p>
                )}
              </div>
              <Link
                to={next ? `/lesson/${next.lesson_id}` : '/subjects'}
                className="inline-flex items-center justify-center px-4 py-2.5 rounded-xl bg-indigo-500 text-white font-semibold text-sm hover:bg-indigo-600 transition-colors"
              >
                {next ? 'Open lesson →' : 'Browse subjects →'}
              </Link>
            </div>

            <div className="glass-panel rounded-3xl p-5 border border-slate-900 shadow-lg space-y-2">
              <span className="inline-flex px-2.5 py-1 text-[10px] font-semibold uppercase tracking-wider bg-slate-800 text-slate-300 border border-slate-700 rounded-lg">
                Latest activity
              </span>
              {latest ? (
                <>
                  <h3 className="text-base font-bold text-white">{latest.lesson_title}</h3>
                  <p className="text-xs text-slate-400">
                    {latest.subject} · {String(latest.difficulty).toLowerCase()} quiz · {relativeDay(latest.at)}
                  </p>
                  <p className="text-2xl font-extrabold text-white tabular-nums">
                    {formatPercent(latest.score)}{' '}
                    <span className={`text-xs font-semibold ${latest.passed ? 'text-emerald-300' : 'text-amber-300'}`}>
                      {latest.passed ? '✓ passed' : '✗ not passed yet'}
                    </span>
                  </p>
                  <TelemetryBadge telemetry={latest.telemetry} />
                </>
              ) : (
                <p className="text-sm text-slate-400">No quizzes yet.</p>
              )}
            </div>
          </div>

          <Panel
            title="Your subjects"
            subtitle={summary.student.grade ? `Grade ${summary.student.grade} — progress counts passed lessons` : undefined}
            action={
              <Link to="/progress" className="text-xs font-bold text-indigo-300 hover:text-indigo-200">
                Full analytics →
              </Link>
            }
          >
            <SubjectPerformance subjects={summary.subjects} compact />
          </Panel>
        </div>

        {/* AI Coach */}
        <div className="glass-panel rounded-3xl p-5 sm:p-6 border border-slate-900 shadow-lg flex flex-col justify-between gap-6">
          <div className="space-y-4">
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <span className="text-teal-400">✦</span> AI Learning Coach
            </h3>
            {!recommendation ? (
              <div className="space-y-3 py-4 text-center">
                <div className="text-4xl" aria-hidden="true">
                  🤖
                </div>
                <p className="text-sm font-semibold text-slate-300">
                  {coach?.status === 'telemetry_unavailable' ? 'Camera data unavailable' : 'No advice yet'}
                </p>
                <p className="text-xs text-slate-500 leading-relaxed">
                  {coach?.status === 'telemetry_unavailable'
                    ? 'Your latest quiz had no valid camera reading, so the coach did not guess. Keep the camera agent running during your next quiz.'
                    : 'Take a quiz with the camera agent running. The coach then suggests your next step.'}
                </p>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="rounded-2xl bg-indigo-500/10 border border-indigo-500/20 p-4 space-y-1">
                  <p className="text-[10px] font-semibold text-indigo-300 uppercase tracking-wider">Suggested next step</p>
                  <p className="text-lg font-extrabold text-white">
                    {actionInfo(recommendation.action).icon} {actionInfo(recommendation.action).label}
                  </p>
                  <p className="text-xs text-slate-400">{actionInfo(recommendation.action).description}</p>
                  {coachAttempt && (
                    <p className="text-[11px] text-slate-500">
                      After: {coachAttempt.lesson_title} ({coachAttempt.subject}
                      {coachAttempt.curriculum_topic ? ` · ${coachAttempt.curriculum_topic}` : ''})
                    </p>
                  )}
                </div>
                <p className="text-sm text-slate-300 leading-relaxed">“{recommendation.explanation}”</p>
                <div className="space-y-1.5" title={CONFIDENCE_NOTE}>
                  <div className="flex items-center justify-between text-[10px] uppercase tracking-wider">
                    <span className="font-semibold text-slate-500">Decision strength (not a probability)</span>
                    <span className="font-bold text-teal-300">{Math.round(recommendation.confidence * 100)}%</span>
                  </div>
                  <ProgressBar percent={recommendation.confidence * 100} color="#0d9488" label="Decision strength" />
                  {recommendation.policy && (
                    <p className="text-[10px] text-slate-500">Decided by: {POLICY_LABELS[recommendation.policy] || recommendation.policy}</p>
                  )}
                </div>
              </div>
            )}
          </div>
          <Link
            to="/recommendations"
            className="w-full inline-flex items-center justify-center px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-800 hover:bg-slate-800 text-xs font-semibold text-slate-300 hover:text-white transition-colors"
          >
            Open the AI Coach →
          </Link>
        </div>
      </div>

      <Panel
        title="Recent activity"
        action={
          <Link to="/progress#activity" className="text-xs font-bold text-indigo-300 hover:text-indigo-200">
            All activity →
          </Link>
        }
      >
        <ActivityFeed events={summary.activity} limit={5} />
      </Panel>
    </div>
  )
}
