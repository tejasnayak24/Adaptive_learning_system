import React, { cloneElement, isValidElement, useId } from 'react'
import { Info } from 'lucide-react'
import { cx } from './cx'

const SIDES = { top: 'bottom-full mb-2', bottom: 'top-full mt-2' }
const ALIGN = { center: 'left-1/2 -translate-x-1/2', start: 'left-0', end: 'right-0' }

/**
 * Hover/focus tooltip. It only enhances: anything important it says must also
 * be reachable without it (visible text, aria-label or the page itself).
 */
export function Tooltip({ content, side = 'top', align = 'center', className, children }) {
  const id = useId()
  if (!content) return children
  const trigger = isValidElement(children) ? cloneElement(children, { 'aria-describedby': id }) : children
  return (
    <span className={cx('group/tt relative inline-flex', className)}>
      {trigger}
      <span
        role="tooltip"
        id={id}
        className={cx(
          'pointer-events-none invisible absolute z-50 w-max max-w-[260px] rounded-lg border border-line-strong bg-[#232d45] px-2.5 py-1.5 text-left text-xs font-normal normal-case leading-snug tracking-normal text-ink opacity-0 shadow-raised transition-opacity duration-150',
          'group-hover/tt:visible group-hover/tt:opacity-100 group-focus-within/tt:visible group-focus-within/tt:opacity-100',
          SIDES[side],
          ALIGN[align]
        )}
      >
        {content}
      </span>
    </span>
  )
}

/** Small focusable "i" that explains a figure. */
export function InfoTip({ text, label = 'More information', side = 'top', align = 'center' }) {
  return (
    <Tooltip content={text} side={side} align={align}>
      <button
        type="button"
        aria-label={label}
        className="grid h-5 w-5 place-items-center rounded-full text-ink-3 transition-colors hover:text-ink-2 focus-visible:text-ink-2"
      >
        <Info size={14} aria-hidden="true" />
      </button>
    </Tooltip>
  )
}
