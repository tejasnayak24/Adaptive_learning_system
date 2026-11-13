import React, { useEffect, useState } from 'react'
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

export default function Recommendations() {
  const { user } = useAuth()
  const [loading, setLoading] = useState(true)
  const [recommendation, setRecommendation] = useState(null)
  const [error, setError] = useState('')
  const [unavailableNote, setUnavailableNote] = useState('')
  const [lessons, setLessons] = useState([])
  const [currentLesson, setCurrentLesson] = useState(null)

  useEffect(() => {
    async function loadRecommendation() {
      try {
        // Recommendations are generated and stored by the server when a
        // quiz is graded, from the attempt's real data.
        const latest = await rlService.getLatest()
        const attempt = latest.attempt

        if (latest.status === 'available' && latest.recommendation?.action) {
          setRecommendation({
            ...latest.recommendation,
            lessonId: attempt?.lesson_id,
            quizId: attempt?.quiz_id,
            lessonTitle: attempt?.lesson_title,
            topicName: attempt?.topic,
            lastScore: Math.round(attempt?.quiz_score ?? 0),
            lastDifficulty: attempt?.difficulty
          })
        } else if (latest.status === 'telemetry_unavailable') {
          setUnavailableNote(
            'Your latest quiz had no camera telemetry, so the coach could not generate an adaptive recommendation. Keep the camera agent running during your next quiz.'
          )
        } else if (latest.status === 'not_generated') {
          setUnavailableNote('The coach could not generate a recommendation for your latest attempt.')
        }
        try {
          if (attempt?.lesson_id) {
            // Lesson detail carries its quizzes and its place in the
            // student's grade/subject sequence (navigation).
            const lessonRes = await lessonService.getLesson(attempt.lesson_id)
            if (lessonRes?.success) setCurrentLesson(lessonRes.data)
          } else {
            const lessonRes = await lessonService.getLessons()
            if (lessonRes?.success) setLessons(lessonRes.data || [])
          }
        } catch {
          // The lesson only refines the next-step link.
        }
      } catch (err) {
        setError(err.message || 'Failed to load your recommendation')
      } finally {
        setLoading(false)
      }
    }
    loadRecommendation()
  }, [user?.id])

  if (loading) {
    return (
      <div className="space-y-6 animate-pulse">
        <div className="h-10 w-1/4 bg-slate-800 rounded-xl"></div>
        <div className="h-4 w-1/2 bg-slate-800 rounded-lg"></div>
        <div className="h-64 bg-slate-800 rounded-3xl mt-8"></div>
      </div>
    )
  }

  const rlStrategies = ALL_ACTIONS.map((name) => ({ name, ...ACTION_CATALOGUE[name] }))

  const nextStep = recommendation
    ? resolveNextStep(recommendation.action, {
        lessonId: recommendation.lessonId,
        quizId: recommendation.quizId,
        difficulty: recommendation.lastDifficulty,
        lessonQuizzes: currentLesson?.quizzes,
        navigation: currentLesson?.navigation,
        lessons
      })
    : null
  const nextStepLink =
    nextStep && (nextStep.kind === 'navigate' || nextStep.kind === 'retry')
      ? { to: nextStep.to, state: { ...(nextStep.state || {}), mode: nextStep.mode, attempt: nextStep.kind === 'retry' ? Date.now() : undefined } }
      : recommendation
        ? { to: `/lesson/${recommendation.lessonId}`, state: { recommendedAction: recommendation.action } }
        : null

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div className="space-y-1.5">
        <h1 className="font-display text-3xl font-extrabold tracking-tight text-white md:text-4xl">
          AI Pedagogy Coach
        </h1>
        <p className="text-slate-400 text-sm leading-relaxed max-w-2xl">
          Your reinforcement-learning coach. After each quiz, Aegis combines your score, difficulty, hints, attempts and camera engagement signals to recommend a next step.
        </p>
      </div>

      {error && (
        <div className="rounded-2xl bg-rose-500/10 border border-rose-500/20 p-4 text-sm text-rose-400">
          {error}
        </div>
      )}

      {/* Active Coach Suggestion */}
      {!recommendation ? (
        <div className="glass-panel rounded-3xl p-8 border border-slate-900 shadow-md text-center py-12 space-y-4">
          <div className="text-5xl">🤖</div>
          <h3 className="text-lg font-bold text-white">
            {unavailableNote ? 'Camera Data Unavailable' : 'AI Coach is Calibrating'}
          </h3>
          <p className="text-xs text-slate-400 max-w-sm mx-auto leading-relaxed">
            {unavailableNote ||
              'The coach needs at least one quiz log to evaluate your study habits and output recommendations. Jump into subjects to begin.'}
          </p>
          <Link to="/subjects" className="inline-flex px-5 py-2.5 rounded-xl bg-indigo-500 hover:bg-indigo-600 text-white font-semibold text-xs shadow-md transition-all">
            Browse Subjects
          </Link>
        </div>
      ) : (
        <div className="glass-panel rounded-3xl p-8 border border-slate-900 shadow-xl space-y-6 relative overflow-hidden">
          <div className="absolute top-0 right-0 h-48 w-48 bg-indigo-500/5 blur-3xl pointer-events-none"></div>

          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-800 pb-5">
            <div className="space-y-1.5">
              <span className="px-2.5 py-0.5 text-[9px] font-bold bg-teal-500/10 text-teal-400 border border-teal-500/20 rounded">
                Active Pedagogy Advice
              </span>
              <h2 className="text-xl font-bold text-white">Curriculum Recommendation</h2>
            </div>
            
            <div
              className="shrink-0 flex items-center gap-2 bg-slate-900 border border-slate-800 rounded-xl px-3 py-1.5"
              title={CONFIDENCE_NOTE}
            >
              <span className="text-[9px] text-slate-500 font-extrabold uppercase">Decision strength</span>
              <span className="text-teal-400 font-extrabold text-sm">{Math.round(recommendation.confidence * 100)}%</span>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="md:col-span-2 space-y-6">
              {/* Action Banner */}
              <div className="space-y-1">
                <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Coach Action Suggestion</span>
                <p className="text-2xl font-extrabold text-white">
                  {actionInfo(recommendation.action).icon} {actionInfo(recommendation.action).label}
                </p>
                <p className="text-xs text-slate-400">{actionInfo(recommendation.action).description}</p>
                {recommendation.policy && (
                  <p className="text-[10px] text-slate-500">
                    Decided by: {POLICY_LABELS[recommendation.policy] || recommendation.policy}
                  </p>
                )}
              </div>

              {/* Justification */}
              <div className="space-y-2">
                <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">AI tutor Justification</span>
                <p className="text-sm text-slate-300 italic bg-slate-900/30 border border-slate-850 p-4 rounded-2xl leading-relaxed">
                  "{recommendation.explanation}"
                </p>
              </div>
            </div>

            {/* Performance Snapshot */}
            <div className="space-y-4 rounded-2xl bg-slate-925 border border-slate-850 p-5 h-fit">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">Trigger State Log</h4>
              <div className="space-y-3 text-xs">
                <div className="flex justify-between">
                  <span className="text-slate-500">Lesson context</span>
                  <span className="font-semibold text-slate-300 truncate max-w-[120px]">{recommendation.lessonTitle}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Last score</span>
                  <span className="font-bold text-white">{recommendation.lastScore}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Last difficulty</span>
                  <span className="font-semibold text-slate-300">{recommendation.lastDifficulty}</span>
                </div>
              </div>
              
              <div className="pt-2">
                {nextStepLink && (
                  <Link
                    to={nextStepLink.to}
                    state={nextStepLink.state}
                    className="w-full inline-flex justify-center py-2.5 rounded-xl bg-indigo-500 text-white font-bold text-[11px] shadow hover:bg-indigo-650 transition-colors"
                  >
                    {nextStep && nextStep.kind !== 'unknown' && nextStep.kind !== 'review' && nextStep.kind !== 'break'
                      ? nextStep.label
                      : `${actionInfo(recommendation.action).label}: open the lesson →`}
                  </Link>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Guide to RL Coach Strategy */}
      <div className="glass-panel rounded-3xl p-6 md:p-8 border border-slate-900 shadow-lg space-y-6">
        <div>
          <h3 className="text-lg font-bold text-white">How the Coach Adapts</h3>
          <p className="text-xs text-slate-500 mt-1">
            A tabular Q-learning policy, trained offline on simulated students, scores all 11 actions for your
            current situation. Safety rules first remove unsuitable actions (for example, moving on before
            passing); the action with the highest learned value is recommended.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {rlStrategies.map((strategy) => (
            <div key={strategy.name} className="flex gap-4 p-4 bg-slate-900/30 border border-slate-850 rounded-2xl">
              <span className="text-2xl select-none">{strategy.icon}</span>
              <div className="space-y-1">
                <h4 className="text-xs font-extrabold text-white tracking-wide">{strategy.name.replace(/_/g, ' ')}</h4>
                <p className="text-xs text-slate-400 leading-relaxed">{strategy.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
