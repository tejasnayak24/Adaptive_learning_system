import React from 'react'
import { cx } from './cx'

const TONES = {
  neutral: 'border-line-strong bg-white/[0.03] text-ink-2',
  brand: 'border-brand-500/30 bg-brand-500/10 text-brand-300',
  mint: 'border-mint-500/30 bg-mint-500/10 text-mint-300',
  success: 'border-success/30 bg-success/10 text-success',
  warning: 'border-warning/30 bg-warning/10 text-warning',
  danger: 'border-danger/30 bg-danger/10 text-danger',
  info: 'border-info/30 bg-info/10 text-info',
}

const SIZES = {
  sm: 'h-5 gap-1 px-1.5 text-[11px]',
  md: 'h-6 gap-1.5 px-2 text-xs',
}

export function Badge({ tone = 'neutral', size = 'md', icon: Icon, dot = false, className, children, ...rest }) {
  return (
    <span
      className={cx(
        'inline-flex max-w-full shrink-0 items-center whitespace-nowrap rounded-md border font-medium leading-none',
        TONES[tone] || TONES.neutral,
        SIZES[size],
        className
      )}
      {...rest}
    >
      {dot && <span className="h-1.5 w-1.5 shrink-0 rounded-full bg-current" aria-hidden="true" />}
      {Icon && <Icon size={size === 'sm' ? 12 : 13} className="shrink-0" aria-hidden="true" />}
      <span className="truncate">{children}</span>
    </span>
  )
}

/** A coloured dot that carries identity next to text (the text keeps ink colours). */
export function ColorDot({ color, size = 8, className }) {
  return (
    <span
      className={cx('inline-block shrink-0 rounded-full', className)}
      style={{ width: size, height: size, background: color }}
      aria-hidden="true"
    />
  )
}
