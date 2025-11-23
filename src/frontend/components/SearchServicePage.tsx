import { SearchBar } from './SearchBar';
import { ClinicList } from './ClinicList';
import { MapView } from './MapView';
import { ArrowLeft } from 'lucide-react';
import { useEffect, useState } from 'react';
import { api, EstablishmentSummary } from '../api/api';
import { Clinic, SearchFilters } from './types';

interface SearchServicePageProps {
  onBack: () => void;
  onSelectClinic: (clinicId: string) => void;
}

const mapEstablishmentToClinic = (establishment: EstablishmentSummary, index: number): Clinic => ({
  id: establishment.cod_unico ?? `clinic-${index}`,
  name: establishment.nombre,
  address: establishment.direccion,
  classification: establishment.calificacion,
  latitude: establishment.latitud ?? undefined,
  longitude: establishment.longitud ?? undefined,
});

export function SearchServicePage({ onBack, onSelectClinic }: SearchServicePageProps) {
  const [filteredClinics, setFilteredClinics] = useState<Clinic[]>([]);
  const [selectedClinic, setSelectedClinic] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchClinics = async (filters?: SearchFilters) => {
    setLoading(true);
    setError(null);
    try {
      const dynamicFilters: Record<string, unknown> = {};

      if (filters?.query) {
        dynamicFilters.establecimiento = { operator: 'contains', value: filters.query };
      }

      const results = await api.searchEstablishments({
        lugar: filters?.location || undefined,
        fecha: filters?.date || undefined,
        tipo: filters?.type || undefined,
        filtros: Object.keys(dynamicFilters).length ? dynamicFilters : undefined,
        page: 1,
      });

      const mapped = results.map(mapEstablishmentToClinic);
      setFilteredClinics(mapped);
      setSelectedClinic(mapped[0]?.id ?? null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'No pudimos obtener los establecimientos');
      setFilteredClinics([]);
      setSelectedClinic(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchClinics();
  }, []);

  const handleClinicClick = (clinicId: string) => {
    setSelectedClinic(clinicId);
  };

  const handleViewDetails = (clinicId: string) => {
    onSelectClinic(clinicId);
  };

  const handleSearch = (filters: SearchFilters) => {
    fetchClinics(filters);
  };

  return (
    <div className="min-h-screen pt-24 pb-12 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Back Button */}
        <button
          onClick={onBack}
          className="flex items-center gap-2 text-green-300 hover:text-white transition-colors mb-6"
        >
          <ArrowLeft className="w-5 h-5" />
          <span>Back to Home</span>
        </button>

        {/* Page Title */}
        <h1 className="text-4xl text-white mb-8">Search Healthcare Services</h1>

        {/* Search Bar */}
        <SearchBar onSearch={handleSearch} isLoading={loading} />

        {error && (
          <div className="mt-4 text-sm text-red-200 bg-red-900/30 border border-red-500/30 rounded-lg px-4 py-3">
            {error}
          </div>
        )}

        {/* Results Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
          {/* Clinic List - Left Side */}
          <ClinicList
            clinics={filteredClinics}
            selectedClinic={selectedClinic}
            onSelectClinic={handleClinicClick}
            onViewDetails={handleViewDetails}
            isLoading={loading}
          />

          {/* Map - Right Side */}
          <MapView
            clinics={filteredClinics}
            selectedClinic={selectedClinic}
            onSelectClinic={handleClinicClick}
            isLoading={loading}
          />
        </div>
      </div>
    </div>
  );
}
