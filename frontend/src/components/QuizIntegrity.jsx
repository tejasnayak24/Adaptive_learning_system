import React, { useEffect, useState } from 'react'
import { ArrowLeft, Check, CirclePause, CloudOff, Hourglass, LoaderCircle, LogOut, OctagonX, RotateCcw, ShieldCheck, TriangleAlert } from 'lucide-react'
import { Button, Callout, Card, Modal, cx } from './ui'

/*
 * What the student sees of the quiz tab-switch rule. Wording is factual:
 * it describes what was measured, never "cheating".
 */

export const END_REASONS = {
  grace_expired: 'The quiz page was hidden for more than 10 seconds.',
  second_tab_switch: 'The quiz page was hidden or reloaded a second time after the warning.',
  left_quiz: 'You left the quiz for another page.',
  no_contact: 'The quiz received no activity for 30 minutes.',
  unverified_no_measurement:
    'We could not confirm when you came back to the quiz (for example, the tab was closed or the connection was lost). This is not recorded as a tab switch.',
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
      <Callout tone="warning" role="status">
        <span className="font-semibold text-warning">
          Warning given: you left this quiz once. If the quiz page is hidden or reloaded again, the quiz will end and will not be graded.
        </span>
      </Callout>
    )
  }
  return (
    <Callout tone="neutral" icon={ShieldCheck}>
      <span className="font-semibold text-ink">Protected quiz.</span> Stay on this page until you submit. If the quiz page is hidden (another tab,
      minimising the browser) or reloaded, you have 10 seconds to come back and you will get one warning. A second time ends the quiz without
      grading. Hints are still available.
    </Callout>
  )
}

export function StrikeWarningModal({ open, onClose }) {
  return (
    <Modal
      open={open}
      onClose={onClose}
      role="alertdialog"
      tone="warning"
      icon={TriangleAlert}
      title="You left the quiz"
      dismissible={false}
      description="The quiz page was hidden or reloaded. You came back in time, so your quiz continues and your answers are saved."
      footer={
        <Button variant="warning" onClick={onClose} autoFocus fullWidth>
          I understand, continue the quiz
        </Button>
      }
    >
      <p className="rounded-lg bg-warning/[0.08] px-3.5 py-3 text-sm font-semibold leading-relaxed text-warning ring-1 ring-inset ring-warning/25">
        If you switch tabs, reload or hide this page again, the quiz will end immediately and will not be graded.
      </p>
    </Modal>
  )
}

