(async () => {
  const base = 'http://127.0.0.1:8000';
  const fetch = globalThis.fetch || (await import('node-fetch')).default;
  const reg = { name: 'smoketester3', email: 'smoketester3+node@example.com', password: 'TestPass123!', age: 32 };
  try { await fetch(base + '/register', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(reg) }); } catch(e) {}
  const r = await fetch(base + '/login', { method: 'POST', headers: { 'Content-Type':'application/json' }, body: JSON.stringify({ email: reg.email, password: reg.password }) });
  const j = await r.json(); const token = j.access_token || j.data?.access_token; console.log('token ok', !!token);
  const lessons = await fetch(base + '/lessons', { headers: { Authorization: 'Bearer ' + token }}).then(r=>r.json());
  const lessonId = lessons.data[0].id; console.log('looking for quiz for lesson', lessonId);
  for (let id=1; id<=30; id++) {
    try {
      const q = await fetch(base + '/quiz/' + id).then(r=>({status:r.status, json: r.ok? r.json(): null})).then(async o=>{ if (o.json) o.body = await o.json(); return o; });
      if (q.status===200 && q.body && q.body.data && q.body.data.quiz && q.body.data.quiz.lesson_id==lessonId) { console.log('found quiz id', id); console.log(JSON.stringify(q.body, null, 2)); break; }
    } catch(e) { }
  }
})();
