import React from 'react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import CarteMadagascar from '../components/CarteMadagascar';

function Accueil() {
    return (
        <div>
            <Navbar />
            <header>
                <h1>Bienvenue sur le Portail des Universités</h1>
                <p>Trouvez facilement les établissements et formations à Madagascar</p>
            </header>
            <main>
                <section>
                    <h2>Carte Interactive des Universités</h2>
                    <CarteMadagascar />
                </section>
                <section>
                    <h2>Statistiques</h2>
                    <p>Découvrez les tendances des inscriptions et effectifs étudiants</p>
                </section>
            </main>
            <Footer />
        </div>
    );
}

export default Accueil;
