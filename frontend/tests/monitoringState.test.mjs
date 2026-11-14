// Run with: npm test   (node --test, no extra dependencies)
import test from 'node:test'
import assert from 'node:assert/strict'
import { combineState } from '../src/context/monitoringState.js'

const consent = { valid: true }
const agentRunning = (over = {}) => ({
  state: 'running',
  session_id: 'ms_1',
  camera: { state: 'ok' },
  backend: { connected: true },
  ...over,
})
const backendView = (state, over = {}) => ({ session_id: 'ms_1', state, verified: state === 'verified', ...over })

test('consent is required first', () => {
  assert.equal(combineState({ consent: { valid: false }, agent: agentRunning(), backend: backendView('verified') }), 'consent_required')
})

test('agent not running', () => {
  assert.equal(combineState({ consent, agent: null, backend: backendView('awaiting_agent') }), 'agent_not_running')
})

test('agent idle or on another session needs pairing', () => {
  assert.equal(combineState({ consent, agent: agentRunning({ state: 'idle', session_id: null }), backend: backendView('awaiting_agent') }), 'pairing')
  assert.equal(combineState({ consent, agent: agentRunning({ session_id: 'ms_other' }), backend: backendView('verified') }), 'pairing')
})

test('agent still opening the camera is not a camera failure', () => {
  assert.equal(combineState({ consent, agent: agentRunning({ state: 'starting' }), backend: backendView('camera_unavailable', { camera_error: 'starting' }) }), 'pairing')
})

test('camera unavailable', () => {
  assert.equal(combineState({ consent, agent: agentRunning({ state: 'camera_unavailable' }), backend: backendView('stale') }), 'camera_unavailable')
})

test('no face and verifying', () => {
  assert.equal(combineState({ consent, agent: agentRunning(), backend: backendView('no_face') }), 'no_face')
  assert.equal(combineState({ consent, agent: agentRunning(), backend: backendView('verifying') }), 'verifying')
})

test('face detected but backend disconnected', () => {
  assert.equal(combineState({ consent, agent: agentRunning({ backend: { connected: false } }), backend: backendView('verified') }), 'backend_disconnected')
  // Agent believes it is connected but the backend has no fresh heartbeat.
  assert.equal(combineState({ consent, agent: agentRunning(), backend: backendView('stale') }), 'backend_disconnected')
})

test('only the backend can verify', () => {
  assert.equal(combineState({ consent, agent: agentRunning(), backend: backendView('verified') }), 'verified')
  assert.equal(combineState({ consent, agent: agentRunning(), backend: null }), 'loading')
  assert.equal(combineState({ consent, agent: agentRunning(), backend: { ...backendView('verified'), verified: false } }), 'loading')
})

test('ended session and pairing errors', () => {
  assert.equal(combineState({ consent, agent: agentRunning(), backend: backendView('ended') }), 'ended')
  assert.equal(combineState({ consent, agent: agentRunning({ state: 'idle' }), backend: backendView('awaiting_agent'), pairingError: 'rejected' }), 'error')
})

test('camera open but first frame not analysed yet is warm-up, not a failure', () => {
  assert.equal(combineState({ consent, agent: agentRunning(), backend: backendView('camera_unavailable', { camera_error: null }) }), 'verifying')
  // Observed in the browser test: the backend still holds the "starting" heartbeat
  // while the agent already reports a running camera.
  assert.equal(combineState({ consent, agent: agentRunning(), backend: backendView('camera_unavailable', { camera_error: 'starting' }) }), 'verifying')
  // A real failure carries an error code and is still reported.
  assert.equal(
    combineState({ consent, agent: agentRunning(), backend: backendView('camera_unavailable', { camera_error: 'stale_measurement' }) }),
    'camera_unavailable'
  )
  assert.equal(
    combineState({ consent, agent: agentRunning({ camera: { state: 'error' } }), backend: backendView('camera_unavailable', { camera_error: null }) }),
    'camera_unavailable'
  )
})
