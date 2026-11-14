import React, { useEffect, useState } from 'react'
import { Camera, CameraOff, Circle, CircleCheck, CirclePause, LoaderCircle, RefreshCw, ScanFace, ShieldCheck, SunDim, Terminal, Users } from 'lucide-react'
import { useMonitoring } from '../context/MonitoringContext'
import { Badge, Button, Callout, Card, Checkbox, cx } from './ui'

/**
 * Wraps a learning page. Content is only usable while camera monitoring is
 * verified. While not verified the page stays mounted (so the lesson
 * position and quiz answers are preserved) but is blurred and inert, and a
 * status panel explains what is wrong and how to fix it.
 */

const STEP_LABELS = [
  ['agent', 'Aegis camera agent running'],
  ['camera', 'Webcam available'],
  ['face', 'Face detected and stable'],
  ['backend', 'Live data reaching Aegis'],
]

function stepStatus(state) {
  // Which checklist steps have passed for a combined state.
  const order = ['agent', 'camera', 'face', 'backend']
  const failedAt = {
    agent_not_running: 'agent',
    pairing: 'agent',
    error: 'agent',
    camera_unavailable: 'camera',
    no_face: 'face',
    verifying: 'face',
    backend_disconnected: 'backend',
    verified: null,
  }[state]
  const index = failedAt === null ? order.length : order.indexOf(failedAt)
  return Object.fromEntries(order.map((step, i) => [step, i < index ? 'done' : i === index ? 'current' : 'pending']))
}

const MESSAGES = {
  loading: ['Preparing camera monitoring…', 'Checking your consent and starting a monitored session.'],
  agent_not_running: [
    'Start the Aegis camera agent',
    'Open a terminal in the facial_analysis folder and run: .\\venv\\Scripts\\Activate.ps1 then python main.py. Aegis will connect to it automatically.',
  ],
  pairing: ['Connecting to the camera agent…', 'The agent is starting your webcam.'],
  camera_unavailable: ['Webcam unavailable', null],
  no_face: [
    'No face detected',
    'Sit in front of the webcam with your face clearly visible. Make sure the room is well lit.',
  ],
  verifying: ['Checking face detection…', 'Hold still for a moment while detection stabilises.'],
  backend_disconnected: [
    'Camera data is not reaching Aegis',
    'The camera agent cannot reach the Aegis server, or its data has stopped arriving. Check that the backend is running; Aegis reconnects automatically.',
  ],
  ended: ['Monitoring session ended', 'Press Retry to start a new monitored session.'],
  error: ['The camera agent could not start monitoring', null],
}

const STATE_ICON = {
  agent_not_running: Terminal,
  camera_unavailable: CameraOff,
  no_face: ScanFace,
  verifying: ScanFace,
  backend_disconnected: CameraOff,
  ended: CameraOff,
  error: CameraOff,
}

