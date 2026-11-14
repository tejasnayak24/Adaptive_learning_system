import React from 'react'
import { ChartLine, ScanFace, Sparkles } from 'lucide-react'
import { Wordmark } from './ui'

const FEATURES = [
  {
    icon: Sparkles,
    title: 'A coach that plans your next step',
    text: 'Recommendations come from a Q-learning policy trained offline on simulated students.'
  },
  {
    icon: ScanFace,
    title: 'Focus support that stays on your device',
    text: 'Your webcam is analysed on this computer. Images and video are never stored or sent.'
  },
  {
    icon: ChartLine,
    title: 'Progress built from your own results',
    text: 'Scores, topics and streaks come only from the quizzes you take.'
  }
]

/** Split layout for sign-in and registration: brand story on the left, form on the right. */
export default function AuthLayout({ title, subtitle, footer, children }) {
  return (
    <div className="min-h-screen bg-canvas lg:grid lg:grid-cols-[minmax(0,1fr)_minmax(0,1.1fr)]">
      <aside className="relative hidden overflow-hidden border-r border-line bg-deep lg:flex lg:flex-col lg:justify-between lg:p-12 xl:p-16">
        <div
          className="bg-dot-grid pointer-events-none absolute inset-0 [mask-image:radial-gradient(ellipse_at_top_left,black_25%,transparent_70%)]"
          aria-hidden="true"
        />
        <div className="pointer-events-none absolute -left-32 -top-32 h-[460px] w-[460px] rounded-full bg-brand-500/[0.14] blur-[120px]" aria-hidden="true" />
        <div className="pointer-events-none absolute -bottom-40 -right-24 h-[380px] w-[380px] rounded-full bg-mint-500/[0.09] blur-[120px]" aria-hidden="true" />

        <div className="relative">
          <Wordmark />
        </div>

        <div className="relative max-w-md space-y-10">
          <div className="space-y-4">
            <h2 className="font-display text-[40px] font-semibold leading-[1.08] tracking-tight text-ink xl:text-[46px]">
              Learning that adapts to{' '}
              <span className="bg-gradient-to-r from-brand-300 to-mint-300 bg-clip-text text-transparent">you</span>.
            </h2>
            <p className="text-[15px] leading-relaxed text-ink-2">
              Clear lessons, protected quizzes and a coach that chooses your next step from your results and your focus.
            </p>
          </div>
          <ul className="space-y-5">
            {FEATURES.map(({ icon: Icon, title: featureTitle, text }) => (
              <li key={featureTitle} className="flex gap-4">
                <span className="grid h-10 w-10 shrink-0 place-items-center rounded-xl border border-line-strong bg-raised text-brand-300 shadow-card">
                  <Icon size={19} aria-hidden="true" />
                </span>
                <span className="space-y-1 pt-0.5">
                  <span className="block text-sm font-semibold text-ink">{featureTitle}</span>
                  <span className="block text-[13px] leading-relaxed text-ink-2">{text}</span>
                </span>
              </li>
            ))}
          </ul>
        </div>

        <p className="relative text-xs text-ink-2">Grades 6–10 · Mathematics, Science, Social Science and English</p>
      </aside>

      <main className="flex min-h-screen flex-col px-5 py-7 sm:px-10 lg:px-16">
        <div className="lg:hidden">
          <Wordmark />
        </div>
        <div className="mx-auto flex w-full max-w-[420px] flex-1 animate-page-in flex-col justify-center py-10">
          <div className="mb-8 space-y-2">
            <h1 className="font-display text-[28px] font-semibold tracking-tight text-ink">{title}</h1>
            {subtitle && <p className="text-sm leading-relaxed text-ink-2">{subtitle}</p>}
          </div>
          {children}
          {footer && <div className="mt-8 border-t border-line pt-6 text-center text-sm text-ink-2">{footer}</div>}
        </div>
      </main>
    </div>
  )
}
