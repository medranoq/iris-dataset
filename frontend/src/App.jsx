
import {BrowserRouter, Routes, Route, Link} from 'react-router-dom'
import PredictionForm from './components/PredictionForm.jsx'
import DatasetView from './components/DatasetView.jsx'

import './App.css'

export default function App() {
    return (
        <BrowserRouter>
            <nav style={{ padding: '1rem', borderBottom: '1px solid #ccc' }}>
                <Link to="/" style={{ marginRight: '1rem' }}>Predicción</Link>
                <Link to="/dataset">Dataset</Link>
            </nav>

            <Routes>
                <Route path="/" element={<PredictionForm />} />
                <Route path="/dataset" element={<DatasetView />} />
            </Routes>
        </BrowserRouter>
    )
}

