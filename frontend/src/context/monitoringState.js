/**
 * Combine the local agent's status and the backend's session status into
 * one monitoring state. Only the backend can make the state "verified":
 * the agent's own report is never trusted on its own.
 */
export function combineState({ consent, agent, backend, pairingError }) {
  if (consent && !consent.valid) return 'consent_required'
  if (backend?.state === 'ended') return 'ended'
  if (!agent) return 'agent_not_running'
  if (pairingError) return 'error'
  if (agent.state === 'idle' || !agent.session_id || (backend && agent.session_id !== backend.session_id)) {
    return 'pairing'
  }
  // While the agent is still opening the webcam, its "not ready yet"
  // heartbeat must not be shown as a camera failure.
  if (agent.state === 'starting') return 'pairing'
  if (agent.state === 'camera_unavailable' || backend?.state === 'camera_unavailable') return 'camera_unavailable'
  if (agent.backend && agent.backend.connected === false) return 'backend_disconnected'
  if (!backend) return 'loading'
  if (backend.state === 'awaiting_agent') return 'pairing'
  if (backend.state === 'stale') return 'backend_disconnected'
  if (backend.state === 'no_face') return 'no_face'
  if (backend.state === 'verifying') return 'verifying'
  if (backend.state === 'verified' && backend.verified) return 'verified'
  return 'loading'
}
