const API_URL = import.meta.env.VITE_API_URL || "";

const STORAGE_KEY = "als_auth_token";

export function getAuthToken() {
  try {
    return localStorage.getItem(STORAGE_KEY);
  } catch (e) {
    return null;
  }
}

export function setAuthToken(token) {
  try {
    localStorage.setItem(STORAGE_KEY, token);
  } catch (e) {
    // ignore
  }
}

export function clearAuthToken() {
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch (e) {
    // ignore
  }
}

async function parseResponse(res) {
  const text = await res.text();
  let data = null;
  try {
    data = text ? JSON.parse(text) : null;
  } catch (e) {
    // non-json response
  }

  if (!res.ok) {
    const err = new Error(data?.detail || data?.message || res.statusText || "Request failed");
    err.status = res.status;
    err.body = data;
    throw err;
  }

  return data;
}

function buildUrl(path) {
  if (!path) return API_URL;
  if (path.startsWith("http://") || path.startsWith("https://")) return path;
  if (!path.startsWith("/")) path = `/${path}`;
  return `${API_URL}${path}`;
}

export async function request(path, { method = "GET", body = null, headers = {}, auth = true } = {}) {
  const url = buildUrl(path);

  const defaultHeaders = {
    "Accept": "application/json",
    "Content-Type": "application/json",
  };

  const opts = {
    method,
    headers: { ...defaultHeaders, ...headers },
  };

  if (auth) {
    const token = getAuthToken();
    if (token) opts.headers["Authorization"] = `Bearer ${token}`;
  }

  if (body != null) {
    opts.body = JSON.stringify(body);
  }

  const res = await fetch(url, opts);
  return parseResponse(res);
}

export const api = {
  get: (path, opts) => request(path, { ...opts, method: "GET" }),
  post: (path, body, opts) => request(path, { ...opts, method: "POST", body }),
  put: (path, body, opts) => request(path, { ...opts, method: "PUT", body }),
  del: (path, opts) => request(path, { ...opts, method: "DELETE" }),
  getAuthToken,
  setAuthToken,
  clearAuthToken,
};

export default api;
