import { useEffect, useState } from 'react'

const QUERY = '(prefers-reduced-motion: reduce)'

function matches() {
  try {
    return typeof window !== 'undefined' && Boolean(window.matchMedia?.(QUERY).matches)
  } catch {
    return false
  }
}

/** True while the system asks for reduced motion (charts then skip animation). */
export function useReducedMotion() {
  const [reduced, setReduced] = useState(matches)
  useEffect(() => {
    const query = window.matchMedia?.(QUERY)
    if (!query) return undefined
    const onChange = () => setReduced(query.matches)
    query.addEventListener('change', onChange)
    return () => query.removeEventListener('change', onChange)
  }, [])
  return reduced
}

/** 'smooth', or 'auto' when reduced motion is requested (for scrollIntoView). */
export function scrollBehavior() {
  return matches() ? 'auto' : 'smooth'
}
