/**
 * Quiz tab-switch reporting (browser side).
 *
 * The browser never decides anything here. It reports what it observed --
 * the quiz page became hidden, is still hidden after N ms, is visible again
 * after N ms -- and the server applies the two-strike rule and replies with
 * the attempt's state (warning, terminated, ...). Throttled or frozen
 * timers in a hidden tab therefore cannot extend the 10-second grace period:
 * the "hidden" report leaves the moment the page is hidden, and the
 * deadline is kept by the server.
 *
 * Absences are measured with both the monotonic clock (performance.now)
 * and the wall clock; the larger value is reported, so neither a sleeping
 * laptop (which can pause the monotonic clock) nor a clock change shortens
 * an absence.
 *
 * Reports that cannot be delivered (network problems) stay queued and are
 * retried; each carries how long it waited and how many sends failed, so
 * the server can tell a network delay from a late return.
 *
 * Window blur/focus and online/offline are reported as diagnostics only.
 *
 * Pure module: clocks, timers, storage and the transport are injected so
 * the logic is unit-tested in Node (tests/quizIntegrity.test.mjs).
 */

export const HIDDEN_TICK_MS = 2000
export const MAX_RETRY_MS = 5000
const AWAY_KEY_PREFIX = 'aegis.quizAway.'

const defaultTimers = {
  setTimeout: (fn, ms) => setTimeout(fn, ms),
  clearTimeout: (id) => clearTimeout(id),
  setInterval: (fn, ms) => setInterval(fn, ms),
  clearInterval: (id) => clearInterval(id),
}

/** Random id for one page load (letters and digits only). */
export function makePageId(random = Math.random) {
  let id = 'p'
  while (id.length < 24) id += Math.floor(random() * 36).toString(36)
  return id
}

