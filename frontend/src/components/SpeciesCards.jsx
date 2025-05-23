import React from 'react'
import axios from 'axios'

const speciesData = [
    { name: 'Setosa', image: '/images/setosa.jpg', target: 'setosa' },
    { name: 'Versicolor', image: '/images/versicolor.jpg', target: 'versicolor' },
    { name: 'Virginica', image: '/images/virginica.jpg', target: 'virginica' }
]

export default function SpeciesCards() {
    async function handleCardClick(target) {
        try {
            const response = await axios.get(`http://localhost:8000/iris/${target}`)
            console.log('Datos de la especie:', response.data)
            alert(`Datos de ${target} cargados correctamente. Revisa la consola para más detalles.`)
        } catch (err) {
            console.error('Error al cargar los datos de la especie:', err)
            alert('Error al cargar los datos de la especie.')
        }
    }

    return (
        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', marginTop: '2rem' }}>
            {speciesData.map((species) => (
                <div
                    key={species.target}
                    style={{
                        border: '1px solid #ccc',
                        borderRadius: '8px',
                        padding: '1rem',
                        textAlign: 'center',
                        cursor: 'pointer',
                        width: '150px'
                    }}
                    onClick={() => handleCardClick(species.target)}
                >
                    <img
                        src={species.image}
                        alt={species.name}
                        style={{ width: '100%', borderRadius: '8px', marginBottom: '0.5rem' }}
                    />
                    <h3>{species.name}</h3>
                </div>
            ))}
        </div>
    )
}