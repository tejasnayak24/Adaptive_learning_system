export function getSubjectFromLesson(lesson) {
  if (!lesson) return 'Science'

  // Use the subject directly if it is provided
  if (lesson.subject) return lesson.subject

  const title = (lesson.title || '').toLowerCase()
  const topic = (lesson.topic || '').toLowerCase()
  const content = (lesson.content || '').toLowerCase()
  const allText = `${title} ${topic} ${content}`

  // Check Social Science FIRST
  if (
    topic.includes('social science') ||
    title.includes('social science') ||
    allText.includes('indian constitution') ||
    allText.includes('history') ||
    allText.includes('geography') ||
    allText.includes('civics') ||
    allText.includes('democracy') ||
    allText.includes('economics') ||
    allText.includes('society') ||
    allText.includes('social science')
  ) {
    return 'Social Science'
  }

  // Mathematics
  if (
    allText.includes('mathematics') ||
    allText.includes('math') ||
    allText.includes('algebra') ||
    allText.includes('geometry') ||
    allText.includes('calculus') ||
    allText.includes('number')
  ) {
    return 'Mathematics'
  }

  // English
  if (
    allText.includes('english') ||
    allText.includes('grammar') ||
    allText.includes('reading') ||
    allText.includes('vocabulary') ||
    allText.includes('literature')
  ) {
    return 'English'
  }

  // Science
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

  return 'Science'
}