/** Join class names, skipping falsy values. */
export function cx(...parts) {
  return parts.flat(Infinity).filter(Boolean).join(' ')
}

/** A React useId value made safe for SVG `url(#id)` references. */
export function svgId(id) {
  return `aegis-${String(id).replace(/[^a-zA-Z0-9_-]/g, '')}`
}

/** "#8875ff" -> "rgb(136 117 255 / alpha)" for soft tints of a colour. */
export function tint(hex, alpha) {
  const value = String(hex || '').replace('#', '')
  if (value.length !== 6) return `rgb(105 117 140 / ${alpha})`
  const n = parseInt(value, 16)
  return `rgb(${(n >> 16) & 255} ${(n >> 8) & 255} ${n & 255} / ${alpha})`
}
