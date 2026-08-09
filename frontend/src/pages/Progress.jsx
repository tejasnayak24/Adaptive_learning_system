import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { progressService } from '../services/progressService'
import { lessonService } from '../services/lessonService'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

export default function Progress() {
  const { user } = useAuth()
  const [loading, setLoading] = useState(true)
  const [progress, setProgress] = useState([])
  const [lessons, setLessons] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    async function loadProgressData() {
      try {
        const progressRes = await progressService.getStudentProgress(user.id)
        const lessonsRes = await lessonService.getLessons()

        if (progressRes.success) setProgress(progressRes.data)
        if (lessonsRes.success) setLessons(lessonsRes.data)
      } catch (err) {
        setError(err.message || 'Failed to load progress analytics')
      } finally {
        setLoading(false)
      }
    }
    loadProgressData()
  }, [user.id])

  if (loading) {
    return (
      <div className="space-y-6 animate-pulse">
        <div className="h-10 w-1/4 bg-slate-800 rounded-xl"></div>
        <div className="h-4 w-1/2 bg-slate-800 rounded-lg"></div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 pt-6">
          <div className="h-80 bg-slate-800 rounded-3xl"></div>
          <div className="h-80 bg-slate-800 rounded-3xl"></div>
        </div>
      </div>
    )
  }

  // Calculate statistics
  const totalLessons = lessons.length
  const completedDistinct = new Set(progress.filter(p => p.completed).map(p => p.lesson_id))
  const completionPercentage = totalLessons > 0 ? Math.round((completedDistinct.size / totalLessons) * 100) : 0
  const totalAttempts = progress.length
  
  const avgScore = totalAttempts > 0 
    ? Math.round(progress.reduce((acc, p) => acc + p.quiz_score, 0) / totalAttempts) 
    : 0
  
  const avgAttention = totalAttempts > 0 
    ? Math.round((progress.reduce((acc, p) => acc + p.attention_score, 0) / totalAttempts) * 100) 
    : 0

  // Format Recharts data
  const sortedProgress = [...progress].sort((a, b) => a.id - b.id)

  const lineChartData = sortedProgress.map((p, idx) => ({
    attempt: `Quiz ${idx + 1}`,
    score: p.quiz_score,
    attention: Math.round(p.attention_score * 100)
  }))

  const topicAggregate = lessons.map(lesson => {
    const attempts = progress.filter(p => p.lesson_id === lesson.id)
    const highestScore = attempts.length > 0 ? Math.max(...attempts.map(a => a.quiz_score)) : 0
    const avgAtt = attempts.length > 0 
      ? Math.round((attempts.reduce((acc, a) => acc + a.attention_score, 0) / attempts.length) * 100) 
      : 0
    
    return {
      name: lesson.title,
      score: highestScore,
      attention: avgAtt
    }
  })

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="space-y-1.5">
        <h1 className="font-display text-3xl font-extrabold tracking-tight text-white md:text-4xl">
          Progress & Analytics
        </h1>
        <p className="text-slate-400 text-sm leading-relaxed max-w-2xl">
          Detailed telemetry logs detailing your quiz score history and facial engagement calibrations across science modules.
        </p>
      </div>

      {error && (
        <div className="rounded-2xl bg-rose-500/10 border border-rose-500/20 p-4 text-sm text-rose-400">
          {error}
        </div>
      )}

      {/* Stats row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="glass-panel rounded-3xl p-6 border border-slate-900 shadow-md">
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">Curriculum Progress</p>
          <div className="mt-4 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-white">{completionPercentage}%</span>
            <span className="text-xs text-slate-400">({completedDistinct.size} / {totalLessons} units)</span>
          </div>
        </div>

        <div className="glass-panel rounded-3xl p-6 border border-slate-900 shadow-md">
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">Total Quiz Attempts</p>
          <div className="mt-4 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-white">{totalAttempts}</span>
            <span className="text-xs text-slate-400">assessments submitted</span>
          </div>
        </div>

        <div className="glass-panel rounded-3xl p-6 border border-slate-900 shadow-md">
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">Avg accuracy score</p>
          <div className="mt-4 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-white">{avgScore}%</span>
            <span className="text-xs text-slate-400">correct answers</span>
          </div>
        </div>

        <div className="glass-panel rounded-3xl p-6 border border-slate-900 shadow-md">
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">Avg attention metric</p>
          <div className="mt-4 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-white">{avgAttention}%</span>
            <span className="text-xs text-teal-400">focus index</span>
          </div>
        </div>
      </div>

      {totalAttempts === 0 ? (
        <div className="glass-panel rounded-3xl p-8 border border-slate-900 shadow-md text-center py-12 space-y-4">
          <div className="text-5xl">📈</div>
          <h3 className="text-lg font-bold text-white">No Analytics Available Yet</h3>
          <p className="text-xs text-slate-400 max-w-sm mx-auto leading-relaxed">
            Progress metrics and graphs will populate as soon as you complete your first lesson assessment quiz.
          </p>
          <Link to="/subjects" className="inline-flex px-5 py-2.5 rounded-xl bg-indigo-500 hover:bg-indigo-650 text-white font-semibold text-xs shadow-md transition-all">
            Begin First Lesson
          </Link>
        </div>
      ) : (
        <>
          {/* Charts Group */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Historical accuracy chart */}
            <div className="glass-panel rounded-3xl p-6 border border-slate-900 shadow-lg space-y-4">
              <div>
                <h3 className="text-base font-bold text-white">Historical Performance Calibration</h3>
                <p className="text-xs text-slate-500">A timeline of your correctness and focus percentages per quiz attempt</p>
              </div>

              <div className="h-72">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={lineChartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" opacity={0.3} />
                    <XAxis dataKey="attempt" stroke="#475569" fontSize={10} tickLine={false} />
                    <YAxis stroke="#475569" fontSize={10} tickLine={false} domain={[0, 100]} />
                    <Tooltip contentStyle={{ background: '#0f172a', borderColor: '#334155', borderRadius: '12px' }} />
                    <Legend verticalAlign="top" height={36} iconType="circle" wrapperStyle={{ fontSize: '11px' }} />
                    <Line type="monotone" dataKey="score" stroke="#6366f1" strokeWidth={3} name="Quiz Accuracy %" dot={{ r: 4 }} />
                    <Line type="monotone" dataKey="attention" stroke="#14b8a6" strokeWidth={2} name="Attention Index %" strokeDasharray="4 4" dot={{ r: 3 }} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Performance by Subject chart */}
            <div className="glass-panel rounded-3xl p-6 border border-slate-900 shadow-lg space-y-4">
              <div>
                <h3 className="text-base font-bold text-white">Competency by Subject</h3>
                <p className="text-xs text-slate-500">Compares your highest quiz scores and average focus level per lesson</p>
              </div>

              <div className="h-72">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={topicAggregate} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" opacity={0.3} />
                    <XAxis dataKey="name" stroke="#475569" fontSize={9} tickLine={false} tickFormatter={(name) => name.split(' ')[0]} />
                    <YAxis stroke="#475569" fontSize={10} tickLine={false} domain={[0, 100]} />
                    <Tooltip contentStyle={{ background: '#0f172a', borderColor: '#334155', borderRadius: '12px' }} />
                    <Legend verticalAlign="top" height={36} iconType="circle" wrapperStyle={{ fontSize: '11px' }} />
                    <Bar dataKey="score" fill="#4f46e5" radius={[4, 4, 0, 0]} name="Highest Quiz Score %" maxBarSize={40} />
                    <Bar dataKey="attention" fill="#2dd4bf" radius={[4, 4, 0, 0]} name="Avg Attention %" maxBarSize={40} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>

          {/* Historical Attempts Table */}
          <div className="glass-panel rounded-3xl border border-slate-900 shadow-lg overflow-hidden">
            <div className="p-6 border-b border-slate-900">
              <h3 className="text-base font-bold text-white">Curriculum Attempts Log</h3>
              <p className="text-xs text-slate-500 mt-1">Audit log of all quiz submissions and state indicators</p>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs border-collapse">
                <thead>
                  <tr className="bg-slate-900/50 text-slate-400 font-semibold tracking-wider uppercase border-b border-slate-900">
                    <th className="py-4 px-6">Lesson Module</th>
                    <th className="py-4 px-6">Difficulty</th>
                    <th className="py-4 px-6">Quiz Score</th>
                    <th className="py-4 px-6">Attention Metric</th>
                    <th className="py-4 px-6">Duration</th>
                    <th className="py-4 px-6">Sync Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-900/80">
                  {[...progress].reverse().map((item) => {
                    const matchedLesson = lessons.find(l => l.id === item.lesson_id) || { title: 'Unknown Lesson' }
                    return (
                      <tr key={item.id} className="hover:bg-slate-900/10 transition-colors">
                        <td className="py-4 px-6 font-bold text-slate-200">{matchedLesson.title}</td>
                        <td className="py-4 px-6">
                          <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                            item.difficulty.toUpperCase() === 'EASY' 
                              ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' 
                              : item.difficulty.toUpperCase() === 'MEDIUM' 
                              ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20' 
                              : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                          }`}>
                            {item.difficulty}
                          </span>
                        </td>
                        <td className="py-4 px-6 font-semibold text-white">{Math.round(item.quiz_score)}%</td>
                        <td className="py-4 px-6 font-semibold text-teal-400">{Math.round(item.attention_score * 100)}%</td>
                        <td className="py-4 px-6 text-slate-450">{item.response_time}s</td>
                        <td className="py-4 px-6 text-slate-500 font-medium">✓ Synced</td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </div>
  )
}
