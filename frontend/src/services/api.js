import axios from 'axios'

const API_BASE_URL = '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request Interceptor: Inject Auth Token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response Interceptor: Handle errors globally
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    // Check for expired/invalid tokens
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token')
      // Custom event to trigger logout or redirect
      window.dispatchEvent(new Event('auth-unauthorized'))
    }
    
    const message = error.response?.data?.detail || error.message || 'An error occurred'
    return Promise.reject(new Error(message))
  }
)

export default api
