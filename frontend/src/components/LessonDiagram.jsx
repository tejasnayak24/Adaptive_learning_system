import React from 'react'
import { ArrowRight, RotateCcw } from 'lucide-react'

// Renders the data-driven lesson diagrams stored in lesson material.
// Supported types: flow, cycle, table, labelled, number_line, bar.

function Flow({ items, cycle }) {
  return (
    <ol className="flex flex-wrap items-center gap-2">
      {items.map((item, index) => (
        <li key={index} className="flex items-center gap-2">
          <span className="rounded-lg border border-brand-500/30 bg-brand-500/[0.08] px-3 py-2 text-[13px] font-medium text-ink">{item}</span>
          {(index < items.length - 1 || cycle) &&
            (index === items.length - 1 ? (
              <RotateCcw size={16} className="text-brand-300" aria-label="back to the start" />
            ) : (
              <ArrowRight size={16} className="text-brand-300" aria-hidden="true" />
            ))}
        </li>
      ))}
    </ol>
  )
}

function Table({ columns, rows }) {
  return (
    <div className="overflow-x-auto rounded-xl border border-line">
      <table className="w-full min-w-[420px] border-collapse text-left text-[13px]">
        <thead>
          <tr className="bg-white/[0.03]">
            {columns.map((column) => (
              <th key={column} scope="col" className="border-b border-line px-3.5 py-2.5 font-semibold text-ink">
                {column}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-line/70">
          {rows.map((row, r) => (
            <tr key={r}>
              {row.map((cell, c) => (
                <td key={c} className="formula px-3.5 py-2.5 text-[#c9d1e2]">
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
    <dl className="grid grid-cols-1 gap-2.5 sm:grid-cols-2">
      {items.map(([label, detail]) => (
        <div key={label} className="rounded-xl border border-line bg-deep/60 px-3.5 py-2.5">
          <dt className="text-[13px] font-semibold text-mint-300">{label}</dt>
          <dd className="mt-0.5 text-[13px] leading-relaxed text-ink-2">{detail}</dd>
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
      <line x1={pad} y1="50" x2={width - pad} y2="50" stroke="#3a4664" strokeWidth="2" strokeLinecap="round" />
      {ticks.map((t) => (
        <g key={t}>
          <line x1={x(t)} y1="45" x2={x(t)} y2="55" stroke="#4f5b75" />
          <text x={x(t)} y="72" textAnchor="middle" fill="#a0abc0" fontSize="11">
            {t}
          </text>
        </g>
      ))}
      {points.map(([value, label], i) => (
        <g key={i}>
          <circle cx={x(value)} cy="50" r="5" fill="#8875ff" stroke="#090d18" strokeWidth="2" />
          <text x={x(value)} y={i % 2 ? 20 : 32} textAnchor="middle" fill="#f4f6ff" fontSize="11">
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
    <div className="space-y-2.5">
      {items.map(([label, value]) => (
        <div key={label} className="flex items-center gap-3 text-[13px]">
          <span className="w-28 shrink-0 text-ink-2 sm:w-36">{label}</span>
          <div className="h-3 flex-1 rounded-full bg-white/[0.06]">
            <div className="h-3 rounded-full bg-mint-500" style={{ width: `${(value / max) * 100}%` }} />
          </div>
          <span className="w-16 text-right font-semibold tabular-nums text-ink">
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
    <figure className="space-y-4 rounded-card border border-line bg-surface p-5 shadow-card">
      {title && <figcaption className="text-sm font-semibold text-ink">{title}</figcaption>}
      {body}
    </figure>
  )
}
