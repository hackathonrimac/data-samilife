import { MapPin } from 'lucide-react';
import { Clinic } from './types';

interface MapViewProps {
  clinics: Clinic[];
  selectedClinic: string | null;
  onSelectClinic: (id: string) => void;
  isLoading?: boolean;
}

export function MapView({ clinics, selectedClinic, onSelectClinic, isLoading = false }: MapViewProps) {
  const clinicsWithCoords = clinics.filter(
    (clinic) =>
      typeof clinic.latitude === 'number' &&
      typeof clinic.longitude === 'number' &&
      clinic.latitude !== null &&
      clinic.longitude !== null
  );

  const latitudes = clinicsWithCoords.map((c) => c.latitude as number);
  const longitudes = clinicsWithCoords.map((c) => c.longitude as number);

  const minLat = latitudes.length ? Math.min(...latitudes) : 0;
  const maxLat = latitudes.length ? Math.max(...latitudes) : 1;
  const minLng = longitudes.length ? Math.min(...longitudes) : 0;
  const maxLng = longitudes.length ? Math.max(...longitudes) : 1;

  const latRange = maxLat - minLat || 1;
  const lngRange = maxLng - minLng || 1;

  const fallbackPositions = [
    { top: '25%', left: '30%' },
    { top: '45%', left: '60%' },
    { top: '60%', left: '25%' },
    { top: '35%', left: '70%' },
    { top: '70%', left: '50%' }
  ];

  const getPosition = (clinic: Clinic, index: number) => {
    if (clinicsWithCoords.length === 0 || clinic.latitude === undefined || clinic.longitude === undefined || clinic.latitude === null || clinic.longitude === null) {
      return fallbackPositions[index % fallbackPositions.length];
    }

    const topPercent = 10 + (((maxLat - clinic.latitude) / latRange) * 80);
    const leftPercent = 10 + (((clinic.longitude - minLng) / lngRange) * 80);

    return {
      top: `${Math.min(90, Math.max(10, topPercent))}%`,
      left: `${Math.min(90, Math.max(10, leftPercent))}%`,
    };
  };

  return (
    <div className="bg-gradient-to-br from-green-900/40 to-green-950/40 backdrop-blur-sm rounded-2xl p-6 border border-green-700/30 h-[600px] relative overflow-hidden">
      <h2 className="text-2xl text-white mb-4">Map View</h2>
      
      {/* Map Container */}
      <div className="relative w-full h-[520px] bg-gradient-to-br from-green-950 to-black rounded-xl overflow-hidden border border-green-700/30">
        {/* Grid overlay to simulate map */}
        <div className="absolute inset-0 opacity-20" style={{
          backgroundImage: `linear-gradient(rgba(134, 239, 172, 0.3) 1px, transparent 1px), linear-gradient(90deg, rgba(134, 239, 172, 0.3) 1px, transparent 1px)`,
          backgroundSize: '40px 40px'
        }}></div>

        {/* Street lines to simulate map */}
        <div className="absolute inset-0">
          <div className="absolute top-1/4 left-0 right-0 h-0.5 bg-green-700/40"></div>
          <div className="absolute top-2/4 left-0 right-0 h-0.5 bg-green-700/40"></div>
          <div className="absolute top-3/4 left-0 right-0 h-0.5 bg-green-700/40"></div>
          <div className="absolute left-1/4 top-0 bottom-0 w-0.5 bg-green-700/40"></div>
          <div className="absolute left-2/4 top-0 bottom-0 w-0.5 bg-green-700/40"></div>
          <div className="absolute left-3/4 top-0 bottom-0 w-0.5 bg-green-700/40"></div>
        </div>

        {isLoading && (
          <div className="absolute inset-0 flex items-center justify-center text-green-200 bg-black/20">
            Loading map data...
          </div>
        )}

        {/* Clinic Markers */}
        {!isLoading && clinics.map((clinic, index) => {
          const position = getPosition(clinic, index);
          const isSelected = selectedClinic === clinic.id;

          return (
            <button
              key={clinic.id}
              onClick={() => onSelectClinic(clinic.id)}
              className={`absolute transform -translate-x-1/2 -translate-y-1/2 transition-all ${
                isSelected ? 'scale-125 z-10' : 'hover:scale-110'
              }`}
              style={{ top: position.top, left: position.left }}
            >
              <div className="relative">
                {/* Marker Pin */}
                <div
                  className={`relative ${
                    isSelected
                      ? 'bg-green-400 shadow-lg shadow-green-400/50'
                      : 'bg-green-600 hover:bg-green-500'
                  } rounded-full p-3 transition-all`}
                >
                  <MapPin className="w-5 h-5 text-white" fill="white" />
                </div>

                {/* Info Popup on Selected */}
                {isSelected && (
                  <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 w-48 bg-black/90 rounded-lg p-3 border border-green-500">
                    <p className="text-white text-sm mb-1">{clinic.name}</p>
                    <p className="text-green-300 text-xs mb-1">{clinic.classification || clinic.institution || 'Healthcare facility'}</p>
                    <p className="text-green-400 text-[11px] truncate">{clinic.address}</p>
                    {/* Arrow */}
                    <div className="absolute top-full left-1/2 transform -translate-x-1/2 -mt-px">
                      <div className="w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-green-500"></div>
                    </div>
                  </div>
                )}
              </div>
            </button>
          );
        })}

        {/* Map Controls */}
        <div className="absolute bottom-4 right-4 flex flex-col gap-2">
          <button className="bg-black/70 text-white p-2 rounded-lg border border-green-700/30 hover:border-green-500 transition-colors">
            +
          </button>
          <button className="bg-black/70 text-white p-2 rounded-lg border border-green-700/30 hover:border-green-500 transition-colors">
            −
          </button>
        </div>

        {/* Map Legend */}
        <div className="absolute top-4 right-4 bg-black/70 backdrop-blur-sm rounded-lg p-3 border border-green-700/30">
          <p className="text-green-300 text-xs mb-2">Legend</p>
          <div className="flex items-center gap-2 text-xs text-white mb-1">
            <div className="w-3 h-3 bg-green-600 rounded-full"></div>
            <span>Healthcare Facility</span>
          </div>
          <div className="flex items-center gap-2 text-xs text-white">
            <div className="w-3 h-3 bg-green-400 rounded-full"></div>
            <span>Selected</span>
          </div>
        </div>
      </div>
    </div>
  );
}
