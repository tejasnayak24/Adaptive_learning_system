import React, { useRef } from 'react'
import { cx } from './cx'

/**
 * Single-choice control (radio group semantics, arrow keys move the choice).
 * options: [{ value, label, icon?, count? }]
 */
export function SegmentedControl({ options, value, onChange, label, size = 'md', className }) {
  const groupRef = useRef(null)

  const onKeyDown = (event) => {
    const keys = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }
    if (!(event.key in keys)) return
    event.preventDefault()
    const index = options.findIndex((option) => option.value === value)
    const next = options[(index + keys[event.key] + options.length) % options.length]
    onChange(next.value)
    requestAnimationFrame(() => {
      groupRef.current?.querySelector(`[data-value="${CSS.escape(String(next.value))}"]`)?.focus()
    })
  }

  return (
    <div
      ref={groupRef}
      role="radiogroup"
      aria-label={label}
      onKeyDown={onKeyDown}
      className={cx('inline-flex max-w-full items-center gap-1 overflow-x-auto rounded-control border border-line bg-deep p-1', className)}
    >
      {options.map((option) => {
        const active = option.value === value
        const Icon = option.icon
        return (
          <button
            key={option.value}
            type="button"
            role="radio"
            aria-checked={active}
            tabIndex={active ? 0 : -1}
            data-value={option.value}
            onClick={() => onChange(option.value)}
            className={cx(
              'inline-flex shrink-0 items-center gap-1.5 rounded-lg font-medium transition-[background-color,color,box-shadow] duration-150',
              size === 'sm' ? 'h-7 px-2.5 text-xs' : 'h-8 px-3 text-[13px]',
              active ? 'bg-raised text-ink shadow-card ring-1 ring-inset ring-line-strong' : 'text-ink-2 hover:text-ink'
            )}
          >
            {Icon && <Icon size={14} aria-hidden="true" />}
            {option.label}
            {option.count !== undefined && <span className={cx('tabular-nums', active ? 'text-ink-2' : 'text-ink-3')}>{option.count}</span>}
          </button>
        )
      })}
    </div>
  )
}
