import React, { useEffect } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

function CarteMadagascar() {
    useEffect(() => {
        const map = L.map('map').setView([-18.8792, 47.5079], 6);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(map);
    }, []);

    return <div id="map" style={{ width: "100%", height: "500px" }}></div>;
}
export default CarteMadagascar;