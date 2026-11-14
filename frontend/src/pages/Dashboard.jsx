import React, { useCallback, useEffect, useState } from 'react'
import {
  ArrowRight,
  BookCheck,
  BookOpen,
  Bot,
  CalendarClock,
  CalendarDays,
  ChartLine,
  CircleCheck,
  CircleDot,
  ClipboardList,
  Compass,
  Flame,
  GraduationCap,
  Sparkles,
  Target
} from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import { analyticsService } from '../services/analyticsService'
import { rlService } from '../services/rlService'
import { CONFIDENCE_NOTE, POLICY_LABELS, actionInfo } from '../utils/recommendationActions'
import { continueTarget, formatPercent, relativeDay } from '../utils/analytics'
import { ActivityFeed, Panel, SubjectPerformance } from '../components/AnalyticsPanels'
import { ActionIcon, DifficultyBadge, SubjectIcon, TelemetryBadge } from '../components/learning'
import {
  Badge,
  Button,
  Callout,
  Card,
  ErrorState,
  PageSkeleton,
  ProgressBar,
  ProgressRing,
  SectionHeader,
  StatCard,
  Tooltip
} from '../components/ui'

function greeting() {
  const hour = new Date().getHours()
  if (hour < 12) return 'Good morning'
  if (hour < 17) return 'Good afternoon'
  return 'Good evening'
}

