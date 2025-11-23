import { ArrowLeft, MapPin, Info, Calendar, Pill, Loader2, AlertTriangle, Globe } from 'lucide-react';
import { useEffect, useRef, useState } from 'react';
import { InformationTab } from './clinic-tabs/InformationTab';
import { BookAppointmentTab } from './clinic-tabs/BookAppointmentTab';
import { MedicationsTab } from './clinic-tabs/MedicationsTab';
import { api, AppointmentSlot, EstablishmentInfo, MedicationInfo } from '../api/api';

interface ClinicDetailPageProps {
  clinicId: string;
  onBack: () => void;
}

type TabType = 'information' | 'appointment' | 'medications';

declare global {
  interface Window {
    google: any;
    initClinicMapPromise?: Promise<void>;
  }
}

export function ClinicDetailPage({ clinicId, onBack }: ClinicDetailPageProps) {
  const [activeTab, setActiveTab] = useState<TabType>('information');
  const [clinic, setClinic] = useState<EstablishmentInfo | null>(null);
  const [appointments, setAppointments] = useState<AppointmentSlot[]>([]);
  const [medications, setMedications] = useState<MedicationInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [mapError, setMapError] = useState<string | null>(null);
  const mapRef = useRef<HTMLDivElement | null>(null);
  const mapInstanceRef = useRef<any>(null);

  useEffect(() => {
    const loadClinicData = async () => {
      setLoading(true);
      setError(null);
      try {
        const [info, appointmentData, medicationData] = await Promise.all([
          api.getEstablishmentInfo(clinicId),
          api.getAppointments(clinicId),
          api.getMedications(clinicId),
        ]);

        setClinic(info);
        setAppointments(appointmentData);
        setMedications(medicationData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'No pudimos cargar la información del establecimiento');
      } finally {
        setLoading(false);
      }
    };

    loadClinicData();
  }, [clinicId]);

  useEffect(() => {
    const loadGoogleMaps = async () => {
      if (window.google?.maps) return;
      if (!import.meta.env.VITE_GOOGLE_MAPS_API_KEY) {
        setMapError('Falta definir VITE_GOOGLE_MAPS_API_KEY para mostrar el mapa');
        return;
      }
      if (!window.initClinicMapPromise) {
        window.initClinicMapPromise = new Promise((resolve, reject) => {
          const script = document.createElement('script');
          script.src = `https://maps.googleapis.com/maps/api/js?key=${import.meta.env.VITE_GOOGLE_MAPS_API_KEY}`;
          script.async = true;
          script.onload = () => resolve();
          script.onerror = () => reject(new Error('No se pudo cargar Google Maps'));
          document.head.appendChild(script);
        });
      }
      await window.initClinicMapPromise;
    };

    const renderMap = async () => {
      if (!clinic) return;
      const lat = typeof clinic.latitud === 'number' ? clinic.latitud : Number(clinic.latitud);
      const lng = typeof clinic.longitud === 'number' ? clinic.longitud : Number(clinic.longitud);
      if (!lat || !lng) return;

      try {
        await loadGoogleMaps();
        if (!mapRef.current || !window.google?.maps) return;

        mapInstanceRef.current = new window.google.maps.Map(mapRef.current, {
          center: { lat, lng },
          zoom: 15,
          mapTypeControl: false,
          streetViewControl: false,
        });

        new window.google.maps.Marker({
          position: { lat, lng },
          map: mapInstanceRef.current,
          title: clinic.nombre,
          animation: window.google.maps.Animation.DROP,
        });
      } catch (err) {
        setMapError(err instanceof Error ? err.message : 'No se pudo mostrar el mapa');
      }
    };

    renderMap();
  }, [clinic]);

  const tabs = [
    { id: 'information' as TabType, label: 'Information', icon: Info },
    { id: 'appointment' as TabType, label: 'Book Appointment', icon: Calendar },
    { id: 'medications' as TabType, label: 'Medications', icon: Pill }
  ];

  return (
    <div className="min-h-screen pt-24 pb-12 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Back Button */}
        <button
          onClick={onBack}
          className="flex items-center gap-2 text-green-300 hover:text-white transition-colors mb-6"
        >
          <ArrowLeft className="w-5 h-5" />
          <span>Back to Search</span>
        </button>

        {loading && (
          <div className="flex items-center gap-2 text-green-200 bg-green-900/30 border border-green-700/40 rounded-xl px-4 py-3 mb-6">
            <Loader2 className="w-5 h-5 animate-spin" />
            <span>Loading clinic information...</span>
          </div>
        )}

        {error && (
          <div className="flex items-center gap-2 text-red-200 bg-red-900/30 border border-red-500/30 rounded-xl px-4 py-3 mb-6">
            <AlertTriangle className="w-5 h-5" />
            <span>{error}</span>
          </div>
        )}

        {!loading && clinic && (
          <>
            {/* Clinic Header */}
            <div className="bg-gradient-to-br from-green-900/40 to-green-950/40 backdrop-blur-sm rounded-2xl p-6 border border-green-700/30 mb-6">
              <h1 className="text-4xl text-white mb-2">{clinic.nombre}</h1>
              <div className="flex flex-wrap items-center gap-4 text-green-200">
                <span className="text-sm">{clinic.clasificacion}</span>
                <span className="text-sm">•</span>
                <div className="flex items-center gap-1">
                  <MapPin className="w-4 h-4" />
                  <span className="text-sm">{clinic.direccion}</span>
                </div>
                <span className="text-sm">•</span>
                <span className="text-sm">{clinic.institucion}</span>
                {clinic.pagina && (
                  <>
                    <span className="text-sm">•</span>
                    <span className="flex items-center gap-1 text-sm">
                      <Globe className="w-4 h-4" />
                      <a href={clinic.pagina} target="_blank" rel="noreferrer" className="text-green-300 hover:text-white underline">
                        Website
                      </a>
                    </span>
                  </>
                )}
              </div>
            </div>

            {/* Main Content */}
            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
              {/* Sidebar Navigation */}
              <div className="lg:col-span-1">
                <div className="bg-gradient-to-br from-green-900/40 to-green-950/40 backdrop-blur-sm rounded-2xl p-4 border border-green-700/30 sticky top-24">
                  <nav className="space-y-2">
                    {tabs.map((tab) => {
                      const Icon = tab.icon;
                      return (
                        <button
                          key={tab.id}
                          onClick={() => setActiveTab(tab.id)}
                          className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${
                            activeTab === tab.id
                              ? 'bg-gradient-to-r from-green-500 to-green-600 text-white shadow-lg shadow-green-500/30'
                              : 'text-green-300 hover:bg-green-900/50 hover:text-white'
                          }`}
                        >
                          <Icon className="w-5 h-5" />
                          <span className="text-sm">{tab.label}</span>
                        </button>
                      );
                    })}
                  </nav>
                </div>
              </div>

              {/* Content Area */}
              <div className="lg:col-span-3">
                {activeTab === 'information' && <InformationTab clinic={clinic} />}
                {activeTab === 'appointment' && (
                  <BookAppointmentTab
                    clinicName={clinic.nombre}
                    appointments={appointments}
                    services={clinic.servicios}
                  />
                )}
                {activeTab === 'medications' && (
                  <MedicationsTab
                    clinicName={clinic.nombre}
                    medications={medications}
                  />
                )}
              </div>
            </div>

            {/* Map Section at bottom */}
            <div className="bg-gradient-to-br from-green-900/40 to-green-950/40 backdrop-blur-sm rounded-2xl p-4 border border-green-700/30 mt-6">
              <h3 className="text-lg text-white mb-3 flex items-center gap-2">
                <MapPin className="w-5 h-5" />
                Ubicación
              </h3>
              <div className="relative w-full h-72 rounded-xl overflow-hidden border border-green-700/30 bg-black/40">
                {mapError && (
                  <div className="absolute inset-0 flex items-center justify-center text-red-200 bg-black/60 text-sm px-4 text-center">
                    {mapError}
                  </div>
                )}
                <div ref={mapRef} className="w-full h-full" />
              </div>
            </div>
          </>
        )}

        {!loading && !clinic && !error && (
          <div className="flex items-center gap-2 text-yellow-200 bg-yellow-900/30 border border-yellow-700/40 rounded-xl px-4 py-3">
            <AlertTriangle className="w-5 h-5" />
            <span>No clinic data available.</span>
          </div>
        )}
      </div>
    </div>
  );
}
