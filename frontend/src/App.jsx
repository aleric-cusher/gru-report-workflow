import { Route, Routes } from 'react-router-dom'
import HomePage from './pages/HomePage'
import ContactPage from './pages/ContactPage'

function App() {

  return (
    <Routes>
      <Route exact path='/' element={<HomePage />} />
      <Route exact path='/contact' element={<ContactPage />} />
    </Routes>
  )
}

export default App
