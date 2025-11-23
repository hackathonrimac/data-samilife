import { SearchBar } from './SearchBar';
import { ClinicList } from './ClinicList';
import { MapView } from './MapView';
import { ArrowLeft } from 'lucide-react';
import { useState } from 'react';

interface SearchServicePageProps {
  onBack: () => void;
  onSelectClinic: (clinicId: string) => void;
}

export interface Clinic {
  id: string;
  name: string;
  type: string;
  address: string;
  insurance: string[];
  rating: number;
  coordinates: { lat: number; lng: number };
  image: string;
}

const mockClinics: Clinic[] = [
  {
    id: '1',
    name: 'Green Valley Medical Center',
    type: 'Hospital',
    address: '123 Health St, Medical District',
    insurance: ['Medicare', 'Blue Cross', 'Aetna'],
    rating: 4.8,
    coordinates: { lat: 40.7580, lng: -73.9855 },
    image: 'hospital'
  },
  {
    id: '2',
    name: 'City Care Clinic',
    type: 'Clinic',
    address: '456 Wellness Ave, Downtown',
    insurance: ['Medicare', 'United Health', 'Cigna'],
    rating: 4.5,
    coordinates: { lat: 40.7614, lng: -73.9776 },
    image: 'clinic'
  },
  {
    id: '3',
    name: 'Sunrise Family Health',
    type: 'Family Practice',
    address: '789 Care Blvd, Northside',
    insurance: ['Blue Cross', 'Aetna', 'Humana'],
    rating: 4.7,
    coordinates: { lat: 40.7489, lng: -73.9680 },
    image: 'medical building'
  },
  {
    id: '4',
    name: 'Advanced Specialty Hospital',
    type: 'Specialty Hospital',
    address: '321 Expert Way, Medical Park',
    insurance: ['Medicare', 'Medicaid', 'United Health'],
    rating: 4.9,
    coordinates: { lat: 40.7549, lng: -73.9840 },
    image: 'modern hospital'
  },
  {
    id: '5',
    name: 'Community Health Center',
    type: 'Community Clinic',
    address: '654 Public Health Rd, Eastside',
    insurance: ['Medicaid', 'Blue Cross', 'Cigna'],
    rating: 4.3,
    coordinates: { lat: 40.7505, lng: -73.9934 },
    image: 'health center'
  }
];

export function SearchServicePage({ onBack, onSelectClinic }: SearchServicePageProps) {
  const [filteredClinics, setFilteredClinics] = useState<Clinic[]>(mockClinics);
  const [selectedClinic, setSelectedClinic] = useState<string | null>(null);

  const handleClinicClick = (clinicId: string) => {
    setSelectedClinic(clinicId);
  };

  const handleViewDetails = (clinicId: string) => {
    onSelectClinic(clinicId);
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
        <SearchBar onSearch={setFilteredClinics} allClinics={mockClinics} />

        {/* Results Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
          {/* Clinic List - Left Side */}
          <ClinicList
            clinics={filteredClinics}
            selectedClinic={selectedClinic}
            onSelectClinic={handleClinicClick}
            onViewDetails={handleViewDetails}
          />

          {/* Map - Right Side */}
          <MapView
            clinics={filteredClinics}
            selectedClinic={selectedClinic}
            onSelectClinic={handleClinicClick}
          />
        </div>
      </div>
    </div>
  );
}