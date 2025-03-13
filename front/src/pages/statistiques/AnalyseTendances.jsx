import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import axios from 'axios';

function AnalyseTendances() {
    const [data, setData] = useState({ labels: [], datasets: [] });

    useEffect(() => {
        axios.get('/api/statistiques/tendances')
            .then(response => {
                setData({
                    labels: response.data.map(item => item.annee),
                    datasets: [{
                        label: 'Évolution des inscriptions',
                        data: response.data.map(item => item.inscriptions),
                        borderColor: 'rgba(255,99,132,1)',
                        fill: false
                    }]
                });
            })
            .catch(error => console.error('Erreur de chargement des tendances:', error));
    }, []);

    return (
        <div>
            <h2>Analyse des Tendances d'Inscriptions</h2>
            <Line data={data} />
        </div>
    );
}
export default AnalyseTendances;
