import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App'
import './styles.css'


// function App() {
//   return (
//     <main className="grid min-h-screen place-items-center bg-slate-950 px-6 text-slate-50">
//       <div className="text-center">
//         <h1 className="text-5xl font-semibold tracking-tight">KhoAI</h1>
//         <p className="mt-4 text-slate-300">Inventory management and demand planning</p>
//       </div>
//     </main>
//   )
// }

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>,
)
