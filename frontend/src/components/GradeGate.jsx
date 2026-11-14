import React, { useState } from 'react'
import { useAuth } from '../context/AuthContext'

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
    <div className="max-w-2xl mx-auto glass-panel rounded-3xl p-8 border border-slate-900 shadow-xl space-y-6 text-center">
      <div className="space-y-2">
        <h1 className="font-display text-2xl font-extrabold text-white">{title || 'Which grade are you in?'}</h1>
        <p className="text-sm text-slate-400">
          {subtitle ||
            'Aegis shows the Mathematics, Science, Social Science and English lessons for your grade. You can change this later.'}
        </p>
      </div>
      <div className="grid grid-cols-5 gap-3">
        {GRADES.map((grade) => (
          <button
            key={grade}
            onClick={() => choose(grade)}
            disabled={saving !== null}
            className={`rounded-2xl border py-5 font-display text-2xl font-extrabold transition-all ${
              current === grade
                ? 'border-indigo-500 bg-indigo-500/20 text-white'
                : 'border-slate-800 bg-slate-900/50 text-slate-300 hover:border-indigo-500/60 hover:text-white'
            } disabled:opacity-50`}
          >
            {saving === grade ? '…' : grade}
            <span className="block text-[10px] font-semibold uppercase tracking-wider text-slate-500">Grade</span>
          </button>
        ))}
      </div>
      {error && <p className="text-xs text-rose-400">{error}</p>}
    </div>
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
