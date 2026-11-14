// Run with: npm test   (node --test, no extra dependencies)
import test from 'node:test'
import assert from 'node:assert/strict'
import { HIDDEN_TICK_MS, createIntegrityTracker, makePageId } from '../src/services/quizIntegrity.js'

/** Fake clocks, timers, storage and server for one tracker. */
function harness({ fail = () => null, storage = new Map(), pageId = 'page-one-aaaaaaaa', mono = 1000, wall = 5_000_000 } = {}) {
  const time = { mono, wall }
  const timers = []
  let nextId = 1
  const sent = []
  const views = []
  const checking = []
  const connection = []
  const store = {
    getItem: (k) => (storage.has(k) ? storage.get(k) : null),
    setItem: (k, v) => storage.set(k, v),
    removeItem: (k) => storage.delete(k),
  }
  const fakeTimers = {
    setTimeout: (fn, ms) => {
      const t = { id: nextId++, at: time.mono + ms, fn, every: null }
      timers.push(t)
      return t.id
    },
    clearTimeout: (id) => {
      const i = timers.findIndex((t) => t.id === id)
      if (i >= 0) timers.splice(i, 1)
    },
    setInterval: (fn, ms) => {
      const t = { id: nextId++, at: time.mono + ms, fn, every: ms }
      timers.push(t)
      return t.id
    },
    clearInterval: (id) => fakeTimers.clearTimeout(id),
  }
  const transport = async (events, opts) => {
    sent.push({ events, opts })
    const error = fail(events, sent.length)
    if (error) throw error
    return { status: 'in_progress', echoed: events.map((e) => e.kind) }
  }
  const tracker = createIntegrityTracker({
    attemptId: 7,
    pageId,
    transport,
    clock: () => time.mono,
    wallClock: () => time.wall,
    timers: fakeTimers,
    storage: store,
    onView: (v) => views.push(v),
    onChecking: (c) => checking.push(c),
    onConnection: (c) => connection.push(c),
  })
  const settle = () => new Promise((resolve) => setImmediate(resolve))
  async function advance(ms) {
    const end = time.mono + ms
    for (;;) {
      timers.sort((a, b) => a.at - b.at)
      const next = timers[0]
      if (!next || next.at > end) break
      const delta = next.at - time.mono
      time.mono = next.at
      time.wall += delta
      if (next.every) next.at += next.every
      else timers.shift()
      next.fn()
      await settle()
    }
    time.wall += end - time.mono
    time.mono = end
    await settle()
  }
  return { tracker, sent, views, checking, connection, storage, time, advance, settle }
}

// Distinct events in send order (a keepalive resend repeats unacknowledged ones).
const kinds = (sent) => {
  const seen = new Map()
  sent.flatMap((s) => s.events).forEach((e) => seen.set(e.seq, e.kind))
  return [...seen.entries()].sort((a, b) => a[0] - b[0]).map(([, kind]) => kind)
}

test('page ids are url-safe and long enough for the server', () => {
  const id = makePageId()
  assert.match(id, /^[a-z0-9]{24}$/)
})

test('hiding reports immediately with keepalive, ticks while hidden, and the return carries the absence', async () => {
  const h = harness()
  h.tracker.pageHidden()
  await h.settle()
  assert.deepEqual(kinds(h.sent), ['hidden'])
  assert.equal(h.sent[0].opts.keepalive, true)

  await h.advance(HIDDEN_TICK_MS * 2)
  const ticks = h.sent.flatMap((s) => s.events).filter((e) => e.kind === 'hidden_tick')
  assert.deepEqual(ticks.map((e) => e.hidden_ms), [2000, 4000])

  await h.advance(1500)
  h.tracker.pageVisible()
  await h.settle()
  const visible = h.sent.at(-1).events.find((e) => e.kind === 'visible')
  assert.equal(visible.hidden_ms, 5500)
  assert.deepEqual(h.checking, [true, false]) // locked until the server answered
  assert.equal(h.storage.size, 0)
})

test('the larger of the monotonic and wall-clock absence is reported (sleeping laptop)', async () => {
  const h = harness()
  h.tracker.pageHidden()
  await h.settle()
  h.time.wall += 120_000 // the monotonic clock paused while the laptop slept
  h.time.mono += 3_000
  h.tracker.pageVisible()
  await h.settle()
  assert.equal(h.sent.at(-1).events.at(-1).hidden_ms, 120_000)
})

test('blur and focus are diagnostics and never start an absence', async () => {
  const h = harness()
  h.tracker.diagnostic('blur')
  h.tracker.diagnostic('focus')
  await h.advance(10_000)
  assert.deepEqual(kinds(h.sent), ['blur', 'focus'])
  assert.equal(h.tracker.hidden, false)
})