export function ConsentPanel() {
  const { consent, giveConsent } = useMonitoring()
  const [understood, setUnderstood] = useState(false)
  const [guardian, setGuardian] = useState(false)
  const [school, setSchool] = useState(false)
  const [error, setError] = useState('')
  const [saving, setSaving] = useState(false)

  const minor = consent?.is_minor
  const canSubmit = understood && (!minor || (guardian && school))

  const submit = async () => {
    setSaving(true)
    setError('')
    try {
      await giveConsent({ guardianConfirmed: guardian, schoolConfirmed: school })
    } catch (err) {
      setError(err.message || 'Could not save your consent')
    } finally {
      setSaving(false)
    }
  }

  return (
    <Card padding="lg" className="mx-auto max-w-2xl space-y-6">
      <div className="flex items-start gap-4">
        <span className="grid h-12 w-12 shrink-0 place-items-center rounded-2xl bg-brand-500/[0.12] text-brand-300 ring-1 ring-inset ring-brand-500/25">
          <ShieldCheck size={23} aria-hidden="true" />
        </span>
        <div className="space-y-1.5">
          <Badge tone="brand" size="sm">
            Camera monitoring consent
          </Badge>
          <h2 className="font-display text-2xl font-semibold tracking-tight text-ink">Before your first lesson</h2>
        </div>
      </div>

      <div className="space-y-4 text-sm leading-relaxed text-ink-2">
        <p className="text-ink">
          Aegis uses your webcam during lessons and quizzes to estimate attention and adapt your learning.
          This is required for every learning session.
        </p>
        <ul className="space-y-2.5 [&_strong]:font-semibold [&_strong]:text-ink">
          {[
            <>Video is analysed <strong>only on this computer</strong> by the Aegis camera agent. No images or video are recorded, stored or sent.</>,
            <>Only numbers and yes/no signals are sent to Aegis: attention level, face present, yawning, looking away and <em>possible</em> drowsiness (eyes closed for a while).</>,
            <>The camera agent may also notice when <strong>more than one face</strong> is visible. Only how many faces and when are recorded &mdash; never who.</>,
            <>During <strong>protected quizzes</strong>, Aegis records when the quiz page is hidden (another tab, a minimised window) and for how long. It never records which tab, website or app you used. Leaving twice, or for more than 10 seconds, ends the quiz without grading.</>,
            <>Only event times and numbers are stored. <strong>Raw webcam images and video are never stored or transmitted.</strong> You can see everything recorded about you on the Session Activity page.</>,
            <>These signals are estimates for learning support. They are not a medical or sleep assessment.</>,
            <>You can withdraw consent at any time; lessons then cannot start.</>,
          ].map((item, index) => (
            <li key={index} className="flex gap-3">
              <span className="mt-[7px] h-1.5 w-1.5 shrink-0 rounded-full bg-brand-400" aria-hidden="true" />
              <span>{item}</span>
            </li>
          ))}
        </ul>
        <p className="text-xs">
          This consent is separate from Windows camera permission. Windows may also ask whether desktop apps can use the camera.
        </p>
      </div>

      <div className="space-y-2.5">
        <Checkbox checked={understood} onChange={(e) => setUnderstood(e.target.checked)}>
          I have read and understand how Aegis uses my webcam and monitors protected quizzes, and I agree.
        </Checkbox>

        {minor && (
          <>
            <Checkbox checked={guardian} onChange={(e) => setGuardian(e.target.checked)}>
              My parent or guardian has authorised camera-based monitoring for my lessons, including multiple-face detection and tab-visibility checks during quizzes.
            </Checkbox>
            <Checkbox checked={school} onChange={(e) => setSchool(e.target.checked)}>
              My school or teacher has approved using Aegis with camera monitoring and protected quizzes.
            </Checkbox>
            <Callout tone="warning">
              Because you are under 18, both confirmations are required. Schools should collect written
              parent/guardian consent before students use camera monitoring.
            </Callout>
          </>
        )}
      </div>

      {error && (
        <Callout tone="danger" role="alert">
          {error}
        </Callout>
      )}

      <Button onClick={submit} disabled={!canSubmit || saving} loading={saving} size="lg" icon={saving ? undefined : ShieldCheck}>
        {saving ? 'Saving…' : 'Give consent and continue'}
      </Button>
    </Card>
  )
}

function StepIcon({ status }) {
  if (status === 'done') return <CircleCheck size={18} className="shrink-0 text-success" aria-hidden="true" />
  if (status === 'current') return <LoaderCircle size={18} className="shrink-0 animate-spin text-warning" aria-hidden="true" />
  return <Circle size={18} className="shrink-0 text-ink-3" aria-hidden="true" />
}

