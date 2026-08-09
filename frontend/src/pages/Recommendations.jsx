import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { progressService } from '../services/progressService'
import { lessonService } from '../services/lessonService'
import { rlService } from '../services/rlService'

const TOPIC_TO_SUBJECT_MAP = {
  "Cell Biology": "Science",
  "Human Body Systems": "Science",
  "Force and Motion": "Science",
  "Matter and Its Properties": "Science",
  "Ecosystems": "Science"
}

export default function Recommendations() {
  const { user } = useAuth()
  const [loading, setLoading] = useState(true)
  const [progress, setProgress] = useState([])
  const [lessons, setLessons] = useState([])
  const [recommendation, setRecommendation] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    async function loadRecommendation() {
      try {
        const progressRes = await progressService.getStudentProgress(user.id)
        const lessonsRes = await lessonService.getLessons()
        
        if (lessonsRes.success) setLessons(lessonsRes.data)
        if (progressRes.success) setProgress(progressRes.data)

        if (progressRes.success && progressRes.data.length > 0 && lessonsRes.success) {
          // Find the most recent progress record
          const sorted = [...progressRes.data].sort((a, b) => b.id - a.id)
          const latest = sorted[0]

          const matchedLesson = lessonsRes.data.find(l => l.id === latest.lesson_id) || {
            title: 'Unknown Lesson',
            topic: 'General'
          }

          const previousAttempt = sorted[1] || { quiz_score: 0 }
          const completedLessonsCount = new Set(
            progressRes.data.filter(p => p.completed).map(p => p.lesson_id)
          ).size
          const attemptsCount = progressRes.data.filter(p => p.lesson_id === latest.lesson_id).length

          // Fetch the RL recommendation
          const resolvedSubject = TOPIC_TO_SUBJECT_MAP[matchedLesson.topic] || 'Science'
          const rlRes = await rlService.getRecommendation({
            subject: resolvedSubject,
            topic: matchedLesson.topic,
            lesson: matchedLesson.title,
            previous_quiz_score: Math.round(previousAttempt.quiz_score),
            current_quiz_score: Math.round(latest.quiz_score),
            attention_score: latest.attention_score,
            yawning: false,
            looking_away: false,
            difficulty: latest.difficulty.toUpperCase(),
            response_time: latest.response_time,
            hints_used: 0,
            lesson_attempts: attemptsCount,
            completed_lessons: completedLessonsCount
          })

          setRecommendation({
            ...rlRes,
            lessonTitle: matchedLesson.title,
            topicName: matchedLesson.topic,
            lastScore: latest.quiz_score,
            lastDifficulty: latest.difficulty
          })
        }
      } catch (err) {
        setError(err.message || 'Failed to generate recommendation logs')
      } finally {
        setLoading(false)
      }
    }
    loadRecommendation()
  }, [user.id])

  if (loading) {
    return (
      <div className="space-y-6 animate-pulse">
        <div className="h-10 w-1/4 bg-slate-800 rounded-xl"></div>
        <div className="h-4 w-1/2 bg-slate-800 rounded-lg"></div>
        <div className="h-64 bg-slate-800 rounded-3xl mt-8"></div>
      </div>
    )
  }

  // Guide helper explaining what each action represents in our RL engine
  const rlStrategies = [
    { name: 'NEXT_LESSON', desc: 'Advance to the next lesson sequence in the curriculum.', icon: '🚀' },
    { name: 'INCREASE_DIFFICULTY', desc: 'Upgrade upcoming quizzes from Easy to Medium or Medium to Hard.', icon: '⚡' },
    { name: 'REPEAT_LESSON', desc: 'Assigned to re-review lesson reading contents to build a firmer foundation.', icon: '🔁' },
    { name: 'DECREASE_DIFFICULTY', desc: 'Calibration tool lowering questions difficulty for remedial practice.', icon: '🛠️' },
    { name: 'FOCUS_RECOVERY', desc: 'Attention-recovery breather to reduce screen fatigue and regain concentration.', icon: '🧘' }
  ]

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div className="space-y-1.5">
        <h1 className="font-display text-3xl font-extrabold tracking-tight text-white md:text-4xl">
          AI Pedagogy Coach
        </h1>
        <p className="text-slate-400 text-sm leading-relaxed max-w-2xl">
          Meet your personal reinforcement-learning tutor. Aegis analyzes quiz scores, response times, and attention logs to adjust your curriculum difficulty.
        </p>
      </div>

      {error && (
        <div className="rounded-2xl bg-rose-500/10 border border-rose-500/20 p-4 text-sm text-rose-400">
          {error}
        </div>
      )}

      {/* Active Coach Suggestion */}
      {!recommendation ? (
        <div className="glass-panel rounded-3xl p-8 border border-slate-900 shadow-md text-center py-12 space-y-4">
          <div className="text-5xl">🤖</div>
          <h3 className="text-lg font-bold text-white">AI Coach is Calibrating</h3>
          <p className="text-xs text-slate-400 max-w-sm mx-auto leading-relaxed">
            The coach needs at least one quiz log to evaluate your study habits and output recommendations. Jump into subjects to begin.
          </p>
          <Link to="/subjects" className="inline-flex px-5 py-2.5 rounded-xl bg-indigo-500 hover:bg-indigo-600 text-white font-semibold text-xs shadow-md transition-all">
            Browse Subjects
          </Link>
        </div>
      ) : (
        <div className="glass-panel rounded-3xl p-8 border border-slate-900 shadow-xl space-y-6 relative overflow-hidden">
          <div className="absolute top-0 right-0 h-48 w-48 bg-indigo-500/5 blur-3xl pointer-events-none"></div>

          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-800 pb-5">
            <div className="space-y-1.5">
              <span className="px-2.5 py-0.5 text-[9px] font-bold bg-teal-500/10 text-teal-400 border border-teal-500/20 rounded">
                Active Pedagogy Advice
              </span>
              <h2 className="text-xl font-bold text-white">Curriculum Recommendation</h2>
            </div>
            
            <div className="shrink-0 flex items-center gap-2 bg-slate-900 border border-slate-800 rounded-xl px-3 py-1.5">
              <span className="text-[9px] text-slate-500 font-extrabold uppercase">Policy Confidence</span>
              <span className="text-teal-400 font-extrabold text-sm">{Math.round(recommendation.confidence * 100)}%</span>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="md:col-span-2 space-y-6">
              {/* Action Banner */}
              <div className="space-y-1">
                <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Coach Action Suggestion</span>
                <p className="text-2xl font-extrabold text-white">
                  {recommendation.action.replace(/_/g, ' ')}
                </p>
              </div>

              {/* Justification */}
              <div className="space-y-2">
                <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">AI tutor Justification</span>
                <p className="text-sm text-slate-300 italic bg-slate-900/30 border border-slate-850 p-4 rounded-2xl leading-relaxed">
                  "{recommendation.explanation}"
                </p>
              </div>
            </div>

            {/* Performance Snapshot */}
            <div className="space-y-4 rounded-2xl bg-slate-925 border border-slate-850 p-5 h-fit">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">Trigger State Log</h4>
              <div className="space-y-3 text-xs">
                <div className="flex justify-between">
                  <span className="text-slate-500">Lesson context</span>
                  <span className="font-semibold text-slate-300 truncate max-w-[120px]">{recommendation.lessonTitle}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Last score</span>
                  <span className="font-bold text-white">{recommendation.lastScore}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Last difficulty</span>
                  <span className="font-semibold text-slate-300">{recommendation.lastDifficulty}</span>
                </div>
              </div>
              
              <div className="pt-2">
                <Link
                  to={`/lesson/${progress.find(p => p.lesson_id)?.lesson_id}`}
                  className="w-full inline-flex justify-center py-2.5 rounded-xl bg-indigo-500 text-white font-bold text-[11px] shadow hover:bg-indigo-650 transition-colors"
                >
                  Resume study session
                </Link>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Guide to RL Coach Strategy */}
      <div className="glass-panel rounded-3xl p-6 md:p-8 border border-slate-900 shadow-lg space-y-6">
        <div>
          <h3 className="text-lg font-bold text-white">How the Coach Adapts</h3>
          <p className="text-xs text-slate-500 mt-1">
            Our Reinforcement Learning policy uses a discrete state-action matrix. Here are the core actions it can trigger:
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {rlStrategies.map((strategy) => (
            <div key={strategy.name} className="flex gap-4 p-4 bg-slate-900/30 border border-slate-850 rounded-2xl">
              <span className="text-2xl select-none">{strategy.icon}</span>
              <div className="space-y-1">
                <h4 className="text-xs font-extrabold text-white tracking-wide">{strategy.name.replace(/_/g, ' ')}</h4>
                <p className="text-xs text-slate-400 leading-relaxed">{strategy.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
