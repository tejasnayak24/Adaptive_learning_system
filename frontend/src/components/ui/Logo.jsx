import React, { useId } from 'react'
import { cx, svgId } from './cx'

/** Aegis mark: a shield carrying an "A". */
export function LogoMark({ size = 32, className }) {
  const gradientId = svgId(useId())
  return (
    <svg width={size} height={size} viewBox="0 0 32 32" className={cx('shrink-0', className)} aria-hidden="true">
      <defs>
        <linearGradient id={gradientId} x1="4" y1="3" x2="28" y2="29" gradientUnits="userSpaceOnUse">
          <stop offset="0" stopColor="#9f92ff" />
          <stop offset="1" stopColor="#43cdb0" />
        </linearGradient>
      </defs>
      <path d="M16 2.5 4.5 6.8v8.4c0 7.1 4.9 12.6 11.5 14.3 6.6-1.7 11.5-7.2 11.5-14.3V6.8Z" fill={`url(#${gradientId})`} />
      <path
        d="M11.2 21.2 16 10l4.8 11.2M12.9 17.2h6.2"
        fill="none"
        stroke="#090d18"
        strokeWidth="2.4"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

export function Wordmark({ compact = false, size = 30, className }) {
  return (
    <span className={cx('flex items-center gap-2.5', className)}>
      <LogoMark size={size} />
      <span className="leading-none">
        <span className="block font-display text-[17px] font-semibold tracking-tight text-ink">Aegis</span>
        {!compact && <span className="mt-1 block text-[11px] font-medium text-ink-2">Adaptive Learning System</span>}
      </span>
    </span>
  )
}
