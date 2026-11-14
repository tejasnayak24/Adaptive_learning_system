import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

/*
 * What the student sees of the quiz tab-switch rule. Wording is factual:
 * it describes what was measured, never "cheating".
 */

export const END_REASONS = {
  grace_expired: 'The quiz page was hidden for more than 10 seconds.',
  second_tab_switch: 'The quiz page was hidden a second time after the warning.',
  left_quiz: 'You left the quiz for another page.',
  no_contact: 'The quiz received no activity for 30 minutes.',
  unverified_no_measurement:
    'We could not confirm when you came back to the quiz (for example, the tab was closed or the connection was lost). This is not recorded as a tab switch.',
  reload_not_verified:
    'The quiz page took too long to come back after a reload, so the attempt could not be verified. This is not recorded as a tab switch.',
}

export function useCountdown(seconds) {
  const [left, setLeft] = useState(seconds ?? 0)
  useEffect(() => {
    setLeft(seconds ?? 0)
  }, [seconds])
  useEffect(() => {
    if (!left || left <= 0) return undefined
    const timer = setTimeout(() => setLeft((value) => Math.max(0, value - 1)), 1000)
    return () => clearTimeout(timer)
  }, [left])
  return left
}

export function formatClock(totalSeconds) {
  const s = Math.max(0, Math.round(totalSeconds || 0))
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`
}

export function IntegrityRulesBanner({ strikes }) {
  if (strikes >= 1) {
    return (
      <div role="status" className="rounded-2xl border border-amber-500/40 bg-amber-500/10 px-4 py-3 text-xs font-semibold text-amber-200">
        ⚠️ Warning given: you left this quiz once. If the quiz page is hidden again, the quiz will end and will not be graded.
      </div>
    )
  }
  return (
    <div className="rounded-2xl border border-slate-700/60 bg-slate-900/40 px-4 py-3 text-xs text-slate-300 leading-relaxed">
      <span className="font-bold text-slate-200">Protected quiz.</span> Stay on this page until you submit. If the quiz page is hidden (another tab, minimising the browser),
      you have 10 seconds to come back and you will get one warning. A second time ends the quiz without grading.
      Hints are still available.
    </div>
  )
}

export function StrikeWarningModal({ open, onClose }) {
  if (!open) return null
  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center bg-slate-950/80 backdrop-blur-sm p-4" role="alertdialog" aria-modal="true" aria-labelledby="strike-warning-title">
      <div className="max-w-md w-full rounded-3xl border border-amber-500/40 bg-slate-900 p-6 space-y-4 shadow-2xl">
        <h2 id="strike-warning-title" className="text-lg font-bold text-amber-300">You left the quiz</h2>
        <p className="text-sm text-slate-300 leading-relaxed">
          The quiz page was hidden. You came back in time, so your quiz continues and your answers are saved.
        </p>
        <p className="text-sm font-semibold text-amber-200 leading-relaxed">
          If you switch tabs or hide this page again, the quiz will end immediately and will not be graded.
        </p>
        <button
          autoFocus
          onClick={onClose}
          className="w-full px-4 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold text-sm"
        >
          I understand, continue the quiz
        </button>
      </div>
    </div>
  )
}

export function CheckingOverlay({ connection, status }) {
  const offline = connection === 'offline'
  const locked = status === 'unverified'
  return (
    <div className="absolute inset-0 z-20 flex items-center justify-center rounded-3xl bg-slate-950/85 backdrop-blur-sm p-6 text-center" role="status" aria-live="polite">
      <div className="space-y-2 max-w-sm">
        <div className="mx-auto h-8 w-8 animate-spin rounded-full border-4 border-indigo-500/20 border-t-indigo-500" />
        <p className="text-sm font-bold text-white">
          {offline ? 'Reconnecting…' : 'Checking your quiz…'}
        </p>
        <p className="text-xs text-slate-400 leading-relaxed">
          {offline
            ? 'The connection to Aegis was lost. Your answers are kept on this device and the quiz continues once the server confirms your return. A network problem is never counted as a tab switch.'
            : locked
              ? 'Your return to the quiz could not be confirmed yet. The quiz is locked until it is.'
              : 'Confirming your return to the quiz with the server.'}
        </p>
      </div>
    </div>
  )
}

export function LeaveQuizModal({ pending, onConfirm, onCancel }) {
  if (!pending) return null
  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center bg-slate-950/80 backdrop-blur-sm p-4" role="dialog" aria-modal="true" aria-labelledby="leave-quiz-title">
      <div className="max-w-md w-full rounded-3xl border border-slate-700 bg-slate-900 p-6 space-y-4 shadow-2xl">
        <h2 id="leave-quiz-title" className="text-lg font-bold text-white">Leave this quiz?</h2>
        <p className="text-sm text-slate-300 leading-relaxed">
          If you leave now, this attempt ends without grading. Your answers so far are saved, it is not recorded as a tab switch,
          and you can start the quiz again after 5 minutes.
        </p>
        <div className="flex gap-3">
          <button autoFocus onClick={onCancel} className="flex-1 px-4 py-2.5 rounded-xl bg-indigo-500 hover:bg-indigo-600 text-white font-bold text-sm">
            Stay on the quiz
          </button>
          <button onClick={onConfirm} className="flex-1 px-4 py-2.5 rounded-xl border border-slate-700 text-slate-300 hover:bg-slate-800 font-semibold text-sm">
            Leave quiz
          </button>
        </div>
      </div>
    </div>
  )
}

function RetakeButton({ secondsLeft, onRetake }) {
  return (
    <button
      onClick={onRetake}
      disabled={secondsLeft > 0}
      className="px-5 py-2.5 rounded-xl bg-indigo-500 hover:bg-indigo-600 text-white font-bold text-sm disabled:opacity-50 disabled:cursor-not-allowed"
    >
      {secondsLeft > 0 ? `Retake available in ${formatClock(secondsLeft)}` : 'Start a new attempt'}
    </button>
  )
}

export function AttemptEndedPanel({ attempt, lessonId, onRetake }) {
  const secondsLeft = useCountdown(attempt?.retry_after_seconds)
  const terminated = attempt?.status === 'terminated'
  const answered = Object.keys(attempt?.answers || {}).length
  return (
    <div className="max-w-xl mx-auto py-10 space-y-6 text-center" role="alert">
      <div className="text-5xl" aria-hidden="true">{terminated ? '⛔' : '⏸️'}</div>
      <h2 className="text-xl font-bold text-white">{terminated ? 'This quiz has ended' : 'This attempt was closed'}</h2>
      <p className="text-sm text-slate-300 leading-relaxed">{END_REASONS[attempt?.end_reason] || 'This attempt can no longer be continued.'}</p>
      <p className="text-xs text-slate-400 leading-relaxed">
        Your {answered} saved answer{answered === 1 ? ' was' : 's were'} kept. This attempt was not graded and does not count towards your
        progress, averages or recommendations.
      </p>
      <div className="flex flex-wrap justify-center gap-3">
        <RetakeButton secondsLeft={secondsLeft} onRetake={onRetake} />
        {lessonId && (
          <Link to={`/lesson/${lessonId}`} className="px-5 py-2.5 rounded-xl border border-slate-700 text-slate-300 hover:bg-slate-800 font-semibold text-sm">
            Back to the lesson
          </Link>
        )}
      </div>
    </div>
  )
}

export function CooldownPanel({ retryAfterSeconds, lessonId, onRetake }) {
  const secondsLeft = useCountdown(retryAfterSeconds)
  return (
    <div className="max-w-xl mx-auto py-10 space-y-6 text-center" role="status">
      <div className="text-5xl" aria-hidden="true">⏳</div>
      <h2 className="text-xl font-bold text-white">Please wait before retaking this quiz</h2>
      <p className="text-sm text-slate-300 leading-relaxed">
        Your previous attempt at this quiz ended without grading. A new attempt can start when the 5-minute wait is over.
      </p>
      <div className="flex flex-wrap justify-center gap-3">
        <RetakeButton secondsLeft={secondsLeft} onRetake={onRetake} />
        {lessonId && (
          <Link to={`/lesson/${lessonId}`} className="px-5 py-2.5 rounded-xl border border-slate-700 text-slate-300 hover:bg-slate-800 font-semibold text-sm">
            Back to the lesson
          </Link>
        )}
      </div>
    </div>
  )
}

export function SaveStatus({ state }) {
  const text = {
    saving: 'Saving answers…',
    saved: 'Answers saved',
    offline: 'Offline: answers kept on this device',
  }[state]
  if (!text) return null
  return (
    <span className={`text-[11px] font-semibold ${state === 'offline' ? 'text-amber-400' : 'text-slate-500'}`} aria-live="polite">
      {text}
    </span>
  )
}
