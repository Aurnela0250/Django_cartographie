import React, { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import axios from 'axios';

function GraphiquesUniversites() {
    const [data, setData] = useState({ labels: [], datasets: [] });

    useEffect(() => {
        axios.get('/api/statistiques/universites')
            .then(response => {
                setData({
                    labels: response.data.map(item => item.nom),
                    datasets: [{
                        label: 'Effectifs étudiants',
                        data: response.data.map(item => item.effectif),
                        backgroundColor: 'rgba(75,192,192,0.6)'
                    }]
                });
            })
            .catch(error => console.error('Erreur de chargement des statistiques:', error));
    }, []);

    return (
        <div>
            <h2>Effectifs des Universités</h2>
            <Bar data={data} />
        </div>
    );
}
export default GraphiquesUniversites;
