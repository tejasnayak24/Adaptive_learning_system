import React from 'react'
import { cx } from './cx'

/**
 * Responsive table: a real <table> from the `sm` breakpoint up, and stacked
 * label/value cards on phones (no sideways scrolling).
 *
 * columns: [{ key, header, render?(row), align?: 'right', primary?: true,
 *             className?, cellClassName?, hideOnMobile?: true }]
 * The `primary` column becomes the card title on phones.
 */
export function DataTable({ columns, rows, rowKey, caption, minWidth = 640, className }) {
  const value = (column, row) => (column.render ? column.render(row) : row[column.key])
  const primary = columns.find((column) => column.primary)
  return (
    <div className={className}>
      <div className="hidden overflow-x-auto sm:block">
        <table className="w-full border-collapse text-left text-[13px]" style={{ minWidth }}>
          {caption && <caption className="sr-only">{caption}</caption>}
          <thead>
            <tr className="border-b border-line">
              {columns.map((column) => (
                <th
                  key={column.key}
                  scope="col"
                  className={cx(
                    'whitespace-nowrap px-4 py-3 text-xs font-medium text-ink-2',
                    column.align === 'right' && 'text-right',
                    column.className
                  )}
                >
                  {column.header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-line/70">
            {rows.map((row, index) => (
              <tr key={rowKey(row, index)} className="transition-colors duration-150 hover:bg-white/[0.02]">
                {columns.map((column) => (
                  <td
                    key={column.key}
                    className={cx('px-4 py-3 align-middle text-ink', column.align === 'right' && 'text-right tabular-nums', column.cellClassName)}
                  >
                    {value(column, row)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <ul className="space-y-2.5 sm:hidden" aria-label={caption}>
        {rows.map((row, index) => (
          <li key={rowKey(row, index)} className="rounded-xl border border-line bg-deep/70 p-3.5">
            {primary && <div className="mb-2.5 text-sm text-ink">{value(primary, row)}</div>}
            <dl className="grid grid-cols-2 gap-x-3 gap-y-2.5">
              {columns
                .filter((column) => column !== primary && !column.hideOnMobile)
                .map((column) => (
                  <div key={column.key} className="min-w-0">
                    <dt className="text-[11px] font-medium text-ink-2">{column.header}</dt>
                    <dd className="mt-0.5 text-[13px] text-ink">{value(column, row)}</dd>
                  </div>
                ))}
            </dl>
          </li>
        ))}
      </ul>
    </div>
  )
}
