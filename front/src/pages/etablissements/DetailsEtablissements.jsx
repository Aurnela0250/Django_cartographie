import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

const DetailsEtablissement = () => {
    // Récupération de l'ID de l'établissement depuis l'URL
    const { id } = useParams();

    // État pour stocker les détails de l'établissement
    const [etablissement, setEtablissement] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Fonction pour récupérer les détails de l'établissement depuis l'API
    useEffect(() => {
        axios.get(`http://localhost:8000/api/etablissements/${id}/`)
            .then(response => {
                setEtablissement(response.data);
                setLoading(false);
            })
            .catch(error => {
                setError("Erreur lors du chargement des données.");
                setLoading(false);
            });
    }, [id]);

    if (loading) return <p>Chargement...</p>;
    if (error) return <p>{error}</p>;

    return (
        <div className="details-container">
            <h1>{etablissement.nom}</h1>
            <img src={etablissement.image_url} alt={etablissement.nom} className="etablissement-image" />
            <p><strong>Adresse :</strong> {etablissement.adresse}</p>
            <p><strong>Type :</strong> {etablissement.type}</p>
            <p><strong>Description :</strong> {etablissement.description}</p>
            <p><strong>Nombre d'étudiants :</strong> {etablissement.nombre_etudiants}</p>
        </div>
    );
};

export default DetailsEtablissement;
