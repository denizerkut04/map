import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import data from './turkiye.json'; // JSON dosyasını import et

const MapComponent = () => {
    const position = [39.0, 35.0]; // turkiye'nin merkezi koordinatları
    const zoomLevel = 6; // turkiye'nin tamamını göstermek için uygun bir zoom seviyesi

    const cities = data; //read usa.json

    return (
        <MapContainer center={position} zoom={zoomLevel} style={{ height: "100vh", width: "100%" }}>
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />


            {cities.map((city, index) => (
                <Marker key={index} position={[city.lat, city.lon]}>
                    <Popup>
                        {city.plaka} {city.il_adi}
                    </Popup>
                </Marker>
            ))}

        </MapContainer>
    );
};

export default MapComponent;