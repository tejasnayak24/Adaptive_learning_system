import React, { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from 'react'
import { useAuth } from './AuthContext'
import { agentClient } from '../services/agentClient'
import { monitoringService } from '../services/monitoringService'
import { combineState } from './monitoringState.js'

/**
 * Camera monitoring for learning sessions.
 *
 * Combined states (``state``):
 *   loading            - checking consent / creating the session
 *   consent_required   - the student has not given (current) consent
 *   agent_not_running  - nothing answers on http://127.0.0.1:8765
 *   pairing            - handing the session to the agent
 *   camera_unavailable - agent running but the webcam cannot be used
 *   no_face            - camera works, no face visible
 *   verifying          - face seen, waiting for stable detection
 *   backend_disconnected - the agent cannot reach the backend, or the
 *                        backend has no fresh heartbeat (stale)
 *   verified           - fresh heartbeats with a stable face (backend says so)
 *   ended / error
 *
 * Only the backend's view can make the state "verified": the browser never
 * trusts the agent's word alone. Pairing tokens live only in local
 * variables; only the (non-secret) session id is kept in sessionStorage so
 * a page reload can reconnect without logging in again.
 */

const MonitoringContext = createContext(null)

const POLL_MS = 1500
const REPAIR_THROTTLE_MS = 4000
const END_AFTER_IDLE_MS = 5000
const SESSION_KEY = 'aegis.monitoring.session'

function readStoredSession(userId) {
  try {
    const raw = sessionStorage.getItem(SESSION_KEY)
    if (!raw) return null
    const parsed = JSON.parse(raw)
    return parsed?.userId === userId ? parsed.sessionId : null
  } catch {
    return null
  }
}

function storeSession(userId, sessionId) {
  try {
    if (sessionId) sessionStorage.setItem(SESSION_KEY, JSON.stringify({ userId, sessionId }))
    else sessionStorage.removeItem(SESSION_KEY)
  } catch {
    // sessionStorage unavailable: reconnection after reload is then manual.
  }
}

export function MonitoringProvider({ children }) {
  const { user } = useAuth()
  const userId = user?.id ?? null

  const [consent, setConsent] = useState(null)
  const [sessionId, setSessionId] = useState(null)
  const [agent, setAgent] = useState(null)
  const [backend, setBackend] = useState(null)
  const [pairingError, setPairingError] = useState(null)
  const [activeUsers, setActiveUsers] = useState(0)

  const sessionRef = useRef(null)
  const lastRepairRef = useRef(0)
  const busyRef = useRef(false)
  const ensureInFlight = useRef(null)

  const setSession = useCallback(
    (id) => {
      sessionRef.current = id
      setSessionId(id)
      storeSession(userId, id)
    },
    [userId]
  )

  const loadConsent = useCallback(async () => {
    const view = await monitoringService.getConsent()
    setConsent(view)
    return view
  }, [])

  /** Hand a fresh single-use pairing token to the agent. */
  const pairAgent = useCallback(async (id, token) => {
    const result = await agentClient.startSession(id, token)
    if (result.ok) {
      setPairingError(null)
      return true
    }
    if (result.error === 'agent_unreachable') {
      setPairingError(null) // shown as "agent not running"
    } else {
      setPairingError(result.message || 'The camera agent could not start monitoring.')
    }
    return false
  }, [])

  const repair = useCallback(async () => {
    const id = sessionRef.current
    if (!id || busyRef.current) return
    busyRef.current = true
    lastRepairRef.current = Date.now()
    try {
      const data = await monitoringService.reissuePairing(id)
      await pairAgent(id, data.pairing_token)
    } catch {
      // Session ended or backend unreachable: the next poll shows it.
    } finally {
      busyRef.current = false
    }
  }, [pairAgent])

  const startNewSession = useCallback(
    async (lessonId) => {
      busyRef.current = true
      try {
        const data = await monitoringService.createSession(lessonId)
        setSession(data.session_id)
        setBackend(null)
        lastRepairRef.current = Date.now()
        await pairAgent(data.session_id, data.pairing_token)
      } finally {
        busyRef.current = false
      }
    },
    [pairAgent, setSession]
  )

  const ensureSessionOnce = useCallback(
    async (lessonId) => {
      if (!userId) return
      const view = await loadConsent()
      if (!view.valid) return

      const existing = sessionRef.current || readStoredSession(userId)
      if (existing) {
        try {
          const status = await monitoringService.getStatus(existing)
          if (status.state !== 'ended') {
            sessionRef.current = existing
            setSessionId(existing)
            setBackend(status)
            return
          }
        } catch {
          // Unknown / foreign session: start a new one.
        }
      }
      await startNewSession(lessonId)
    },
    [loadConsent, startNewSession, userId]
  )

  /**
   * Called by learning pages: make sure a monitored session exists.
   * Concurrent calls (e.g. React StrictMode running effects twice) share
   * one in-flight request, so only one session is ever created.
   */
  const ensureSession = useCallback(
    (lessonId) => {
      if (!ensureInFlight.current) {
        ensureInFlight.current = ensureSessionOnce(lessonId).finally(() => {
          ensureInFlight.current = null
        })
      }
      return ensureInFlight.current
    },
    [ensureSessionOnce]
  )

  const endSession = useCallback(async () => {
    const id = sessionRef.current
    if (!id) return
    setSession(null)
    setBackend(null)
    setAgent(null)
    await Promise.allSettled([agentClient.stopSession(id), monitoringService.endSession(id)])
  }, [setSession])

  /** Retry button: reconnect (or restart if the session ended). */
  const retry = useCallback(async () => {
    setPairingError(null)
    if (backend?.state === 'ended' || !sessionRef.current) {
      setSession(null)
      await startNewSession(null)
    } else {
      await repair()
    }
  }, [backend, repair, setSession, startNewSession])

  const giveConsent = useCallback(
    async (options) => {
      const view = await monitoringService.giveConsent(options)
      setConsent(view)
      return view
    },
    []
  )

  // Poll the agent and the backend while a learning page is open.
  useEffect(() => {
    if (!activeUsers || !sessionId) return undefined
    let cancelled = false

    async function poll() {
      const [agentStatus, backendStatus] = await Promise.all([
        agentClient.getStatus(),
        monitoringService.getStatus(sessionId).catch(() => null),
      ])
      if (cancelled) return
      setAgent(agentStatus)
      if (backendStatus) setBackend(backendStatus)

      // The agent restarted or lost the session: re-pair automatically.
      const agentLost =
        agentStatus &&
        (agentStatus.state === 'idle' || agentStatus.session_id !== sessionId) &&
        backendStatus &&
        backendStatus.state !== 'ended'
      if (agentLost && Date.now() - lastRepairRef.current > REPAIR_THROTTLE_MS) {
        repair()
      }
    }

    poll()
    const timer = setInterval(poll, POLL_MS)
    return () => {
      cancelled = true
      clearInterval(timer)
    }
  }, [activeUsers, sessionId, repair])

  // End the monitored session shortly after the last learning page closes
  // (the delay lets the student move from a lesson to its quiz).
  useEffect(() => {
    if (activeUsers > 0 || !sessionRef.current) return undefined
    const timer = setTimeout(() => {
      endSession()
    }, END_AFTER_IDLE_MS)
    return () => clearTimeout(timer)
  }, [activeUsers, endSession])

  // Logging out ends monitoring.
  useEffect(() => {
    if (!userId && sessionRef.current) endSession()
  }, [userId, endSession])

  const register = useCallback(() => {
    setActiveUsers((n) => n + 1)
    return () => setActiveUsers((n) => Math.max(0, n - 1))
  }, [])

  const state = combineState({ consent, agent, backend, pairingError })

  const value = useMemo(
    () => ({
      state,
      verified: state === 'verified',
      consent,
      sessionId,
      agent,
      backend,
      pairingError,
      ensureSession,
      retry,
      endSession,
      giveConsent,
      register,
    }),
    [state, consent, sessionId, agent, backend, pairingError, ensureSession, retry, endSession, giveConsent, register]
  )

  return <MonitoringContext.Provider value={value}>{children}</MonitoringContext.Provider>
}

export function useMonitoring() {
  const context = useContext(MonitoringContext)
  if (!context) throw new Error('useMonitoring must be used within a MonitoringProvider')
  return context
}
