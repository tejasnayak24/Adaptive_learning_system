import React, { Suspense, useEffect, useRef, useState } from 'react'
import { Link, Outlet, useLocation, useNavigate } from 'react-router-dom'
import {
  BookOpen,
  Camera,
  CameraOff,
  ChartLine,
  GraduationCap,
  LayoutDashboard,
  LoaderCircle,
  LogOut,
  Menu,
  ShieldCheck,
  Sparkles,
  X
} from 'lucide-react'
import GradeGate from '../components/GradeGate'
import { useAuth } from '../context/AuthContext'
import { useMonitoring } from '../context/MonitoringContext'
import { Badge, Breadcrumbs, Button, IconButton, Modal, PageSkeleton, Tooltip, Wordmark, cx } from '../components/ui'

const NAV_SECTIONS = [
  {
    label: 'Learn',
    items: [
      { name: 'Dashboard', to: '/', icon: LayoutDashboard, match: (path) => path === '/' },
      {
        name: 'My Learning',
        to: '/subjects',
        icon: BookOpen,
        match: (path) => path.startsWith('/subjects') || path.startsWith('/lesson/') || path.startsWith('/quiz/')
      }
    ]
  },
  {
    label: 'Insights',
    items: [
      { name: 'Progress', to: '/progress', icon: ChartLine, match: (path) => path.startsWith('/progress') },
      { name: 'AI Coach', to: '/recommendations', icon: Sparkles, match: (path) => path.startsWith('/recommendations') },
      { name: 'Session Activity', to: '/activity', icon: ShieldCheck, match: (path) => path.startsWith('/activity') }
    ]
  }
]

function routeTrail(path) {
  if (path.startsWith('/lesson/')) return [{ label: 'My Learning', to: '/subjects' }, { label: 'Lesson' }]
  if (path.startsWith('/quiz/')) return [{ label: 'My Learning', to: '/subjects' }, { label: 'Quiz' }]
  for (const section of NAV_SECTIONS) {
    const item = section.items.find((entry) => entry.match(path))
    if (item) return [{ label: section.label }, { label: item.name }]
  }
  return [{ label: 'Aegis' }]
}

const isLearningRoute = (path) => path.startsWith('/lesson/') || path.startsWith('/quiz/')

// Camera state shown in the top bar while a lesson or quiz is open. Display
// only: MonitoringGate decides what the student can do.
const MONITORING_PILL = {
  verified: { tone: 'success', icon: Camera, label: 'Camera verified' },
  consent_required: { tone: 'warning', icon: CameraOff, label: 'Consent needed' },
  agent_not_running: { tone: 'warning', icon: CameraOff, label: 'Camera agent not running' },
  camera_unavailable: { tone: 'warning', icon: CameraOff, label: 'Webcam unavailable' },
  no_face: { tone: 'warning', icon: CameraOff, label: 'No face detected' },
  backend_disconnected: { tone: 'warning', icon: CameraOff, label: 'Camera data delayed' },
  ended: { tone: 'neutral', icon: CameraOff, label: 'Monitoring ended' },
  error: { tone: 'danger', icon: CameraOff, label: 'Camera error' }
}

function MonitoringPill() {
  const { state, sessionId } = useMonitoring()
  const starting = !sessionId && state !== 'consent_required'
  const pill = (!starting && MONITORING_PILL[state]) || { tone: 'info', icon: LoaderCircle, label: 'Checking camera…', spin: true }
  return (
    <Badge tone={pill.tone} icon={pill.icon} className={cx(pill.spin && '[&_svg]:animate-spin')} role="status" aria-live="polite">
      {pill.label}
    </Badge>
  )
}

function initials(name) {
  const parts = String(name || '').trim().split(/\s+/).filter(Boolean)
  if (!parts.length) return 'ST'
  return (parts[0][0] + (parts.length > 1 ? parts[parts.length - 1][0] : '')).toUpperCase()
}

