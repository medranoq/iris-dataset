import React, { useEffect, useState } from 'react'
import axios from 'axios'

export default function SpeciesCards() {
    const [speciesData, setSpeciesData] = useState([])

    useEffect(() => {
        async function fetchSpecies() {
            try {
                const response = await axios.get('http://localhost:8000/spices')
                // Ajustamos el formato recibido para que coincida con las props que espera el componente
                const formattedData = response.data.spices.map(item => ({
                    target: item.target,
                    name: item.target_name,
                    image: `http://localhost:8000${item.image_url}`
                }))
                setSpeciesData(formattedData)
            } catch (err) {
                console.error('Error al obtener los datos de especies:', err)
                alert('No se pudieron cargar las especies.')
            }
        }

        fetchSpecies()
    }, [])

    async function handleCardClick(target) {
        try {
            const response = await axios.get(`http://localhost:8000/spices/${target}`)
            console.log('Datos de la especie:', response.data)
            alert(`Datos de ${target} cargados correctamente. Revisa la consola para más detalles.`)
        } catch (err) {
            console.error('Error al cargar los datos de la especie:', err)
            alert('Error al cargar los datos de la especie.')
        }

        // Aquí podrías redirigir a otra página o mostrar más detalles de la especie

        return (
            <div>
                {/* Aquí podrías renderizar más detalles de la especie */}
                <h2>{target} Details</h2>
            </div>
        )
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
