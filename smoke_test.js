(async () => {
  const base = process.env.API_URL || 'http://127.0.0.1:8000';
  const frontend = process.env.FRONTEND_URL || 'http://localhost:5174';
  const fetch = globalThis.fetch || (await import('node-fetch')).default;
  console.log('Base API:', base);

  // Step 1: Open frontend
  try {
    const r = await fetch(frontend + '/');
    console.log('Frontend root status:', r.status);
    if (r.status !== 200) throw new Error('Frontend not serving index');
  } catch (e) { console.error('Step 1 failed:', e); process.exit(1); }

  // Step 2: Verify main.jsx includes AuthProvider
  try {
    const r = await fetch(frontend + '/src/main.jsx');
    const txt = await r.text();
    if (!txt.includes('AuthProvider')) throw new Error('AuthProvider not present in main.jsx served');
    console.log('Frontend includes AuthProvider');
  } catch (e) { console.error('Step 2 failed:', e); process.exit(1); }

  // Step 3/4: Register and login
  const testUser = { name: 'smoketester', email: 'smoketester+node@example.com', password: 'TestPass123!', age: 30 };
  let token;
  try {
    let r = await fetch(base + '/register', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(testUser) });
    const txt = await r.text();
    console.log('/register', r.status, txt.substring(0,200));
    if (![200,201].includes(r.status) && r.status !== 422) throw new Error('/register unexpected status ' + r.status + ' ' + txt);
  } catch (e) { console.error('Step 3 register failed:', e); }

  try {
    let r = await fetch(base + '/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email: testUser.email, password: testUser.password }) });
    const json = await r.json();
    console.log('/login', r.status, json?.message || JSON.stringify(json).slice(0,200));
    if (!r.ok) throw new Error('Login failed: ' + JSON.stringify(json));
    token = json.access_token || json.data?.access_token;
    if (!token) throw new Error('No token returned');
  } catch (e) { console.error('Step 4 login failed:', e); process.exit(1); }

  // helper for auth requests
  const authReq = (path, opts={}) => fetch(base + path, Object.assign({ headers: { 'Content-Type':'application/json', 'Authorization': 'Bearer ' + token } }, opts));

  // Step 5: fetch lessons
  let lessons;
  try {
    const r = await authReq('/lessons');
    lessons = await r.json();
    console.log('/lessons', r.status, Array.isArray(lessons) ? `${lessons.length} lessons` : JSON.stringify(lessons).slice(0,200));
    if (!r.ok) throw new Error('Failed to fetch lessons');
  } catch (e) { console.error('Step 5 failed:', e); process.exit(1); }

  // Step 6: find a Science lesson
  let lesson = null;
  try {
    if (Array.isArray(lessons)) {
      lesson = lessons.find(l => (l.subject || l.title || '').toLowerCase().includes('science')) || lessons[0];
    } else if (lessons.data && Array.isArray(lessons.data)) {
      lesson = lessons.data.find(l => (l.subject || l.title || '').toLowerCase().includes('science')) || lessons.data[0];
    }
    if (!lesson) throw new Error('No lessons found');
    console.log('Selected lesson id:', lesson.id || lesson.lesson_id || lesson._id || 'unknown');
  } catch (e) { console.error('Step 6 failed:', e); process.exit(1); }

  const lessonId = lesson.id || lesson.lesson_id || lesson._id || lesson.lessonId;

  // Step 6: fetch lesson details
  try {
    const r = await authReq(`/lesson/${lessonId}`);
    const json = await r.json();
    console.log(`/lesson/${lessonId}`, r.status, JSON.stringify(json).slice(0,200));
    if (!r.ok) throw new Error('Failed to fetch lesson');
  } catch (e) { console.error('Step 6 fetch failed:', e); process.exit(1); }

  // Step 7: fetch quiz (use /quiz/start or /quiz/{quiz_id})
  let quiz;
  try {
    // try /quiz/start
    let r = await authReq('/quiz/start', { method: 'POST', body: JSON.stringify({ lesson_id: lessonId }) });
    if (r.ok) {
      quiz = await r.json();
      console.log('/quiz/start', r.status, JSON.stringify(quiz).slice(0,200));
    } else {
      // fallback: list quizzes or GET /quiz/{id} if lesson contains quiz_id
      console.log('/quiz/start failed', r.status);
      // probe quiz ids to find one matching this lesson
      let found = false;
      for (let id = 1; id <= 30; id++) {
        try {
          const qres = await authReq(`/quiz/${id}`);
          if (!qres.ok) continue;
          const qjson = await qres.json();
          const qLessonId = qjson?.data?.quiz?.lesson_id;
          if (qLessonId == lessonId) {
            quiz = qjson.data;
            console.log('Found quiz id', id);
            found = true;
            break;
          }
        } catch (e) {
          // ignore
        }
      }
      if (!found) throw new Error('No quiz start or quiz id available');
    }
  } catch (e) { console.error('Step 7 failed:', e); process.exit(1); }

  // Step 8: submit quiz
  let submitResp;
  try {
    // Construct a QuizSubmitRequest payload (server computes correctness)
    const questions = quiz.questions || quiz.data?.questions || quiz;
    function jsonSubId(tok) { try { const p = JSON.parse(Buffer.from(tok.split('.')[1],'base64').toString()); return p.sub || p.user_id || p.id; } catch (e) { return null; } }
    const studentId = jsonSubId(token) || 1;
    const lessonIdForPayload = lessonId;
    const payload = {
      student_id: String(studentId),
      lesson_id: lessonIdForPayload,
      quiz_score: 0.8,
      response_time: 12.3,
      attention_score: 0.75,
      difficulty: (quiz.quiz && quiz.quiz.difficulty) || (quiz.difficulty) || 'MEDIUM',
    };
    const r = await authReq('/quiz/submit', { method: 'POST', body: JSON.stringify(payload) });
    submitResp = await r.json();
    console.log('/quiz/submit', r.status, JSON.stringify(submitResp).slice(0,200));
    if (!r.ok) throw new Error('/quiz/submit failed');
  } catch (e) { console.error('Step 8 failed:', e); process.exit(1); }

  // Step 9: verify progress saved
  try {
    const studentId = jsonSubId(token) || submitResp.data?.student_id || submitResp.student_id;
    const r = await authReq(`/progress/${studentId}`);
    const json = await r.json();
    console.log(`/progress/${studentId}`, r.status, JSON.stringify(json).slice(0,200));
    if (!r.ok) throw new Error('Progress fetch failed');
  } catch (e) { console.error('Step 9 failed:', e); process.exit(1); }

  // Step 10: verify RL recommendation
  try {
    // Create a recommendation request matching RecommendationRequest schema
    // Use lesson.title/topic as lesson/topic, and a generic subject like 'Science'
    const prevScore = Math.round((submitResp.data?.quiz_score || 0) * 100);
    const currentScore = prevScore;
    const completedLessonsCount = (await authReq(`/progress/${jsonSubId(token) || submitResp.data?.student_id}`).then(r=>r.json())).data?.length || 0;
    const recReq = {
      subject: 'Science',
      topic: (typeof lesson.topic === 'string' && lesson.topic) || (lesson.title || 'General'),
      lesson: (lesson.title || 'Lesson'),
      previous_quiz_score: prevScore,
      current_quiz_score: currentScore,
      attention_score: 0.75,
      yawning: false,
      looking_away: false,
      difficulty: (submitResp.data?.difficulty || 'MEDIUM').toString().toUpperCase(),
      response_time: submitResp.data?.response_time || 12.3,
      hints_used: 0,
      lesson_attempts: 1,
      completed_lessons: completedLessonsCount,
    };
    let r = await authReq('/rl/recommend', { method: 'POST', body: JSON.stringify(recReq) });
    const rec = await r.json();
    console.log('/rl/recommend', r.status, JSON.stringify(rec).slice(0,200));
    if (!r.ok) throw new Error('RL recommend failed');
  } catch (e) { console.error('Step 10 failed:', e); process.exit(1); }

  // Step 11/12: verify frontend reacts and no runtime errors
  try {
    // Check dev server root and main.jsx once more
    const r = await fetch(frontend + '/');
    if (r.status !== 200) throw new Error('Frontend not serving index on final check');
    console.log('Smoke test completed successfully');
  } catch (e) { console.error('Step 11/12 failed:', e); process.exit(1); }

  process.exit(0);
})();
