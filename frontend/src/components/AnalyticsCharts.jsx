import React, { useId, useState } from 'react'
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  LabelList,
  Line,
  LineChart,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from 'recharts'
import { ChartColumn, Table2 } from 'lucide-react'
import { ATTENTION_COLOR, SCORE_COLOR, SUBJECT_ORDER, formatDate, formatPercent, topicStatusInfo } from '../utils/analytics'
import { TOPIC_STATUS_COLORS, TOPIC_STATUS_VISUALS, subjectVisual } from './visuals'
import { useReducedMotion } from '../hooks/useReducedMotion'
import { Button, Card, DataTable, SectionHeader, cx, svgId } from './ui'

// Chart components live in their own module so only the pages that draw
// charts (Progress & Analytics) load the charting library.
//
// Marks follow one spec: 2px lines, markers r=4 with a 2px surface ring,
// bars at most 24px thick with 4px rounded data ends, a solid hairline grid,
// and text in ink colours (never the data colour).

const SURFACE = '#151c2d'
const GRID_STROKE = '#222b40'
const TICK = { fill: '#a0abc0', fontSize: 11 }
const AXIS = { stroke: GRID_STROKE, tickLine: false, axisLine: false, tick: TICK }
const MOTION = { animationDuration: 700, animationEasing: 'ease-out' }

/** Card with a chart and a "table" twin, so no value depends on hovering. */
export function ChartCard({ title, description, action, legend, table, className, children }) {
  const [asTable, setAsTable] = useState(false)
  const headingId = useId()
  return (
    <Card as="section" aria-labelledby={headingId} className={cx('space-y-4', className)}>
      <SectionHeader
        id={headingId}
        title={title}
        description={description}
        action={
          <>
            {action}
            {table && (
              <Button
                variant="ghost"
                size="xs"
                icon={asTable ? ChartColumn : Table2}
                onClick={() => setAsTable((value) => !value)}
                aria-pressed={asTable}
              >
                {asTable ? 'Chart' : 'Table'}
              </Button>
            )}
          </>
        }
      />
      {legend && !asTable && <div className="flex flex-wrap gap-x-4 gap-y-2 text-xs text-ink-2">{legend}</div>}
      {asTable && table ? (
        <DataTable caption={`${title} (table view)`} columns={table.columns} rows={table.rows} rowKey={table.rowKey} minWidth={360} />
      ) : (
        children
      )}
    </Card>
  )
}

export function LegendItem({ color, label, shape = 'square', icon: Icon }) {
  return (
    <span className="inline-flex items-center gap-1.5">
      {shape === 'line' ? (
        <span className="h-[2px] w-3.5 rounded-full" style={{ background: color }} aria-hidden="true" />
      ) : (
        <span className="h-2.5 w-2.5 rounded-[3px]" style={{ background: color }} aria-hidden="true" />
      )}
      {Icon && <Icon size={13} className="text-ink-2" aria-hidden="true" />}
      {label}
    </span>
  )
}

function TooltipCard({ children }) {
  return <div className="max-w-[260px] rounded-xl border border-line-strong bg-[#1e2740]/95 px-3 py-2.5 text-xs shadow-raised">{children}</div>
}

function KeyLine({ color }) {
  return <span className="mt-1.5 inline-block h-[2px] w-3 shrink-0 rounded-full" style={{ background: color }} aria-hidden="true" />
}

function AttemptTooltip({ active, payload, kind }) {
  if (!active || !payload?.length) return null
  const row = payload[0].payload
  const value = kind === 'attention' ? row.attention : row.score
  return (
    <TooltipCard>
      <div className="flex items-start gap-2">
        <KeyLine color={kind === 'attention' ? ATTENTION_COLOR : SCORE_COLOR} />
        <div className="min-w-0 space-y-0.5">
          <p className="text-sm font-semibold text-ink">
            {formatPercent(value)} <span className="text-xs font-normal text-ink-2">{kind === 'attention' ? 'attention' : 'score'}</span>
          </p>
          <p className="truncate text-ink">{row.lesson}</p>
          <p className="text-ink-2">
            Attempt {row.label} · {row.subject} · {String(row.difficulty || '').toLowerCase()}
            {row.mode && row.mode !== 'standard' ? ` · ${row.mode}` : ''}
          </p>
          <p className="text-ink-2">{formatDate(row.at, { withTime: true })}</p>
        </div>
      </div>
    </TooltipCard>
  )
}

function weekLabel(week, long = false) {
  const date = new Date(`${week}T00:00:00`)
  return date.toLocaleDateString(undefined, long ? { day: 'numeric', month: 'short', year: 'numeric' } : { day: 'numeric', month: 'short' })
}

function WeekTooltip({ active, payload }) {
  if (!active || !payload?.length) return null
  const row = payload[0].payload
  return (
    <TooltipCard>
      <p className="text-sm font-semibold text-ink">
        {row.attempts} <span className="text-xs font-normal text-ink-2">quiz attempt{row.attempts === 1 ? '' : 's'}</span>
      </p>
      <p className="text-ink-2">Week of {weekLabel(row.week, true)}</p>
    </TooltipCard>
  )
}

