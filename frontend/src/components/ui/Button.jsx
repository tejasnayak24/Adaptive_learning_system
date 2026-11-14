import React from 'react'
import { Link } from 'react-router-dom'
import { LoaderCircle } from 'lucide-react'
import { cx } from './cx'

const BASE =
  'inline-flex select-none items-center justify-center font-semibold transition-[background-color,border-color,color,box-shadow,transform] duration-150 ease-out active:scale-[0.98] disabled:pointer-events-none disabled:opacity-45 aria-disabled:pointer-events-none aria-disabled:opacity-45'

const VARIANTS = {
  primary: 'bg-brand-600 text-white shadow-button hover:bg-brand-650 hover:shadow-glow',
  secondary: 'border border-line-strong bg-raised text-ink hover:border-[#3a4664] hover:bg-overlay',
  ghost: 'text-ink-2 hover:bg-white/[0.05] hover:text-ink',
  subtle: 'bg-white/[0.045] text-ink hover:bg-white/[0.08]',
  mint: 'bg-mint-500 text-canvas shadow-button hover:bg-mint-400',
  warning: 'bg-warning text-canvas shadow-button hover:bg-[#f8c463]',
  danger: 'bg-danger-strong text-white shadow-button hover:bg-[#b52f41]',
  'danger-ghost': 'text-danger hover:bg-danger/10',
  link: 'rounded-md text-brand-300 underline-offset-4 hover:text-brand-200 hover:underline active:scale-100',
}

const SIZES = {
  xs: 'min-h-7 gap-1 rounded-lg px-2.5 py-1 text-xs',
  sm: 'min-h-8 gap-1.5 rounded-lg px-3 py-1.5 text-[13px]',
  md: 'min-h-10 gap-2 rounded-control px-4 py-2 text-sm',
  lg: 'min-h-12 gap-2 rounded-control px-5 py-2.5 text-[15px]',
}

const ICON_SIZE = { xs: 14, sm: 15, md: 16, lg: 18 }

/**
 * Button, or a router Link styled as one when `to` is given. Links stay real
 * <a href> elements: the quiz leave-guard relies on intercepting them.
 */
export function Button({
  variant = 'primary',
  size = 'md',
  to,
  state,
  replace,
  href,
  icon: Icon,
  iconRight: IconRight,
  loading = false,
  fullWidth = false,
  wrap = false,
  className,
  children,
  type,
  disabled,
  ref,
  ...rest
}) {
  const classes = cx(
    BASE,
    VARIANTS[variant],
    variant === 'link' ? 'gap-1.5 text-sm' : SIZES[size],
    wrap ? 'whitespace-normal text-left' : 'whitespace-nowrap',
    fullWidth && 'w-full',
    className
  )
  const iconSize = ICON_SIZE[size] || 16
  const content = (
    <>
      {loading ? (
        <LoaderCircle size={iconSize} className="shrink-0 animate-spin" aria-hidden="true" />
      ) : Icon ? (
        <Icon size={iconSize} className="shrink-0" aria-hidden="true" />
      ) : null}
      {children}
      {IconRight && !loading ? <IconRight size={iconSize} className="shrink-0" aria-hidden="true" /> : null}
    </>
  )

  if (to !== undefined) {
    return (
      <Link ref={ref} to={to} state={state} replace={replace} className={classes} aria-disabled={disabled || undefined} {...rest}>
        {content}
      </Link>
    )
  }
  if (href) {
    return (
      <a ref={ref} href={href} className={classes} {...rest}>
        {content}
      </a>
    )
  }
  return (
    <button
      ref={ref}
      type={type || 'button'}
      disabled={disabled || loading}
      aria-busy={loading || undefined}
      className={classes}
      {...rest}
    >
      {content}
    </button>
  )
}

const ICON_DIMENSIONS = { sm: 'h-8 w-8 rounded-lg', md: 'h-10 w-10 rounded-control', lg: 'h-11 w-11 rounded-control' }

/** Square icon-only button. `label` is required: it is the accessible name. */
export function IconButton({ icon: Icon, label, size = 'md', variant = 'ghost', className, ref, ...rest }) {
  return (
    <button
      ref={ref}
      type="button"
      aria-label={label}
      className={cx(BASE, VARIANTS[variant], ICON_DIMENSIONS[size], 'shrink-0', className)}
      {...rest}
    >
      <Icon size={size === 'sm' ? 16 : 18} aria-hidden="true" />
    </button>
  )
}
