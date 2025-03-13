import React, { useEffect, useState } from 'react';
import { getEtablissements } from '../../api/apiEtablissements'; // Import API

const Etablissements = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const etablissements = await getEtablissements();
      setData(etablissements);
    };

    fetchData();
  }, []);

  return (
    <div>
      <h1>Liste des établissements</h1>
      <ul>
        {data.length > 0 ? (
          data.map((item) => (
            <li key={item.id}>{item.nom}</li> // Assurez-vous que "nom" existe dans votre API
          ))
        ) : (
          <p>Aucune donnée disponible</p>
        )}
      </ul>
    </div>
  );
};

export default Etablissements;
