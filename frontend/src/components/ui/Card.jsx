import React from 'react'
import { Link } from 'react-router-dom'
import { ChevronRight } from 'lucide-react'
import { cx } from './cx'

const PADDING = { none: '', sm: 'p-4', md: 'p-5 sm:p-6', lg: 'p-6 sm:p-8' }

/** The standard surface: fine border, restrained shadow, 14px radius. */
export function Card({ as: Tag = 'div', padding = 'md', interactive = false, className, children, ...rest }) {
  return (
    <Tag
      className={cx(
        'rounded-card border border-line bg-surface shadow-card',
        interactive &&
          'transition-[border-color,background-color,transform] duration-200 ease-out hover:-translate-y-0.5 hover:border-line-strong hover:bg-[#182034]',
        PADDING[padding],
        className
      )}
      {...rest}
    >
      {children}
    </Tag>
  )
}

/** Small uppercase label above a heading or a group. */
export function Eyebrow({ className, children }) {
  return <p className={cx('text-[11px] font-semibold uppercase tracking-[0.14em] text-ink-2', className)}>{children}</p>
}

export function SectionHeader({ title, description, action, icon: Icon, as: Tag = 'h2', id, className }) {
  return (
    <div className={cx('flex flex-wrap items-start justify-between gap-x-4 gap-y-3', className)}>
      <div className="min-w-0 flex-1">
        <Tag id={id} className="flex items-center gap-2 font-display text-[17px] font-semibold tracking-tight text-ink">
          {Icon && <Icon size={18} className="shrink-0 text-brand-400" aria-hidden="true" />}
          <span className="min-w-0">{title}</span>
        </Tag>
        {description && <p className="mt-1 max-w-3xl text-[13px] leading-relaxed text-ink-2">{description}</p>}
      </div>
      {action && <div className="flex min-w-0 max-w-full flex-wrap items-center gap-2">{action}</div>}
    </div>
  )
}

export function Breadcrumbs({ items, className }) {
  if (!items?.length) return null
  return (
    <nav aria-label="Breadcrumb" className={cx('min-w-0', className)}>
      <ol className="flex flex-wrap items-center gap-x-1 gap-y-0.5 text-[13px] text-ink-2">
        {items.map((item, index) => {
          const last = index === items.length - 1
          return (
            <li key={`${item.label}-${index}`} className="flex min-w-0 items-center gap-1">
              {item.to && !last ? (
                <Link to={item.to} state={item.state} className="max-w-[16rem] truncate rounded transition-colors hover:text-ink">
                  {item.label}
                </Link>
              ) : (
                <span className={cx('max-w-[18rem] truncate', last && 'font-medium text-ink')} aria-current={last ? 'page' : undefined}>
                  {item.label}
                </span>
              )}
              {!last && <ChevronRight size={14} className="shrink-0 text-ink-3" aria-hidden="true" />}
            </li>
          )
        })}
      </ol>
    </nav>
  )
}

/** Page title block: optional breadcrumbs/eyebrow, title, description, actions. */
export function PageHeader({ eyebrow, title, description, actions, breadcrumbs, meta, className }) {
  return (
    <header className={cx('flex flex-col gap-5 md:flex-row md:items-end md:justify-between', className)}>
      <div className="min-w-0 space-y-2.5">
        {breadcrumbs && <Breadcrumbs items={breadcrumbs} />}
        {eyebrow && <Eyebrow className="text-brand-300">{eyebrow}</Eyebrow>}
        <h1 className="font-display text-[28px] font-semibold leading-[1.15] tracking-tight text-ink sm:text-[32px]">{title}</h1>
        {description && <div className="max-w-2xl text-sm leading-relaxed text-ink-2">{description}</div>}
        {meta && <div className="flex flex-wrap items-center gap-2 pt-1">{meta}</div>}
      </div>
      {actions && <div className="flex shrink-0 flex-wrap items-center gap-2">{actions}</div>}
    </header>
  )
}
