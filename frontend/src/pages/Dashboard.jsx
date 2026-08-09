import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { lessonService } from '../services/lessonService'
import { progressService } from '../services/progressService'
import { rlService } from '../services/rlService'
import api from '../services/api'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'



export default function Dashboard() {
  const { user } = useAuth()
  const [lessons, setLessons] = useState([])
  const [progress, setProgress] = useState([])
  const [recommendation, setRecommendation] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const getGreeting = () => {
    const hr = new Date().getHours()
    if (hr < 12) return 'Good morning'
    if (hr < 17) return 'Good afternoon'
    return 'Good evening'
  }

  useEffect(() => {
    async function loadData() {
      try {
        const lessonsRes = await lessonService.getLessons()
        const progressRes = await progressService.getStudentProgress(user.id)

        if (lessonsRes.success) {
          setLessons(lessonsRes.data)
        }
        if (progressRes.success) {
          setProgress(progressRes.data)
        }

        // Fetch RL recommendation if the student has progress records
        if (progressRes.success && progressRes.data.length > 0) {
          const sortedProgress = [...progressRes.data].sort((a, b) => b.id - a.id)
          const latest = sortedProgress[0]
          
          // Find matching lesson info
          const matchedLesson = lessonsRes.data.find(l => l.id === latest.lesson_id) || {
            title: 'Unknown Lesson',
            topic: 'General'
          }

          const previousAttempt = sortedProgress[1] || { quiz_score: 0 }

          // Count completed distinct lessons
          const completedLessonsCount = new Set(
            progressRes.data.filter(p => p.completed).map(p => p.lesson_id)
          ).size

          // Count attempts for the current lesson
          const attemptsCount = progressRes.data.filter(p => p.lesson_id === latest.lesson_id).length

          // Make the recommend API request
          try {
            const payload = {
              subject: latest.subject || matchedLesson.subject,
              topic: matchedLesson.topic,
              lesson: matchedLesson.title,
              previous_quiz_score: Math.round(previousAttempt.quiz_score),
              current_quiz_score: Math.round(latest.quiz_score),
              difficulty: latest.difficulty,
              response_time: latest.response_time,
              hints_used: 0,
              lesson_attempts: attemptsCount,
              completed_lessons: completedLessonsCount
            }
            if (latest.attention_score !== null && latest.attention_score !== undefined) {
              payload.attention_score = latest.attention_score
            }
            const rlRes = await rlService.getRecommendation(payload)
            setRecommendation(rlRes)
          } catch (rlErr) {
            console.error('Failed to load recommendation:', rlErr)
          }
        }
      } catch (err) {
        setError(err.message || 'Failed to load dashboard data')
      } finally {
        setLoading(false)
      }
    }

    loadData()
  }, [user.id])

  if (loading) {
    return (
      <div className="space-y-8 animate-pulse">
        <div className="h-16 w-2/3 bg-slate-800 rounded-2xl"></div>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="h-32 bg-slate-800 rounded-3xl"></div>
          ))}
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 h-80 bg-slate-800 rounded-3xl"></div>
          <div className="h-80 bg-slate-800 rounded-3xl"></div>
        </div>
      </div>
    )
  }

  // Calculate statistics
  const distinctCompleted = new Set(progress.filter(p => p.completed).map(p => p.lesson_id))
  const completionPercentage = lessons.length > 0 ? Math.round((distinctCompleted.size / lessons.length) * 100) : 0
  const avgScore = progress.length > 0 ? Math.round(progress.reduce((acc, p) => acc + p.quiz_score, 0) / progress.length) : 0

  // Find a lesson to recommend continuing (first uncompleted or next lesson)
  const continueLesson = lessons.find(l => !distinctCompleted.has(l.id)) || lessons[0]

  // Recharts data format: quiz attempts sorted by ID ascending
  const chartData = [...progress]
    .sort((a, b) => a.id - b.id)
    .map((p, idx) => ({
      attempt: `Quiz ${idx + 1}`,
      score: p.quiz_score,
      attention: Math.round(p.attention_score * 100)
    }))

  return (
    <div className="space-y-8">
      {/* Greetings Banner */}
      <div className="relative overflow-hidden rounded-3xl border border-slate-800 bg-gradient-to-r from-indigo-950/40 via-slate-900/40 to-slate-950 p-8 shadow-2xl">
        <div className="absolute top-0 right-0 h-40 w-40 bg-indigo-500/10 blur-3xl pointer-events-none"></div>
        <div className="relative z-10 space-y-2">
          <h1 className="font-display text-3xl md:text-4xl font-extrabold tracking-tight text-white">
            {getGreeting()}, <span className="bg-gradient-to-r from-indigo-400 to-teal-300 bg-clip-text text-transparent">{user.name}</span>!
          </h1>
          <p className="text-slate-400 max-w-xl text-sm leading-relaxed">
            {distinctCompleted.size === 0 
              ? "Welcome to Aegis! Click on 'Continue Learning' below to launch your first science lesson and adaptive assessment."
              : `You have completed ${distinctCompleted.size} out of ${lessons.length} curriculum lessons. Let's keep the momentum going!`}
          </p>
        </div>
      </div>

      {/* Grid Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="glass-panel rounded-3xl p-6 relative border border-slate-900 shadow-md">
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">Overall Progress</p>
          <div className="mt-4 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-white">{completionPercentage}%</span>
            <span className="text-xs text-teal-400 font-medium">completed</span>
          </div>
          <div className="mt-3 w-full bg-slate-900 rounded-full h-1.5 overflow-hidden">
            <div className="bg-gradient-to-r from-indigo-500 to-teal-400 h-1.5 rounded-full" style={{ width: `${completionPercentage}%` }}></div>
          </div>
        </div>

        <div className="glass-panel rounded-3xl p-6 relative border border-slate-900 shadow-md">
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">Lessons Finished</p>
          <div className="mt-4 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-white">{distinctCompleted.size}</span>
            <span className="text-xs text-slate-400">/ {lessons.length} topics</span>
          </div>
          <div className="absolute right-6 bottom-6 text-2xl">📚</div>
        </div>

        <div className="glass-panel rounded-3xl p-6 relative border border-slate-900 shadow-md">
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">Avg Quiz Score</p>
          <div className="mt-4 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-white">{avgScore}%</span>
            <span className={`text-xs font-medium ${avgScore >= 80 ? 'text-emerald-400' : avgScore >= 60 ? 'text-amber-400' : 'text-slate-400'}`}>
              {avgScore >= 80 ? 'Excellent' : avgScore >= 60 ? 'Passing' : 'Needs Practice'}
            </span>
          </div>
          <div className="absolute right-6 bottom-6 text-2xl">🎯</div>
        </div>

        <div className="glass-panel rounded-3xl p-6 relative border border-slate-900 shadow-md">
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">Learning Streak</p>
          <div className="mt-4 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-white">Unavailable</span>
            <span className="text-xs text-slate-550 font-medium">not tracked</span>
          </div>
          <div className="absolute right-6 bottom-6 text-2xl">🔥</div>
        </div>
      </div>

      {/* Main Grid Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Analytics & Continue Section */}
        <div className="lg:col-span-2 space-y-8">
          
          {/* Continue Learning card */}
          {continueLesson && (
            <div className="glass-panel rounded-3xl p-6 border border-slate-900 shadow-lg relative overflow-hidden flex flex-col sm:flex-row sm:items-center sm:justify-between gap-6">
              <div className="space-y-1.5">
                <span className="inline-flex px-2.5 py-1 text-[10px] font-semibold uppercase tracking-wider bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 rounded-lg">
                  Continue Learning
                </span>
                <h3 className="text-xl font-bold text-white">{continueLesson.title}</h3>
                <p className="text-xs text-slate-400">Subject: Science &bull; Topic: {continueLesson.topic}</p>
              </div>
              <Link
                to={`/lesson/${continueLesson.id}`}
                className="shrink-0 inline-flex items-center justify-center gap-2 px-5 py-3 rounded-xl bg-indigo-500 text-white font-semibold text-sm hover:bg-indigo-600 transition-colors shadow-md shadow-indigo-500/10 hover:shadow-indigo-500/20 active:scale-[0.98] transform"
              >
                Resume Lesson
                <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7" />
                </svg>
              </Link>
            </div>
          )}

          {/* Performance Trends Chart */}
          <div className="glass-panel rounded-3xl p-6 border border-slate-900 shadow-lg space-y-4">
            <div>
              <h3 className="text-lg font-bold text-white">Learning Performance</h3>
              <p className="text-xs text-slate-500">Tracks your quiz score percentages and attention metrics</p>
            </div>
            
            {chartData.length === 0 ? (
              <div className="flex h-52 flex-col items-center justify-center text-center p-4">
                <div className="text-3xl mb-2">📊</div>
                <p className="text-sm font-medium text-slate-400">No assessment data logged yet</p>
                <p className="text-xs text-slate-500 mt-1">Complete a lesson quiz to populate progress charts.</p>
              </div>
            ) : (
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" opacity={0.3} />
                    <XAxis dataKey="attempt" stroke="#475569" fontSize={11} tickLine={false} />
                    <YAxis stroke="#475569" fontSize={11} tickLine={false} domain={[0, 100]} />
                    <Tooltip 
                      contentStyle={{ background: '#0f172a', borderColor: '#334155', borderRadius: '12px' }}
                      labelStyle={{ color: '#94a3b8', fontWeight: '600' }}
                    />
                    <Line type="monotone" dataKey="score" stroke="#6366f1" strokeWidth={3} name="Quiz Score %" dot={{ r: 4 }} activeDot={{ r: 6 }} />
                    <Line type="monotone" dataKey="attention" stroke="#14b8a6" strokeWidth={2} name="Attention Score %" strokeDasharray="5 5" dot={{ r: 3 }} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            )}
          </div>
        </div>

        {/* AI Learning Assistant recommendation */}
        <div className="space-y-6">
          <div className="glass-panel rounded-3xl p-6 border border-slate-900 shadow-lg h-full flex flex-col justify-between">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                  <span className="text-teal-400">✦</span> AI Learning Coach
                </h3>
                {recommendation && (
                  <span className="px-2 py-0.5 text-[9px] font-bold bg-teal-500/10 text-teal-400 rounded border border-teal-500/20">
                    Active recommendation
                  </span>
                )}
              </div>
              
              {!recommendation ? (
                <div className="space-y-4 py-6 text-center">
                  <div className="text-4xl">🤖</div>
                  <div className="space-y-1">
                    <p className="text-sm font-semibold text-slate-300">Ready to calibrate</p>
                    <p className="text-xs text-slate-500 leading-relaxed">
                      Complete a quiz at the end of any lesson. The Reinforcement Learning engine will analyze your engagement and accuracy to generate personalized pacing tips.
                    </p>
                  </div>
                </div>
              ) : (
                <div className="space-y-4 pt-2">
                  {/* Action Badge */}
                  <div className="rounded-2xl bg-indigo-500/10 border border-indigo-500/20 p-4 space-y-1">
                    <p className="text-[10px] font-semibold text-indigo-400 uppercase tracking-wider">PEDAGOGICAL ACTION</p>
                    <p className="text-lg font-extrabold text-white">
                      {recommendation.action.replace(/_/g, ' ')}
                    </p>
                  </div>

                  {/* Explanation */}
                  <div className="space-y-1">
                    <p className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider">Coach Justification</p>
                    <p className="text-sm text-slate-300 leading-relaxed">
                      "{recommendation.explanation}"
                    </p>
                  </div>

                  {/* Confidence bar */}
                  <div className="space-y-1.5">
                    <div className="flex items-center justify-between text-xs">
                      <span className="font-semibold text-slate-500 uppercase tracking-wider text-[10px]">Confidence</span>
                      <span className="font-bold text-teal-400">{Math.round(recommendation.confidence * 100)}%</span>
                    </div>
                    <div className="w-full bg-slate-900 rounded-full h-1.5 overflow-hidden">
                      <div className="bg-teal-500 h-1.5 rounded-full" style={{ width: `${recommendation.confidence * 100}%` }}></div>
                    </div>
                  </div>
                </div>
              )}
            </div>

            <div className="border-t border-slate-800/80 pt-4 mt-6">
              <Link 
                to="/recommendations"
                className="w-full inline-flex items-center justify-center gap-1.5 px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-800 hover:bg-slate-800 text-xs font-semibold text-slate-300 hover:text-white transition-colors"
              >
                Go to AI Coach page
                <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                </svg>
              </Link>
            </div>
          </div>
        </div>

      </div>

      {/* Curriculum Summary */}
      <div className="glass-panel rounded-3xl p-6 border border-slate-900 shadow-lg space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-bold text-white">Your Curriculum</h3>
            <p className="text-xs text-slate-500">Track and choose subjects from your current Science studies</p>
          </div>
          <Link to="/subjects" className="text-xs font-bold text-indigo-400 hover:text-indigo-300 transition-colors">
            View Subject Browser &rarr;
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {lessons.slice(0, 4).map((lesson) => {
            const isCompleted = distinctCompleted.has(lesson.id)
            return (
              <div 
                key={lesson.id} 
                className="flex items-center justify-between p-4 rounded-2xl bg-slate-900/30 border border-slate-800/80 hover:border-slate-700/60 transition-colors"
              >
                <div className="space-y-1 min-w-0">
                  <p className="text-sm font-bold text-slate-200 truncate">{lesson.title}</p>
                  <p className="text-xs text-slate-500 truncate">Topic: {lesson.topic}</p>
                </div>
                
                {isCompleted ? (
                  <span className="shrink-0 inline-flex items-center gap-1.5 px-2.5 py-1 text-[10px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full">
                    <svg className="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7" />
                    </svg>
                    Completed
                  </span>
                ) : (
                  <Link 
                    to={`/lesson/${lesson.id}`}
                    className="shrink-0 px-3 py-1.5 text-[11px] font-semibold bg-slate-900 border border-slate-700 hover:bg-indigo-600 hover:border-indigo-600 hover:text-white rounded-lg text-slate-300 transition-all"
                  >
                    Start Study
                  </Link>
                )}
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}
