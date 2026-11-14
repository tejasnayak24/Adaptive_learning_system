/**
 * Client for the local Aegis camera agent (facial_analysis/main.py).
 *
 * The agent listens only on http://127.0.0.1:8765. It accepts requests only
 * from the Aegis frontend origin and requires the X-Aegis-Client header, so
 * other websites cannot control it. The single-use pairing token is sent in
 * the POST body only -- never in a URL, never stored in localStorage.
 */
export const AGENT_URL = 'http://127.0.0.1:8765'

const CLIENT_HEADERS = {
  'Content-Type': 'application/json',
  'X-Aegis-Client': 'aegis-web',
}

async function request(path, { method = 'GET', body, timeoutMs = 2500 } = {}) {
  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), timeoutMs)

  try {
    const response = await fetch(`${AGENT_URL}${path}`, {
      method,
      headers: method === 'GET' ? undefined : CLIENT_HEADERS,
      body: body === undefined ? undefined : JSON.stringify(body),
      credentials: 'omit',
      cache: 'no-store',
      signal: controller.signal,
    })
    const data = await response.json().catch(() => ({}))
    return { ok: response.ok, status: response.status, data }
  } finally {
    clearTimeout(timer)
  }
}

export const agentClient = {
  /** Agent status, or null when the agent is not running / unreachable. */
  async getStatus() {
    try {
      const result = await request('/status', { timeoutMs: 1500 })
      return result.ok ? result.data : null
    } catch {
      return null
    }
  },

  /**
   * Hand a single-use pairing token to the agent so it can claim the session.
   * Resolves to { ok, error, message }.
   */
  async startSession(sessionId, pairingToken) {
    try {
      const result = await request('/session/start', {
        method: 'POST',
        body: { session_id: sessionId, pairing_token: pairingToken },
        timeoutMs: 8000,
      })
      return {
        ok: result.ok,
        error: result.data?.error || (result.ok ? null : `http_${result.status}`),
        message: result.data?.message || null,
      }
    } catch {
      return { ok: false, error: 'agent_unreachable', message: null }
    }
  },

  async stopSession(sessionId) {
    try {
      await request('/session/stop', { method: 'POST', body: { session_id: sessionId } })
    } catch {
      // Best effort: the backend also ends the session and revokes the agent.
    }
  },
}
