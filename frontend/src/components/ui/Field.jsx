import React, { useId, useState } from 'react'
import { Check, ChevronDown, CircleAlert, Eye, EyeOff } from 'lucide-react'
import { cx } from './cx'

export const INPUT_CLASS =
  'block w-full rounded-control border border-line-strong bg-deep text-sm text-ink placeholder:text-ink-3 shadow-[inset_0_1px_2px_rgb(0_0_0/0.25)] transition-[border-color,box-shadow] duration-150 hover:border-[#3a4664] focus:border-brand-500 focus:outline-none focus:ring-4 focus:ring-brand-500/20 disabled:opacity-50'

function describedBy(...ids) {
  const value = ids.filter(Boolean).join(' ')
  return value || undefined
}

/** Labelled text input with optional leading icon, hint, error and trailing slot. */
export function TextField({ id, label, icon: Icon, hint, error, endAdornment, className, inputClassName, ...inputProps }) {
  const autoId = useId()
  const fieldId = id || autoId
  const hintId = hint ? `${fieldId}-hint` : null
  const errorId = error ? `${fieldId}-error` : null
  return (
    <div className={cx('space-y-1.5', className)}>
      {label && (
        <label htmlFor={fieldId} className="block text-[13px] font-medium text-ink-2">
          {label}
        </label>
      )}
      <div className="relative">
        {Icon && (
          <Icon size={17} className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 text-ink-3" aria-hidden="true" />
        )}
        <input
          id={fieldId}
          aria-invalid={error ? true : undefined}
          aria-describedby={describedBy(hintId, errorId)}
          className={cx(
            INPUT_CLASS,
            'h-11 px-3.5',
            Icon && 'pl-10',
            endAdornment && 'pr-12',
            error && 'border-danger/60 focus:border-danger focus:ring-danger/20',
            inputClassName
          )}
          {...inputProps}
        />
        {endAdornment && <div className="absolute inset-y-0 right-1 flex items-center">{endAdornment}</div>}
      </div>
      {hint && !error && (
        <p id={hintId} className="text-xs text-ink-2">
          {hint}
        </p>
      )}
      {error && (
        <p id={errorId} className="flex items-center gap-1.5 text-xs font-medium text-danger">
          <CircleAlert size={13} className="shrink-0" aria-hidden="true" />
          {error}
        </p>
      )}
    </div>
  )
}

/** Password input with a show/hide toggle. */
export function PasswordField(props) {
  const [visible, setVisible] = useState(false)
  return (
    <TextField
      {...props}
      type={visible ? 'text' : 'password'}
      endAdornment={
        <button
          type="button"
          onClick={() => setVisible((value) => !value)}
          aria-label={visible ? 'Hide password' : 'Show password'}
          aria-pressed={visible}
          className="grid h-9 w-9 place-items-center rounded-lg text-ink-3 transition-colors hover:bg-white/[0.05] hover:text-ink"
        >
          {visible ? <EyeOff size={17} aria-hidden="true" /> : <Eye size={17} aria-hidden="true" />}
        </button>
      }
    />
  )
}

/** Native select (keyboard and screen-reader friendly) with the house style. */
export function SelectField({ id, label, hint, className, selectClassName, size = 'md', children, ...selectProps }) {
  const autoId = useId()
  const fieldId = id || autoId
  return (
    <div className={cx('space-y-1.5', className)}>
      {label && (
        <label htmlFor={fieldId} className="block text-[13px] font-medium text-ink-2">
          {label}
        </label>
      )}
      <div className="relative">
        <select
          id={fieldId}
          className={cx(
            INPUT_CLASS,
            'appearance-none pr-9',
            size === 'sm' ? 'h-9 pl-3 text-[13px]' : 'h-11 pl-3.5',
            selectClassName
          )}
          {...selectProps}
        >
          {children}
        </select>
        <ChevronDown size={16} className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-ink-3" aria-hidden="true" />
      </div>
      {hint && <p className="text-xs text-ink-2">{hint}</p>}
    </div>
  )
}

/** Large tappable checkbox row. */
export function Checkbox({ id, checked, onChange, className, children }) {
  const autoId = useId()
  const fieldId = id || autoId
  return (
    <label
      htmlFor={fieldId}
      className={cx(
        'flex cursor-pointer items-start gap-3 rounded-control border border-line bg-deep/70 p-3.5 transition-colors hover:border-line-strong has-checked:border-brand-500/45 has-checked:bg-brand-500/[0.06]',
        className
      )}
    >
      <span className="relative mt-0.5 grid h-5 w-5 shrink-0 place-items-center">
        <input
          id={fieldId}
          type="checkbox"
          checked={checked}
          onChange={onChange}
          className="peer h-5 w-5 cursor-pointer appearance-none rounded-md border border-[#46526f] bg-canvas transition-colors checked:border-brand-500 checked:bg-brand-600 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand-400"
        />
        <Check
          size={14}
          strokeWidth={3}
          className="pointer-events-none absolute text-white opacity-0 transition-opacity peer-checked:opacity-100"
          aria-hidden="true"
        />
      </span>
      <span className="text-sm leading-relaxed text-ink">{children}</span>
    </label>
  )
}
