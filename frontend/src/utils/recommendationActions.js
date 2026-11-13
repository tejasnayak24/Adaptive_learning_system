// What each of the RL engine's 11 actions means for the student, and how
// the website carries it out. Pure functions (no React) so they can be
// unit-tested with `npm test`.

export const ACTION_CATALOGUE = {
  NEXT_LESSON: {
    label: 'Next lesson',
    icon: '🚀',
    description: 'Move on to the next lesson in the curriculum.'
  },
  REPEAT_LESSON: {
    label: 'Repeat lesson',
    icon: '🔁',
    description: 'Study the same lesson again to strengthen the basics.'
  },
  INCREASE_DIFFICULTY: {
    label: 'Increase difficulty',
    icon: '⚡',
    description: 'Take the next harder quiz for this lesson (Easy → Medium → Hard).'
  },
  DECREASE_DIFFICULTY: {
    label: 'Decrease difficulty',
    icon: '🛠️',
    description: 'Take an easier quiz for this lesson to rebuild confidence.'
  },
  PRACTICE_QUIZ: {
    label: 'Practice quiz',
    icon: '📝',
    description: 'Retake this quiz to consolidate what you have just learned.'
  },
  QUICK_CHALLENGE: {
    label: 'Quick challenge',
    icon: '⏱️',
    description: 'A short, timed attempt to keep learning engaging.'
  },
  SHOW_WORKED_EXAMPLE: {
    label: 'Worked example',
    icon: '📖',
    description: 'Go through the solved answers step by step before trying again.'
  },
  PROVIDE_HINT: {
    label: 'Retry with hints',
    icon: '💡',
    description: 'Retake the quiz and use the hint on questions you are unsure about.'
  },
  FOCUS_RECOVERY: {
    label: 'Focus-recovery break',
    icon: '🧘',
    description: 'A short break to rest your eyes and regain concentration.'
  },
  SHOW_REAL_WORLD_APPLICATION: {
    label: 'Real-world application',
    icon: '🌍',
    description: 'Revisit the lesson and connect it to everyday situations.'
  },
  SKIP_TO_ADVANCED_TOPIC: {
    label: 'Skip to advanced topic',
    icon: '🎯',
    description: 'Skip ahead two lessons to more advanced material.'
  }
}

export const ALL_ACTIONS = Object.keys(ACTION_CATALOGUE)

export const POLICY_LABELS = {
  q_learning: 'Learned Q-table',
  q_learning_nearest_state: 'Nearest learned situation',
  fallback: 'Safe fallback (situation not learned)',
  rules: 'Hand-written rules (before Phase 4)'
}

export function actionInfo(action) {
  return (
    ACTION_CATALOGUE[action] || {
      label: `Unrecognised recommendation (${action || 'none'})`,
      icon: '❔',
      description: 'This recommendation type is not supported by this version of the website.'
    }
  )
}

const LEVELS = ['EASY', 'MEDIUM', 'HARD']

function quizAtLevel(quizzes, level) {
  return (quizzes || []).find((q) => String(q.difficulty || '').toUpperCase() === level) || null
}

function lessonAfter(lessons, lessonId, steps) {
  const sorted = [...(lessons || [])].sort((a, b) => (a.id ?? 0) - (b.id ?? 0))
  const index = sorted.findIndex((l) => l.id === lessonId)
  if (index === -1 || sorted.length === 0) return null
  if (index + 1 >= sorted.length) return null
  return sorted[Math.min(index + steps, sorted.length - 1)]
}

/**
 * Turn a recommended action into a concrete next step.
 *
 * ctx: { lessonId, quizId, difficulty, lessonQuizzes, navigation, lessons, onResults }
 *   navigation -- the lesson's curriculum navigation from the API
 *                 ({ next, skip, ... } within the student's grade and subject);
 *                 preferred over `lessons` for pacing actions.
 *   onResults  -- true on the quiz results screen (answer review visible).
 *
 * Returns { kind, label, to?, state?, mode?, level? } where kind is one of
 *   'navigate' -- go to `to` (with router `state`)
 *   'retry'    -- restart the current quiz (`mode`: practice | hints | challenge)
 *   'review'   -- scroll to the answer review on the results screen
 *   'break'    -- show the focus-recovery break
 *   'unknown'  -- unrecognised action (shown explicitly, never silently)
 */
