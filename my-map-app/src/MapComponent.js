import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import usadata from './usa.json'; // JSON dosyasını import et

const MapComponent = () => {
    const position = [37.0902, -95.7129]; // ABD'nin merkezi koordinatları
    const zoomLevel = 4; // ABD'nin tamamını göstermek için uygun bir zoom seviyesi

    const cities = usadata; //read usa.json


    const cities1 =
    [
        {
            "name": "New York",
            "coordinates": [40.7128, -74.0060]
        },
        {
            "name": "Los Angeles",
            "coordinates": [34.0522, -118.2437]
        },
        {
            "name": "Chicago",
            "coordinates": [41.8781, -87.6298]
        },
        {
            "name": "Houston",
            "coordinates": [29.7604, -95.3698]
        },
        {
            "name": "Miami",
            "coordinates": [25.7617, -80.1918]
        }
    ]

    return (
        <MapContainer center={position} zoom={zoomLevel} style={{ height: "100vh", width: "100%" }}>
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />


            {cities.map((city, index) => (
                <Marker key={index} position={[city.latitude, city.longitude]}>
                    <Popup>
                        {city.state} {city.location}
                    </Popup>
                </Marker>
            ))}

        </MapContainer>
    );
};

export default MapComponent;