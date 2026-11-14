import { useEffect, useRef, useState } from 'react'
import { createIntegrityTracker, makePageId } from '../services/quizIntegrity'
import { quizService } from '../services/quizService'

/*
 * React wiring for the quiz tab-switch rule.
 *
 * useQuizIntegrity reports page visibility (and, for diagnostics only,
 * window focus and network changes) for an open, protected attempt. The
 * server decides; the hook passes its decisions to ``onView``.
 *
 * useLeaveGuard asks for confirmation before leaving the quiz for another
 * Aegis page (links and the browser's Back button). A confirmed departure
 * abandons the attempt -- not a violation.
 */

// One tracker per attempt per page load. React StrictMode mounts effects
// twice in development; sharing the tracker keeps sequence numbers and the
// page id stable, so nothing is reported twice.
const registry = new Map()

function navigationType() {
  try {
    return performance.getEntriesByType('navigation')[0]?.type || 'navigate'
  } catch {
    return 'navigate'
  }
}

function acquireTracker(attemptId, initialStatus, handlers) {
  let entry = registry.get(attemptId)
  if (entry) {
    if (entry.releaseTimer) clearTimeout(entry.releaseTimer)
    entry.releaseTimer = null
    entry.handlers = handlers
    entry.refs += 1
    return entry
  }
  entry = { refs: 1, releaseTimer: null, handlers }
  const pageId = makePageId()
  entry.tracker = createIntegrityTracker({
    attemptId,
    pageId,
    transport: (events, { keepalive }) => quizService.sendAttemptEvents(attemptId, pageId, events, { keepalive }),
    storage: typeof sessionStorage === 'undefined' ? null : sessionStorage,
    onView: (view) => entry.handlers.onView(view),
    onChecking: (value) => entry.handlers.onChecking(value),
    onConnection: (value) => entry.handlers.onConnection(value),
  })
  registry.set(attemptId, entry)
  entry.tracker.start({ serverStatus: initialStatus, navigationType: navigationType() })
  return entry
}

function releaseTracker(attemptId, onReleased) {
  const entry = registry.get(attemptId)
  if (!entry) return
  entry.refs -= 1
  if (entry.refs > 0) return
  // Wait a moment: a StrictMode remount re-acquires the same tracker.
  entry.releaseTimer = setTimeout(() => {
    registry.delete(attemptId)
    entry.tracker.dispose()
    onReleased?.()
  }, 300)
}

export function useQuizIntegrity({ attemptId, active, initialStatus, onView, onUnmountOpen }) {
  const [checking, setChecking] = useState(false)
  const [connection, setConnection] = useState('ok')
  const latest = useRef({ onView, onUnmountOpen, active })
  useEffect(() => {
    latest.current = { onView, onUnmountOpen, active }
  })

  useEffect(() => {
    if (!attemptId || !active) return undefined

    const entry = acquireTracker(attemptId, initialStatus, {
      onView: (view) => latest.current.onView?.(view),
      onChecking: setChecking,
      onConnection: setConnection,
    })
    const tracker = entry.tracker

    if (typeof document !== 'undefined' && document.visibilityState === 'hidden') {
      tracker.pageHidden()
    }

    const onVisibility = () => {
      if (document.visibilityState === 'hidden') tracker.pageHidden()
      else tracker.pageVisible()
    }
    const onBlur = () => tracker.diagnostic('blur')
    const onFocus = () => tracker.diagnostic('focus')
    const onOnline = () => tracker.diagnostic('online')
    const onOffline = () => tracker.diagnostic('offline')
    const onPageHide = () => tracker.pageHide()
    const onBeforeUnload = (event) => {
      tracker.beforeUnload()
      // Ask before a reload or close (the browser shows its own wording).
      event.preventDefault()
      event.returnValue = ''
    }

    document.addEventListener('visibilitychange', onVisibility)
    window.addEventListener('blur', onBlur)
    window.addEventListener('focus', onFocus)
    window.addEventListener('online', onOnline)
    window.addEventListener('offline', onOffline)
    window.addEventListener('pagehide', onPageHide)
    window.addEventListener('beforeunload', onBeforeUnload)

    return () => {
      document.removeEventListener('visibilitychange', onVisibility)
      window.removeEventListener('blur', onBlur)
      window.removeEventListener('focus', onFocus)
      window.removeEventListener('online', onOnline)
      window.removeEventListener('offline', onOffline)
      window.removeEventListener('pagehide', onPageHide)
      window.removeEventListener('beforeunload', onBeforeUnload)
      // The quiz page itself went away (not a reload): if the attempt is
      // still open, that is leaving the quiz.
      releaseTracker(attemptId, () => {
        if (latest.current.active) latest.current.onUnmountOpen?.()
      })
    }
    // initialStatus only matters when the tracker is first created.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [attemptId, active])

  const endReporting = () => registry.get(attemptId)?.tracker.end()
  const flush = () => registry.get(attemptId)?.tracker.flush()

  return { checking, connection, endReporting, flush }
}

/**
 * Confirmation before leaving an open quiz for another Aegis page.
 * Returns ``pending`` (a departure waiting for an answer), ``confirm`` and
 * ``cancel``. ``onLeave`` runs before the navigation (it abandons the attempt).
 */
export function useLeaveGuard({ active, navigate, onLeave }) {
  const [pending, setPending] = useState(null)
  const latest = useRef({ active, navigate, onLeave })
  useEffect(() => {
    latest.current = { active, navigate, onLeave }
  })

  useEffect(() => {
    if (!active) return undefined

    // Links anywhere in the app (sidebar, header, "back to lesson"...).
    // Capture phase on the document runs before React Router's handlers.
    const onClick = (event) => {
      if (event.defaultPrevented || event.button !== 0) return
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return
      const anchor = event.target?.closest?.('a[href]')
      if (!anchor || anchor.target === '_blank' || anchor.hasAttribute('download')) return
      const url = new URL(anchor.href, window.location.href)
      if (url.origin !== window.location.origin) return
      if (url.pathname === window.location.pathname && url.search === window.location.search) return
      event.preventDefault()
      event.stopPropagation()
      setPending({ kind: 'link', to: `${url.pathname}${url.search}${url.hash}` })
    }

    // The Back button: an extra history entry for this same page catches
    // the first Back press, so the student can be asked first.
    if (!window.history.state?.aegisQuizGuard) {
      window.history.pushState({ ...window.history.state, aegisQuizGuard: true }, '', window.location.href)
    }
    const onPopState = (event) => {
      if (!latest.current.active || event.state?.aegisQuizGuard) return
      window.history.pushState({ ...window.history.state, aegisQuizGuard: true }, '', window.location.href)
      setPending({ kind: 'back' })
    }

    document.addEventListener('click', onClick, true)
    window.addEventListener('popstate', onPopState)
    return () => {
      document.removeEventListener('click', onClick, true)
      window.removeEventListener('popstate', onPopState)
    }
  }, [active])

  const confirm = async () => {
    const target = pending
    setPending(null)
    if (!target) return
    await latest.current.onLeave?.()
    if (target.kind === 'link') latest.current.navigate(target.to)
    else window.history.go(-2) // past the guard entry and the quiz page
  }
  const cancel = () => setPending(null)

  return { pending, confirm, cancel }
}
