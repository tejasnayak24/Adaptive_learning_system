import api from './api'

export const authService = {
  async login(email, password) {
    const response = await api.post('/login', { email, password })
    // response is already unwrapped by the axios interceptor (response.data)
    if (response.access_token) {
      localStorage.setItem('token', response.access_token)
    }
    return response
  },

  async register(name, email, password, age) {
    return await api.post('/register', {
      name,
      email,
      password,
      age: parseInt(age, 10),
    })
  },

  async getProfile() {
    return await api.get('/profile')
  },

  logout() {
    localStorage.removeItem('token')
  },

  isAuthenticated() {
    return !!localStorage.getItem('token')
  }
}
