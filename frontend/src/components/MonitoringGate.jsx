import React, { useEffect, useState } from 'react'
import { useMonitoring } from '../context/MonitoringContext'

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
    <div className="max-w-2xl mx-auto glass-panel rounded-3xl border border-slate-800 p-8 space-y-5">
      <div className="space-y-1">
        <span className="px-2.5 py-0.5 text-[10px] font-bold bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 rounded">
          Camera monitoring consent
        </span>
        <h2 className="text-2xl font-display font-extrabold text-white">Before your first lesson</h2>
      </div>

      <div className="space-y-3 text-sm text-slate-300 leading-relaxed">
        <p>
          Aegis uses your webcam during lessons and quizzes to estimate attention and adapt your learning.
          This is required for every learning session.
        </p>
        <ul className="list-disc pl-5 space-y-1 text-slate-400">
          <li>Video is analysed <strong className="text-slate-200">only on this computer</strong> by the Aegis camera agent. No images or video are recorded, stored or sent.</li>
          <li>Only numbers and yes/no signals are sent to Aegis: attention level, face present, yawning, looking away and <em>possible</em> drowsiness (eyes closed for a while).</li>
          <li>The camera agent may also notice when <strong className="text-slate-200">more than one face</strong> is visible. Only how many faces and when are recorded &mdash; never who.</li>
          <li>During <strong className="text-slate-200">protected quizzes</strong>, Aegis records when the quiz page is hidden (another tab, a minimised window) and for how long. It never records which tab, website or app you used. Leaving twice, or for more than 10 seconds, ends the quiz without grading.</li>
          <li>Only event times and numbers are stored. <strong className="text-slate-200">Raw webcam images and video are never stored or transmitted.</strong> You can see everything recorded about you on the Session Activity page.</li>
          <li>These signals are estimates for learning support. They are not a medical or sleep assessment.</li>
          <li>You can withdraw consent at any time; lessons then cannot start.</li>
        </ul>
        <p className="text-xs text-slate-500">
          This consent is separate from Windows camera permission. Windows may also ask whether desktop apps can use the camera.
        </p>
      </div>

      <div className="space-y-3 text-sm">
        <label className="flex gap-3 items-start text-slate-200">
          <input type="checkbox" className="mt-1" checked={understood} onChange={(e) => setUnderstood(e.target.checked)} />
          <span>I have read and understand how Aegis uses my webcam and monitors protected quizzes, and I agree.</span>
        </label>

        {minor && (
          <>
            <label className="flex gap-3 items-start text-slate-200">
              <input type="checkbox" className="mt-1" checked={guardian} onChange={(e) => setGuardian(e.target.checked)} />
              <span>My parent or guardian has authorised camera-based monitoring for my lessons, including multiple-face detection and tab-visibility checks during quizzes.</span>
            </label>
            <label className="flex gap-3 items-start text-slate-200">
              <input type="checkbox" className="mt-1" checked={school} onChange={(e) => setSchool(e.target.checked)} />
              <span>My school or teacher has approved using Aegis with camera monitoring and protected quizzes.</span>
            </label>
            <p className="text-xs text-amber-300/80">
              Because you are under 18, both confirmations are required. Schools should collect written
              parent/guardian consent before students use camera monitoring.
            </p>
          </>
        )}
      </div>

      {error && <p className="text-sm text-rose-400">{error}</p>}

      <button
        onClick={submit}
        disabled={!canSubmit || saving}
        className="px-6 py-3 rounded-xl bg-indigo-500 hover:bg-indigo-600 disabled:bg-slate-800 disabled:text-slate-500 text-white font-bold text-sm"
      >
        {saving ? 'Saving…' : 'Give consent and continue'}
      </button>
    </div>
  )
}

function StatusPanel({ hasVerifiedBefore }) {
  const { state, agent, backend, pairingError, retry } = useMonitoring()
  const [retrying, setRetrying] = useState(false)
  const steps = stepStatus(state)
  const [title, defaultHelp] = MESSAGES[state] || MESSAGES.loading

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
    <div className="glass-panel rounded-3xl border border-slate-800 p-6 space-y-4 max-w-lg w-full shadow-2xl bg-slate-950/90">
      {hasVerifiedBefore && (
        <p className="text-xs font-bold uppercase tracking-wider text-amber-300">
          Learning paused — your place and answers are saved
        </p>
      )}
      <h3 className="text-lg font-bold text-white">{title}</h3>
      {help && <p className="text-sm text-slate-400 leading-relaxed">{help}</p>}

      <ul className="space-y-2">
        {STEP_LABELS.map(([key, label]) => (
          <li key={key} className="flex items-center gap-3 text-sm">
            <span
              className={`h-5 w-5 rounded-full flex items-center justify-center text-[10px] font-bold ${
                steps[key] === 'done'
                  ? 'bg-emerald-500/20 text-emerald-300'
                  : steps[key] === 'current'
                    ? 'bg-amber-500/20 text-amber-300 animate-pulse'
                    : 'bg-slate-800 text-slate-500'
              }`}
            >
              {steps[key] === 'done' ? '✓' : steps[key] === 'current' ? '•' : ''}
            </span>
            <span className={steps[key] === 'pending' ? 'text-slate-500' : 'text-slate-200'}>{label}</span>
          </li>
        ))}
      </ul>

      {lightingLow && (
        <p className="text-xs text-amber-300">The room looks dark. More light helps face detection.</p>
      )}

      <button
        onClick={onRetry}
        disabled={retrying}
        className="px-5 py-2.5 rounded-xl bg-indigo-500 hover:bg-indigo-600 disabled:bg-slate-800 text-white font-semibold text-xs"
      >
        {retrying ? 'Retrying…' : 'Retry'}
      </button>
    </div>
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
    <div className="relative">
      {multipleFaces && (
        <div
          role="status"
          aria-live="polite"
          className="mb-4 rounded-2xl border border-amber-500/40 bg-amber-500/10 px-4 py-3 text-xs font-semibold text-amber-200"
        >
          👥 More than one face is visible to your camera. If you are studying alone, make sure only you are in view.
          This is noted in your session activity; it does not stop your lesson or quiz.
        </div>
      )}
      <div
        aria-hidden={!verified}
        inert={!verified}
        className={verified ? '' : 'pointer-events-none select-none blur-md opacity-40 transition'}
      >
        {children}
      </div>

      {!verified && (
        <div className="absolute inset-0 z-40 flex items-start justify-center pt-16 px-4">
          {startError ? (
            <div className="glass-panel rounded-3xl border border-rose-500/30 p-6 max-w-lg text-sm text-rose-300">
              {startError}
            </div>
          ) : (
            <StatusPanel hasVerifiedBefore={hasVerifiedBefore} />
          )}
        </div>
      )}
    </div>
  )
}
