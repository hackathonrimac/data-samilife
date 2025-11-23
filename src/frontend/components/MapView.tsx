import { useEffect, useRef, useState } from 'react';
import { Clinic } from './types';

interface MapViewProps {
  clinics: Clinic[];
  selectedClinic: string | null;
  onSelectClinic: (id: string) => void;
  isLoading?: boolean;
}

declare global {
  interface Window {
    google: any;
    initMapPromise?: Promise<void>;
  }
}

const LIMA_CENTER = { lat: -12.0464, lng: -77.0428 };

export function MapView({ clinics, selectedClinic, onSelectClinic, isLoading = false }: MapViewProps) {
  const mapRef = useRef<HTMLDivElement | null>(null);
  const mapInstanceRef = useRef<any>(null);
  const markersRef = useRef<any[]>([]);
  const [mapError, setMapError] = useState<string | null>(null);

  const loadGoogleMaps = async () => {
    if (window.google?.maps) return;

    if (!import.meta.env.VITE_GOOGLE_MAPS_API_KEY) {
      setMapError('Missing Google Maps API key (VITE_GOOGLE_MAPS_API_KEY)');
      return;
    }

    if (!window.initMapPromise) {
      window.initMapPromise = new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = `https://maps.googleapis.com/maps/api/js?key=${import.meta.env.VITE_GOOGLE_MAPS_API_KEY}`;
        script.async = true;
        script.onload = () => resolve();
        script.onerror = () => reject(new Error('Failed to load Google Maps script'));
        document.head.appendChild(script);
      });
    }

    await window.initMapPromise;
  };

  useEffect(() => {
    (async () => {
      try {
        await loadGoogleMaps();
        if (!mapRef.current || !window.google?.maps) return;
        mapInstanceRef.current = new window.google.maps.Map(mapRef.current, {
          center: LIMA_CENTER,
          zoom: 12,
          mapTypeControl: false,
          streetViewControl: false,
        });
      } catch (err) {
        setMapError(err instanceof Error ? err.message : 'Failed to load map');
      }
    })();
  }, []);

  useEffect(() => {
    if (!mapInstanceRef.current || !window.google?.maps) return;

    // Clear previous markers
    markersRef.current.forEach((m) => m.setMap(null));
    markersRef.current = [];

    const bounds = new window.google.maps.LatLngBounds();
    let hasValidCoords = false;

    clinics.forEach((clinic) => {
      if (typeof clinic.latitude !== 'number' || typeof clinic.longitude !== 'number') return;
      const position = { lat: clinic.latitude, lng: clinic.longitude };
      const marker = new window.google.maps.Marker({
        position,
        map: mapInstanceRef.current,
        title: clinic.name,
        animation: window.google.maps.Animation.DROP,
      });

      marker.addListener('click', () => onSelectClinic(clinic.id));

      markersRef.current.push(marker);
      bounds.extend(position);
      hasValidCoords = true;
    });

    if (hasValidCoords) {
      mapInstanceRef.current.fitBounds(bounds);
    } else {
      mapInstanceRef.current.setCenter(LIMA_CENTER);
      mapInstanceRef.current.setZoom(12);
    }
  }, [clinics, onSelectClinic]);

  return (
    <div className="bg-gradient-to-br from-green-900/40 to-green-950/40 backdrop-blur-sm rounded-2xl p-6 border border-green-700/30 h-[600px] relative overflow-hidden">
      <h2 className="text-2xl text-white mb-4">Map View</h2>

      <div className="relative w-full h-[520px] rounded-xl overflow-hidden border border-green-700/30 bg-black/40">
        {mapError && (
          <div className="absolute inset-0 flex items-center justify-center text-red-200 bg-black/60 text-sm px-4 text-center">
            {mapError}
          </div>
        )}
        {isLoading && (
          <div className="absolute inset-0 flex items-center justify-center text-green-200 bg-black/40">
            Loading map data...
          </div>
        )}
        <div ref={mapRef} className="w-full h-full" />
      </div>
    </div>
  );
}
