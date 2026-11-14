import React from 'react'
import { CircleCheck, CircleX, Inbox, Info, LoaderCircle, RefreshCw, Sparkles, TriangleAlert } from 'lucide-react'
import { Button } from './Button'
import { Card } from './Card'
import { cx } from './cx'

export function EmptyState({ icon: Icon = Inbox, title, text, action, compact = false, className }) {
  return (
    <div className={cx('flex flex-col items-center justify-center px-4 text-center', compact ? 'py-8' : 'py-12', className)}>
      <span className="grid h-12 w-12 place-items-center rounded-2xl border border-line-strong bg-raised text-ink-2 shadow-card">
        <Icon size={22} aria-hidden="true" />
      </span>
      <p className="mt-4 font-display text-base font-semibold text-ink">{title}</p>
      {text && <p className="mt-1.5 max-w-sm text-[13px] leading-relaxed text-ink-2">{text}</p>}
      {action && <div className="mt-5 flex flex-wrap justify-center gap-2">{action}</div>}
    </div>
  )
}

export function ErrorState({ title = 'We could not load your learning data.', message, onRetry, className }) {
  return (
    <Card role="alert" padding="lg" className={cx('mx-auto max-w-lg text-center', className)}>
      <span className="mx-auto grid h-12 w-12 place-items-center rounded-2xl bg-danger/10 text-danger ring-1 ring-inset ring-danger/25">
        <TriangleAlert size={22} aria-hidden="true" />
      </span>
      <p className="mt-4 font-display text-base font-semibold text-ink">{title}</p>
      {message && <p className="mt-1.5 text-[13px] leading-relaxed text-ink-2">{message}</p>}
      {onRetry && (
        <Button variant="secondary" size="sm" icon={RefreshCw} onClick={onRetry} className="mt-5">
          Try again
        </Button>
      )}
    </Card>
  )
}

const CALLOUT_TONES = {
  info: { box: 'border-info/25 bg-info/[0.07]', icon: Info, iconClass: 'text-info' },
  brand: { box: 'border-brand-500/30 bg-brand-500/[0.08]', icon: Sparkles, iconClass: 'text-brand-300' },
  mint: { box: 'border-mint-500/25 bg-mint-500/[0.07]', icon: Sparkles, iconClass: 'text-mint-300' },
  success: { box: 'border-success/25 bg-success/[0.07]', icon: CircleCheck, iconClass: 'text-success' },
  warning: { box: 'border-warning/30 bg-warning/[0.08]', icon: TriangleAlert, iconClass: 'text-warning' },
  danger: { box: 'border-danger/30 bg-danger/[0.08]', icon: CircleX, iconClass: 'text-danger' },
  neutral: { box: 'border-line-strong bg-white/[0.025]', icon: Info, iconClass: 'text-ink-2' },
}

/** Inline message block. Pass role="alert" or role="status" where it announces something. */
export function Callout({ tone = 'info', icon, title, action, className, children, ...rest }) {
  const style = CALLOUT_TONES[tone] || CALLOUT_TONES.info
  const Icon = icon || style.icon
  return (
    <div className={cx('flex gap-3 rounded-card border px-4 py-3.5', style.box, className)} {...rest}>
      <Icon size={18} className={cx('mt-0.5 shrink-0', style.iconClass)} aria-hidden="true" />
      <div className="min-w-0 flex-1 space-y-1 text-[13px] leading-relaxed text-ink-2">
        {title && <p className="text-sm font-semibold text-ink">{title}</p>}
        {children}
      </div>
      {action && <div className="shrink-0 self-center">{action}</div>}
    </div>
  )
}

export function Spinner({ size = 20, className, label = 'Loading' }) {
  return (
    <span role="status" className={cx('inline-flex items-center', className)}>
      <LoaderCircle size={size} className="animate-spin text-brand-400" aria-hidden="true" />
      <span className="sr-only">{label}</span>
    </span>
  )
}

export function Skeleton({ className }) {
  return <div className={cx('skeleton', className)} aria-hidden="true" />
}

/** Page-level loading placeholder shaped like the page that is loading. */
export function PageSkeleton({ variant = 'dashboard', label = 'Loading' }) {
  return (
    <div className="space-y-6" aria-busy="true" aria-label={label} role="status">
      {variant === 'reading' ? (
        <div className="mx-auto max-w-3xl space-y-5">
          <Skeleton className="h-4 w-48" />
          <Skeleton className="h-10 w-3/4" />
          <Skeleton className="h-4 w-1/3" />
          <div className="space-y-3 pt-6">
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-5/6" />
          </div>
          <Skeleton className="h-48 w-full rounded-card" />
        </div>
      ) : (
        <>
          <Skeleton className="h-36 w-full rounded-card" />
          <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
            {[0, 1, 2, 3].map((index) => (
              <Skeleton key={index} className="h-28 rounded-card" />
            ))}
          </div>
          <div className="grid gap-6 lg:grid-cols-3">
            <Skeleton className="h-72 rounded-card lg:col-span-2" />
            <Skeleton className="h-72 rounded-card" />
          </div>
        </>
      )}
      <span className="sr-only">{label}</span>
    </div>
  )
}
