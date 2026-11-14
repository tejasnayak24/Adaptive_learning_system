import React, { useState } from 'react'
import { CircleCheck, Earth, Eye, ListChecks, NotebookPen, Target } from 'lucide-react'
import LessonDiagram from './LessonDiagram'
import { cx } from './ui'

// Renders a lesson's structured material (stored as JSON in the database).
// Section ids let recommendations jump straight to the right part:
//   #worked-examples (SHOW_WORKED_EXAMPLE), #real-world (SHOW_REAL_WORLD_APPLICATION).

/** Ids of the material's parts, in reading order, for the "in this lesson" strip. */
export function materialOutline(material) {
  if (!material) return []
  const parts = []
  if (material.objectives?.length) parts.push({ id: 'objectives', label: 'Objectives', count: material.objectives.length })
  if (material.sections?.length) parts.push({ id: 'section-1', label: 'Sections', count: material.sections.length })
  if (material.definitions?.length) parts.push({ id: 'key-terms', label: 'Key terms', count: material.definitions.length })
  if (material.worked?.length) parts.push({ id: 'worked-examples', label: 'Worked examples', count: material.worked.length })
  if (material.real_world) parts.push({ id: 'real-world', label: 'In the real world' })
  if (material.takeaways?.length) parts.push({ id: 'takeaways', label: 'Takeaways', count: material.takeaways.length })
  if (material.practice?.length) parts.push({ id: 'practice', label: 'Practice', count: material.practice.length })
  return parts
}

function Section({ id, number, title, children }) {
  return (
    <section id={id} className="scroll-mt-24 space-y-4">
      <h2 className="flex items-baseline gap-3 font-display text-xl font-semibold tracking-tight text-ink sm:text-[22px]">
        {number !== undefined && (
          <span className="translate-y-[-2px] text-sm font-semibold tabular-nums text-brand-300" aria-hidden="true">
            {String(number).padStart(2, '0')}
          </span>
        )}
        <span>{title}</span>
      </h2>
      {children}
    </section>
  )
}

function PracticeItem({ index, question, answer }) {
  const [shown, setShown] = useState(false)
  return (
    <li className="rounded-card border border-line bg-surface p-4 shadow-card">
      <p className="flex gap-3 text-[15px] leading-relaxed text-ink">
        <span className="font-semibold tabular-nums text-ink-2">{index + 1}.</span>
        <span className="formula">{question}</span>
      </p>
      {shown ? (
        <p className="formula mt-3 flex items-start gap-2 rounded-lg bg-mint-500/[0.08] px-3 py-2 text-sm text-mint-200 ring-1 ring-inset ring-mint-500/25">
          <CircleCheck size={16} className="mt-0.5 shrink-0 text-mint-400" aria-hidden="true" />
          <span>
            <span className="sr-only">Answer: </span>
            {answer}
          </span>
        </p>
      ) : (
        <button
          type="button"
          onClick={() => setShown(true)}
          className="mt-3 inline-flex items-center gap-1.5 rounded-lg px-2 py-1 text-[13px] font-semibold text-brand-300 transition-colors hover:bg-brand-500/10 hover:text-brand-200"
        >
          <Eye size={15} aria-hidden="true" />
          Check my answer
        </button>
      )}
    </li>
  )
}

