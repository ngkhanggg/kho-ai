import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './styles.css'
import App from './App'

import { BrowserRouter, Routes, Route } from 'react-router-dom'
import AuthLayout from './features/auth/AuthLayout'
import SignInPage from './features/auth/SignInPage'
import SignUpPage from './features/auth/SignUpPage'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route index element={<App />} />

        <Route element={<AuthLayout />}>
          <Route path="login" element={<SignInPage/>} />
          <Route path="register" element={<SignUpPage/>} />
        </Route>
      </Routes>
    </BrowserRouter>
  </StrictMode>,
)
