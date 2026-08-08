(async () => {
  const base = 'http://127.0.0.1:8000';
  const fetch = globalThis.fetch || (await import('node-fetch')).default;
  const reg = { name: 'smoketester2', email: 'smoketester2+node@example.com', password: 'TestPass123!', age: 31 };
  try {
    let r = await fetch(base + '/register', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(reg) });
    console.log('/register', r.status);
  } catch (e) { }
  let r = await fetch(base + '/login', { method: 'POST', headers: { 'Content-Type':'application/json' }, body: JSON.stringify({ email: reg.email, password: reg.password }) });
  const j = await r.json();
  const token = j.access_token || j.data?.access_token;
  console.log('token ok', !!token);
  const lessons = await fetch(base + '/lessons', { headers: { Authorization: 'Bearer ' + token }}).then(r=>r.json());
  console.log(JSON.stringify(lessons, null, 2));
})();
