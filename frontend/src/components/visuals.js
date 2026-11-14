import {
  ArrowRight,
  BookCheck,
  BookOpen,
  BookOpenText,
  Camera,
  CameraOff,
  ChevronsDown,
  ChevronsRight,
  ChevronsUp,
  Circle,
  CircleAlert,
  CircleCheck,
  CircleDashed,
  CircleQuestionMark,
  Coffee,
  Earth,
  EyeOff,
  FlaskConical,
  Landmark,
  Lightbulb,
  NotebookPen,
  PenLine,
  Repeat,
  RotateCw,
  Sigma,
  Timer,
  Trophy,
} from 'lucide-react'
import { SUBJECT_COLORS } from '../utils/analytics'
import { tint } from './ui/cx'

/*
 * One place that turns domain values (subjects, coach actions, activity,
 * topic status, camera telemetry) into icons and colours, so every page
 * shows them the same way. Labels and meanings stay in utils/.
 */

const SUBJECT_ICONS = {
  Mathematics: Sigma,
  Science: FlaskConical,
  'Social Science': Landmark,
  English: BookOpenText,
}

export function subjectVisual(subject) {
  const color = SUBJECT_COLORS[subject] || '#69758c'
  return {
    icon: SUBJECT_ICONS[subject] || BookOpen,
    color,
    soft: tint(color, 0.12),
    ring: tint(color, 0.3),
    glow: tint(color, 0.18),
  }
}

const ACTION_ICONS = {
  NEXT_LESSON: ArrowRight,
  REPEAT_LESSON: Repeat,
  INCREASE_DIFFICULTY: ChevronsUp,
  DECREASE_DIFFICULTY: ChevronsDown,
  PRACTICE_QUIZ: PenLine,
  QUICK_CHALLENGE: Timer,
  SHOW_WORKED_EXAMPLE: NotebookPen,
  PROVIDE_HINT: Lightbulb,
  FOCUS_RECOVERY: Coffee,
  SHOW_REAL_WORLD_APPLICATION: Earth,
  SKIP_TO_ADVANCED_TOPIC: ChevronsRight,
}

export function actionIcon(action) {
  return ACTION_ICONS[action] || CircleQuestionMark
}

/** Icon and tone for an analytics activity event. */
export function activityVisual(event) {
  switch (event?.type) {
    case 'quiz_attempt':
      return event.passed ? { icon: CircleCheck, tone: 'success' } : { icon: RotateCw, tone: 'neutral' }
    case 'lesson_completed':
      return { icon: BookCheck, tone: 'mint' }
    case 'subject_completed':
      return { icon: Trophy, tone: 'brand' }
    default:
      return { icon: Circle, tone: 'neutral' }
  }
}

/** Topic status (analytics) -> icon and tone. */
export const TOPIC_STATUS_VISUALS = {
  strong: { icon: CircleCheck, tone: 'success' },
  needs_revision: { icon: RotateCw, tone: 'warning' },
  weak: { icon: CircleAlert, tone: 'danger' },
  insufficient_data: { icon: CircleDashed, tone: 'neutral' },
  not_started: { icon: Circle, tone: 'neutral' },
}

/** Fill colours for topic-status charts (status tokens; never subject colours). */
export const TOPIC_STATUS_COLORS = {
  strong: '#3dd68c',
  needs_revision: '#f5b544',
  weak: '#f2666e',
  insufficient_data: '#4f5b75',
  not_started: '#2c3650',
}

export const TELEMETRY_VISUALS = {
  measured: { icon: Camera, tone: 'success' },
  unavailable: { icon: CameraOff, tone: 'warning' },
  not_monitored: { icon: EyeOff, tone: 'neutral' },
}

export const DIFFICULTY_LEVEL = { EASY: 1, MEDIUM: 2, HARD: 3 }

export function difficultyName(difficulty) {
  const value = String(difficulty || '').toUpperCase()
  return value ? value.charAt(0) + value.slice(1).toLowerCase() : 'Quiz'
}

export const TONE_TEXT = {
  success: 'text-success',
  warning: 'text-warning',
  danger: 'text-danger',
  brand: 'text-brand-300',
  mint: 'text-mint-300',
  info: 'text-info',
  neutral: 'text-ink-2',
}

export const TONE_SOFT = {
  success: 'bg-success/[0.12] text-success ring-success/25',
  warning: 'bg-warning/[0.12] text-warning ring-warning/25',
  danger: 'bg-danger/[0.12] text-danger ring-danger/25',
  brand: 'bg-brand-500/[0.12] text-brand-300 ring-brand-500/25',
  mint: 'bg-mint-500/[0.12] text-mint-300 ring-mint-500/25',
  info: 'bg-info/[0.12] text-info ring-info/25',
  neutral: 'bg-white/[0.05] text-ink-2 ring-white/10',
}
