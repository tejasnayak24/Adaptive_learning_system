import React, { useState } from 'react'
import LessonDiagram from './LessonDiagram'

// Renders a lesson's structured material (stored as JSON in the database).
// Section ids let recommendations jump straight to the right part:
//   #worked-examples (SHOW_WORKED_EXAMPLE), #real-world (SHOW_REAL_WORLD_APPLICATION).

function Section({ id, title, children }) {
  return (
    <section id={id} className="space-y-3 scroll-mt-24">
      <h2 className="font-display text-lg font-bold text-white">{title}</h2>
      {children}
    </section>
  )
}

function PracticeItem({ index, question, answer }) {
  const [shown, setShown] = useState(false)
  return (
    <li className="rounded-2xl border border-slate-800 bg-slate-900/30 p-4 text-sm">
      <p className="text-slate-200">
        {index + 1}. {question}
      </p>
      {shown ? (
        <p className="mt-2 text-xs text-teal-300">Answer: {answer}</p>
      ) : (
        <button onClick={() => setShown(true)} className="mt-2 text-xs font-semibold text-indigo-400 hover:text-indigo-300">
          Check my answer
        </button>
      )}
    </li>
  )
}

export default function LessonMaterial({ material, highlight }) {
  if (!material) return null
  const ring = (key) => (highlight === key ? 'ring-2 ring-teal-400/60 rounded-2xl p-3 -m-3' : '')

  return (
    <div className="space-y-10 text-slate-300 leading-relaxed text-sm md:text-base">
      {material.objectives?.length > 0 && (
        <div className="rounded-2xl border border-indigo-500/20 bg-indigo-500/5 p-5">
          <h2 className="text-xs font-bold uppercase tracking-wider text-indigo-300">Learning objectives</h2>
          <ul className="mt-2 list-disc space-y-1 pl-5 text-sm">
            {material.objectives.map((objective) => (
              <li key={objective}>{objective}</li>
            ))}
          </ul>
        </div>
      )}

      {material.intro && <p>{material.intro}</p>}

      {(material.sections || []).map(([heading, body]) => (
        <Section key={heading} title={heading}>
          {String(body)
            .split('\n\n')
            .map((paragraph, i) => (
              <p key={i}>{paragraph}</p>
            ))}
        </Section>
      ))}

      {material.diagram && <LessonDiagram diagram={material.diagram} />}

      {material.definitions?.length > 0 && (
        <Section title="Key terms">
          <dl className="grid grid-cols-1 gap-3 sm:grid-cols-2">
            {material.definitions.map(([term, meaning]) => (
              <div key={term} className="rounded-xl border border-slate-800 bg-slate-900/30 p-3">
                <dt className="text-sm font-bold text-white">{term}</dt>
                <dd className="text-xs text-slate-400">{meaning}</dd>
              </div>
            ))}
          </dl>
        </Section>
      )}

      {material.examples?.length > 0 && (
        <Section title="Examples">
          <ul className="list-disc space-y-1 pl-5">
            {material.examples.map((example) => (
              <li key={example}>{example}</li>
            ))}
          </ul>
        </Section>
      )}

      {material.worked?.length > 0 && (
        <Section id="worked-examples" title="Worked examples">
          <div className={`space-y-4 ${ring('worked-examples')}`}>
            {material.worked.map((item, index) => (
              <div key={index} className="rounded-2xl border border-slate-800 bg-slate-900/30 p-4">
                <p className="font-semibold text-white">
                  Example {index + 1}: {item.problem}
                </p>
                <ol className="mt-2 list-decimal space-y-1 pl-5 text-sm">
                  {item.steps.map((step, s) => (
                    <li key={s}>{step}</li>
                  ))}
                </ol>
                <p className="mt-2 text-sm font-semibold text-teal-300">Answer: {item.answer}</p>
              </div>
            ))}
          </div>
        </Section>
      )}

      {material.real_world && (
        <Section id="real-world" title="In the real world">
          <p className={`rounded-2xl border border-teal-500/20 bg-teal-500/5 p-4 ${ring('real-world')}`}>
            {material.real_world}
          </p>
        </Section>
      )}

      {material.takeaways?.length > 0 && (
        <Section title="Key takeaways">
          <ul className="space-y-1">
            {material.takeaways.map((takeaway) => (
              <li key={takeaway} className="flex gap-2">
                <span className="text-teal-400">✓</span>
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
