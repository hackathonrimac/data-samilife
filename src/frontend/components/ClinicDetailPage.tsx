import { ArrowLeft, MapPin, Info, Calendar, Pill } from 'lucide-react';
import { useState } from 'react';
import { InformationTab } from './clinic-tabs/InformationTab';
import { BookAppointmentTab } from './clinic-tabs/BookAppointmentTab';
import { MedicationsTab } from './clinic-tabs/MedicationsTab';

interface ClinicDetailPageProps {
  clinicId: string;
  onBack: () => void;
}

type TabType = 'information' | 'appointment' | 'medications';

// Mock clinic data - in a real app, this would come from an API
const clinicData: Record<string, any> = {
  '1': {
    id: '1',
    name: 'Green Valley Medical Center',
    type: 'Hospital',
    address: '123 Health St, Medical District',
    phone: '+1 (555) 123-4567',
    email: 'contact@greenvalley.com',
    rating: 4.8,
    description: 'Green Valley Medical Center is a state-of-the-art healthcare facility dedicated to providing comprehensive medical services with a patient-centered approach. Our team of experienced healthcare professionals offers specialized care across multiple disciplines, ensuring the highest quality treatment for all our patients.',
    image: 'hospital building',
    hours: 'Mon-Fri: 8:00 AM - 8:00 PM, Sat-Sun: 9:00 AM - 5:00 PM',
    specialties: [
      {
        id: '1',
        name: 'Cardiology',
        doctors: [
          {
            id: '1',
            name: 'Dr. Sarah Johnson',
            title: 'Cardiologist',
            experience: '15 years',
            availability: ['Mon 9:00 AM', 'Wed 2:00 PM', 'Fri 10:00 AM']
          },
          {
            id: '2',
            name: 'Dr. Michael Chen',
            title: 'Cardiac Surgeon',
            experience: '20 years',
            availability: ['Tue 11:00 AM', 'Thu 3:00 PM']
          }
        ]
      },
      {
        id: '2',
        name: 'Orthopedics',
        doctors: [
          {
            id: '3',
            name: 'Dr. Robert Williams',
            title: 'Orthopedic Surgeon',
            experience: '12 years',
            availability: ['Mon 1:00 PM', 'Wed 9:00 AM', 'Fri 2:00 PM']
          }
        ]
      },
      {
        id: '3',
        name: 'Pediatrics',
        doctors: [
          {
            id: '4',
            name: 'Dr. Emily Davis',
            title: 'Pediatrician',
            experience: '10 years',
            availability: ['Mon 10:00 AM', 'Tue 2:00 PM', 'Thu 11:00 AM', 'Fri 9:00 AM']
          },
          {
            id: '5',
            name: 'Dr. James Martinez',
            title: 'Pediatric Specialist',
            experience: '8 years',
            availability: ['Wed 1:00 PM', 'Fri 3:00 PM']
          }
        ]
      }
    ],
    medications: [
      { id: '1', name: 'Amoxicillin', category: 'Antibiotics', inStock: true, price: '$15.99' },
      { id: '2', name: 'Lisinopril', category: 'Blood Pressure', inStock: true, price: '$12.50' },
      { id: '3', name: 'Metformin', category: 'Diabetes', inStock: true, price: '$10.00' },
      { id: '4', name: 'Atorvastatin', category: 'Cholesterol', inStock: true, price: '$18.75' },
      { id: '5', name: 'Omeprazole', category: 'Gastric', inStock: false, price: '$14.25' },
      { id: '6', name: 'Albuterol', category: 'Respiratory', inStock: true, price: '$22.00' }
    ]
  },
  '2': {
    id: '2',
    name: 'City Care Clinic',
    type: 'Clinic',
    address: '456 Wellness Ave, Downtown',
    phone: '+1 (555) 234-5678',
    email: 'info@citycare.com',
    rating: 4.5,
    description: 'City Care Clinic provides accessible and affordable healthcare services to the community. Our experienced medical professionals are committed to delivering personalized care in a welcoming environment.',
    image: 'medical clinic',
    hours: 'Mon-Fri: 9:00 AM - 6:00 PM, Sat: 10:00 AM - 3:00 PM',
    specialties: [
      {
        id: '1',
        name: 'General Practice',
        doctors: [
          {
            id: '1',
            name: 'Dr. Lisa Anderson',
            title: 'General Practitioner',
            experience: '18 years',
            availability: ['Mon 9:00 AM', 'Tue 10:00 AM', 'Wed 2:00 PM', 'Thu 11:00 AM']
          }
        ]
      },
      {
        id: '2',
        name: 'Dermatology',
        doctors: [
          {
            id: '2',
            name: 'Dr. Kevin Park',
            title: 'Dermatologist',
            experience: '9 years',
            availability: ['Tue 1:00 PM', 'Thu 3:00 PM', 'Fri 10:00 AM']
          }
        ]
      }
    ],
    medications: [
      { id: '1', name: 'Ibuprofen', category: 'Pain Relief', inStock: true, price: '$8.99' },
      { id: '2', name: 'Cetirizine', category: 'Allergy', inStock: true, price: '$11.50' },
      { id: '3', name: 'Hydrocortisone Cream', category: 'Topical', inStock: true, price: '$9.75' }
    ]
  }
};

export function ClinicDetailPage({ clinicId, onBack }: ClinicDetailPageProps) {
  const [activeTab, setActiveTab] = useState<TabType>('information');
  
  const clinic = clinicData[clinicId] || clinicData['1'];

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

        {/* Clinic Header */}
        <div className="bg-gradient-to-br from-green-900/40 to-green-950/40 backdrop-blur-sm rounded-2xl p-6 border border-green-700/30 mb-6">
          <h1 className="text-4xl text-white mb-2">{clinic.name}</h1>
          <div className="flex items-center gap-4 text-green-200">
            <span className="text-sm">{clinic.type}</span>
            <span className="text-sm">•</span>
            <div className="flex items-center gap-1">
              <MapPin className="w-4 h-4" />
              <span className="text-sm">{clinic.address}</span>
            </div>
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
            {activeTab === 'appointment' && <BookAppointmentTab clinic={clinic} />}
            {activeTab === 'medications' && <MedicationsTab clinic={clinic} />}
          </div>
        </div>
      </div>
    </div>
  );
}
