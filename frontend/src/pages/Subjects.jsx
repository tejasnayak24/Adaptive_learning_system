import React, { useEffect, useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { GradePicker } from '../components/GradeGate'
import { SUBJECTS, curriculumService } from '../services/curriculumService'

const LEVEL_STYLE = {
  EASY: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
  MEDIUM: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
  HARD: 'bg-rose-500/10 text-rose-400 border-rose-500/20'
}

const SUBJECT_ICON = { Mathematics: '➗', Science: '🔬', 'Social Science': '🌏', English: '📖' }

function LessonCard({ lesson, subject }) {
  const status = lesson.best_score >= 80 ? 'Mastered' : lesson.attempts > 0 ? 'In progress' : 'Not started'
  const statusStyle =
    status === 'Mastered'
      ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
      : status === 'In progress'
        ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
        : 'bg-slate-800 text-slate-400'

  return (
    <div className="glass-panel glass-panel-hover rounded-3xl p-5 border border-slate-900 shadow-md flex flex-col justify-between gap-4">
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider">Lesson {lesson.position}</span>
          <span className={`px-2 py-0.5 text-[9px] font-bold rounded-full ${statusStyle}`}>{status}</span>
        </div>
        <h4 className="text-base font-bold text-white leading-snug">{lesson.title}</h4>
        <div className="flex flex-wrap gap-1.5">
          {lesson.quizzes.map((quiz) => (
            <span key={quiz.id} className={`px-2 py-0.5 text-[9px] font-bold rounded border ${LEVEL_STYLE[quiz.difficulty] || ''}`}>
              {quiz.difficulty}
            </span>
          ))}
        </div>
      </div>
      <div className="border-t border-slate-800/60 pt-3 flex items-center justify-between">
        <p className="text-xs text-slate-400">
          {lesson.attempts > 0 ? (
            <>
              Best <span className="font-extrabold text-white">{Math.round(lesson.best_score)}%</span> · {lesson.attempts}{' '}
              attempt{lesson.attempts === 1 ? '' : 's'}
            </>
          ) : (
            'No attempts yet'
          )}
        </p>
        <Link
          to={`/lesson/${lesson.id}`}
          state={{ subject }}
          className="inline-flex px-4 py-2 rounded-xl bg-slate-900 hover:bg-indigo-600 border border-slate-800 hover:border-indigo-600 text-xs font-semibold text-slate-200 hover:text-white transition-all"
        >
          {lesson.attempts > 0 ? 'Continue' : 'Start'}
        </Link>
      </div>
    </div>
  )
}

export default function Subjects() {
  const { user } = useAuth()
  const [curriculum, setCurriculum] = useState(null)
  const location = useLocation()
  // Analytics pages link here with the subject to open.
  const [selectedSubject, setSelectedSubject] = useState(
    SUBJECTS.includes(location.state?.subject) ? location.state.subject : SUBJECTS[0]
  )
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [changingGrade, setChangingGrade] = useState(false)

  useEffect(() => {
    let cancelled = false
    async function load() {
      setLoading(true)
      setError('')
      try {
        const res = await curriculumService.getCurriculum()
        if (!cancelled) setCurriculum(res.data)
      } catch (err) {
        if (!cancelled) setError(err.message || 'Failed to load your curriculum')
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    load()
    return () => {
      cancelled = true
    }
  }, [user?.grade])

  if (changingGrade) {
    return (
      <div className="space-y-4">
        <GradePicker
          current={user?.grade}
          title="Change your grade"
          subtitle="Your previous quiz results are kept. You will see the lessons for the grade you choose."
          onPicked={() => setChangingGrade(false)}
        />
        <div className="text-center">
          <button onClick={() => setChangingGrade(false)} className="text-xs font-semibold text-slate-400 hover:text-slate-200">
            Cancel
          </button>
        </div>
      </div>
    )
  }

  if (loading) {
    return (
      <div className="space-y-6 animate-pulse">
        <div className="h-10 w-1/4 bg-slate-800 rounded-xl"></div>
        <div className="h-4 w-1/2 bg-slate-800 rounded-lg"></div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 pt-6">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="h-48 bg-slate-800 rounded-3xl"></div>
          ))}
        </div>
      </div>
    )
  }

  const subjects = curriculum?.subjects || []
  const subject = subjects.find((s) => s.subject === selectedSubject)

  return (
    <div className="space-y-8">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div className="space-y-1.5">
          <h1 className="font-display text-3xl font-extrabold tracking-tight text-white md:text-4xl">Curriculum Browser</h1>
          <p className="text-slate-400 text-sm leading-relaxed max-w-2xl">
            Your Grade {curriculum?.grade ?? user?.grade} lessons, organised by subject, unit and topic. Each lesson has
            explanations, worked examples and Easy, Medium and Hard quizzes.
          </p>
        </div>
        {(user?.role || 'student') === 'student' && (
          <button
            onClick={() => setChangingGrade(true)}
            className="self-start rounded-xl border border-slate-800 bg-slate-950 px-4 py-2 text-xs font-semibold text-slate-300 hover:text-white"
          >
            Grade {user?.grade} · Change
          </button>
        )}
      </div>

      {error && (
        <div className="rounded-2xl bg-rose-500/10 border border-rose-500/20 p-4 text-sm text-rose-400">{error}</div>
      )}

      <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
        {SUBJECTS.map((name) => {
          const data = subjects.find((s) => s.subject === name)
          const total = data?.lesson_count || 0
          const done = data?.lessons_attempted || 0
          const selected = selectedSubject === name
          return (
            <button
              key={name}
              onClick={() => setSelectedSubject(name)}
              className={`rounded-2xl border p-4 text-left transition-all ${
                selected
                  ? 'bg-indigo-500/15 border-indigo-500 shadow-md shadow-indigo-500/20'
                  : 'bg-slate-950 border-slate-900 hover:border-slate-700'
              }`}
            >
              <p className="text-xl">{SUBJECT_ICON[name]}</p>
              <p className="mt-1 text-sm font-bold text-white">{name}</p>
              <p className="text-[11px] text-slate-400">
                {done}/{total} lessons started
              </p>
              <div className="mt-2 h-1.5 w-full rounded-full bg-slate-900">
                <div
                  className="h-1.5 rounded-full bg-teal-500"
                  style={{ width: `${total ? (done / total) * 100 : 0}%` }}
                />
              </div>
            </button>
          )
        })}
      </div>

      {!subject ? (
        <div className="glass-panel rounded-3xl p-12 border border-slate-900 shadow-md text-center space-y-3">
          <div className="text-5xl">📚</div>
          <h3 className="text-lg font-bold text-white">No lessons yet</h3>
          <p className="text-xs text-slate-400 max-w-sm mx-auto leading-relaxed">
            No {selectedSubject} lessons are available for your grade. Ask your teacher to import the curriculum.
          </p>
        </div>
      ) : (
        <div className="space-y-10">
          {subject.units.map((unit) => (
            <div key={unit.id} className="space-y-6">
              <div className="flex items-center gap-4">
                <h2 className="font-display text-xl font-bold text-white shrink-0 tracking-wide">{unit.title}</h2>
                <div className="h-px bg-slate-800/80 w-full"></div>
              </div>
              {unit.topics.map((topic) => (
                <div key={topic.id} className="space-y-3">
                  <div>
                    <h3 className="text-sm font-bold uppercase tracking-wider text-indigo-300">{topic.title}</h3>
                    {topic.description && <p className="text-xs text-slate-400">{topic.description}</p>}
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                    {topic.lessons.map((lesson) => (
                      <LessonCard key={lesson.id} lesson={lesson} subject={selectedSubject} />
                    ))}
                  </div>
                </div>
              ))}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
