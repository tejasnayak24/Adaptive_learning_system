import React, { useEffect, useId, useState } from 'react'
import { cx, svgId } from './cx'

function clampPercent(value) {
  const number = Number(value)
  if (!Number.isFinite(number)) return 0
  return Math.max(0, Math.min(100, number))
}

/** Starts at 0 and moves to `value` after mount, so bars and rings animate in. */
function useEntrance(value) {
  const [shown, setShown] = useState(0)
  useEffect(() => {
    const frame = requestAnimationFrame(() => setShown(value))
    return () => cancelAnimationFrame(frame)
  }, [value])
  return shown
}

const HEIGHTS = { xs: 'h-1', sm: 'h-1.5', md: 'h-2', lg: 'h-2.5' }
const FILLS = {
  brand: 'bg-brand-500',
  mint: 'bg-mint-500',
  gradient: 'bg-gradient-to-r from-brand-500 to-mint-500',
  success: 'bg-success',
  warning: 'bg-warning',
  danger: 'bg-danger',
  neutral: 'bg-ink-3',
}

export function ProgressBar({ value, label, tone = 'brand', color, size = 'md', className }) {
  const percent = clampPercent(value)
  const shown = useEntrance(percent)
  return (
    <div
      role="progressbar"
      aria-label={label}
      aria-valuenow={Math.round(percent)}
      aria-valuemin={0}
      aria-valuemax={100}
      className={cx('w-full overflow-hidden rounded-full bg-white/[0.07]', HEIGHTS[size], className)}
    >
      <div
        className={cx('h-full rounded-full transition-[width] duration-700 ease-out-quint', !color && FILLS[tone])}
        style={{ width: `${shown}%`, ...(color ? { background: color } : null) }}
      />
    </div>
  )
}

/** Circular progress; children render in the centre. */
export function ProgressRing({ value, size = 120, stroke = 10, label, color, className, children }) {
  const percent = clampPercent(value)
  const shown = useEntrance(percent)
  const gradientId = svgId(useId())
  const radius = (size - stroke) / 2
  const circumference = 2 * Math.PI * radius
  return (
    <div
      className={cx('relative inline-grid shrink-0 place-items-center', className)}
      style={{ width: size, height: size }}
      role="img"
      aria-label={label}
    >
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} className="-rotate-90" aria-hidden="true">
        <defs>
          <linearGradient id={gradientId} x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="#9f92ff" />
            <stop offset="100%" stopColor="#43cdb0" />
          </linearGradient>
        </defs>
        <circle cx={size / 2} cy={size / 2} r={radius} fill="none" stroke="rgb(255 255 255 / 0.07)" strokeWidth={stroke} />
        {percent > 0 && (
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke={color || `url(#${gradientId})`}
            strokeWidth={stroke}
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={circumference * (1 - shown / 100)}
            style={{ transition: 'stroke-dashoffset 900ms cubic-bezier(0.22, 1, 0.36, 1)' }}
          />
        )}
      </svg>
      <div className="absolute inset-0 grid place-items-center text-center">{children}</div>
    </div>
  )
}

/** Three-step level glyph for quiz difficulty (an ordinal scale, not a status). */
export function LevelBars({ level = 1, className }) {
  return (
    <span className={cx('inline-flex items-end gap-[2px]', className)} aria-hidden="true">
      {[1, 2, 3].map((step) => (
        <span
          key={step}
          className={cx('w-[3px] rounded-sm', step <= level ? 'bg-brand-300' : 'bg-white/15')}
          style={{ height: 4 + step * 3 }}
        />
      ))}
    </span>
  )
}