export function CheckingOverlay({ connection, status }) {
  const offline = connection === 'offline'
  const locked = status === 'unverified'
  return (
    <div
      className="absolute inset-0 z-20 flex items-center justify-center rounded-[inherit] bg-canvas/85 p-6 text-center backdrop-blur-sm"
      role="status"
      aria-live="polite"
    >
      <div className="max-w-sm space-y-3">
        <span className="mx-auto grid h-12 w-12 place-items-center rounded-2xl bg-raised text-brand-300 ring-1 ring-inset ring-line-strong">
          {offline ? <CloudOff size={22} aria-hidden="true" /> : <LoaderCircle size={22} className="animate-spin" aria-hidden="true" />}
        </span>
        <p className="font-display text-base font-semibold text-ink">{offline ? 'Reconnecting…' : 'Checking your quiz…'}</p>
        <p className="text-[13px] leading-relaxed text-ink-2">
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
  return (
    <Modal
      open={Boolean(pending)}
      onClose={onCancel}
      tone="neutral"
      icon={LogOut}
      title="Leave this quiz?"
      description="If you leave now, this attempt ends without grading. Your answers so far are saved, it is not recorded as a tab switch, and you can start the quiz again after 5 minutes."
      footer={
        <>
          <Button variant="secondary" onClick={onConfirm}>
            Leave quiz
          </Button>
          <Button onClick={onCancel} autoFocus>
            Stay on the quiz
          </Button>
        </>
      }
    />
  )
}

function RetakeButton({ secondsLeft, onRetake }) {
  return (
    <Button onClick={onRetake} disabled={secondsLeft > 0} icon={secondsLeft > 0 ? Hourglass : RotateCcw}>
      {secondsLeft > 0 ? `Retake available in ${formatClock(secondsLeft)}` : 'Start a new attempt'}
    </Button>
  )
}

function EndedLayout({ icon: Icon, tone, title, children, actions, role }) {
  const tones = {
    danger: 'bg-danger/[0.12] text-danger ring-danger/25',
    neutral: 'bg-white/[0.06] text-ink-2 ring-white/10',
    warning: 'bg-warning/[0.12] text-warning ring-warning/25',
  }
  return (
    <Card padding="lg" className="mx-auto max-w-xl space-y-6 text-center" role={role}>
      <span className={cx('mx-auto grid h-14 w-14 place-items-center rounded-2xl ring-1 ring-inset', tones[tone])}>
        <Icon size={26} aria-hidden="true" />
      </span>
      <div className="space-y-2.5">
        <h2 className="font-display text-xl font-semibold text-ink">{title}</h2>
        {children}
      </div>
      <div className="flex flex-wrap justify-center gap-3">{actions}</div>
    </Card>
  )
}

export function AttemptEndedPanel({ attempt, lessonId, onRetake }) {
  const secondsLeft = useCountdown(attempt?.retry_after_seconds)
  const terminated = attempt?.status === 'terminated'
  const answered = Object.keys(attempt?.answers || {}).length
  return (
    <EndedLayout
      role="alert"
      icon={terminated ? OctagonX : CirclePause}
      tone={terminated ? 'danger' : 'neutral'}
      title={terminated ? 'This quiz has ended' : 'This attempt was closed'}
      actions={
        <>
          <RetakeButton secondsLeft={secondsLeft} onRetake={onRetake} />
          {lessonId && (
            <Button to={`/lesson/${lessonId}`} variant="secondary" icon={ArrowLeft}>
              Back to the lesson
            </Button>
          )}
        </>
      }
    >
      <p className="text-sm leading-relaxed text-ink">{END_REASONS[attempt?.end_reason] || 'This attempt can no longer be continued.'}</p>
      <p className="text-[13px] leading-relaxed text-ink-2">
        Your {answered} saved answer{answered === 1 ? ' was' : 's were'} kept. This attempt was not graded and does not count towards your
        progress, averages or recommendations.
      </p>
    </EndedLayout>
  )
}

export function CooldownPanel({ retryAfterSeconds, lessonId, onRetake, endReason }) {
  const secondsLeft = useCountdown(retryAfterSeconds)
  return (
    <EndedLayout
      role="status"
      icon={Hourglass}
      tone="warning"
      title="Please wait before retaking this quiz"
      actions={
        <>
          <RetakeButton secondsLeft={secondsLeft} onRetake={onRetake} />
          {lessonId && (
            <Button to={`/lesson/${lessonId}`} variant="secondary" icon={ArrowLeft}>
              Back to the lesson
            </Button>
          )}
        </>
      }
    >
      <p className="text-sm leading-relaxed text-ink">
        Your previous attempt at this quiz ended without grading. A new attempt can start when the 5-minute wait is over.
      </p>
      {END_REASONS[endReason] && <p className="text-[13px] leading-relaxed text-ink-2">{END_REASONS[endReason]}</p>}
    </EndedLayout>
  )
}

export function SaveStatus({ state }) {
  const text = {
    saving: 'Saving answers…',
    saved: 'Answers saved',
    offline: 'Offline: answers kept on this device',
  }[state]
  if (!text) return null
  const Icon = state === 'offline' ? CloudOff : state === 'saving' ? LoaderCircle : Check
  return (
    <span
      className={cx('inline-flex items-center gap-1.5 text-xs font-medium', state === 'offline' ? 'text-warning' : 'text-ink-2')}
      aria-live="polite"
    >
      <Icon size={14} className={cx('shrink-0', state === 'saving' && 'animate-spin', state === 'saved' && 'text-success')} aria-hidden="true" />
      {text}
    </span>
  )
}
