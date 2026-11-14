import React, { useEffect, useId, useRef } from 'react'
import { cx } from './cx'

const FOCUSABLE =
  'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'

const TONES = {
  brand: 'bg-brand-500/[0.12] text-brand-300 ring-brand-500/25',
  warning: 'bg-warning/[0.12] text-warning ring-warning/25',
  danger: 'bg-danger/[0.12] text-danger ring-danger/25',
  neutral: 'bg-white/[0.06] text-ink-2 ring-white/10',
}

const WIDTHS = { sm: 'max-w-sm', md: 'max-w-md', lg: 'max-w-lg' }

/**
 * Dialog rendered in place (no portal): a dialog inside a region that is
 * paused (inert) stays paused with it, which the quiz relies on.
 * Focus moves into the dialog, Tab stays inside, Escape closes it when
 * `dismissible`, and focus returns to where it was on close.
 */
export function Modal({
  open,
  onClose,
  title,
  description,
  icon: Icon,
  tone = 'brand',
  role = 'dialog',
  size = 'md',
  dismissible = true,
  footer,
  className,
  children,
}) {
  const panelRef = useRef(null)
  const titleId = useId()
  const descriptionId = useId()
  const closeRef = useRef(onClose)
  useEffect(() => {
    closeRef.current = onClose
  })

  useEffect(() => {
    if (!open) return undefined
    const previous = document.activeElement
    const panel = panelRef.current
    if (panel && !panel.contains(document.activeElement)) {
      const target = panel.querySelector('[autofocus], [data-autofocus]') || panel.querySelector(FOCUSABLE) || panel
      target.focus?.()
    }
    const onKeyDown = (event) => {
      if (event.key === 'Escape' && dismissible) {
        event.stopPropagation()
        closeRef.current?.()
        return
      }
      if (event.key !== 'Tab' || !panel) return
      const items = [...panel.querySelectorAll(FOCUSABLE)].filter((el) => el.offsetParent !== null)
      if (!items.length) return
      const first = items[0]
      const last = items[items.length - 1]
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault()
        last.focus()
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault()
        first.focus()
      }
    }
    document.addEventListener('keydown', onKeyDown)
    return () => {
      document.removeEventListener('keydown', onKeyDown)
      if (previous && typeof previous.focus === 'function' && document.contains(previous)) previous.focus()
    }
  }, [open, dismissible])

  if (!open) return null

  return (
    <div className="fixed inset-0 z-[60] flex items-end justify-center p-4 sm:items-center">
      <div
        className="absolute inset-0 animate-fade-in bg-[#05070d]/80 backdrop-blur-[3px]"
        onClick={dismissible ? () => closeRef.current?.() : undefined}
        aria-hidden="true"
      />
      <div
        ref={panelRef}
        role={role}
        aria-modal="true"
        aria-labelledby={title ? titleId : undefined}
        aria-describedby={description ? descriptionId : undefined}
        tabIndex={-1}
        className={cx(
          'relative w-full animate-pop-in rounded-panel border border-line-strong bg-raised p-6 shadow-raised focus:outline-none',
          WIDTHS[size],
          className
        )}
      >
        {(Icon || title) && (
          <div className="flex items-start gap-4">
            {Icon && (
              <span className={cx('grid h-11 w-11 shrink-0 place-items-center rounded-xl ring-1 ring-inset', TONES[tone])}>
                <Icon size={21} aria-hidden="true" />
              </span>
            )}
            <div className="min-w-0 space-y-1.5 pt-0.5">
              {title && (
                <h2 id={titleId} className="font-display text-lg font-semibold leading-snug text-ink">
                  {title}
                </h2>
              )}
              {description && (
                <div id={descriptionId} className="text-sm leading-relaxed text-ink-2">
                  {description}
                </div>
              )}
            </div>
          </div>
        )}
        {children && <div className={cx(Icon || title ? 'mt-4' : '')}>{children}</div>}
        {footer && <div className="mt-6 flex flex-col-reverse gap-2.5 sm:flex-row sm:justify-end">{footer}</div>}
      </div>
    </div>
  )
}
