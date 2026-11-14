import React, { useCallback, useEffect, useState } from 'react'
import {
  ArrowRight,
  Bot,
  BrainCircuit,
  CalendarClock,
  ChevronRight,
  ClipboardList,
  Clock,
  Funnel,
  Minus,
  ShieldCheck,
  Sparkles,
  TrendingDown,
  TrendingUp
} from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import { rlService } from '../services/rlService'
import { lessonService } from '../services/lessonService'
import {
  ACTION_CATALOGUE,
  ALL_ACTIONS,
  CONFIDENCE_NOTE,
  POLICY_LABELS,
  actionInfo,
  resolveNextStep
} from '../utils/recommendationActions'
import { formatDate, formatPercent, outcomeText } from '../utils/analytics'
import { Panel } from '../components/AnalyticsPanels'
import { ActionIcon, DifficultyBadge, SubjectChip } from '../components/learning'
import { TONE_SOFT } from '../components/visuals'
import {
  Badge,
  Button,
  Callout,
  Card,
  EmptyState,
  ErrorState,
  PageHeader,
  PageSkeleton,
  ProgressBar,
  SectionHeader,
  Tooltip,
  cx
} from '../components/ui'

const OUTCOME_VISUAL = {
  emerald: { icon: TrendingUp, tone: 'success', text: 'text-success' },
  rose: { icon: TrendingDown, tone: 'danger', text: 'text-danger' },
  slate: { icon: Minus, tone: 'neutral', text: 'text-ink-2' }
}

const HOW_IT_WORKS = [
  {
    icon: ClipboardList,
    title: 'Reads your quiz',
    text: 'Score, quiz level, hints, how many tries you needed and what the camera noticed.'
  },
  {
    icon: ShieldCheck,
    title: 'Removes unsuitable steps',
    text: 'Safety rules come first, for example no moving on before you pass.'
  },
  {
    icon: BrainCircuit,
    title: 'Picks the highest-value step',
    text: 'A Q-learning table trained offline on simulated students scores the remaining steps.'
  }
]

function DetailRow({ label, children }) {
  return (
    <div className="flex items-center justify-between gap-4 py-2.5 text-[13px]">
      <dt className="shrink-0 text-ink-2">{label}</dt>
      <dd className="min-w-0 truncate text-right font-medium text-ink">{children || '—'}</dd>
    </div>
  )
}

