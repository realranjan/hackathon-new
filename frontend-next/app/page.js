"use client";
import { useEffect, useRef, useState } from 'react';
import mapboxgl from 'mapbox-gl';
import axios from 'axios';

mapboxgl.accessToken = process.env.NEXT_PUBLIC_MAPBOX_TOKEN;

export default function Home() {
  const mapContainer = useRef(null);
  const map = useRef(null);
  const [alerts, setAlerts] = useState([]);
  const lastFetch = useRef(0);

  // Throttle fetching alerts to once every 10 seconds
  useEffect(() => {
    const fetchAlerts = () => {
      const now = Date.now();
      if (now - lastFetch.current > 10000) { // 10 seconds
        axios.get('http://localhost:8000/alerts/')
          .then(res => setAlerts(res.data.alerts));
        lastFetch.current = now;
      }
    };
    fetchAlerts();
    const interval = setInterval(fetchAlerts, 2000); // check every 2s, but only fetch if 10s passed
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (map.current) return;
    map.current = new mapboxgl.Map({
      container: mapContainer.current,
      style: 'mapbox://styles/mapbox/streets-v11',
      center: [77.7, 12.95], // Default to Bangalore
      zoom: 4
    });
  }, []);

  useEffect(() => {
    if (!map.current) return;
    alerts.forEach(alert => {
      // Example: Use hardcoded coords for demo
      const coords = {
        'Bangalore Port': [77.7, 12.95],
        'Chennai': [80.27, 13.08],
        'Mumbai': [72.88, 19.07]
      }[alert.event.location];
      if (coords) {
        new mapboxgl.Marker()
          .setLngLat(coords)
          .setPopup(new mapboxgl.Popup().setText(
            `${alert.event.event_type} at ${alert.event.location}\nRisk: ${alert.action_plan.risk_score}`
          ))
          .addTo(map.current);
      }
    });
  }, [alerts]);

  return (
    <div>
      <h1>SupplyWhiz Map Dashboard</h1>
      <div ref={mapContainer} style={{ width: '100%', height: '600px' }} />
    </div>
  );
} 