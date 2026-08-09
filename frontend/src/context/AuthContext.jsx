import React, { createContext, useContext, useState, useEffect } from 'react'
import { authService } from '../services/authService'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  const fetchProfile = async () => {
    try {
      const response = await authService.getProfile()
      if (response.success && response.data) {
        setUser(response.data)
      } else {
        setUser(null)
        authService.logout()
      }
    } catch (err) {
      setUser(null)
      authService.logout()
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      fetchProfile()
    } else {
      setLoading(false)
    }

    // Listen for global unauthorized events (e.g. from axios interceptor)
    const handleUnauthorized = () => {
      setUser(null)
    }

    window.addEventListener('auth-unauthorized', handleUnauthorized)
    return () => {
      window.removeEventListener('auth-unauthorized', handleUnauthorized)
    }
  }, [])

  const login = async (email, password) => {
    setLoading(true)
    try {
      const res = await authService.login(email, password)
      if (res.success) {
        await fetchProfile()
      }
      return res
    } catch (err) {
      setLoading(false)
      throw err
    }
  }

  const register = async (name, email, password, age) => {
    setLoading(true)
    try {
      const res = await authService.register(name, email, password, age)
      setLoading(false)
      return res
    } catch (err) {
      setLoading(false)
      throw err
    }
  }

  const logout = () => {
    authService.logout()
    setUser(null)
  }

  const value = {
    user,
    loading,
    login,
    register,
    logout,
    refreshUser: fetchProfile
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
