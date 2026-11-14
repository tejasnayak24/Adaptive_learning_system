import test from 'node:test'
import assert from 'node:assert/strict'

import {
  ACTION_CATALOGUE,
  ALL_ACTIONS,
  actionInfo,
  resolveNextStep
} from '../src/utils/recommendationActions.js'

// The RL engine's Action enum, in index order (rl_engine/core/actions.py).
const ENGINE_ACTIONS = [
  'NEXT_LESSON',
  'REPEAT_LESSON',
  'INCREASE_DIFFICULTY',
  'DECREASE_DIFFICULTY',
  'PRACTICE_QUIZ',
  'QUICK_CHALLENGE',
  'SHOW_WORKED_EXAMPLE',
  'PROVIDE_HINT',
  'FOCUS_RECOVERY',
  'SHOW_REAL_WORLD_APPLICATION',
  'SKIP_TO_ADVANCED_TOPIC'
]

const ctx = {
  lessonId: 2,
  quizId: 21,
  difficulty: 'Medium',
  lessonQuizzes: [
    { id: 20, difficulty: 'Easy' },
    { id: 21, difficulty: 'Medium' },
    { id: 22, difficulty: 'Hard' }
  ],
  lessons: [{ id: 1 }, { id: 2 }, { id: 3 }, { id: 4 }, { id: 5 }],
  onResults: true
}

test('catalogue covers exactly the 11 engine actions', () => {
  assert.deepEqual([...ALL_ACTIONS].sort(), [...ENGINE_ACTIONS].sort())
  for (const action of ENGINE_ACTIONS) {
    assert.ok(ACTION_CATALOGUE[action].label)
    assert.ok(ACTION_CATALOGUE[action].description)
  }
})

test('every action resolves to a specific next step, never a generic button', () => {
  for (const action of ENGINE_ACTIONS) {
    const step = resolveNextStep(action, ctx)
    assert.notEqual(step.kind, 'unknown', action)
    assert.ok(step.label && !/back to subjects/i.test(step.label), `${action}: ${step.label}`)
  }
})

test('every action still resolves with minimal context (Recommendations page)', () => {
  for (const action of ENGINE_ACTIONS) {
    const step = resolveNextStep(action, { lessonId: 2 })
    assert.notEqual(step.kind, 'unknown', action)
  }
})

test('pacing actions pick the right lesson', () => {
  assert.equal(resolveNextStep('NEXT_LESSON', ctx).to, '/lesson/3')
  assert.equal(resolveNextStep('SKIP_TO_ADVANCED_TOPIC', ctx).to, '/lesson/4')
  assert.equal(resolveNextStep('REPEAT_LESSON', ctx).to, '/lesson/2')
  const last = resolveNextStep('NEXT_LESSON', { ...ctx, lessonId: 5 })
  assert.equal(last.to, '/subjects')
})

test('difficulty actions open the neighbouring quiz level', () => {
  assert.equal(resolveNextStep('INCREASE_DIFFICULTY', ctx).to, '/quiz/22')
  assert.equal(resolveNextStep('DECREASE_DIFFICULTY', ctx).to, '/quiz/20')
  const noHarder = resolveNextStep('INCREASE_DIFFICULTY', { ...ctx, difficulty: 'HARD' })
  assert.equal(noHarder.kind, 'retry')
})

test('practice, hint and challenge retry the quiz in the right mode', () => {
  assert.deepEqual(
    ['PRACTICE_QUIZ', 'PROVIDE_HINT', 'QUICK_CHALLENGE'].map((a) => resolveNextStep(a, ctx).mode),
    ['practice', 'hints', 'challenge']
  )
  assert.equal(resolveNextStep('PRACTICE_QUIZ', ctx).to, '/quiz/21')
})

test('worked example, break and real-world actions', () => {
  const worked = resolveNextStep('SHOW_WORKED_EXAMPLE', ctx)
  assert.equal(worked.to, '/lesson/2')
  assert.equal(worked.state.recommendedAction, 'SHOW_WORKED_EXAMPLE')
  assert.equal(resolveNextStep('SHOW_WORKED_EXAMPLE', { onResults: true }).kind, 'review')
  assert.equal(resolveNextStep('FOCUS_RECOVERY', ctx).kind, 'break')
  const realWorld = resolveNextStep('SHOW_REAL_WORLD_APPLICATION', ctx)
  assert.equal(realWorld.state.recommendedAction, 'SHOW_REAL_WORLD_APPLICATION')
})

test('unknown actions are reported explicitly', () => {
  const step = resolveNextStep('TELEPORT', ctx)
  assert.equal(step.kind, 'unknown')
  assert.match(actionInfo('TELEPORT').label, /Unrecognised/)
})

test('pacing uses curriculum navigation (grade and subject order), not lesson ids', () => {
  const navigation = { next: { id: 41, title: 'Tenses' }, skip: { id: 57, title: 'Letters' } }
  const withNav = { ...ctx, lessonId: 40, navigation }
  assert.equal(resolveNextStep('NEXT_LESSON', withNav).to, '/lesson/41')
  assert.equal(resolveNextStep('SKIP_TO_ADVANCED_TOPIC', withNav).to, '/lesson/57')
  const end = resolveNextStep('NEXT_LESSON', { ...ctx, navigation: { next: null, skip: null } })
  assert.equal(end.to, '/subjects')
  assert.match(end.label, /Subject complete/)
})
