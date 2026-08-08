const http = require('http');
const https = require('https');

async function fetchJson(path) {
  const res = await fetch(path);
  console.log(path, res.status);
  const text = await res.text();
  try {
    const obj = JSON.parse(text);
    if (obj.paths) console.log('paths count:', Object.keys(obj.paths).length);
    if (obj.paths) console.log(Object.keys(obj.paths).slice(0,50).join('\n'));
  } catch (e) {
    console.log('body len', text.length);
  }
}

(async () => {
  try {
    await fetchJson('http://127.0.0.1:8000/openapi.json');
  } catch (e) { console.error('openapi error', e.message); }

  try {
    const r = await fetch('http://127.0.0.1:8000/auth/register', {method: 'OPTIONS'});
    console.log('/auth/register', r.status);
  } catch (e) { console.error('/auth/register error', e.message); }

  try {
    const r2 = await fetch('http://127.0.0.1:8000/auth/login', {method: 'OPTIONS'});
    console.log('/auth/login', r2.status);
  } catch (e) { console.error('/auth/login error', e.message); }
})();
