import React, { useEffect, useState } from 'react';
import axios from 'axios';

function GestionUtilisateurs() {
    const [users, setUsers] = useState([]);

    useEffect(() => {
        axios.get('/api/utilisateurs')
            .then(response => setUsers(response.data))
            .catch(error => console.error('Erreur chargement utilisateurs:', error));
    }, []);

    return (
        <div>
            <h2>Gestion des Utilisateurs</h2>
            <ul>
                {users.map(user => (
                    <li key={user.id}>{user.nom} - {user.email}</li>
                ))}
            </ul>
        </div>
    );
}
export default GestionUtilisateurs;