/** Quiz score per attempt with the pass mark. One series: the title names it. */
export function ScoreTrendChart({ rows, passScore = 50, height = 280 }) {
  const reduced = useReducedMotion()
  const fillId = svgId(useId())
  return (
    <div style={{ height }} role="img" aria-label={`Area chart of ${rows.length} quiz scores in order, with the ${passScore}% pass mark`}>
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={rows} margin={{ top: 12, right: 14, left: 0, bottom: 0 }}>
          <defs>
            <linearGradient id={fillId} x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={SCORE_COLOR} stopOpacity={0.22} />
              <stop offset="100%" stopColor={SCORE_COLOR} stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid stroke={GRID_STROKE} vertical={false} />
          <XAxis dataKey="label" {...AXIS} minTickGap={18} tickMargin={8} />
          <YAxis {...AXIS} domain={[0, 100]} ticks={[0, 25, 50, 75, 100]} tickFormatter={(v) => `${v}%`} width={42} />
          <ReferenceLine
            y={passScore}
            stroke="#69758c"
            strokeDasharray="4 4"
            label={{ value: `Pass ${passScore}%`, position: 'insideTopRight', fill: '#a0abc0', fontSize: 11 }}
          />
          <Tooltip content={<AttemptTooltip kind="score" />} cursor={{ stroke: '#3a4664', strokeWidth: 1 }} />
          <Area
            type="monotone"
            dataKey="score"
            name="Quiz score"
            stroke={SCORE_COLOR}
            strokeWidth={2}
            fill={`url(#${fillId})`}
            dot={{ r: 4, strokeWidth: 2, stroke: SURFACE, fill: SCORE_COLOR }}
            activeDot={{ r: 6, strokeWidth: 2, stroke: SURFACE, fill: SCORE_COLOR }}
            isAnimationActive={!reduced}
            {...MOTION}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  )
}

