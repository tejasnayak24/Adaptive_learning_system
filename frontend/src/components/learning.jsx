import React from 'react'
import { Minus, TrendingDown, TrendingUp } from 'lucide-react'
import { Badge, ColorDot, LevelBars, Tooltip, cx } from './ui'
import { TELEMETRY_HELP, TELEMETRY_LABELS, topicStatusInfo } from '../utils/analytics'
import { DIFFICULTY_LEVEL, TELEMETRY_VISUALS, TOPIC_STATUS_VISUALS, difficultyName, subjectVisual } from './visuals'

/*
 * Small domain atoms shared by the learning and insight pages: subject
 * identity, quiz difficulty, camera telemetry, topic status and score trend.
 */

/** Tinted square carrying a subject's icon in its colour. */
export function SubjectIcon({ subject, size = 'md', className }) {
  const visual = subjectVisual(subject)
  const Icon = visual.icon
  const dims = { sm: 'h-8 w-8 rounded-lg', md: 'h-10 w-10 rounded-xl', lg: 'h-12 w-12 rounded-[14px]' }
  const iconSize = { sm: 16, md: 19, lg: 23 }
  return (
    <span
      className={cx('grid shrink-0 place-items-center ring-1 ring-inset', dims[size], className)}
      style={{ background: visual.soft, color: visual.color, '--tw-ring-color': visual.ring }}
      aria-hidden="true"
    >
      <Icon size={iconSize[size]} />
    </span>
  )
}

/** Subject name with its colour dot (the text keeps ink colours). */
export function SubjectChip({ subject, className }) {
  return (
    <span className={cx('inline-flex min-w-0 items-center gap-1.5', className)}>
      <ColorDot color={subjectVisual(subject).color} />
      <span className="truncate">{subject}</span>
    </span>
  )
}

/** Quiz level as a three-step glyph plus its name (an ordinal scale, not a status). */
export function DifficultyBadge({ difficulty, size = 'md', className }) {
  const level = DIFFICULTY_LEVEL[String(difficulty || '').toUpperCase()] || 1
  return (
    <span
      className={cx(
        'inline-flex shrink-0 items-center gap-1.5 whitespace-nowrap rounded-md border border-line-strong bg-white/[0.03] font-medium text-ink-2',
        size === 'sm' ? 'h-5 px-1.5 text-[11px]' : 'h-6 px-2 text-xs',
        className
      )}
    >
      <LevelBars level={level} />
      {difficultyName(difficulty)}
    </span>
  )
}

/** Camera telemetry state of a quiz. Pages that list these also show a legend. */
export function TelemetryBadge({ telemetry, size = 'sm' }) {
  const visual = TELEMETRY_VISUALS[telemetry] || TELEMETRY_VISUALS.not_monitored
  return (
    <Tooltip content={TELEMETRY_HELP[telemetry]}>
      <Badge tone={visual.tone} icon={visual.icon} size={size}>
        {TELEMETRY_LABELS[telemetry] || telemetry}
      </Badge>
    </Tooltip>
  )
}

export function TopicStatusBadge({ status, size = 'md' }) {
  const info = topicStatusInfo(status)
  const visual = TOPIC_STATUS_VISUALS[status] || TOPIC_STATUS_VISUALS.not_started
  return (
    <Badge tone={visual.tone} icon={visual.icon} size={size}>
      {info.label}
    </Badge>
  )
}

/**
 * First-three vs last-three score comparison (utils/analytics trendDirection).
 * "Needs revision" when scores are falling; null = not enough quizzes yet.
 */
export function TrendBadge({ trend, size = 'sm' }) {
  if (!trend) {
    return (
      <Badge tone="neutral" size={size} icon={Minus}>
        Too few quizzes
      </Badge>
    )
  }
  if (trend.direction === 'up') {
    return (
      <Badge tone="success" size={size} icon={TrendingUp}>
        Improving
      </Badge>
    )
  }
  if (trend.direction === 'down') {
    return (
      <Badge tone="warning" size={size} icon={TrendingDown}>
        Needs revision
      </Badge>
    )
  }
  return (
    <Badge tone="info" size={size} icon={Minus}>
      Stable
    </Badge>
  )
}
