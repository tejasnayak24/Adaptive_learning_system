import React, { useState } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { ArrowRight, KeyRound, Mail } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import AuthLayout from '../components/AuthLayout'
import { Button, Callout, PasswordField, TextField } from '../components/ui'

export default function Login() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [fieldErrors, setFieldErrors] = useState({})
  const [loading, setLoading] = useState(false)

  // Redirect to dashboard, or where they came from
  const from = location.state?.from?.pathname || '/'
  // e.g. "Registration successful! Please sign in." from the register page
  const info = typeof location.state?.info === 'string' ? location.state.info : ''

  const handleSubmit = async (e) => {
    e.preventDefault()
    // Same rules as before (both fields required, email format), shown next
    // to the fields instead of as browser pop-ups.
    const form = e.currentTarget
    const errors = {}
    if (!email) errors.email = 'Enter your email address'
    else if (!form.elements.email.validity.valid) errors.email = 'Enter a valid email address'
    if (!password) errors.password = 'Enter your password'
    setFieldErrors(errors)

    if (!email || !password) {
      setError('Please fill in all fields')
      form.elements[errors.email ? 'email' : 'password']?.focus()
      return
    }
    if (errors.email) {
      setError('')
      form.elements.email.focus()
      return
    }

    setError('')
    setLoading(true)
    try {
      await login(email, password)
      navigate(from, { replace: true })
    } catch (err) {
      setError(err.message || 'Login failed. Please check your credentials.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <AuthLayout
      title="Welcome back"
      subtitle="Sign in to continue your lessons, quizzes and coaching."
      footer={
        <>
          New to Aegis?{' '}
          <Link to="/register" className="font-semibold text-brand-300 underline-offset-4 transition-colors hover:text-brand-200 hover:underline">
            Create an account
          </Link>
        </>
      }
    >
      <div className="space-y-5">
        {info && !error && (
          <Callout tone="success" role="status">
            {info}
          </Callout>
        )}
        {error && (
          <Callout tone="danger" role="alert">
            {error}
          </Callout>
        )}

        <form onSubmit={handleSubmit} noValidate className="space-y-5">
          <TextField
            id="email"
            name="email"
            type="email"
            label="Email address"
            icon={Mail}
            autoComplete="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="name@school.com"
            error={fieldErrors.email}
          />
          <PasswordField
            id="password"
            name="password"
            label="Password"
            icon={KeyRound}
            autoComplete="current-password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Your password"
            error={fieldErrors.password}
          />
          <Button type="submit" size="lg" fullWidth loading={loading} iconRight={loading ? undefined : ArrowRight}>
            {loading ? 'Signing in…' : 'Sign in'}
          </Button>
        </form>
      </div>
    </AuthLayout>
  )
}