function NavItem({ item, path, onNavigate }) {
  const Icon = item.icon
  const active = item.match(path)
  const exact = path === item.to
  return (
    <Link
      to={item.to}
      onClick={onNavigate}
      aria-current={active ? (exact ? 'page' : 'true') : undefined}
      className={cx(
        'group relative flex h-10 items-center gap-3 rounded-[10px] px-3 text-sm font-medium transition-[background-color,color] duration-200',
        active ? 'bg-white/[0.06] text-ink' : 'text-ink-2 hover:bg-white/[0.035] hover:text-ink'
      )}
    >
      <span
        className={cx(
          'absolute left-0 top-2 bottom-2 w-[3px] rounded-r-full bg-brand-400 transition-[opacity,transform] duration-200 ease-out',
          active ? 'scale-y-100 opacity-100' : 'scale-y-50 opacity-0'
        )}
        aria-hidden="true"
      />
      <Icon
        size={18}
        className={cx('shrink-0 transition-colors duration-200', active ? 'text-brand-300' : 'text-ink-3 group-hover:text-ink-2')}
        aria-hidden="true"
      />
      <span className="truncate">{item.name}</span>
    </Link>
  )
}

function Navigation({ path, onNavigate }) {
  return (
    <nav aria-label="Main" className="space-y-7">
      {NAV_SECTIONS.map((section) => (
        <div key={section.label} className="space-y-1.5">
          <p className="px-3 text-[11px] font-semibold uppercase tracking-[0.14em] text-ink-2/80">{section.label}</p>
          <div className="space-y-0.5">
            {section.items.map((item) => (
              <NavItem key={item.to} item={item} path={path} onNavigate={onNavigate} />
            ))}
          </div>
        </div>
      ))}
    </nav>
  )
}

function ProfileBlock({ user, onSignOut }) {
  if (!user) return null
  const role = (user.role || 'student').toLowerCase()
  const roleLabel = role === 'student' ? (user.grade ? `Grade ${user.grade} student` : 'Student') : role.charAt(0).toUpperCase() + role.slice(1)
  return (
    <div className="border-t border-line p-3">
      <div className="flex items-center gap-3 rounded-xl px-2 py-2">
        <span className="grid h-9 w-9 shrink-0 place-items-center rounded-full bg-gradient-to-br from-brand-500/35 to-mint-500/25 text-[13px] font-semibold text-ink ring-1 ring-inset ring-white/10">
          {initials(user.name)}
        </span>
        <div className="min-w-0 flex-1">
          <p className="truncate text-sm font-medium text-ink">{user.name}</p>
          <p className="truncate text-xs text-ink-2">{roleLabel}</p>
        </div>
        <Tooltip content="Sign out" side="top" align="end">
          <IconButton icon={LogOut} label="Sign out" size="sm" onClick={onSignOut} />
        </Tooltip>
      </div>
    </div>
  )
}

