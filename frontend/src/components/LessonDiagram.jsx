import React from 'react'

// Renders the data-driven lesson diagrams stored in lesson material.
// Supported types: flow, cycle, table, labelled, number_line, bar.

function Flow({ items, cycle }) {
  return (
    <ol className="flex flex-wrap items-stretch gap-2">
      {items.map((item, index) => (
        <li key={index} className="flex items-center gap-2">
          <span className="rounded-xl border border-indigo-500/30 bg-indigo-500/10 px-3 py-2 text-xs font-semibold text-indigo-100">
            {item}
          </span>
          {(index < items.length - 1 || cycle) && (
            <span aria-hidden="true" className="text-indigo-400">
              {index === items.length - 1 ? '↺' : '→'}
            </span>
          )}
        </li>
      ))}
    </ol>
  )
}

function Table({ columns, rows }) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-left text-xs">
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column} className="border-b border-slate-700 px-3 py-2 font-bold text-slate-300">
                {column}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, r) => (
            <tr key={r} className="odd:bg-slate-900/40">
              {row.map((cell, c) => (
                <td key={c} className="border-b border-slate-800 px-3 py-2 text-slate-300">
                  {cell}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function Labelled({ items }) {
  return (
    <dl className="grid grid-cols-1 gap-2 sm:grid-cols-2">
      {items.map(([label, detail]) => (
        <div key={label} className="rounded-xl border border-slate-800 bg-slate-900/40 px-3 py-2">
          <dt className="text-xs font-bold text-teal-300">{label}</dt>
          <dd className="text-xs text-slate-300">{detail}</dd>
        </div>
      ))}
    </dl>
  )
}

function NumberLine({ min, max, points }) {
  const width = 600
  const pad = 30
  const x = (value) => pad + ((value - min) / (max - min || 1)) * (width - 2 * pad)
  const ticks = []
  const span = max - min
  const step = span <= 2 ? 0.25 : span <= 20 ? 1 : Math.ceil(span / 10)
  for (let v = min; v <= max + 1e-9; v += step) ticks.push(Math.round(v * 100) / 100)
  return (
    <svg viewBox={`0 0 ${width} 90`} className="w-full" role="img" aria-label="Number line">
      <line x1={pad} y1="50" x2={width - pad} y2="50" stroke="currentColor" className="text-slate-500" strokeWidth="2" />
      {ticks.map((t) => (
        <g key={t}>
          <line x1={x(t)} y1="45" x2={x(t)} y2="55" stroke="currentColor" className="text-slate-500" />
          <text x={x(t)} y="72" textAnchor="middle" className="fill-slate-400" fontSize="11">
            {t}
          </text>
        </g>
      ))}
      {points.map(([value, label], i) => (
        <g key={i}>
          <circle cx={x(value)} cy="50" r="5" className="fill-indigo-400" />
          <text x={x(value)} y={i % 2 ? 20 : 32} textAnchor="middle" className="fill-indigo-200" fontSize="11">
            {label}
          </text>
        </g>
      ))}
    </svg>
  )
}

function Bar({ items, unit }) {
  const max = Math.max(...items.map(([, v]) => v), 1)
  return (
    <div className="space-y-2">
      {items.map(([label, value]) => (
        <div key={label} className="flex items-center gap-3 text-xs">
          <span className="w-36 shrink-0 text-slate-300">{label}</span>
          <div className="h-4 flex-1 rounded bg-slate-900">
            <div className="h-4 rounded bg-teal-500/70" style={{ width: `${(value / max) * 100}%` }} />
          </div>
          <span className="w-16 text-right font-semibold text-slate-200">
            {unit === '₹' ? `₹${value}` : `${value}${unit ? ` ${unit}` : ''}`}
          </span>
        </div>
      ))}
    </div>
  )
}

export default function LessonDiagram({ diagram }) {
  if (!diagram) return null
  const { type, title } = diagram
  let body = null
  if (type === 'flow' || type === 'cycle') body = <Flow items={diagram.items || []} cycle={type === 'cycle'} />
  else if (type === 'table') body = <Table columns={diagram.columns || []} rows={diagram.rows || []} />
  else if (type === 'labelled') body = <Labelled items={diagram.items || []} />
  else if (type === 'number_line') body = <NumberLine min={diagram.min} max={diagram.max} points={diagram.points || []} />
  else if (type === 'bar') body = <Bar items={diagram.items || []} unit={diagram.unit} />
  if (!body) return null

  return (
    <figure className="rounded-2xl border border-slate-800 bg-slate-950/40 p-4 space-y-3">
      {title && <figcaption className="text-xs font-bold uppercase tracking-wider text-slate-400">{title}</figcaption>}
      {body}
    </figure>
  )
}
