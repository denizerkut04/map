import React, {useEffect, useState} from 'react';
import {MapContainer, TileLayer, Marker, Popup, Polyline} from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import Delaunator from 'delaunator';
import axios from "axios"; // Default import

const MapComponent = () => {

    const [cities, setCities] = useState([
        {
            "plaka": 0,
            "il_adi": "test",
            "lat": 39,
            "lon": 32
        }
    ]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);


    useEffect(() => {
        // REST API çağrısını gerçekleştirme
        axios.get('http://127.0.0.1:5000/api/harita')
            .then(response => {
                setCities(response.data);
                setLoading(false);
            })
            .catch(error => {
                setError(error);
                setLoading(false);
            });
    }, []);


    const position = [39.0, 35.0]; // turkiye'nin merkezi koordinatları
    const zoomLevel = 6; // turkiye'nin tamamını göstermek için uygun bir zoom seviyesi

    /*
    const ankaraCoords = cities.find(city => city.plaka === 6);
    const istanbulCoords = cities.find(city => city.plaka === 34);
    const lineAnkIst = [
            [ankaraCoords.lat, ankaraCoords.lon],
            [istanbulCoords.lat, istanbulCoords.lon]
    ];
    */

    const coordinates = cities.map(city =>
        [city.lat, city.lon]
    ); // delaunay kullanimina uygun hale getirdik

    // Delaunay Üçgenlemesi uygulama
    const delaunay = Delaunator.from(coordinates);
    const triangles = delaunay.triangles;

    // Üçgenlerin köşe koordinatlarını çıkar
    const lines = [];
    for (let i = 0; i < triangles.length; i += 3) {
        const triangle = [triangles[i], triangles[i + 1], triangles[i + 2], triangles[i]];
        lines.push(triangle.map(index => coordinates[index]));
    }

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

            {lines.map((line, index) => (
                <Polyline key={index} positions={line} color="blue" weight={2} />
            ))}

        </MapContainer>
    );
};

export default MapComponent;