function firstName(name) {
  return String(name || '').trim().split(/\s+/)[0] || 'there'
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

  if (loading) return <PageSkeleton label="Loading your dashboard" />
  if (error && !summary) return <ErrorState message={error} onRetry={load} />

  const o = summary.overview
  const latest = o.latest_activity
  const next = continueTarget(summary)
  const recommendation = coach?.status === 'available' ? coach.recommendation : null
  const coachAttempt = coach?.attempt
  const grade = summary.student.grade
  const today = new Date().toLocaleDateString(undefined, { weekday: 'long', day: 'numeric', month: 'long' })

  return (
    <div className="space-y-6">
      {error && (
        <Callout tone="warning" role="status">
          Showing your last loaded data — refresh failed: {error}
        </Callout>
      )}

      {/* Greeting and completion */}
      <Card padding="none" className="relative overflow-hidden">
        <div
          className="bg-dot-grid pointer-events-none absolute inset-0 [mask-image:radial-gradient(ellipse_at_top_left,black_10%,transparent_65%)]"
          aria-hidden="true"
        />
        <div className="pointer-events-none absolute -left-24 -top-32 h-80 w-80 rounded-full bg-brand-500/[0.13] blur-3xl" aria-hidden="true" />
        <div className="pointer-events-none absolute -bottom-32 right-10 h-72 w-72 rounded-full bg-mint-500/[0.07] blur-3xl" aria-hidden="true" />
        <div className="relative grid gap-8 p-6 sm:p-8 lg:grid-cols-[minmax(0,1fr)_auto] lg:items-center lg:gap-12">
          <div className="space-y-5">
            <div className="flex flex-wrap items-center gap-2">
              {grade && (
                <Badge tone="brand" icon={GraduationCap}>
                  Grade {grade}
                </Badge>
              )}
              {o.current_streak_days >= 1 && (
                <Tooltip content="Consecutive days (UTC) with at least one quiz submitted">
                  <Badge tone="warning" icon={Flame} tabIndex={0}>
                    {o.current_streak_days}-day streak
                  </Badge>
                </Tooltip>
              )}
              <Badge icon={CalendarDays}>{today}</Badge>
            </div>
            <div className="space-y-2.5">
              <h1 className="font-display text-[30px] font-semibold leading-tight tracking-tight text-ink sm:text-[38px]">
                {greeting()}, {firstName(summary.student.name)}
              </h1>
              <p className="max-w-xl text-[15px] leading-relaxed text-ink-2">
                {o.quiz_attempts === 0
                  ? 'Welcome to Aegis! Open a lesson, read it, then take its quiz. Your progress and your AI coach start working after your first quiz.'
                  : `You have completed ${o.lessons_completed} of ${o.lessons_total} lessons in your grade. A lesson counts as completed when you pass one of its quizzes (${summary.definitions.pass_score}% or more).`}
              </p>
            </div>
            <div className="flex flex-wrap gap-3">
              <Button to={next ? `/lesson/${next.lesson_id}` : '/subjects'} size="lg" iconRight={ArrowRight}>
                {next ? 'Continue learning' : 'Browse subjects'}
              </Button>
              <Button to="/progress" variant="secondary" size="lg" icon={ChartLine}>
                View progress
              </Button>
            </div>
          </div>
          <div className="flex items-center gap-5 lg:flex-col lg:gap-3">
            <ProgressRing value={o.completion_percent} size={164} stroke={12} label={`Curriculum completion ${formatPercent(o.completion_percent, '0%')}`}>
              <span>
                <span className="block text-[36px] font-semibold leading-none tracking-tight text-ink">
                  {formatPercent(o.completion_percent, '0%')}
                </span>
                <span className="mt-1.5 block text-xs font-medium text-ink-2">curriculum</span>
              </span>
            </ProgressRing>
            <p className="max-w-[10rem] text-sm leading-snug text-ink-2 lg:text-center">
              <span className="font-semibold text-ink">{o.lessons_completed}</span> of {o.lessons_total} lessons passed
            </p>
          </div>
        </div>
      </Card>

      {/* Key figures */}
      <div className="grid grid-cols-2 gap-3 sm:gap-4 xl:grid-cols-4">
        <StatCard
          label="Lessons completed"
          value={`${o.lessons_completed}/${o.lessons_total}`}
          sub={`${o.lessons_attempted} started`}
          icon={BookCheck}
          tone="mint"
        />
        <StatCard
          label="Quiz attempts"
          value={o.quiz_attempts}
          sub={o.days_active ? `on ${o.days_active} day${o.days_active === 1 ? '' : 's'}` : 'none yet'}
          icon={ClipboardList}
          tone="brand"
        />
        <StatCard
          label="Average score"
          value={formatPercent(o.average_score)}
          sub={o.average_score === null ? 'take a quiz to see it' : `best ${formatPercent(o.best_score)}`}
          icon={Target}
          tone="info"
        />
        <StatCard label="Subjects" value={o.subjects_available} sub={grade ? `in Grade ${grade}` : 'choose a grade'} icon={Compass} tone="neutral" />
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <div className="space-y-6 lg:col-span-2">
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            {/* Continue learning */}
            <Card className="flex flex-col">
              <div className="flex items-start justify-between gap-3">
                <p className="text-[13px] font-medium text-ink-2">Continue learning</p>
                {next && <SubjectIcon subject={next.subject} size="sm" />}
              </div>
              {next ? (
                <div className="mt-3 space-y-1">
                  <h2 className="font-display text-lg font-semibold leading-snug text-ink">{next.lesson_title}</h2>
                  <p className="text-[13px] text-ink-2">
                    {next.subject} · {next.topic}
                  </p>
                </div>
              ) : (
                <p className="mt-3 text-sm leading-relaxed text-ink">
                  {o.lessons_total > 0 ? 'Every lesson in your grade is completed!' : 'Choose your grade to start.'}
                </p>
              )}
              <div className="mt-auto pt-5">
                <Button to={next ? `/lesson/${next.lesson_id}` : '/subjects'} fullWidth iconRight={ArrowRight} icon={next ? BookOpen : undefined}>
                  {next ? 'Open lesson' : 'Browse subjects'}
                </Button>
              </div>
            </Card>

            {/* Latest activity */}
            <Card className="flex flex-col">
              <div className="flex items-start justify-between gap-3">
                <p className="text-[13px] font-medium text-ink-2">Latest activity</p>
                {latest && <span className="text-xs text-ink-2">{relativeDay(latest.at)}</span>}
              </div>
              {latest ? (
                <>
                  <div className="mt-3 space-y-1">
                    <h2 className="font-display text-lg font-semibold leading-snug text-ink">{latest.lesson_title}</h2>
                    <div className="flex flex-wrap items-center gap-2 text-[13px] text-ink-2">
                      <span>{latest.subject}</span>
                      <DifficultyBadge difficulty={latest.difficulty} size="sm" />
                    </div>
                  </div>
                  <div className="mt-auto flex flex-wrap items-end justify-between gap-3 pt-5">
                    <div className="flex items-baseline gap-2.5">
                      <p className="text-[28px] font-semibold leading-none text-ink">{formatPercent(latest.score)}</p>
                      <Badge tone={latest.passed ? 'success' : 'warning'} icon={latest.passed ? CircleCheck : CircleDot} size="sm">
                        {latest.passed ? 'Passed' : 'Not passed yet'}
                      </Badge>
                    </div>
                    <TelemetryBadge telemetry={latest.telemetry} />
                  </div>
                </>
              ) : (
                <p className="mt-3 text-sm text-ink-2">No quizzes yet.</p>
              )}
            </Card>
          </div>

          <Panel
            title="Your subjects"
            subtitle={grade ? `Grade ${grade} · progress counts passed lessons` : undefined}
            icon={BookOpen}
            action={
              <Button to="/progress" variant="ghost" size="sm" iconRight={ArrowRight}>
                Full analytics
              </Button>
            }
          >
            <SubjectPerformance subjects={summary.subjects} compact />
          </Panel>

          <Panel
            title="Recent activity"
            icon={CalendarClock}
            action={
              <Button to="/progress#activity" variant="ghost" size="sm" iconRight={ArrowRight}>
                All activity
              </Button>
            }
          >
            <ActivityFeed events={summary.activity} limit={5} />
          </Panel>
        </div>

        <div className="space-y-6">
          {/* AI coach */}
          <Card className="flex flex-col gap-5">
            <SectionHeader icon={Sparkles} title="AI Learning Coach" description="Offline-trained Q-learning policy" />
            {!recommendation ? (
              <div className="space-y-2 rounded-xl border border-line bg-deep/60 px-4 py-6 text-center">
                <span className="mx-auto grid h-11 w-11 place-items-center rounded-xl bg-white/[0.05] text-ink-2 ring-1 ring-inset ring-white/10">
                  <Bot size={21} aria-hidden="true" />
                </span>
                <p className="text-sm font-semibold text-ink">
                  {coach?.status === 'telemetry_unavailable' ? 'Camera data unavailable' : 'No advice yet'}
                </p>
                <p className="text-[13px] leading-relaxed text-ink-2">
                  {coach?.status === 'telemetry_unavailable'
                    ? 'Your latest quiz had no valid camera reading, so the coach did not guess. Keep the camera agent running during your next quiz.'
                    : 'Take a quiz with the camera agent running. The coach then suggests your next step.'}
                </p>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="space-y-2 rounded-xl border border-brand-500/25 bg-brand-500/[0.07] p-4">
                  <p className="text-xs font-medium text-brand-300">Suggested next step</p>
                  <p className="flex items-center gap-2.5 font-display text-lg font-semibold text-ink">
                    <span className="grid h-8 w-8 shrink-0 place-items-center rounded-lg bg-brand-500/[0.16] text-brand-200">
                      <ActionIcon action={recommendation.action} size={17} />
                    </span>
                    {actionInfo(recommendation.action).label}
                  </p>
                  <p className="text-[13px] leading-relaxed text-ink-2">{actionInfo(recommendation.action).description}</p>
                  {coachAttempt && (
                    <p className="text-xs text-ink-2">
                      After: {coachAttempt.lesson_title} ({coachAttempt.subject}
                      {coachAttempt.curriculum_topic ? ` · ${coachAttempt.curriculum_topic}` : ''})
                    </p>
                  )}
                </div>
                <p className="text-sm italic leading-relaxed text-ink">“{recommendation.explanation}”</p>
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-xs">
                    <Tooltip content={CONFIDENCE_NOTE} align="start">
                      <span tabIndex={0} className="cursor-help rounded text-ink-2 underline decoration-line-strong decoration-dotted underline-offset-4">
                        Decision strength (not a probability)
                      </span>
                    </Tooltip>
                    <span className="font-semibold text-mint-300">{Math.round(recommendation.confidence * 100)}%</span>
                  </div>
                  <ProgressBar value={recommendation.confidence * 100} tone="mint" size="sm" label="Decision strength" />
                  {recommendation.policy && (
                    <p className="text-[11px] text-ink-2">Decided by: {POLICY_LABELS[recommendation.policy] || recommendation.policy}</p>
                  )}
                </div>
              </div>
            )}
            <Button to="/recommendations" variant="secondary" fullWidth iconRight={ArrowRight}>
              Open the AI Coach
            </Button>
          </Card>

          {/* Streak */}
          <Card>
            <div className="flex items-center gap-3.5">
              <span className="grid h-11 w-11 shrink-0 place-items-center rounded-xl bg-warning/[0.12] text-warning ring-1 ring-inset ring-warning/25">
                <Flame size={21} aria-hidden="true" />
              </span>
              <div>
                <p className="text-[13px] font-medium text-ink-2">Learning streak</p>
                <p className="text-2xl font-semibold text-ink">
                  {o.current_streak_days} day{o.current_streak_days === 1 ? '' : 's'}
                </p>
              </div>
            </div>
            <dl className="mt-5 grid grid-cols-2 gap-3">
              <div className="rounded-lg bg-deep/70 p-3 ring-1 ring-inset ring-line">
                <dt className="text-[11px] text-ink-2">Longest streak</dt>
                <dd className="mt-1 text-sm font-semibold text-ink">
                  {o.longest_streak_days} day{o.longest_streak_days === 1 ? '' : 's'}
                </dd>
              </div>
              <div className="rounded-lg bg-deep/70 p-3 ring-1 ring-inset ring-line">
                <dt className="text-[11px] text-ink-2">Active days</dt>
                <dd className="mt-1 text-sm font-semibold text-ink">{o.days_active}</dd>
              </div>
            </dl>
            <p className="mt-3 text-[11px] leading-relaxed text-ink-2">Days with at least one quiz submitted (UTC).</p>
          </Card>
        </div>
      </div>
    </div>
  )
}
