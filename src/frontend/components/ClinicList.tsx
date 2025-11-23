import { MapPin, Shield, Info } from 'lucide-react';
import { Clinic } from './types';
import { ImageWithFallback } from './figma/ImageWithFallback';

interface ClinicListProps {
  clinics: Clinic[];
  selectedClinic: string | null;
  onSelectClinic: (id: string) => void;
  onViewDetails: (id: string) => void;
  isLoading?: boolean;
}

export function ClinicList({ clinics, selectedClinic, onSelectClinic, onViewDetails, isLoading = false }: ClinicListProps) {
  return (
    <div className="bg-gradient-to-br from-green-900/40 to-green-950/40 backdrop-blur-sm rounded-2xl p-6 border border-green-700/30 h-[600px] overflow-y-auto">
      <h2 className="text-2xl text-white mb-4">Results ({clinics.length})</h2>
      
      <div className="space-y-4">
        {isLoading && (
          <div className="text-green-200 text-sm bg-black/30 border border-green-700/40 rounded-xl p-4">
            Searching for clinics...
          </div>
        )}

        {!isLoading && clinics.length === 0 && (
          <div className="text-green-200 text-sm bg-black/30 border border-green-700/40 rounded-xl p-4">
            No clinics found with the current filters.
          </div>
        )}

        {!isLoading && clinics.map((clinic) => (
          <div
            key={clinic.id}
            onClick={() => onSelectClinic(clinic.id)}
            className={`w-full text-left bg-black/30 rounded-xl p-4 border transition-all cursor-pointer ${
              selectedClinic === clinic.id
                ? 'border-green-500 shadow-lg shadow-green-500/20'
                : 'border-green-700/30 hover:border-green-500/50'
            }`}
          >
            <div className="flex gap-4">
              {/* Clinic Image */}
              <div className="w-24 h-24 rounded-lg bg-green-800/30 overflow-hidden flex-shrink-0">
                <ImageWithFallback
                  src={`https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=200&h=200&fit=crop`}
                  alt={clinic.name}
                  className="w-full h-full object-cover"
                />
              </div>

              {/* Clinic Info */}
              <div className="flex-1 min-w-0">
                <h3 className="text-white mb-1">{clinic.name || 'Establecimiento sin nombre'}</h3>
                <p className="text-sm text-green-300 mb-2">{clinic.classification || 'Sin clasificación'}</p>
                
                <div className="flex items-center gap-2 text-sm text-green-200 mb-2">
                  <MapPin className="w-4 h-4" />
                  <span className="truncate">{clinic.address}</span>
                </div>

                <div className="flex items-center gap-3 text-xs text-green-300">
                  {clinic.institution && (
                    <span className="inline-flex items-center gap-1">
                      <Shield className="w-4 h-4 text-green-400" />
                      <span>{clinic.institution}</span>
                    </span>
                  )}
                  <span className="inline-flex items-center gap-1">
                    <Info className="w-4 h-4 text-green-400" />
                    <span>Code: {clinic.id}</span>
                  </span>
                </div>

                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onViewDetails(clinic.id);
                  }}
                  className="mt-3 px-4 py-1.5 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg hover:shadow-lg hover:shadow-green-500/30 transition-all text-sm"
                >
                  View Details
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
