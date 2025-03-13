import React from 'react';
import { Link } from 'react-router-dom';

function Sidebar() {
    return (
        <aside>
            <ul>
                <li><Link to="/">Accueil</Link></li>
                <li><Link to="/etablissements">Établissements</Link></li>
                <li><Link to="/statistiques">Statistiques</Link></li>
            </ul>
        </aside>
    );
}
export default Sidebar;