export default function AppLayout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const path = location.pathname
  const [drawerOpen, setDrawerOpen] = useState(false)
  const [confirmSignOut, setConfirmSignOut] = useState(false)
  const drawerCloseRef = useRef(null)
  const menuButtonRef = useRef(null)

  // Close the drawer whenever the route changes.
  useEffect(() => {
    setDrawerOpen(false)
  }, [path])

  useEffect(() => {
    if (!drawerOpen) return undefined
    drawerCloseRef.current?.focus()
    const onKeyDown = (event) => {
      if (event.key === 'Escape') setDrawerOpen(false)
    }
    document.addEventListener('keydown', onKeyDown)
    const menuButton = menuButtonRef.current
    return () => {
      document.removeEventListener('keydown', onKeyDown)
      menuButton?.focus()
    }
  }, [drawerOpen])

  const handleLogout = () => {
    setConfirmSignOut(false)
    logout()
    navigate('/login')
  }

  const skipToContent = (event) => {
    // Focus the content without a URL fragment (a fragment change would look
    // like a Back press to the quiz's leave-guard).
    event.preventDefault()
    document.getElementById('main-content')?.focus()
  }

  // Remount (and fade in) per section, not per lesson: moving between
  // lessons keeps the monitored session's components mounted.
  const transitionKey = path.split('/')[1] || 'home'

  return (
    <div className="min-h-full bg-canvas">
      <a
        href="#main-content"
        onClick={skipToContent}
        className="sr-only z-[70] rounded-lg bg-brand-600 px-4 py-2 text-sm font-semibold text-white focus:not-sr-only focus:fixed focus:left-4 focus:top-4"
      >
        Skip to content
      </a>

      {/* Desktop sidebar */}
      <aside className="fixed inset-y-0 left-0 z-30 hidden w-[260px] flex-col border-r border-line bg-deep lg:flex">
        <div className="flex h-16 shrink-0 items-center px-5">
          <Link to="/" aria-label="Aegis dashboard" className="rounded-lg">
            <Wordmark />
          </Link>
        </div>
        <div className="flex-1 overflow-y-auto px-3 pb-4 pt-3">
          <Navigation path={path} />
        </div>
        <ProfileBlock user={user} onSignOut={() => setConfirmSignOut(true)} />
      </aside>

      {/* Mobile drawer */}
      {drawerOpen && (
        <div className="fixed inset-0 z-50 lg:hidden" role="dialog" aria-modal="true" aria-label="Navigation">
          <div className="absolute inset-0 animate-fade-in bg-[#05070d]/75" onClick={() => setDrawerOpen(false)} aria-hidden="true" />
          <div className="relative flex h-full w-[min(300px,86vw)] animate-drawer-in flex-col border-r border-line bg-deep shadow-raised">
            <div className="flex h-16 shrink-0 items-center justify-between pl-5 pr-3">
              <Wordmark />
              <IconButton ref={drawerCloseRef} icon={X} label="Close navigation" onClick={() => setDrawerOpen(false)} />
            </div>
            <div className="flex-1 overflow-y-auto px-3 pb-4 pt-3">
              <Navigation path={path} onNavigate={() => setDrawerOpen(false)} />
            </div>
            <ProfileBlock
              user={user}
              onSignOut={() => {
                setDrawerOpen(false)
                setConfirmSignOut(true)
              }}
            />
          </div>
        </div>
      )}

      <div className="flex min-h-full flex-col lg:pl-[260px]">
        <header className="sticky top-0 z-20 border-b border-line/80 bg-canvas/85 backdrop-blur-md">
          <div className="mx-auto flex h-16 max-w-[1240px] items-center gap-3 px-4 sm:px-6 lg:px-10">
            <IconButton
              ref={menuButtonRef}
              icon={Menu}
              label="Open navigation"
              className="-ml-2 lg:hidden"
              onClick={() => setDrawerOpen(true)}
              aria-expanded={drawerOpen}
            />
            <Link to="/" aria-label="Aegis dashboard" className="rounded-lg lg:hidden">
              <Wordmark compact size={26} />
            </Link>
            <Breadcrumbs items={routeTrail(path)} className="hidden lg:block" />
            <div className="ml-auto flex min-w-0 items-center gap-2">
              {isLearningRoute(path) && <MonitoringPill />}
              {user?.grade && (
                <Badge tone="neutral" icon={GraduationCap} className="hidden sm:inline-flex">
                  Grade {user.grade}
                </Badge>
              )}
            </div>
          </div>
        </header>

        <main id="main-content" tabIndex={-1} className="flex-1 focus:outline-none">
          <div className="mx-auto w-full max-w-[1240px] px-4 pb-16 pt-6 sm:px-6 lg:px-10 lg:pt-8">
            <GradeGate>
              {/* Pages are lazy-loaded; the shell stays while one loads. */}
              <Suspense fallback={<PageSkeleton />}>
                <div key={transitionKey} className="animate-page-in">
                  <Outlet />
                </div>
              </Suspense>
            </GradeGate>
          </div>
        </main>
      </div>

      <Modal
        open={confirmSignOut}
        onClose={() => setConfirmSignOut(false)}
        title="Sign out of Aegis?"
        icon={LogOut}
        tone="neutral"
        size="sm"
        description={
          <>
            {user?.email && (
              <>
                You are signed in as <span className="font-medium text-ink">{user.email}</span>.{' '}
              </>
            )}
            Camera monitoring stops when you sign out, and a quiz that is still open is closed without grading.
          </>
        }
        footer={
          <>
            <Button variant="secondary" onClick={() => setConfirmSignOut(false)} data-autofocus>
              Stay signed in
            </Button>
            <Button variant="danger" icon={LogOut} onClick={handleLogout}>
              Sign out
            </Button>
          </>
        }
      />
    </div>
  )
}
