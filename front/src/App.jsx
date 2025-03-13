import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Accueil from './pages/Accueil';
import ListeEtablissements from './pages/etablissements/ListeEtablissements';
import DetailsEtablissements from './pages/etablissements/DetailsEtablissements';
import Connexion from './pages/utilisateurs/Connexion';
import Inscription from './pages/utilisateurs/Inscription';
import ProfilUtilisateur from './pages/utilisateurs/ProfilUtilisateur';
import GestionUtilisateurs from './pages/utilisateurs/GestionUtilisateurs';
import Navbar from './components/Navbar';
import Footer from './components/Footer';

function App() {
    return (
        <Router>
            <div className="app-container">
                <Navbar />
                <Routes>
                    <Route path="/" element={<Accueil />} />
                    <Route path="/etablissements" element={<ListeEtablissements />} />
                    <Route path="/etablissement/:id" element={<DetailsEtablissements />} />
                    <Route path="/connexion" element={<Connexion />} />
                    <Route path="/inscription" element={<Inscription />} />
                    <Route path="/profil" element={<ProfilUtilisateur />} />
                    <Route path="/gestion-utilisateurs" element={<GestionUtilisateurs />} />
                </Routes>
                <Footer />
            </div>
        </Router>
    );
}

export default App;
