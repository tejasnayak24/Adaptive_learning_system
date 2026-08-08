import api from "./api";

const LOGIN_PATHS = ["/login", "/auth/login", "/token"];

async function tryLogin(body) {
  // Prefer JSON /login; fall back to /auth/login or token form if needed.
  for (const path of LOGIN_PATHS) {
    try {
      // /token expects form data; handle specially
      if (path === "/token") {
        const form = new URLSearchParams();
        form.append("username", body.email);
        form.append("password", body.password);
        const res = await fetch((import.meta.env.VITE_API_URL || "") + path, {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: form.toString(),
        });
        const data = await res.json();
        if (res.ok && data.access_token) return { access_token: data.access_token };
        continue;
      }

      const resp = await api.post(path, body, { auth: false });
      // Response may be { access_token } or TokenResponse
      if (resp?.access_token) return { access_token: resp.access_token };
      if (resp?.data?.access_token) return { access_token: resp.data.access_token };
    } catch (e) {
      // try next
    }
  }

  throw new Error("Login failed");
}

export async function login(email, password) {
  const tokenResp = await tryLogin({ email, password });
  const token = tokenResp.access_token;
  if (!token) throw new Error("No access token returned");
  api.setAuthToken(token);
  return token;
}

export async function register(name, email, password) {
  // backend RegisterRequest likely expects name, email, password
  // Try both /register and /auth/register
  const paths = ["/register", "/auth/register"];
  for (const path of paths) {
    try {
      const resp = await api.post(path, { name, email, password }, { auth: false });
      return resp;
    } catch (e) {
      // try next
    }
  }
  throw new Error("Registration failed");
}

export function logout() {
  api.clearAuthToken();
}

export async function getProfile() {
  return api.get("/profile");
}

export default { login, register, logout, getProfile };