/** Attention per measured quiz (camera). One series. */
export function AttentionTrendChart({ rows, height = 220 }) {
  const reduced = useReducedMotion()
  return (
    <div style={{ height }} role="img" aria-label={`Line chart of attention in ${rows.length} measured quizzes`}>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={rows} margin={{ top: 12, right: 14, left: 0, bottom: 0 }}>
          <CartesianGrid stroke={GRID_STROKE} vertical={false} />
          <XAxis dataKey="label" {...AXIS} minTickGap={18} tickMargin={8} />
          <YAxis {...AXIS} domain={[0, 100]} ticks={[0, 50, 100]} tickFormatter={(v) => `${v}%`} width={42} />
          <Tooltip content={<AttemptTooltip kind="attention" />} cursor={{ stroke: '#3a4664', strokeWidth: 1 }} />
          <Line
            type="monotone"
            dataKey="attention"
            name="Attention"
            stroke={ATTENTION_COLOR}
            strokeWidth={2}
            dot={{ r: 4, strokeWidth: 2, stroke: SURFACE, fill: ATTENTION_COLOR }}
            activeDot={{ r: 6, strokeWidth: 2, stroke: SURFACE, fill: ATTENTION_COLOR }}
            isAnimationActive={!reduced}
            {...MOTION}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

/** Quiz attempts per week. One series. */
export function WeeklyActivityChart({ weeks, height = 220 }) {
  const reduced = useReducedMotion()
  return (
    <div style={{ height }} role="img" aria-label={`Column chart of quiz attempts per week over ${weeks.length} weeks`}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={weeks} margin={{ top: 12, right: 14, left: 0, bottom: 0 }}>
          <CartesianGrid stroke={GRID_STROKE} vertical={false} />
          <XAxis dataKey="week" {...AXIS} minTickGap={14} tickMargin={8} tickFormatter={(w) => weekLabel(w)} />
          <YAxis {...AXIS} allowDecimals={false} width={30} />
          <Tooltip content={<WeekTooltip />} cursor={{ fill: 'rgb(255 255 255 / 0.03)' }} />
          <Bar
            dataKey="attempts"
            name="Quiz attempts"
            fill={SCORE_COLOR}
            radius={[4, 4, 0, 0]}
            maxBarSize={24}
            isAnimationActive={!reduced}
            {...MOTION}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

function SubjectTooltip({ active, payload }) {
  if (!active || !payload?.length) return null
  const row = payload[0].payload
  return (
    <TooltipCard>
      <div className="flex items-start gap-2">
        <KeyLine color={subjectVisual(row.subject).color} />
        <div className="space-y-0.5">
          <p className="text-sm font-semibold text-ink">
            {formatPercent(row.score)} <span className="text-xs font-normal text-ink-2">average score</span>
          </p>
          <p className="text-ink">{row.subject}</p>
          <p className="text-ink-2">
            {row.attempts} quiz{row.attempts === 1 ? '' : 'zes'} · {row.completed}/{row.total} lessons passed
          </p>
        </div>
      </div>
    </TooltipCard>
  )
}

/** Average score by subject (subjects with at least one quiz), named on the axis. */
export function SubjectScoreChart({ subjects, passScore = 50 }) {
  const reduced = useReducedMotion()
  const rows = SUBJECT_ORDER.map((name) => subjects.find((s) => s.subject === name))
    .filter((s) => s && s.quiz_attempts > 0 && s.average_score !== null && s.average_score !== undefined)
    .map((s) => ({
      subject: s.subject,
      score: Math.round(s.average_score),
      attempts: s.quiz_attempts,
      completed: s.lessons_completed,
      total: s.lessons_total
    }))
  if (!rows.length) return null
  const height = rows.length * 44 + 36
  return (
    <div style={{ height }} role="img" aria-label="Bar chart of average quiz score by subject">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={rows} layout="vertical" margin={{ top: 4, right: 44, left: 0, bottom: 0 }} barCategoryGap={10}>
          <CartesianGrid stroke={GRID_STROKE} horizontal={false} />
          <XAxis type="number" domain={[0, 100]} ticks={[0, 25, 50, 75, 100]} tickFormatter={(v) => `${v}%`} {...AXIS} />
          <YAxis type="category" dataKey="subject" {...AXIS} width={112} tick={{ ...TICK, fill: '#f4f6ff', fontSize: 12 }} />
          <ReferenceLine x={passScore} stroke="#69758c" strokeDasharray="4 4" />
          <Tooltip content={<SubjectTooltip />} cursor={{ fill: 'rgb(255 255 255 / 0.03)' }} />
          <Bar dataKey="score" name="Average score" barSize={20} radius={[0, 4, 4, 0]} isAnimationActive={!reduced} {...MOTION}>
            {rows.map((row) => (
              <Cell key={row.subject} fill={subjectVisual(row.subject).color} />
            ))}
            <LabelList dataKey="score" position="right" formatter={(v) => `${v}%`} fill="#f4f6ff" fontSize={12} />
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

export const TOPIC_STATUS_KEYS = ['strong', 'needs_revision', 'weak', 'insufficient_data', 'not_started']

/** Topic counts by status for each subject. */
export function topicStatusRows(topics) {
  return SUBJECT_ORDER.map((subject) => {
    const own = (topics || []).filter((t) => t.subject === subject)
    if (!own.length) return null
    const row = { subject, total: own.length }
    for (const key of TOPIC_STATUS_KEYS) row[key] = own.filter((t) => t.status === key).length
    return row
  }).filter(Boolean)
}

function TopicStatusTooltip({ active, payload }) {
  if (!active || !payload?.length) return null
  const row = payload[0].payload
  return (
    <TooltipCard>
      <p className="mb-1.5 text-sm font-semibold text-ink">{row.subject}</p>
      <ul className="space-y-1">
        {TOPIC_STATUS_KEYS.filter((key) => row[key] > 0).map((key) => (
          <li key={key} className="flex items-center justify-between gap-4">
            <span className="flex items-center gap-1.5 text-ink-2">
              <KeyLine color={TOPIC_STATUS_COLORS[key]} />
              {topicStatusInfo(key).label}
            </span>
            <span className="font-semibold text-ink tabular-nums">{row[key]}</span>
          </li>
        ))}
      </ul>
    </TooltipCard>
  )
}

/** Each subject's topics split by status: one bar per subject, parts in status order. */
export function TopicStatusChart({ topics }) {
  const reduced = useReducedMotion()
  const rows = topicStatusRows(topics)
  if (!rows.length) return null
  const height = rows.length * 44 + 8
  return (
    <div style={{ height }} role="img" aria-label="Stacked bar chart of topic status counts for each subject">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={rows} layout="vertical" margin={{ top: 4, right: 8, left: 0, bottom: 4 }} barCategoryGap={12}>
          <XAxis type="number" hide domain={[0, 'dataMax']} />
          <YAxis type="category" dataKey="subject" {...AXIS} width={112} tick={{ ...TICK, fill: '#f4f6ff', fontSize: 12 }} />
          <Tooltip content={<TopicStatusTooltip />} cursor={{ fill: 'rgb(255 255 255 / 0.03)' }} />
          {TOPIC_STATUS_KEYS.map((key) => (
            <Bar
              key={key}
              dataKey={key}
              stackId="topics"
              name={topicStatusInfo(key).label}
              fill={TOPIC_STATUS_COLORS[key]}
              stroke={SURFACE}
              strokeWidth={2}
              barSize={22}
              radius={3}
              isAnimationActive={!reduced}
              {...MOTION}
            />
          ))}
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

export function TopicStatusLegend() {
  return TOPIC_STATUS_KEYS.map((key) => (
    <LegendItem key={key} color={TOPIC_STATUS_COLORS[key]} icon={TOPIC_STATUS_VISUALS[key].icon} label={topicStatusInfo(key).label} />
  ))
}
