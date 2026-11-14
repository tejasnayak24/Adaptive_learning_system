import React from 'react'
import {
  Bar,
  BarChart,
  CartesianGrid,
  Line,
  LineChart,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from 'recharts'
import {
  ATTENTION_COLOR,
  SCORE_COLOR,
  TELEMETRY_HELP,
  attentionSummary,
  formatDate,
  formatPercent,
  observationText
} from '../utils/analytics'
import { Panel, TelemetryBadge } from './AnalyticsPanels'

// Chart components live in their own module so that only pages that draw
// charts (Progress & Analytics) load the charting library.

const AXIS = { stroke: '#475569', fontSize: 11, tickLine: false }
const GRID = { strokeDasharray: '3 3', stroke: '#1e293b', vertical: false }

const TONES = {
  emerald: 'bg-emerald-500/10 text-emerald-300 border-emerald-500/25',
  amber: 'bg-amber-500/10 text-amber-300 border-amber-500/25',
  slate: 'bg-slate-800/60 text-slate-300 border-slate-700'
}

// ------------------------------------------------------------------ charts

function ChartTooltip({ active, payload, kind }) {
  if (!active || !payload?.length) return null
  const row = payload[0].payload
  return (
    <div className="rounded-xl border border-slate-700 bg-slate-950/95 px-3 py-2 text-xs shadow-xl space-y-0.5 max-w-[240px]">
      {kind === 'week' ? (
        <>
          <p className="font-semibold text-white">Week of {formatDate(row.week)}</p>
          <p className="text-slate-300">
            {row.attempts} quiz attempt{row.attempts === 1 ? '' : 's'}
          </p>
        </>
      ) : (
        <>
          <p className="font-semibold text-white">
            Attempt {row.label} · {kind === 'attention' ? `${formatPercent(row.attention)} attention` : formatPercent(row.score)}
          </p>
          <p className="text-slate-300 truncate">{row.lesson}</p>
          <p className="text-slate-500">
            {row.subject} · {String(row.difficulty || '').toLowerCase()}
            {row.mode && row.mode !== 'standard' ? ` · ${row.mode}` : ''}
          </p>
          <p className="text-slate-500">{formatDate(row.at, { withTime: true })}</p>
        </>
      )}
    </div>
  )
}

export function ScoreTrendChart({ rows, passScore = 50, height = 260 }) {
  return (
    <div style={{ height }} role="img" aria-label="Line chart of quiz scores by attempt">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={rows} margin={{ top: 8, right: 12, left: -18, bottom: 0 }}>
          <CartesianGrid {...GRID} />
          <XAxis dataKey="label" {...AXIS} minTickGap={16} />
          <YAxis {...AXIS} domain={[0, 100]} ticks={[0, 25, 50, 75, 100]} unit="%" />
          <ReferenceLine
            y={passScore}
            stroke="#64748b"
            strokeDasharray="4 4"
            label={{ value: `Pass ${passScore}%`, position: 'insideTopRight', fill: '#94a3b8', fontSize: 10 }}
          />
          <Tooltip content={<ChartTooltip kind="score" />} cursor={{ stroke: '#334155' }} />
          <Line
            type="monotone"
            dataKey="score"
            name="Quiz score"
            stroke={SCORE_COLOR}
            strokeWidth={2}
            dot={{ r: 4, strokeWidth: 2, stroke: '#07090e', fill: SCORE_COLOR }}
            activeDot={{ r: 6 }}
            isAnimationActive={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

export function WeeklyActivityChart({ weeks, height = 200 }) {
  return (
    <div style={{ height }} role="img" aria-label="Bar chart of quiz attempts per week">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={weeks} margin={{ top: 8, right: 12, left: -24, bottom: 0 }}>
          <CartesianGrid {...GRID} />
          <XAxis
            dataKey="week"
            {...AXIS}
            minTickGap={12}
            tickFormatter={(w) => new Date(`${w}T00:00:00`).toLocaleDateString(undefined, { day: 'numeric', month: 'short' })}
          />
          <YAxis {...AXIS} allowDecimals={false} />
          <Tooltip content={<ChartTooltip kind="week" />} cursor={{ fill: '#1e293b55' }} />
          <Bar dataKey="attempts" name="Quiz attempts" fill={SCORE_COLOR} radius={[4, 4, 0, 0]} maxBarSize={36} isAnimationActive={false} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

// --------------------------------------------------------------- attention

export function AttentionPanel({ attention, trendRows }) {
  const summary = attentionSummary(attention)
  const measuredRows = (trendRows || []).filter((r) => r.attention !== null && r.attention !== undefined)

  return (
    <Panel
      title="Focus during quizzes (camera)"
      subtitle="The camera agent measures attention while you take a quiz. Aegis stores one average per quiz, not a continuous recording, so these figures describe your quizzes only."
    >
      <p
        className={`rounded-2xl border px-4 py-3 text-xs leading-relaxed ${
          summary.level === 'ok' ? TONES.emerald : summary.level === 'limited' ? TONES.amber : TONES.slate
        }`}
      >
        {summary.message}
      </p>

      {attention && attention.attempts_total > 0 && (
        <>
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
            <MiniStat
              label="Average attention"
              value={formatPercent(attention.average_attention)}
              note={attention.measured_attempts ? `${attention.measured_attempts} measured quizzes` : 'no measurements'}
            />
            <MiniStat label="Yawning seen in" value={observationText(attention.yawning)} />
            <MiniStat label="Looking away seen in" value={observationText(attention.looking_away)} />
            <MiniStat label="Drowsiness seen in" value={observationText(attention.drowsiness)} />
          </div>

          <div className="flex flex-wrap gap-2 text-[11px]">
            <span className="inline-flex items-center gap-1.5">
              <TelemetryBadge telemetry="measured" />
              <span className="text-slate-400 tabular-nums">{attention.measured_attempts}</span>
            </span>
            <span className="inline-flex items-center gap-1.5">
              <TelemetryBadge telemetry="unavailable" />
              <span className="text-slate-400 tabular-nums">{attention.unavailable_attempts}</span>
            </span>
            {attention.not_monitored_attempts > 0 && (
              <span className="inline-flex items-center gap-1.5">
                <TelemetryBadge telemetry="not_monitored" />
                <span className="text-slate-400 tabular-nums">{attention.not_monitored_attempts}</span>
              </span>
            )}
          </div>
          {attention.unavailable_attempts > 0 && (
            <p className="text-[11px] text-slate-500 leading-relaxed">{TELEMETRY_HELP.unavailable}</p>
          )}

          {measuredRows.length >= 2 ? (
            <div style={{ height: 200 }} role="img" aria-label="Line chart of attention per measured quiz">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={measuredRows} margin={{ top: 8, right: 12, left: -18, bottom: 0 }}>
                  <CartesianGrid {...GRID} />
                  <XAxis dataKey="label" {...AXIS} minTickGap={16} />
                  <YAxis {...AXIS} domain={[0, 100]} ticks={[0, 50, 100]} unit="%" />
                  <Tooltip content={<ChartTooltip kind="attention" />} cursor={{ stroke: '#334155' }} />
                  <Line
                    type="monotone"
                    dataKey="attention"
                    name="Attention"
                    stroke={ATTENTION_COLOR}
                    strokeWidth={2}
                    dot={{ r: 4, strokeWidth: 2, stroke: '#07090e', fill: ATTENTION_COLOR }}
                    isAnimationActive={false}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <p className="text-xs text-slate-500">
              The attention trend appears once at least two quizzes have a camera measurement. Quiz numbers match the score trend above.
            </p>
          )}

          {attention.by_subject?.length > 1 && (
            <ul className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
              {attention.by_subject.map((s) => (
                <li key={s.subject} className="flex justify-between rounded-xl bg-slate-900/40 border border-slate-800 px-3 py-2">
                  <span className="text-slate-300">{s.subject}</span>
                  <span className="text-slate-200 font-semibold tabular-nums">
                    {formatPercent(s.average_attention)}{' '}
                    <span className="text-slate-500 font-normal">({s.measured_attempts})</span>
                  </span>
                </li>
              ))}
            </ul>
          )}
        </>
      )}
    </Panel>
  )
}

function MiniStat({ label, value, note }) {
  return (
    <div className="rounded-2xl bg-slate-900/40 border border-slate-800 p-3">
      <p className="text-[10px] font-semibold uppercase tracking-wider text-slate-500">{label}</p>
      <p className="mt-1 text-sm font-bold text-white">{value}</p>
      {note && <p className="text-[10px] text-slate-500">{note}</p>}
    </div>
  )
}
