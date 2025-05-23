import React, { useState } from 'react'
import axios from 'axios'

const classStyles = {
    setosa: { backgroundColor: '#a8e6cf', padding: '1rem', borderRadius: '8px' },
    versicolor: { backgroundColor: '#ffd3b6', padding: '1rem', borderRadius: '8px' },
    virginica: { backgroundColor: '#ffaaa5', padding: '1rem', borderRadius: '8px' }
}

export default function PredictionForm() {
    const [formData, setFormData] = useState({
        sepal_length: '',
        sepal_width: '',
        petal_length: '',
        petal_width: ''
    })

    const [result, setResult] = useState(null)
    const [error, setError] = useState(null)
    const [loading, setLoading] = useState(false)

    function handleChange(e) {
        setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }))
    }

    async function handleSubmit(e) {
        e.preventDefault()
        setError(null)
        setLoading(true)
        setResult(null)

        try {
            const response = await axios.post('http://localhost:8000/predict', formData,
                {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
            setResult(response.data.prediction)
        } catch (err) {
            setError('Error al hacer la predicción')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div style={{maxWidth: '400px', margin: '2rem auto'}}>
            <h1>Iris Classification</h1>

            <form onSubmit={handleSubmit} style={{display: 'flex', flexDirection: 'column' }}>
                <label>
                    Sepal Length:
                    <input
                        type="number"
                        step="0.1"
                        name="sepal_length"
                        value={formData.sepal_length}
                        onChange={handleChange}
                        required
                    />
                </label>
                <br/>
                <label>
                    Sepal Width:
                    <input
                        type="number"
                        step="0.1"
                        name="sepal_width"
                        value={formData.sepal_width}
                        onChange={handleChange}
                        required
                    />
                </label>
                <br/>
                <label>
                    Petal Length:
                    <input
                        type="number"
                        step="0.1"
                        name="petal_length"
                        value={formData.petal_length}
                        onChange={handleChange}
                        required
                    />
                </label>
                <br/>
                <label>
                    Petal Width:
                    <input
                        type="number"
                        step="0.1"
                        name="petal_width"
                        value={formData.petal_width}
                        onChange={handleChange}
                        required
                    />
                </label>
                <br/>
                <button type="submit" disabled={loading} style={{marginTop: '1rem'}}>
                    {loading ? 'Clasificando...' : 'Clasificar'}
                </button>
            </form>
            {error && <p style={{color: 'red'}}>{error}</p>}

            {result && (
                <div style={{marginTop: '2rem'}}>
                    <h2>Predicción:</h2>
                    <div style={classStyles[result.toLowerCase()] || {}}>
                        <strong>{result}</strong>
                    </div>
                </div>
            )}
        </div>
    )
}
