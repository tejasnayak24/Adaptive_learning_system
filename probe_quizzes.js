(async () => {
  const base = 'http://127.0.0.1:8000';
  const fetch = globalThis.fetch || (await import('node-fetch')).default;
  const reg = { name: 'probeuser', email: 'probeuser+node@example.com', password: 'TestPass123!', age: 40 };
  try { await fetch(base + '/register', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(reg) }); } catch(e) {}
  const r = await fetch(base + '/login', { method: 'POST', headers: { 'Content-Type':'application/json' }, body: JSON.stringify({ email: reg.email, password: reg.password }) });
  const j = await r.json(); const token = j.access_token || j.data?.access_token; console.log('token ok', !!token);
  for (let id=1; id<=30; id++){
    try{
      let res = await fetch(base + '/quiz/' + id, { headers: { Authorization: 'Bearer ' + token }});
      if (res.status===200) { const body = await res.json(); console.log('quiz', id, 'OK lesson_id=', body?.data?.quiz?.lesson_id); }
    } catch(e){}
  }
})();