export function createIntegrityTracker({
  attemptId,
  pageId,
  transport,
  clock = () => performance.now(),
  wallClock = () => Date.now(),
  timers = defaultTimers,
  storage = null,
  onView = () => {},
  onChecking = () => {},
  onConnection = () => {},
}) {
  const awayKey = `${AWAY_KEY_PREFIX}${attemptId}`
  let seq = 0
  let outbox = []
  let sending = false
  let retryTimer = null
  let retryDelay = 500
  let tickTimer = null
  let hiddenAt = null // { mono, wall } while the page is hidden
  let unloading = false
  let unloadingTimer = null
  let pendingReturnSeq = null // a return report not yet confirmed by the server
  let pageGone = false // pagehide fired: this page is being unloaded
  let disposed = false
  let ended = false

  const absenceMs = () => {
    if (!hiddenAt) return 0
    const mono = clock() - hiddenAt.mono
    const wall = wallClock() - hiddenAt.wall
    return Math.max(0, Math.round(Math.max(mono, wall)))
  }

  const store = {
    get() {
      try {
        return JSON.parse(storage?.getItem(awayKey) || 'null')
      } catch {
        return null
      }
    },
    set(value) {
      try {
        storage?.setItem(awayKey, JSON.stringify(value))
      } catch {
        // storage unavailable: a reload then cannot be measured (server stays safe)
      }
    },
    clear() {
      try {
        storage?.removeItem(awayKey)
      } catch {
        // ignore
      }
    },
  }

  function push(kind, extra = {}) {
    if (disposed) return null
    seq += 1
    const event = { seq, kind, client_ms: Math.round(clock()), ...extra, _created: clock(), _failures: 0 }
    outbox.push(event)
    return event
  }

  function scheduleRetry() {
    if (retryTimer || disposed) return
    retryTimer = timers.setTimeout(() => {
      retryTimer = null
      flush()
    }, retryDelay)
    retryDelay = Math.min(retryDelay * 2, MAX_RETRY_MS)
  }

  async function flush({ keepalive = false } = {}) {
    if (disposed || outbox.length === 0) return
    // One ordinary request at a time. A keepalive flush (page hiding or
    // unloading) never waits: it resends every unacknowledged event, so the
    // server -- which drops sequence numbers it has seen -- gets them in order
    // even if an earlier request is still in flight or is cancelled.
    if (sending && !keepalive) return
    const wasSending = sending
    sending = true
    const batch = outbox.slice(0, 50)
    const now = clock()
    const payload = batch.map(({ _created, _failures, ...event }) => ({
      ...event,
      delivery_failures: _failures,
      queued_ms: Math.max(0, Math.round(now - _created)),
    }))
    try {
      const view = await transport(payload, { keepalive })
      outbox = outbox.filter((event) => !batch.includes(event))
      retryDelay = 500
      onConnection('ok')
      if (pendingReturnSeq !== null && batch.some((event) => event.seq === pendingReturnSeq)) {
        pendingReturnSeq = null
        onChecking(false)
      }
      if (view) {
        if (['terminated', 'abandoned', 'submitted'].includes(view.status)) ended = true
        onView(view)
      }
    } catch (error) {
      const status = error?.status ?? null
      if (status && status >= 400 && status < 500 && status !== 408 && status !== 429) {
        // The server refused the batch (it will not accept it later either).
        outbox = outbox.filter((event) => !batch.includes(event))
        if (pendingReturnSeq !== null && batch.some((event) => event.seq === pendingReturnSeq)) {
          pendingReturnSeq = null
          onChecking(false)
        }
        onConnection('rejected')
      } else {
        batch.forEach((event) => {
          event._failures += 1
        })
        onConnection('offline')
        scheduleRetry()
      }
    } finally {
      // A keepalive flush that overlapped an ordinary one leaves it in charge.
      if (!wasSending) sending = false
    }
    if (!wasSending && outbox.length && !retryTimer && !disposed) flush()
  }

  function stopTicks() {
    if (tickTimer !== null) {
      timers.clearInterval(tickTimer)
      tickTimer = null
    }
  }

  const api = {
    /** Call once the attempt is known. */
    start({ serverStatus = 'in_progress', navigationType = 'navigate' } = {}) {
      const record = store.get()
      if (record && record.pageId !== pageId) {
        // The previous page of this attempt was hidden / closed / reloaded.
        store.clear()
        pendingReturnSeq = push('resume', {
          hidden_ms: Math.max(0, Math.round(wallClock() - record.wall)),
          reload: navigationType === 'reload',
        }).seq
        onChecking(true)
        flush()
      } else if (serverStatus === 'away' || serverStatus === 'unverified') {
        // The server knows of an absence we cannot measure (e.g. a new tab).
        pendingReturnSeq = push('resume').seq
        onChecking(true)
        flush()
      }
    },

    /** The page became hidden. */
    pageHidden() {
      if (hiddenAt || ended) return
      hiddenAt = { mono: clock(), wall: wallClock() }
      store.set({ wall: hiddenAt.wall, pageId })
      push(unloading ? 'pagehide' : 'hidden')
      flush({ keepalive: true })
      stopTicks()
      tickTimer = timers.setInterval(() => {
        if (!hiddenAt) return
        push('hidden_tick', { hidden_ms: absenceMs() })
        flush({ keepalive: true })
      }, HIDDEN_TICK_MS)
    },

    /** The page is visible again. */
    pageVisible() {
      // A page that is being unloaded never "comes back"; the next page
      // reports the return (and the measured gap) instead.
      if (pageGone) return
      stopTicks()
      if (!hiddenAt) return
      const hidden = absenceMs()
      hiddenAt = null
      store.clear()
      if (ended) return
      pendingReturnSeq = push('visible', { hidden_ms: hidden }).seq
      onChecking(true)
      flush()
    },

    /** beforeunload: the page is about to be reloaded or closed (maybe). */
    beforeUnload() {
      unloading = true
      if (unloadingTimer !== null) timers.clearTimeout(unloadingTimer)
      // If the page is still here a moment later, the unload was cancelled.
      unloadingTimer = timers.setTimeout(() => {
        unloading = false
        unloadingTimer = null
      }, 1000)
    },

    /** pagehide: the page is going away now. */
    pageHide() {
      pageGone = true
      if (ended) return
      if (!hiddenAt) {
        unloading = true
        api.pageHidden()
      } else {
        push('pagehide')
        flush({ keepalive: true })
      }
    },

    diagnostic(kind) {
      if (ended) return
      push(kind)
      if (kind === 'online') {
        retryDelay = 500
        if (retryTimer) {
          timers.clearTimeout(retryTimer)
          retryTimer = null
        }
      }
      flush()
    },

    flush,

    /** The attempt ended (submitted, terminated, abandoned): stop reporting. */
    end() {
      ended = true
      stopTicks()
      store.clear()
    },

    dispose() {
      disposed = true
      stopTicks()
      if (retryTimer) timers.clearTimeout(retryTimer)
      if (unloadingTimer !== null) timers.clearTimeout(unloadingTimer)
    },

    // For tests and diagnostics.
    get pending() {
      return outbox.length
    },
    get hidden() {
      return hiddenAt !== null
    },
  }
  return api
}
