import axios from 'axios'

const API_BASE_URL = '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

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

api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token')
      window.dispatchEvent(new Event('auth-unauthorized'))
    }

    let message = 'An error occurred'

    if (error.response?.data) {
      const data = error.response.data

      if (typeof data.detail === 'string') {
        message = data.detail
      } else if (Array.isArray(data.detail)) {
        message = data.detail
          .map(err => `${err.loc?.join('.') || 'field'}: ${err.msg}`)
          .join(', ')
      } else if (typeof data.message === 'string') {
        message = data.message
      } else if (typeof data.detail === 'object' && data.detail !== null) {
        message = data.detail.message || JSON.stringify(data.detail)
      } else if (typeof data === 'string') {
        message = data
      }
    } else {
      message = error.message || 'An error occurred'
    }

    const failure = new Error(message)
    // Keep the HTTP status so pages can tell a refusal (403/404) from a
    // network problem.
    failure.status = error.response?.status ?? null
    // Structured details (e.g. a quiz attempt's state or a cooldown).
    failure.detail = error.response?.data?.detail ?? null
    return Promise.reject(failure)
  }
)

export default api