export default function LessonMaterial({ material, highlight }) {
  if (!material) return null
  const ring = (key) => (highlight === key ? 'rounded-2xl ring-2 ring-mint-400/60 ring-offset-4 ring-offset-canvas' : '')

  return (
    <div className="space-y-12">
      {material.objectives?.length > 0 && (
        <section id="objectives" className="scroll-mt-24 rounded-card border border-brand-500/25 bg-brand-500/[0.06] p-5 sm:p-6">
          <h2 className="flex items-center gap-2 text-sm font-semibold text-brand-200">
            <Target size={17} aria-hidden="true" />
            By the end of this lesson you can
          </h2>
          <ul className="mt-3 grid gap-2 sm:grid-cols-2">
            {material.objectives.map((objective) => (
              <li key={objective} className="flex gap-2.5 text-sm leading-relaxed text-ink">
                <CircleCheck size={16} className="mt-0.5 shrink-0 text-brand-300" aria-hidden="true" />
                <span>{objective}</span>
              </li>
            ))}
          </ul>
        </section>
      )}

      {material.intro && <p className="text-[17px] leading-[1.8] text-ink">{material.intro}</p>}

      {(material.sections || []).map(([heading, body], index) => (
        <Section key={heading} id={`section-${index + 1}`} number={index + 1} title={heading}>
          <div className="reading">
            {String(body)
              .split('\n\n')
              .map((paragraph, i) => (
                <p key={i}>{paragraph}</p>
              ))}
          </div>
        </Section>
      ))}

      {material.diagram && <LessonDiagram diagram={material.diagram} />}

      {material.definitions?.length > 0 && (
        <Section id="key-terms" title="Key terms">
          <dl className="grid grid-cols-1 gap-3 sm:grid-cols-2">
            {material.definitions.map(([term, meaning]) => (
              <div key={term} className="rounded-xl border border-line bg-surface px-4 py-3.5 shadow-card">
                <dt className="text-sm font-semibold text-ink">{term}</dt>
                <dd className="formula mt-1 text-[13px] leading-relaxed text-ink-2">{meaning}</dd>
              </div>
            ))}
          </dl>
        </Section>
      )}

      {material.examples?.length > 0 && (
        <Section id="examples" title="Examples">
          <ul className="space-y-2.5">
            {material.examples.map((example) => (
              <li key={example} className="formula flex gap-3 rounded-xl border border-line bg-deep/60 px-4 py-3 text-[15px] leading-relaxed text-ink">
                <span className="mt-[9px] h-1.5 w-1.5 shrink-0 rounded-full bg-mint-400" aria-hidden="true" />
                <span>{example}</span>
              </li>
            ))}
          </ul>
        </Section>
      )}

      {material.worked?.length > 0 && (
        <Section id="worked-examples" title="Worked examples">
          <div className={cx('space-y-4', ring('worked-examples'))}>
            {material.worked.map((item, index) => (
              <article key={index} className="overflow-hidden rounded-card border border-line bg-surface shadow-card">
                <header className="flex items-start gap-3 border-b border-line bg-white/[0.015] px-5 py-4">
                  <span className="grid h-8 w-8 shrink-0 place-items-center rounded-lg bg-brand-500/[0.12] text-brand-300 ring-1 ring-inset ring-brand-500/25">
                    <NotebookPen size={16} aria-hidden="true" />
                  </span>
                  <div className="min-w-0">
                    <p className="text-xs font-medium text-ink-2">Example {index + 1}</p>
                    <p className="formula mt-0.5 text-[15px] font-medium leading-relaxed text-ink">{item.problem}</p>
                  </div>
                </header>
                <ol className="space-y-3 px-5 py-4">
                  {item.steps.map((step, s) => (
                    <li key={s} className="flex gap-3">
                      <span className="mt-0.5 grid h-6 w-6 shrink-0 place-items-center rounded-full bg-deep text-[11px] font-semibold tabular-nums text-ink-2 ring-1 ring-inset ring-line-strong">
                        {s + 1}
                      </span>
                      <span className="formula text-[15px] leading-relaxed text-[#c9d1e2]">{step}</span>
                    </li>
                  ))}
                </ol>
                <p className="formula mx-5 mb-5 flex items-start gap-2.5 rounded-lg bg-mint-500/[0.08] px-4 py-3 text-[15px] font-medium text-mint-200 ring-1 ring-inset ring-mint-500/25">
                  <CircleCheck size={18} className="mt-0.5 shrink-0 text-mint-400" aria-hidden="true" />
                  <span>
                    <span className="sr-only">Answer: </span>
                    {item.answer}
                  </span>
                </p>
              </article>
            ))}
          </div>
        </Section>
      )}

      {material.real_world && (
        <Section id="real-world" title="In the real world">
          <div className={cx('flex gap-4 rounded-card border border-mint-500/25 bg-mint-500/[0.06] p-5', ring('real-world'))}>
            <span className="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-mint-500/[0.12] text-mint-300 ring-1 ring-inset ring-mint-500/25">
              <Earth size={19} aria-hidden="true" />
            </span>
            <p className="text-[15px] leading-relaxed text-ink">{material.real_world}</p>
          </div>
        </Section>
      )}

      {material.takeaways?.length > 0 && (
        <Section id="takeaways" title="Key takeaways">
          <ul className="space-y-2.5 rounded-card border border-line bg-surface p-5 shadow-card">
            {material.takeaways.map((takeaway) => (
              <li key={takeaway} className="formula flex gap-3 text-[15px] leading-relaxed text-ink">
                <ListChecks size={18} className="mt-0.5 shrink-0 text-mint-400" aria-hidden="true" />
                <span>{takeaway}</span>
              </li>
            ))}
          </ul>
        </Section>
      )}

      {material.practice?.length > 0 && (
        <Section id="practice" title="Practice exercises">
          <ol className="space-y-3">
            {material.practice.map(([question, answer], index) => (
              <PracticeItem key={index} index={index} question={question} answer={answer} />
            ))}
          </ol>
        </Section>
      )}
    </div>
  )
}
