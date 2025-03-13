import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:8000/api/etablissements/';

// Récupérer la liste des établissements
export const getEtablissements = async () => {
  try {
    const response = await axios.get(BASE_URL);
    return response.data;
  } catch (error) {
    console.error('Erreur lors de la récupération des établissements:', error);
    return [];
  }
};

// Créer un nouvel établissement
export const createEtablissement = async (etablissementData) => {
  try {
    const response = await axios.post(BASE_URL, etablissementData, {
      headers: { 'Content-Type': 'application/json' },
    });
    return response.data; // Retourne les données de l'établissement créé
  } catch (error) {
    console.error('Erreur lors de la création de l’établissement:', error);
    return null;
  }
};
