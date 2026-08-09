import React, { useEffect, useState } from 'react'
import { Link, useParams, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { lessonService } from '../services/lessonService'
import { progressService } from '../services/progressService'

export default function LessonDetail() {
  const { id } = useParams()
  const { user } = useAuth()
  const navigate = useNavigate()
  const [lesson, setLesson] = useState(null)
  const [lessonProgress, setLessonProgress] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function loadLessonData() {
      try {
        const lessonRes = await lessonService.getLesson(id)
        if (lessonRes.success) {
          setLesson(lessonRes.data)
        }

        const progressRes = await progressService.getStudentProgress(user.id)
        if (progressRes.success) {
          // Filter progress logs for this specific lesson
          const filtered = progressRes.data.filter(p => p.lesson_id === parseInt(id, 10))
          setLessonProgress(filtered)
        }
      } catch (err) {
        setError(err.message || 'Failed to load lesson content')
      } finally {
        setLoading(false)
      }
    }
    loadLessonData()
  }, [id, user.id])

  if (loading) {
    return (
      <div className="space-y-6 animate-pulse">
        <div className="h-4 w-20 bg-slate-800 rounded"></div>
        <div className="h-10 w-2/3 bg-slate-800 rounded-xl"></div>
        <div className="h-6 w-1/4 bg-slate-800 rounded-lg"></div>
        <div className="space-y-3 pt-6">
          <div className="h-4 w-full bg-slate-800 rounded"></div>
          <div className="h-4 w-full bg-slate-800 rounded"></div>
          <div className="h-4 w-3/4 bg-slate-800 rounded"></div>
        </div>
        <div className="h-40 bg-slate-800 rounded-3xl mt-8"></div>
      </div>
    )
  }

  if (error || !lesson) {
    return (
      <div className="space-y-6">
        <Link to="/subjects" className="text-sm font-semibold text-indigo-400 hover:text-indigo-300 flex items-center gap-1">
          &larr; Back to Curriculum
        </Link>
        <div className="rounded-2xl bg-rose-500/10 border border-rose-500/20 p-6 text-center text-rose-400">
          <p className="font-bold">Error loading lesson</p>
          <p className="text-xs mt-1 text-rose-300/80">{error || 'Lesson not found'}</p>
        </div>
      </div>
    )
  }

  // Extract quizzes associated with this lesson
  const quizzes = lesson.quizzes || []
  
  const getQuizByDifficulty = (diff) => {
    return quizzes.find(q => q.difficulty.toLowerCase() === diff.toLowerCase())
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Navigation Breadcrumb */}
      <div>
        <Link 
          to="/subjects" 
          className="inline-flex items-center gap-1 text-xs font-semibold uppercase tracking-wider text-indigo-400 hover:text-indigo-300 transition-colors"
        >
          <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M15 19l-7-7 7-7" />
          </svg>
          Curriculum Browser
        </Link>
      </div>

      {/* Header Info */}
      <div className="space-y-3 border-b border-slate-900 pb-6">
        <div className="flex items-center gap-2">
          <span className="px-2.5 py-0.5 text-[10px] font-semibold bg-slate-900 text-slate-400 border border-slate-800 rounded">
            Science
          </span>
          <span className="text-slate-600">&bull;</span>
          <span className="text-xs font-medium text-slate-400">
            Topic: {lesson.topic}
          </span>
        </div>
        <h1 className="font-display text-3xl md:text-4xl font-extrabold text-white tracking-tight">
          {lesson.title}
        </h1>
      </div>

      {/* Reading pane */}
      <article className="prose prose-invert max-w-none text-slate-300 leading-relaxed text-sm md:text-base space-y-6">
        {lesson.content.split('\n\n').map((paragraph, index) => (
          <p key={index} className="indent-0">
            {paragraph}
          </p>
        ))}
      </article>

      {/* Assessments Section */}
      <div className="glass-panel rounded-3xl p-6 md:p-8 border border-slate-900 shadow-xl space-y-6 mt-12 relative overflow-hidden">
        <div className="absolute top-0 right-0 h-32 w-32 bg-indigo-500/5 blur-2xl pointer-events-none"></div>
        
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <span>📝</span> Assessments
          </h3>
          <p className="text-xs text-slate-500 mt-1">
            Choose a quiz difficulty below. Aegis will dynamically adapt the curriculum based on your performance.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {['Easy', 'Medium', 'Hard'].map((diff) => {
            const quiz = getQuizByDifficulty(diff)
            const attemptsCount = lessonProgress.filter(p => p.difficulty.toLowerCase() === diff.toLowerCase()).length
            const bestAttempt = lessonProgress
              .filter(p => p.difficulty.toLowerCase() === diff.toLowerCase())
              .sort((a, b) => b.quiz_score - a.quiz_score)[0]

            return (
              <div 
                key={diff}
                className="rounded-2xl p-5 border bg-slate-900/30 border-slate-800/80 hover:border-slate-700/60 flex flex-col justify-between h-44 transition-all duration-300"
              >
                <div>
                  <div className="flex items-center justify-between">
                    <span className={`px-2 py-0.5 text-[9px] font-bold rounded ${
                      diff === 'Easy' 
                        ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' 
                        : diff === 'Medium' 
                        ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20' 
                        : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                    }`}>
                      {diff} Quiz
                    </span>
                  </div>

                  <p className="text-[10px] text-slate-500 font-semibold uppercase tracking-wider mt-4">
                    Performance
                  </p>
                  <p className="text-xs text-slate-400 mt-1">
                    {attemptsCount === 0 
                      ? 'No attempts yet' 
                      : `Best: ${Math.round(bestAttempt.quiz_score)}% (${attemptsCount} attempts)`}
                  </p>
                </div>

                {quiz ? (
                  <Link
                    to={`/quiz/${quiz.id}`}
                    className="mt-4 w-full inline-flex items-center justify-center py-2 rounded-xl text-xs font-semibold border bg-slate-900 border-slate-800 hover:bg-slate-800 text-slate-350 hover:text-white transition-all"
                  >
                    Take quiz
                  </Link>
                ) : (
                  <button 
                    disabled 
                    className="mt-4 w-full py-2 rounded-xl text-xs font-semibold bg-slate-950 border border-slate-900 text-slate-700 cursor-not-allowed"
                  >
                    Unavailable
                  </button>
                )}
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}