test('undeliverable reports are retried and say how long they waited', async () => {
  let offline = true
  const h = harness({ fail: () => (offline ? Object.assign(new Error('Network Error'), { status: null }) : null) })
  h.tracker.pageHidden()
  await h.settle()
  await h.advance(3000)
  h.tracker.pageVisible()
  await h.settle()
  assert.equal(h.tracker.pending > 0, true)
  assert.equal(h.connection.includes('offline'), true)

  offline = false
  await h.advance(MAX_WAIT())
  const last = h.sent.at(-1).events
  const visible = last.find((e) => e.kind === 'visible')
  assert.equal(visible.hidden_ms, 3000)
  assert.ok(visible.delivery_failures >= 1)
  assert.ok(visible.queued_ms > 0)
  assert.equal(h.tracker.pending, 0)
  assert.equal(h.checking.at(-1), false)
})

function MAX_WAIT() {
  return 6000
}

test('a refused batch is dropped, not retried forever', async () => {
  const h = harness({ fail: () => Object.assign(new Error('Unprocessable'), { status: 422 }) })
  h.tracker.diagnostic('blur')
  await h.advance(20_000)
  assert.equal(h.sent.length, 1)
  assert.equal(h.tracker.pending, 0)
})

test('reload: beforeunload marks the hide as an unload and the new page reports the measured gap', async () => {
  const storage = new Map()
  const first = harness({ storage })
  first.tracker.beforeUnload()
  first.tracker.pageHidden()
  first.tracker.pageHide()
  await first.settle()
  assert.deepEqual(kinds(first.sent), ['pagehide', 'pagehide'])

  const second = harness({ storage, pageId: 'page-two-bbbbbbbb', wall: first.time.wall + 1800 })
  second.tracker.start({ serverStatus: 'away', navigationType: 'reload' })
  await second.settle()
  const resume = second.sent[0].events[0]
  assert.equal(resume.kind, 'resume')
  assert.equal(resume.reload, true)
  assert.equal(resume.hidden_ms, 1800)
})

test('a cancelled unload is a normal hide again after a moment', async () => {
  const h = harness()
  h.tracker.beforeUnload()
  await h.advance(1500)
  h.tracker.pageHidden()
  await h.settle()
  assert.deepEqual(kinds(h.sent), ['hidden'])
})

test('a new tab for an absence the server knows about sends a resume without a measurement', async () => {
  const h = harness()
  h.tracker.start({ serverStatus: 'unverified', navigationType: 'navigate' })
  await h.settle()
  const resume = h.sent[0].events[0]
  assert.equal(resume.kind, 'resume')
  assert.equal('hidden_ms' in resume, false)
})

test('nothing is reported after the attempt ended', async () => {
  const h = harness()
  h.tracker.end()
  h.tracker.pageHidden()
  await h.advance(5000)
  h.tracker.pageVisible()
  await h.settle()
  assert.deepEqual(kinds(h.sent), [])
})

test('a hide while an ordinary request is in flight is sent at once and in order', async () => {
  let release
  const gate = new Promise((resolve) => {
    release = resolve
  })
  const sent = []
  const tracker = createIntegrityTracker({
    attemptId: 1,
    pageId: 'page-three-cccccccc',
    transport: async (events, opts) => {
      sent.push({ seqs: events.map((e) => e.seq), keepalive: opts.keepalive })
      if (sent.length === 1) await gate
      return { status: 'in_progress' }
    },
    clock: () => 0,
    wallClock: () => 0,
    timers: { setTimeout: () => 0, clearTimeout: () => {}, setInterval: () => 0, clearInterval: () => {} },
  })
  tracker.diagnostic('focus') // ordinary request, held in flight
  tracker.pageHidden() // must not wait for it
  await new Promise((resolve) => setImmediate(resolve))
  assert.deepEqual(sent, [
    { seqs: [1], keepalive: false },
    { seqs: [1, 2], keepalive: true },
  ])
  release()
})

test('after pagehide the old page never reports a return (the next page does)', async () => {
  const storage = new Map()
  const h = harness({ storage })
  h.tracker.pageHide()
  h.tracker.pageVisible() // e.g. a visibilitychange fired during unload
  await h.settle()
  assert.deepEqual(kinds(h.sent), ['pagehide'])
  assert.equal(storage.size, 1) // the gap record survives for the reloaded page
})

test('a cancelled reload (prompt dismissed, page stays) sends nothing', async () => {
  const h = harness()
  h.tracker.beforeUnload() // the browser asks; the student cancels
  await h.advance(5000)
  assert.deepEqual(kinds(h.sent), [])
  assert.equal(h.tracker.hidden, false)
})

test('a confirmed reload is reported as an incident by both pages', async () => {
  const storage = new Map()
  const first = harness({ storage })
  first.tracker.beforeUnload()
  first.tracker.pageHide() // prompt accepted: the page is unloaded
  await first.settle()
  assert.deepEqual(kinds(first.sent), ['pagehide']) // the server opens the incident now
  const second = harness({ storage, pageId: 'page-reloaded-cccc', wall: first.time.wall + 1200 })
  second.tracker.start({ serverStatus: 'away', navigationType: 'reload' })
  await second.settle()
  const [resume] = second.sent[0].events
  assert.equal(resume.kind, 'resume')
  assert.equal(resume.reload, true)
  assert.equal(resume.hidden_ms, 1200)
})