export function resolveNextStep(action, ctx = {}) {
  const { lessonId, quizId, difficulty, lessonQuizzes, navigation, lessons, onResults } = ctx
  const level = String(difficulty || '').toUpperCase()
  const levelIndex = LEVELS.indexOf(level)
  const lessonPage = (label) => ({
    kind: 'navigate',
    label,
    to: lessonId ? `/lesson/${lessonId}` : '/subjects',
    state: { recommendedAction: action }
  })
  const retry = (mode, label) =>
    quizId
      ? { kind: 'retry', mode, label, to: `/quiz/${quizId}` }
      : lessonPage('Open the lesson to retake its quiz')

  switch (action) {
    case 'NEXT_LESSON':
    case 'SKIP_TO_ADVANCED_TOPIC': {
      const steps = action === 'NEXT_LESSON' ? 1 : 2
      const target = navigation
        ? (action === 'NEXT_LESSON' ? navigation.next : navigation.skip) || null
        : lessonAfter(lessons, lessonId, steps)
      if (target) {
        return {
          kind: 'navigate',
          label: action === 'NEXT_LESSON' ? 'Go to the next lesson →' : 'Skip ahead to an advanced lesson →',
          to: `/lesson/${target.id}`,
          state: { recommendedAction: action }
        }
      }
      return {
        kind: 'navigate',
        label: navigation || (lessons && lessons.length) ? 'Subject complete — choose what to study next →' : 'Browse lessons →',
        to: '/subjects'
      }
    }

    case 'REPEAT_LESSON':
      return lessonPage('Study the lesson again →')

    case 'INCREASE_DIFFICULTY':
    case 'DECREASE_DIFFICULTY': {
      const delta = action === 'INCREASE_DIFFICULTY' ? 1 : -1
      const targetLevel = levelIndex === -1 ? null : LEVELS[levelIndex + delta]
      const target = targetLevel ? quizAtLevel(lessonQuizzes, targetLevel) : null
      if (target) {
        const name = targetLevel.charAt(0) + targetLevel.slice(1).toLowerCase()
        return {
          kind: 'navigate',
          label: `Take the ${name} quiz →`,
          to: `/quiz/${target.id}`,
          level: targetLevel,
          state: { recommendedAction: action }
        }
      }
      if (!lessonQuizzes) return lessonPage('Open the lesson to choose a quiz level →')
      return retry('practice', `No ${targetLevel ? targetLevel.toLowerCase() : 'other'} quiz yet — retake this quiz →`)
    }

    case 'PRACTICE_QUIZ':
      return retry('practice', 'Retake this quiz →')

    case 'PROVIDE_HINT':
      return retry('hints', 'Retake with hints →')

    case 'QUICK_CHALLENGE':
      return retry('challenge', 'Start the quick challenge →')

    case 'SHOW_WORKED_EXAMPLE':
      // Lessons now contain real step-by-step worked examples; the lesson page
      // scrolls to and highlights them. Without a lesson, fall back to the
      // answer review on the results screen.
      return lessonId
        ? lessonPage('Study the worked examples →')
        : onResults
          ? { kind: 'review', label: 'Review the worked answers ↓' }
          : { kind: 'navigate', label: 'Browse lessons →', to: '/subjects' }

    case 'FOCUS_RECOVERY':
      return { kind: 'break', label: 'Start a short break →' }

    case 'SHOW_REAL_WORLD_APPLICATION':
      return lessonPage('See how this is used in real life →')

    default:
      return { kind: 'unknown', label: actionInfo(action).label }
  }
}

/** Student-facing explanation of the confidence number. */
export const CONFIDENCE_NOTE =
  'Decision strength: how clearly the learned values favour this action over the next best, ' +
  'and how often this situation was seen in training. It is not a probability.'
