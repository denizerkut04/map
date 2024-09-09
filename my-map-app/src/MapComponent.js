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
    const [shortestPath, setShortestPath] = useState([]); // En kısa yol

    const [city1, setCity1] = useState('');
    const [city2, setCity2] = useState('');
    const [drawLine, setDrawLine] = useState(false); // Butona tıklanınca çizgi çizilecek

    const handleDrawLine = () => {
        // İlk kontrol: Her iki şehir de seçili mi?
        if (!(city1 && city2)) {
            alert('Lütfen her iki şehir için de bir seçim yapınız.');
        } else {
            // Şehirler aynı mı?
            if (city1 === city2) {
                alert('Şehirler farklı olmalı!');
            } else {
                // Eğer şehirler farklıysa, en kısa yolu bul.
                const shortest = findShortestPath(parseInt(city1), parseInt(city2));
                if (shortest) {
                    setShortestPath(shortest);
                } else {
                    alert('En kısa yol bulunamadı.');
                }
            }
        }
    };

    useEffect(() => {
        // REST API çağrısını gerçekleştirme
        axios.get('http://127.0.0.1:5001/api/harita')
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

    // Grafik oluşturmak için bir adjacency list yapısı
        const graph = {};
        for (let i = 0; i < triangles.length; i += 3) {
            const [a, b, c] = [triangles[i], triangles[i + 1], triangles[i + 2]];
            addEdge(graph, a, b);
            addEdge(graph, b, c);
            addEdge(graph, c, a);
        }

        function addEdge(graph, from, to) {
            if (!graph[from]) graph[from] = [];
            if (!graph[to]) graph[to] = [];
            graph[from].push(to);
            graph[to].push(from);
        }

        // Dijkstra algoritmasını uygulayarak en kısa yolu bul
        const findShortestPath = (start, end) => {
            const distances = {};
            const previous = {};
            const queue = [];

            // Tüm düğümleri sonsuz mesafe ile başlatıyoruz
            cities.forEach((city, index) => {
                distances[index] = Infinity;
                previous[index] = null;
            });
            distances[start] = 0;
            queue.push([start, 0]);

            while (queue.length > 0) {
                const [currentNode] = queue.shift();

                if (currentNode === end) {
                    // En kısa yolu geri izliyoruz
                    const path = [];
                    let step = end;
                    while (step !== null) {
                        path.unshift(step);
                        step = previous[step];
                    }
                    return path.map(node => coordinates[node]);
                }
                graph[currentNode].forEach(neighbor => {
                    const alt = distances[currentNode] + 1; // Eşit mesafe olarak 1 kabul ettik
                    if (alt < distances[neighbor]) {
                        distances[neighbor] = alt;
                        previous[neighbor] = currentNode;
                        queue.push([neighbor, alt]);
                    }
                });
            }

            return null; // Eğer yol bulunamazsa
        };

        return (
        <div>

            <div style={{marginBottom: '10px'}}>
                <label>
                    Şehir 1:
                    <select value={city1} onChange={(e) => setCity1(e.target.value)}>
                        <option value="">Seçiniz</option>
                        {cities.map((city, index) => (
                            <option key={index} value={city.plaka}>{city.plaka} {city.il_adi}</option>
                        ))}
                    </select>
                </label>

                <label>
                    Şehir 2:
                    <select value={city2} onChange={(e) => setCity2(e.target.value)}>
                        <option value="">Seçiniz</option>
                        {cities.map((city, index) => (
                            <option key={index} value={city.plaka}>{city.plaka} {city.il_adi}</option>
                        ))}
                    </select>
                </label>

                <button onClick={handleDrawLine}>Çizgi Çiz</button>
            </div>

            <MapContainer center={position} zoom={zoomLevel} style={{height: "100vh", width: "100%"}}>
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
                    <Polyline key={index} positions={line} color="blue" weight={2}/>
                ))}
                {shortestPath.length > 0 && (
                    <Polyline positions={shortestPath} color="red" weight={3}/>
                )}

            </MapContainer>
        </div>
    );
};

export default MapComponent;