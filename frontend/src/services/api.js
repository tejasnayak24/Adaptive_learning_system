import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

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

    const detail = error.response?.data?.detail

    let message = 'An error occurred'

    if (typeof detail === 'string') {
      message = detail
    } else if (Array.isArray(detail)) {
      message = detail
        .map(item => item.msg || JSON.stringify(item))
        .join(', ')
    } else if (detail && typeof detail === 'object') {
      message = detail.message || JSON.stringify(detail)
    } else if (error.message) {
      message = error.message
    }

    return Promise.reject(new Error(message))
  }
)

export default api
