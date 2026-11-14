import React, { useState } from 'react'
import { GraduationCap, LoaderCircle } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import { Callout, Card, cx } from './ui'

export const GRADES = [6, 7, 8, 9, 10]

// Shown instead of the page when a student has no grade yet (accounts
// created before grades existed). Choosing one keeps all existing progress.
export function GradePicker({ current, onPicked, title, subtitle }) {
  const { setGrade } = useAuth()
  const [saving, setSaving] = useState(null)
  const [error, setError] = useState('')

  const choose = async (grade) => {
    setSaving(grade)
    setError('')
    try {
      await setGrade(grade)
      onPicked?.(grade)
    } catch (err) {
      setError(err.message || 'Could not save your grade')
    } finally {
      setSaving(null)
    }
  }

  return (
    <Card padding="lg" className="mx-auto max-w-2xl space-y-7 text-center">
      <div className="space-y-3">
        <span className="mx-auto grid h-12 w-12 place-items-center rounded-2xl bg-brand-500/[0.12] text-brand-300 ring-1 ring-inset ring-brand-500/25">
          <GraduationCap size={24} aria-hidden="true" />
        </span>
        <h1 className="font-display text-2xl font-semibold tracking-tight text-ink">{title || 'Which grade are you in?'}</h1>
        <p className="mx-auto max-w-md text-sm leading-relaxed text-ink-2">
          {subtitle ||
            'Aegis shows the Mathematics, Science, Social Science and English lessons for your grade. You can change this later.'}
        </p>
      </div>
      <div className="grid grid-cols-5 gap-2 sm:gap-3" role="group" aria-label="Grades">
        {GRADES.map((grade) => {
          const selected = current === grade
          return (
            <button
              key={grade}
              type="button"
              onClick={() => choose(grade)}
              disabled={saving !== null}
              aria-pressed={selected}
              className={cx(
                'group flex flex-col items-center justify-center gap-1 rounded-xl border py-4 transition-[border-color,background-color,transform] duration-200 active:scale-[0.97] disabled:opacity-60 sm:py-5',
                selected
                  ? 'border-brand-500/60 bg-brand-500/[0.12] text-ink'
                  : 'border-line-strong bg-deep text-ink-2 hover:border-brand-500/40 hover:bg-brand-500/[0.05] hover:text-ink'
              )}
            >
              <span className="font-display text-2xl font-semibold sm:text-3xl">
                {saving === grade ? <LoaderCircle size={24} className="animate-spin" aria-label="Saving" /> : grade}
              </span>
              <span className="text-[10px] font-semibold uppercase tracking-[0.12em] text-ink-2">Grade</span>
            </button>
          )
        })}
      </div>
      {error && (
        <Callout tone="danger" role="alert" className="text-left">
          {error}
        </Callout>
      )}
    </Card>
  )
}

export default function GradeGate({ children }) {
  const { user } = useAuth()
  const needsGrade = user && (user.role || 'student') === 'student' && !user.grade
  if (needsGrade) {
    return <GradePicker />
  }
  return children
}