function StatusPanel({ hasVerifiedBefore }) {
  const { state, agent, backend, pairingError, retry } = useMonitoring()
  const [retrying, setRetrying] = useState(false)
  const steps = stepStatus(state)
  const [title, defaultHelp] = MESSAGES[state] || MESSAGES.loading
  const Icon = STATE_ICON[state] || Camera

  let help = defaultHelp
  if (state === 'camera_unavailable') {
    help =
      agent?.camera?.message ||
      'The webcam could not be used. Close other apps that may be using it (Teams, Zoom, Camera), check Windows Settings > Privacy & security > Camera, then press Retry.'
  }
  if (state === 'error') help = pairingError

  const lightingLow = agent?.lighting?.ok === false || backend?.lighting_ok === false

  const onRetry = async () => {
    setRetrying(true)
    try {
      await retry()
    } finally {
      setRetrying(false)
    }
  }

  return (
    <Card padding="lg" className="w-full max-w-lg space-y-5 bg-raised shadow-raised" role="status" aria-live="polite">
      {hasVerifiedBefore && (
        <Badge tone="warning" icon={CirclePause}>
          Learning paused — your place and answers are saved
        </Badge>
      )}
      <div className="flex items-start gap-4">
        <span className="grid h-11 w-11 shrink-0 place-items-center rounded-xl bg-white/[0.06] text-ink-2 ring-1 ring-inset ring-white/10">
          <Icon size={21} aria-hidden="true" />
        </span>
        <div className="min-w-0 space-y-1.5">
          <h3 className="font-display text-lg font-semibold leading-snug text-ink">{title}</h3>
          {help && <p className="text-sm leading-relaxed text-ink-2">{help}</p>}
        </div>
      </div>

      {state === 'agent_not_running' && (
        <pre className="overflow-x-auto rounded-lg border border-line bg-canvas px-4 py-3 font-mono text-[12.5px] leading-relaxed text-ink">
          <code>{'cd facial_analysis\n.\\venv\\Scripts\\Activate.ps1\npython main.py'}</code>
        </pre>
      )}

      <ul className="space-y-2.5 rounded-xl border border-line bg-deep/70 p-4">
        {STEP_LABELS.map(([key, label]) => (
          <li key={key} className="flex items-center gap-3 text-sm">
            <StepIcon status={steps[key]} />
            <span className={steps[key] === 'pending' ? 'text-ink-3' : 'text-ink'}>{label}</span>
          </li>
        ))}
      </ul>

      {lightingLow && (
        <Callout tone="warning" icon={SunDim}>
          The room looks dark. More light helps face detection.
        </Callout>
      )}

      <Button onClick={onRetry} disabled={retrying} loading={retrying} icon={retrying ? undefined : RefreshCw}>
        {retrying ? 'Retrying…' : 'Retry'}
      </Button>
    </Card>
  )
}

export default function MonitoringGate({ lessonId = null, children }) {
  const monitoring = useMonitoring()
  const { state, verified, register, ensureSession } = monitoring
  const [hasVerifiedBefore, setHasVerifiedBefore] = useState(false)
  const [startError, setStartError] = useState('')

  useEffect(() => register(), [register])

  useEffect(() => {
    ensureSession(lessonId).catch((err) => setStartError(err.message || 'Could not start camera monitoring'))
    // Re-run when consent becomes valid.
  }, [ensureSession, lessonId, monitoring.consent?.valid])

  useEffect(() => {
    if (verified) setHasVerifiedBefore(true)
  }, [verified])

  if (state === 'consent_required') {
    return <ConsentPanel />
  }

  // Sustained multiple-face signal from the camera agent: an informational
  // banner while it lasts (no popup, no lock, nothing recorded as misconduct).
  const multipleFaces = verified && monitoring.backend?.multiple_faces === true

  return (
    <div className={cx('relative', !verified && 'min-h-[560px]')}>
      {multipleFaces && (
        <Callout tone="warning" icon={Users} role="status" aria-live="polite" className="mb-5">
          <span className="font-medium text-ink">
            More than one face is visible to your camera. If you are studying alone, make sure only you are in view.
            This is noted in your session activity; it does not stop your lesson or quiz.
          </span>
        </Callout>
      )}
      <div
        aria-hidden={!verified}
        inert={!verified}
        className={verified ? '' : 'pointer-events-none select-none opacity-40 blur-md transition'}
      >
        {children}
      </div>

      {!verified && (
        <div className="absolute inset-0 z-10 flex items-start justify-center px-1 pt-8 sm:px-4 sm:pt-14">
          {startError ? (
            <Callout tone="danger" role="alert" className="max-w-lg">
              {startError}
            </Callout>
          ) : (
            <StatusPanel hasVerifiedBefore={hasVerifiedBefore} />
          )}
        </div>
      )}
    </div>
  )
}
