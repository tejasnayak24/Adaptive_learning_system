import React, { useCallback, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
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
import { EmptyState, ErrorState, LoadingSkeleton, Panel, ProgressBar } from '../components/AnalyticsPanels'

const OUTCOME_TONE = {
  emerald: 'text-emerald-300',
  rose: 'text-rose-300',
  slate: 'text-slate-400'
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

  if (loading) return <LoadingSkeleton blocks={0} />
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

  return (
    <div className="max-w-5xl mx-auto space-y-6 sm:space-y-8">
      <div className="space-y-1.5">
        <h1 className="font-display text-3xl font-extrabold tracking-tight text-white md:text-4xl">AI Coach</h1>
        <p className="text-slate-400 text-sm leading-relaxed max-w-3xl">
          After every quiz, your coach looks at your score, the quiz level, hints, how many tries you needed and what the camera noticed, then
          picks one of 11 next steps. It learned which steps help most by practising on thousands of simulated students.
        </p>
      </div>

      {/* Latest recommendation */}
      {!recommendation ? (
        <Panel>
          <EmptyState
            icon="🤖"
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
              <Link to="/subjects" className="mt-2 inline-flex px-5 py-2.5 rounded-xl bg-indigo-500 hover:bg-indigo-600 text-white font-semibold text-xs">
                Browse subjects
              </Link>
            }
          />
        </Panel>
      ) : (
        <section className="glass-panel rounded-3xl p-5 sm:p-8 border border-slate-900 shadow-xl space-y-6 relative overflow-hidden">
          <div className="absolute top-0 right-0 h-48 w-48 bg-indigo-500/5 blur-3xl pointer-events-none" />
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8">
            <div className="md:col-span-2 space-y-5">
              <div className="space-y-1">
                <span className="text-[10px] text-teal-300 font-bold uppercase tracking-wider">Your next step</span>
                <p className="text-2xl font-extrabold text-white">
                  {info.icon} {info.label}
                </p>
                <p className="text-sm text-slate-300">{info.description}</p>
              </div>

              <div className="space-y-2">
                <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Why the coach chose this</span>
                <p className="text-sm text-slate-300 bg-slate-900/40 border border-slate-800 p-4 rounded-2xl leading-relaxed">
                  {recommendation.explanation}
                </p>
              </div>

              {nextStepLink && (
                <Link
                  to={nextStepLink.to}
                  state={nextStepLink.state}
                  className="inline-flex justify-center px-5 py-3 rounded-xl bg-indigo-500 text-white font-bold text-sm shadow hover:bg-indigo-600 transition-colors"
                >
                  {nextStepLabel}
                </Link>
              )}
            </div>

            <div className="space-y-4 rounded-2xl bg-slate-925 border border-slate-800 p-5 h-fit">
              <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400">Based on your quiz</h2>
              <dl className="space-y-2.5 text-xs">
                <Row label="Subject" value={attempt?.subject} />
                <Row label="Topic" value={attempt?.curriculum_topic || attempt?.topic} />
                <Row label="Lesson" value={attempt?.lesson_title} />
                <Row label="Score" value={`${formatPercent(attempt?.quiz_score)} (${String(attempt?.difficulty || '').toLowerCase()})`} />
                <Row label="Attention" value={formatPercent(attempt?.attention_score === null || attempt?.attention_score === undefined ? null : attempt.attention_score * 100)} />
                <Row label="When" value={formatDate(attempt?.created_at, { withTime: true })} />
              </dl>
              <div className="pt-2 space-y-1.5" title={CONFIDENCE_NOTE}>
                <div className="flex justify-between text-[10px] uppercase tracking-wider">
                  <span className="text-slate-500 font-semibold">Decision strength</span>
                  <span className="text-teal-300 font-bold">{Math.round(recommendation.confidence * 100)}%</span>
                </div>
                <ProgressBar percent={recommendation.confidence * 100} color="#0d9488" label="Decision strength" />
                <p className="text-[10px] text-slate-500 leading-relaxed">
                  How clearly this step beat the others. It is not a probability.
                  {runnerUp && ACTION_CATALOGUE[runnerUp] ? ` Second choice: ${ACTION_CATALOGUE[runnerUp].label}.` : ''}
                </p>
                {recommendation.policy && (
                  <p className="text-[10px] text-slate-500">Decided by: {POLICY_LABELS[recommendation.policy] || recommendation.policy}</p>
                )}
              </div>
            </div>
          </div>
        </section>
      )}

      {/* History */}
      <Panel
        title="Earlier advice and what happened next"
        subtitle="Each piece of advice is checked against your next quiz. “Followed” is worked out from that quiz (for example, whether you moved to a harder level); some steps, like taking a break, cannot be checked."
      >
        {historyError && <p className="text-xs text-amber-300">{historyError}</p>}
        {history.length === 0 ? (
          <EmptyState icon="🕘" title="No earlier advice yet" text="Advice from your quizzes will be listed here." />
        ) : (
          <ol className="space-y-2">
            {history.map((item) => {
              const itemInfo = actionInfo(item.action)
              const outcome = outcomeText(item.outcome)
              return (
                <li key={item.id} className="rounded-2xl bg-slate-900/40 border border-slate-800 px-4 py-3 space-y-1">
                  <div className="flex flex-wrap items-baseline justify-between gap-2">
                    <p className="text-sm font-semibold text-white">
                      <span aria-hidden="true">{itemInfo.icon}</span> {itemInfo.label}
                    </p>
                    <span className="text-[10px] text-slate-500">{formatDate(item.created_at, { withTime: true })}</span>
                  </div>
                  <p className="text-[11px] text-slate-400">
                    After {formatPercent(item.context?.score)} on “{item.context?.lesson_title || 'a lesson'}”
                    {item.context?.subject ? ` · ${item.context.subject}` : ''}
                    {item.context?.topic ? ` · ${item.context.topic}` : ''}
                  </p>
                  <p className={`text-[11px] ${OUTCOME_TONE[outcome.tone]}`}>{outcome.text}</p>
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
      >
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {ALL_ACTIONS.map((name) => {
            const strategy = ACTION_CATALOGUE[name]
            const active = recommendation?.action === name
            return (
              <div
                key={name}
                className={`flex gap-3 p-4 rounded-2xl border ${active ? 'bg-indigo-500/10 border-indigo-500/30' : 'bg-slate-900/30 border-slate-800'}`}
              >
                <span className="text-2xl select-none" aria-hidden="true">
                  {strategy.icon}
                </span>
                <div className="space-y-1">
                  <h3 className="text-xs font-extrabold text-white tracking-wide">
                    {strategy.label}
                    {active && <span className="ml-2 text-[10px] font-bold text-teal-300">Current advice</span>}
                  </h3>
                  <p className="text-xs text-slate-400 leading-relaxed">{strategy.description}</p>
                </div>
              </div>
            )
          })}
        </div>
      </Panel>
    </div>
  )
}

function Row({ label, value }) {
  return (
    <div className="flex justify-between gap-3">
      <dt className="text-slate-500 shrink-0">{label}</dt>
      <dd className="font-semibold text-slate-200 text-right truncate">{value || '—'}</dd>
    </div>
  )
}
