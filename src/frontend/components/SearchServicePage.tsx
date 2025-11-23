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

const mapEstablishmentToClinic = (establishment: EstablishmentSummary, index: number, page: number): Clinic => ({
  id: establishment.cod_unico ?? `clinic-${page}-${index}`,
  name: establishment.nombre,
  address: establishment.direccion,
  classification: establishment.calificacion,
  latitude: establishment.latitud ?? undefined,
  longitude: establishment.longitud ?? undefined,
  distanceKm: establishment.distance ?? undefined,
});

export function SearchServicePage({ onBack, onSelectClinic }: SearchServicePageProps) {
  const [filteredClinics, setFilteredClinics] = useState<Clinic[]>([]);
  const [selectedClinic, setSelectedClinic] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [loadingMore, setLoadingMore] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [lastFilters, setLastFilters] = useState<SearchFilters>({});
  const perPage = 10;
  const [userLocation, setUserLocation] = useState<{ lat: number; lng: number } | null>(null);
  const [locationStatus, setLocationStatus] = useState<'idle' | 'requesting' | 'denied' | 'error' | 'granted'>('idle');

  const distanceKm = (clinic: Clinic) => {
    if (!userLocation || typeof clinic.latitude !== 'number' || typeof clinic.longitude !== 'number') return Number.POSITIVE_INFINITY;
    const toRad = (deg: number) => (deg * Math.PI) / 180;
    const R = 6371;
    const dLat = toRad(clinic.latitude - userLocation.lat);
    const dLon = toRad(clinic.longitude - userLocation.lng);
    const lat1 = toRad(userLocation.lat);
    const lat2 = toRad(clinic.latitude);
    const a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.sin(dLon / 2) * Math.sin(dLon / 2) * Math.cos(lat1) * Math.cos(lat2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  };

  const sortByDistance = (clinics: Clinic[]) => {
    if (!userLocation) return clinics;
    return [...clinics].sort((a, b) => distanceKm(a) - distanceKm(b));
  };

  const fetchClinics = async ({
    filters,
    page: requestedPage = 1,
    append = false,
  }: { filters?: SearchFilters; page?: number; append?: boolean } = {}) => {
    const isLoadMore = append || requestedPage > 1;
    setLoading(!isLoadMore);
    setLoadingMore(isLoadMore);
    setError(null);
    try {
      const effectiveFilters = filters ?? lastFilters ?? {};
      const dynamicFilters: Record<string, unknown> = {};

      if (effectiveFilters.query) {
        dynamicFilters.establecimiento = { operator: 'contains', value: effectiveFilters.query };
      }

      const results = await api.searchEstablishments({
        lugar: effectiveFilters.location || undefined,
        fecha: effectiveFilters.date || undefined,
        tipo: effectiveFilters.type || undefined,
        latitud: effectiveFilters.latitude ?? userLocation?.lat,
        longitud: effectiveFilters.longitude ?? userLocation?.lng,
        filtros: Object.keys(dynamicFilters).length ? dynamicFilters : undefined,
        page: requestedPage,
      });

      const mapped = results.map((est, idx) => mapEstablishmentToClinic(est, idx, requestedPage));

      if (append) {
        setFilteredClinics((prev) => {
          const combined = [...prev, ...mapped.filter((m) => !prev.some((p) => p.id === m.id))];
          return sortByDistance(combined);
        });
      } else {
        const sorted = sortByDistance(mapped);
        setFilteredClinics(sorted);
        setSelectedClinic(sorted[0]?.id ?? null);
      }

      setHasMore(mapped.length === perPage);
      setPage(requestedPage);
      if (filters) {
        setLastFilters(filters);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'No pudimos obtener los establecimientos');
      // Solo limpiar resultados si es la primera página; de lo contrario, mantener los ya cargados.
      if (!isLoadMore) {
        setFilteredClinics([]);
        setSelectedClinic(null);
        setHasMore(false);
      } else {
        setHasMore(false);
      }
    } finally {
      setLoading(false);
      setLoadingMore(false);
    }
  };

  useEffect(() => {
    fetchClinics({ page: 1 });
  }, []);

  useEffect(() => {
    if (!navigator.geolocation) {
      setLocationStatus('error');
      return;
    }
    setLocationStatus('requesting');
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setUserLocation({ lat: pos.coords.latitude, lng: pos.coords.longitude });
        setLocationStatus('granted');
        fetchClinics({ filters: { ...lastFilters, latitude: pos.coords.latitude, longitude: pos.coords.longitude }, page: 1, append: false });
      },
      () => {
        setLocationStatus('denied');
      },
      { enableHighAccuracy: true, timeout: 10000 }
    );
  }, []);

  const handleClinicClick = (clinicId: string) => {
    setSelectedClinic(clinicId);
  };

  const handleViewDetails = (clinicId: string) => {
    onSelectClinic(clinicId);
  };

  const handleSearch = (filters: SearchFilters) => {
    setPage(1);
    fetchClinics({ filters, page: 1, append: false });
  };

  const handleLoadMore = () => {
    if (loading || !hasMore) return;
    fetchClinics({ filters: lastFilters, page: page + 1, append: true });
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
        {locationStatus === 'requesting' && (
          <div className="mt-2 text-sm text-green-200">Obteniendo tu ubicación para mostrar centros cercanos...</div>
        )}
        {locationStatus === 'denied' && (
          <div className="mt-2 text-sm text-yellow-300">No autorizaste ubicación; mostramos resultados generales.</div>
        )}
        {locationStatus === 'error' && (
          <div className="mt-2 text-sm text-yellow-300">No pudimos acceder a tu ubicación; mostramos resultados generales.</div>
        )}

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

        {/* Pagination / Load more */}
        {filteredClinics.length > 0 && (
          <div className="mt-8 flex items-center justify-center">
            <button
              onClick={handleLoadMore}
              disabled={loadingMore || loading || !hasMore}
              className={`px-6 py-3 rounded-xl border transition-all ${
                hasMore
                  ? 'border-green-500 text-green-100 hover:bg-green-900/40'
                  : 'border-green-900 text-green-500 cursor-not-allowed'
              }`}
            >
              {loadingMore ? 'Cargando...' : hasMore ? 'Cargar más centros' : 'No hay más resultados'}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
