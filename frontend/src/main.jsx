import React from 'react'
import ReactDOM from 'react-dom/client'
// Fonts are bundled with the app (no requests to third-party font servers).
import '@fontsource-variable/inter'
import '@fontsource-variable/outfit'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
