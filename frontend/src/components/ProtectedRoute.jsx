import React from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import { LoaderCircle } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import { LogoMark } from './ui'

export default function ProtectedRoute({ children }) {
  const { user, loading } = useAuth()
  const location = useLocation()

  if (loading) {
    return (
      <div className="flex min-h-screen w-full items-center justify-center bg-canvas" role="status" aria-live="polite">
        <div className="flex flex-col items-center gap-5">
          <LogoMark size={44} />
          <div className="flex items-center gap-2 text-sm font-medium text-ink-2">
            <LoaderCircle size={16} className="animate-spin text-brand-400" aria-hidden="true" />
            Loading Aegis…
          </div>
        </div>
      </div>
    )
  }

  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  return children
}