export default function Recommendations() {
  const { user } = useAuth()
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [latest, setLatest] = useState(null)
  const [history, setHistory] = useState([])
  const [historyError, setHistoryError] = useState('')
  const [currentLesson, setCurrentLesson] = useState(null)

  const load = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      // Recommendations are produced by the server's Q-learning policy when
      // a quiz is graded; this page only displays them.
      const [latestRes, historyRes] = await Promise.all([
        rlService.getLatest(),
        rlService.getHistory(20).catch((err) => {
          setHistoryError(err.message || 'Could not load earlier advice')
          return []
        })
      ])
      setLatest(latestRes)
      setHistory(Array.isArray(historyRes) ? historyRes : [])
      if (latestRes?.attempt?.lesson_id) {
        try {
          // Lesson detail carries its quizzes and its place in the grade/subject sequence.
          const lessonRes = await lessonService.getLesson(latestRes.attempt.lesson_id)
          if (lessonRes?.success) setCurrentLesson(lessonRes.data)
        } catch {
          // Only refines the next-step link.
        }
      }
    } catch (err) {
      setError(err.message || 'Failed to load your recommendation')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    load()
  }, [load, user?.id])

  if (loading) return <PageSkeleton label="Loading your AI coach" />
  if (error) return <ErrorState message={error} onRetry={load} />

  const attempt = latest?.attempt
  const recommendation = latest?.status === 'available' ? latest.recommendation : null
  const info = recommendation ? actionInfo(recommendation.action) : null
  const runnerUp = typeof recommendation?.runner_up === 'string' ? recommendation.runner_up : recommendation?.runner_up?.action

  const nextStep = recommendation
    ? resolveNextStep(recommendation.action, {
        lessonId: attempt?.lesson_id,
        quizId: attempt?.quiz_id,
        difficulty: attempt?.difficulty,
        lessonQuizzes: currentLesson?.quizzes,
        navigation: currentLesson?.navigation
      })
    : null
  const nextStepLink =
    nextStep && (nextStep.kind === 'navigate' || nextStep.kind === 'retry')
      ? { to: nextStep.to, state: { ...(nextStep.state || {}), mode: nextStep.mode, attempt: nextStep.kind === 'retry' ? Date.now() : undefined } }
      : recommendation && attempt
        ? { to: `/lesson/${attempt.lesson_id}`, state: { recommendedAction: recommendation.action } }
        : null
  const nextStepLabel =
    nextStep && !['unknown', 'review', 'break'].includes(nextStep.kind)
      ? nextStep.label
      : nextStep?.kind === 'break'
        ? 'Take a 2–5 minute break, then reopen the lesson →'
        : `${info?.label}: open the lesson →`
  const strength = recommendation ? Math.round(recommendation.confidence * 100) : 0

  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="Insights"
        title="AI Coach"
        description="After every quiz, your coach looks at your score, the quiz level, hints, how many tries you needed and what the camera noticed, then picks one of 11 next steps. It learned which steps help most by practising on thousands of simulated students."
        meta={
          <>
            <Badge tone="brand" icon={BrainCircuit}>
              Q-learning policy · trained offline
            </Badge>
            <Badge icon={ShieldCheck}>Safety rules applied first</Badge>
          </>
        }
      />

      {/* Current recommendation */}
      {!recommendation ? (
        <Card>
          <EmptyState
            icon={Bot}
            title={
              latest?.status === 'telemetry_unavailable'
                ? 'No advice for your last quiz — camera data was unavailable'
                : latest?.status === 'not_generated'
                  ? 'The coach could not give advice for your last quiz'
                  : 'No advice yet'
            }
            text={
              latest?.status === 'telemetry_unavailable'
                ? 'The coach needs a real camera reading from the quiz and never guesses how focused you were. Keep the camera agent running during your next quiz.'
                : latest?.status === 'not_generated'
                  ? 'Take another quiz and the coach will try again.'
                  : 'Finish a lesson quiz with the camera agent running and your first piece of advice will appear here.'
            }
            action={
              <Button to="/subjects" iconRight={ArrowRight}>
                Browse subjects
              </Button>
            }
          />
        </Card>
      ) : (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <Card as="section" padding="lg" aria-labelledby="current-advice" className="relative space-y-6 overflow-hidden lg:col-span-2">
            <div className="pointer-events-none absolute -right-20 -top-24 h-64 w-64 rounded-full bg-brand-500/[0.12] blur-3xl" aria-hidden="true" />
            <div className="relative flex flex-wrap items-center justify-between gap-3">
              <Badge tone="mint" icon={Sparkles}>
                Your next step
              </Badge>
              {attempt?.created_at && <span className="text-xs text-ink-2">After your quiz on {formatDate(attempt.created_at, { withTime: true })}</span>}
            </div>
            <div className="relative flex items-start gap-4">
              <span className="grid h-14 w-14 shrink-0 place-items-center rounded-2xl bg-brand-500/[0.14] text-brand-200 ring-1 ring-inset ring-brand-500/30">
                <ActionIcon action={recommendation.action} size={26} />
              </span>
              <div className="min-w-0 space-y-1.5">
                <h2 id="current-advice" className="font-display text-[26px] font-semibold leading-tight tracking-tight text-ink">
                  {info.label}
                </h2>
                <p className="text-[15px] leading-relaxed text-ink-2">{info.description}</p>
              </div>
            </div>
            <figure className="relative space-y-2">
              <figcaption className="text-xs font-medium text-ink-2">Why the coach chose this</figcaption>
              <blockquote className="rounded-xl border border-line bg-deep/70 px-4 py-3.5 text-sm leading-relaxed text-ink">
                {recommendation.explanation}
              </blockquote>
            </figure>
            {nextStepLink && (
              <div className="relative">
                <Button to={nextStepLink.to} state={nextStepLink.state} size="lg" wrap icon={ArrowRight}>
                  {nextStepLabel}
                </Button>
              </div>
            )}
          </Card>

          <Card as="aside" aria-label="Based on your quiz" className="space-y-5">
            <SectionHeader as="h3" title="Based on your quiz" icon={ClipboardList} />
            <dl className="divide-y divide-line/70">
              <DetailRow label="Subject">{attempt?.subject && <SubjectChip subject={attempt.subject} className="justify-end" />}</DetailRow>
              <DetailRow label="Topic">{attempt?.curriculum_topic || attempt?.topic}</DetailRow>
              <DetailRow label="Lesson">{attempt?.lesson_title}</DetailRow>
              <DetailRow label="Score">
                <span className="inline-flex items-center gap-2">
                  {formatPercent(attempt?.quiz_score)}
                  {attempt?.difficulty && <DifficultyBadge difficulty={attempt.difficulty} size="sm" />}
                </span>
              </DetailRow>
              <DetailRow label="Attention">
                {formatPercent(attempt?.attention_score === null || attempt?.attention_score === undefined ? null : attempt.attention_score * 100)}
              </DetailRow>
              <DetailRow label="When">{formatDate(attempt?.created_at, { withTime: true })}</DetailRow>
            </dl>
            <div className="space-y-2 rounded-xl border border-line bg-deep/70 p-4">
              <div className="flex items-center justify-between text-xs">
                <Tooltip content={CONFIDENCE_NOTE} align="start">
                  <span tabIndex={0} className="cursor-help rounded font-medium text-ink-2 underline decoration-line-strong decoration-dotted underline-offset-4">
                    Decision strength
                  </span>
                </Tooltip>
                <span className="font-semibold text-mint-300">{strength}%</span>
              </div>
              <ProgressBar value={strength} tone="mint" size="sm" label="Decision strength" />
              <p className="text-[11px] leading-relaxed text-ink-2">
                How clearly this step beat the others. It is not a probability.
                {runnerUp && ACTION_CATALOGUE[runnerUp] ? ` Second choice: ${ACTION_CATALOGUE[runnerUp].label}.` : ''}
              </p>
              {recommendation.policy && (
                <p className="flex items-center gap-1.5 pt-1 text-[11px] text-ink-2">
                  <BrainCircuit size={13} aria-hidden="true" />
                  Decided by: {POLICY_LABELS[recommendation.policy] || recommendation.policy}
                </p>
              )}
            </div>
          </Card>
        </div>
      )}

      {/* How the coach decides */}
      <Card as="section" aria-labelledby="how-it-works" className="space-y-5">
        <SectionHeader id="how-it-works" title="How your coach decides" icon={Funnel} />
        <ol className="grid grid-cols-1 gap-3 md:grid-cols-3">
          {HOW_IT_WORKS.map(({ icon: Icon, title, text }, index) => (
            <li key={title} className="relative flex gap-3 rounded-xl border border-line bg-deep/60 p-4">
              <span className="grid h-9 w-9 shrink-0 place-items-center rounded-lg bg-brand-500/[0.12] text-brand-300 ring-1 ring-inset ring-brand-500/25">
                <Icon size={17} aria-hidden="true" />
              </span>
              <div className="min-w-0 space-y-1">
                <p className="text-sm font-semibold text-ink">
                  <span className="mr-1.5 tabular-nums text-ink-3">{index + 1}.</span>
                  {title}
                </p>
                <p className="text-[13px] leading-relaxed text-ink-2">{text}</p>
              </div>
              {index < HOW_IT_WORKS.length - 1 && (
                <ChevronRight size={16} className="absolute -right-3 top-1/2 hidden -translate-y-1/2 text-ink-3 md:block" aria-hidden="true" />
              )}
            </li>
          ))}
        </ol>
        <p className="text-xs leading-relaxed text-ink-2">
          The coach is not a chatbot or a live language model. Its Q-table was trained offline and is only read, never updated, while it advises
          you.
        </p>
      </Card>

      {/* History */}
      <Panel
        title="Earlier advice and what happened next"
        subtitle="Each piece of advice is checked against your next quiz. “Followed” is worked out from that quiz (for example, whether you moved to a harder level); some steps, like taking a break, cannot be checked."
        icon={CalendarClock}
      >
        {historyError && (
          <Callout tone="warning" role="status">
            {historyError}
          </Callout>
        )}
        {history.length === 0 ? (
          <EmptyState icon={Clock} title="No earlier advice yet" text="Advice from your quizzes will be listed here." compact />
        ) : (
          <ol className="relative space-y-3">
            {history.map((item, index) => {
              const itemInfo = actionInfo(item.action)
              const outcome = outcomeText(item.outcome)
              const visual = OUTCOME_VISUAL[outcome.tone] || OUTCOME_VISUAL.slate
              const OutcomeIcon = item.outcome?.status === 'recorded' ? visual.icon : Clock
              return (
                <li key={item.id} className="relative flex gap-4">
                  {index < history.length - 1 && <span className="absolute bottom-[-14px] left-[19px] top-11 w-px bg-line" aria-hidden="true" />}
                  <span className="relative grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-raised text-ink-2 ring-1 ring-inset ring-line-strong">
                    <ActionIcon action={item.action} size={18} />
                  </span>
                  <div className="min-w-0 flex-1 rounded-xl border border-line bg-deep/60 px-4 py-3">
                    <div className="flex flex-wrap items-baseline justify-between gap-2">
                      <p className="text-sm font-semibold text-ink">{itemInfo.label}</p>
                      <span className="text-[11px] text-ink-2">{formatDate(item.created_at, { withTime: true })}</span>
                    </div>
                    <p className="mt-1 text-xs text-ink-2">
                      After {formatPercent(item.context?.score)} on “{item.context?.lesson_title || 'a lesson'}”
                      {item.context?.subject ? ` · ${item.context.subject}` : ''}
                      {item.context?.topic ? ` · ${item.context.topic}` : ''}
                    </p>
                    <p className={cx('mt-2 flex items-start gap-2 text-xs', item.outcome?.status === 'recorded' ? visual.text : 'text-ink-2')}>
                      <span className={cx('grid h-5 w-5 shrink-0 place-items-center rounded-md ring-1 ring-inset', TONE_SOFT[item.outcome?.status === 'recorded' ? visual.tone : 'neutral'])}>
                        <OutcomeIcon size={12} aria-hidden="true" />
                      </span>
                      <span className="pt-0.5">{outcome.text}</span>
                    </p>
                  </div>
                </li>
              )
            })}
          </ol>
        )}
      </Panel>

      {/* All 11 actions */}
      <Panel
        title="The 11 steps your coach can suggest"
        subtitle="A Q-learning table, trained offline on simulated students, gives every step a score for your situation. Safety rules first remove unsuitable steps (for example, moving on before you pass), then the highest-scoring step is chosen."
        icon={Sparkles}
      >
        <div className="grid grid-cols-1 gap-3 md:grid-cols-2 xl:grid-cols-3">
          {ALL_ACTIONS.map((name) => {
            const strategy = ACTION_CATALOGUE[name]
            const active = recommendation?.action === name
            return (
              <div
                key={name}
                className={cx(
                  'flex gap-3 rounded-xl border p-4 transition-colors',
                  active ? 'border-brand-500/45 bg-brand-500/[0.08]' : 'border-line bg-deep/60 hover:border-line-strong'
                )}
              >
                <span
                  className={cx(
                    'grid h-9 w-9 shrink-0 place-items-center rounded-lg ring-1 ring-inset',
                    active ? 'bg-brand-500/[0.16] text-brand-200 ring-brand-500/35' : 'bg-raised text-ink-2 ring-line-strong'
                  )}
                >
                  <ActionIcon action={name} size={17} />
                </span>
                <div className="min-w-0 space-y-1">
                  <h3 className="flex flex-wrap items-center gap-2 text-sm font-semibold text-ink">
                    {strategy.label}
                    {active && (
                      <Badge tone="mint" size="sm">
                        Current advice
                      </Badge>
                    )}
                  </h3>
                  <p className="text-[13px] leading-relaxed text-ink-2">{strategy.description}</p>
                </div>
              </div>
            )
          })}
        </div>
      </Panel>
    </div>
  )
}
