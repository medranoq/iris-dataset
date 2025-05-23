import React, {useEffect, useState} from 'react'
import axios from 'axios'
import {
    BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer
} from 'recharts'

export default function DatasetView() {
    const [data, setData] = useState([])
    const [metadata, setMetadata] = useState(null)
    const [loading, setLoading] = useState(true)
    const fieldMap = [{key: 'sepal_length', label: 'Sepal Length (cm)'}, {
        key: 'sepal_width',
        label: 'Sepal Width (cm)'
    }, {key: 'petal_length', label: 'Petal Length (cm)'}, {key: 'petal_width', label: 'Petal Width (cm)'},]

    useEffect(() => {
        async function fetchData() {
            try {
                const response = await axios.get('http://localhost:8000/iris')
                const irisRows = response.data.data
                const meta = response.data.metadata

                const targetNames = ['setosa', 'versicolor', 'virginica']
                const processed = irisRows.map((row, idx) => ({
                    ...row, species: targetNames[Math.floor(idx / 50)]
                }))

                setData(processed)
                setMetadata(meta)
            } catch (err) {
                console.error('Error al cargar los datos del dataset:', err)
                setData([])
                setMetadata(null)
            } finally {
                setLoading(false)
            }
        }

        fetchData()
    }, [])

    if (loading) return <p>Cargando datos...</p>
    if (!data.length) return <p>No hay datos disponibles.</p>

    const classCounts = data.reduce((acc, item) => {
        acc[item.species] = (acc[item.species] || 0) + 1
        return acc
    }, {})

    const chartData = Object.entries(classCounts).map(([key, value]) => ({
        species: key, count: value
    }))

    return (<div style={{padding: '2rem', fontFamily: 'sans-serif'}}>
            <h1>Información del Dataset Iris</h1>

            {/* GRID de dos columnas arriba */}
            <div
                style={{
                    display: 'grid',
                    gridTemplateColumns: '1fr 1fr',
                    gap: '2rem',
                    marginBottom: '3rem',
                    alignItems: 'flex-start'
                }}
            >
                {/* Descripción */}
                <section>
                    <h2>Descripción</h2>
                    {metadata && (<>
            <pre style={{
                whiteSpace: 'pre-wrap',
                background: '#0000000',
                padding: '1rem',
                borderRadius: '8px',
                maxHeight: '300px',
                overflow: 'auto'
            }}>
              {metadata.description}
            </pre>

                            <div style={{marginTop: '1rem'}}>
                                <h3>Características</h3>
                                <ul>
                                    {metadata.feature_names.map((name, i) => (<li key={i}>{name}</li>))}
                                </ul>
                                <p><strong>Instancias:</strong> {metadata.shape[0]}</p>
                                <p><strong>Atributos:</strong> {metadata.shape[1]}</p>
                            </div>
                        </>)}
                </section>

                {/* Gráfico */}
                <section>
                    <h2>Distribución de Clases</h2>
                    <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={chartData}>
                            <XAxis dataKey="species"/>
                            <YAxis/>
                            <Tooltip/>
                            <Legend/>
                            <Bar dataKey="count" fill="#8884d8"/>
                        </BarChart>
                    </ResponsiveContainer>
                </section>
            </div>

            {/* Tabla de datos abajo */}
            <section>
                <h2>Datos del Dataset</h2>
                <div style={{
                    overflowX: 'auto', border: '1px solid #ccc', borderRadius: '8px'
                }}>
                    <table style={{width: '100%', borderCollapse: 'collapse'}}>
                        <thead style={{background: '#f0f0f0'}}>
                        <tr>
                            {fieldMap.map((col) => (
                                <th key={col.key} style={{padding: '8px', border: '1px solid #ddd'}}>{col.label}</th>))}
                            <th style={{padding: '8px', border: '1px solid #ddd'}}>Species</th>
                        </tr>
                        </thead>
                        <tbody>
                        {data.map((row, idx) => (<tr key={idx}>
                                {fieldMap.map((col) => (
                                    <td key={col.key} style={{padding: '8px', border: '1px solid #eee'}}>
                                        {row[col.key]}
                                    </td>))}
                                <td style={{padding: '8px', border: '1px solid #eee'}}>{row.species}</td>
                            </tr>))}
                        </tbody>
                    </table>
                </div>
            </section>
        </div>)

}
