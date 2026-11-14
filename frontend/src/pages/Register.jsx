import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { ArrowRight, CalendarDays, CircleAlert, KeyRound, Mail, UserRound } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import AuthLayout from '../components/AuthLayout'
import { GRADES } from '../components/GradeGate'
import { Button, Callout, PasswordField, TextField, cx } from '../components/ui'

export default function Register() {
  const { register } = useAuth()
  const navigate = useNavigate()
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [age, setAge] = useState('')
  const [grade, setGradeChoice] = useState('')
  const [error, setError] = useState('')
  const [fieldErrors, setFieldErrors] = useState({})
  const [loading, setLoading] = useState(false)

  // Field messages mirror the inputs' own constraints (required, email
  // format, age >= 1 in whole years, password 8-72 characters).
  const validate = (form) => {
    const errors = {}
    const fields = form.elements
    if (!name) errors.name = 'Enter your full name'
    if (!email) errors.email = 'Enter your email address'
    else if (!fields.email.validity.valid) errors.email = 'Enter a valid email address'
    if (!age) errors.age = 'Enter your age'
    else if (!fields.age.validity.valid || parseInt(age, 10) <= 0) errors.age = 'Enter a valid age (a whole number of 1 or more)'
    if (!grade) errors.grade = 'Choose your grade'
    if (!password) errors.password = 'Choose a password'
    else if (!fields.password.validity.valid) errors.password = 'Use at least 8 characters'
    return errors
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    const form = e.currentTarget
    const errors = validate(form)
    setFieldErrors(errors)
    const first = ['name', 'email', 'age', 'grade', 'password'].find((key) => errors[key])

    if (!name || !email || !password || !age || !grade) {
      setError('Please fill in all fields')
      if (first === 'grade') form.querySelector('input[name="grade"]')?.focus()
      else if (first) form.elements[first]?.focus()
      return
    }

    if (parseInt(age, 10) <= 0) {
      setError('Please enter a valid age')
      form.elements.age.focus()
      return
    }

    if (first) {
      setError('Please check the highlighted fields')
      form.elements[first]?.focus()
      return
    }

    setError('')
    setLoading(true)
    try {
      await register(name, email, password, age, grade)
      // Redirect to login after successful registration
      navigate('/login', { state: { info: 'Registration successful! Please sign in.' } })
    } catch (err) {
      setError(err.message || 'Registration failed. Email might already be in use.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <AuthLayout
      title="Create your account"
      subtitle="Set up your profile and Aegis shows the lessons for your grade."
      footer={
        <>
          Already have an account?{' '}
          <Link to="/login" className="font-semibold text-brand-300 underline-offset-4 transition-colors hover:text-brand-200 hover:underline">
            Sign in
          </Link>
        </>
      }
    >
      <div className="space-y-5">
        {error && (
          <Callout tone="danger" role="alert">
            {error}
          </Callout>
        )}

        <form onSubmit={handleSubmit} noValidate className="space-y-5">
          <TextField
            id="name"
            name="name"
            label="Full name"
            icon={UserRound}
            autoComplete="name"
            required
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Your name"
            error={fieldErrors.name}
          />
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
          <TextField
            id="age"
            name="age"
            type="number"
            label="Age"
            icon={CalendarDays}
            inputMode="numeric"
            required
            min="1"
            value={age}
            onChange={(e) => setAge(e.target.value)}
            placeholder="14"
            error={fieldErrors.age}
          />

          <fieldset aria-describedby={fieldErrors.grade ? 'grade-error' : undefined}>
            <legend className="text-[13px] font-medium text-ink-2">Grade</legend>
            <div className="mt-1.5 grid grid-cols-5 gap-2">
              {GRADES.map((g) => (
                <label key={g} className="relative">
                  <input
                    type="radio"
                    name="grade"
                    value={g}
                    required
                    checked={grade === String(g)}
                    onChange={(e) => setGradeChoice(e.target.value)}
                    className="peer sr-only"
                  />
                  <span
                    className={cx(
                      'flex h-11 cursor-pointer items-center justify-center rounded-control border bg-deep text-sm font-semibold text-ink-2 transition-[border-color,background-color,color] duration-150 hover:border-[#3a4664] hover:text-ink',
                      'peer-checked:border-brand-500 peer-checked:bg-brand-500/[0.12] peer-checked:text-ink',
                      'peer-focus-visible:outline-2 peer-focus-visible:outline-offset-2 peer-focus-visible:outline-brand-400',
                      fieldErrors.grade ? 'border-danger/60' : 'border-line-strong'
                    )}
                  >
                    <span className="sr-only">Grade </span>
                    {g}
                  </span>
                </label>
              ))}
            </div>
            {fieldErrors.grade && (
              <p id="grade-error" className="mt-1.5 flex items-center gap-1.5 text-xs font-medium text-danger">
                <CircleAlert size={13} aria-hidden="true" />
                {fieldErrors.grade}
              </p>
            )}
          </fieldset>

          <PasswordField
            id="password"
            name="password"
            label="Password"
            icon={KeyRound}
            autoComplete="new-password"
            required
            minLength={8}
            maxLength={72}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="At least 8 characters"
            hint="8 to 72 characters."
            error={fieldErrors.password}
          />

          <Button type="submit" size="lg" fullWidth loading={loading} iconRight={loading ? undefined : ArrowRight}>
            {loading ? 'Creating account…' : 'Create account'}
          </Button>
        </form>
      </div>
    </AuthLayout>
  )
}
