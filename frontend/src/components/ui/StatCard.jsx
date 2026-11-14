import React from 'react'
import { Card } from './Card'
import { InfoTip } from './Tooltip'
import { cx } from './cx'

const ICON_TONES = {
  brand: 'bg-brand-500/[0.12] text-brand-300 ring-brand-500/20',
  mint: 'bg-mint-500/[0.12] text-mint-300 ring-mint-500/20',
  warning: 'bg-warning/[0.12] text-warning ring-warning/20',
  info: 'bg-info/[0.12] text-info ring-info/20',
  neutral: 'bg-white/[0.05] text-ink-2 ring-white/10',
}

/** Label, one big value (proportional figures), an optional sub-line. */
export function StatCard({ label, value, sub, icon: Icon, tone = 'brand', help, className, children }) {
  return (
    <Card className={cx('flex flex-col', className)}>
      <div className="flex items-start justify-between gap-3">
        <div className="flex min-w-0 items-start gap-1.5">
          <p className="text-[13px] font-medium leading-snug text-ink-2">{label}</p>
          {help && <InfoTip text={help} label={`About ${label}`} />}
        </div>
        {Icon && (
          <span className={cx('grid h-9 w-9 shrink-0 place-items-center rounded-[10px] ring-1 ring-inset', ICON_TONES[tone])}>
            <Icon size={18} aria-hidden="true" />
          </span>
        )}
      </div>
      <p className="mt-2 text-[28px] font-semibold leading-none tracking-tight text-ink">{value}</p>
      {sub && <p className="mt-2 text-xs leading-relaxed text-ink-2">{sub}</p>}
      {children}
    </Card>
  )
}
