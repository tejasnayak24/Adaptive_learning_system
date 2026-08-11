export function getSubjectFromLesson(lesson) {
  if (!lesson) return 'Science'
  if (lesson.subject) return lesson.subject

  const title = (lesson.title || '').toLowerCase()
  const topic = (lesson.topic || '').toLowerCase()
  const content = (lesson.content || '').toLowerCase()
  const allText = `${title} ${topic} ${content}`

  if (
    allText.includes('cell') ||
    allText.includes('biology') ||
    allText.includes('body') ||
    allText.includes('system') ||
    allText.includes('force') ||
    allText.includes('motion') ||
    allText.includes('matter') ||
    allText.includes('ecosystem') ||
    allText.includes('organism') ||
    allText.includes('science')
  ) {
    return 'Science'
  }
  if (
    allText.includes('math') ||
    allText.includes('algebra') ||
    allText.includes('geometry') ||
    allText.includes('calculus') ||
    allText.includes('number')
  ) {
    return 'Mathematics'
  }
  if (
    allText.includes('history') ||
    allText.includes('geography') ||
    allText.includes('civics') ||
    allText.includes('society') ||
    allText.includes('social')
  ) {
    return 'Social Science'
  }
  if (
    allText.includes('english') ||
    allText.includes('grammar') ||
    allText.includes('reading') ||
    allText.includes('vocabulary') ||
    allText.includes('literature')
  ) {
    return 'English'
  }
  return 'Science' // default fallback
}
