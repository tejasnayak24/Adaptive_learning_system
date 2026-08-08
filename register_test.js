(async () => {
  try {
    const base = 'http://127.0.0.1:8000';
    const body = { name: 'smoketest-node', email: 'smoketest.node@example.com', password: 'TestPassword123!', age: 25 };
    let r = await fetch(base + '/register', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
    console.log('/register', r.status, await r.text());

    r = await fetch(base + '/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email: body.email, password: body.password }) });
    console.log('/login', r.status, await r.text());
  } catch (e) { console.error(e); }
})();
