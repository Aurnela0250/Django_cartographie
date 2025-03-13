import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
    return (
        <nav>
            <ul>
                <li><Link to="/">Accueil</Link></li>
                <li><Link to="/etablissements">Établissements</Link></li>
                <li><Link to="/utilisateurs">Utilisateurs</Link></li>
                <li><Link to="/statistiques">Statistiques</Link></li>
            </ul>
        </nav>
    );
}
export default Navbar;
