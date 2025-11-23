import { User, Clock, Award, Calendar } from 'lucide-react';
import { useState } from 'react';

interface BookAppointmentTabProps {
  clinic: any;
}

export function BookAppointmentTab({ clinic }: BookAppointmentTabProps) {
  const [selectedSpecialty, setSelectedSpecialty] = useState<string | null>(null);
  const [selectedDoctor, setSelectedDoctor] = useState<string | null>(null);

  const handleBookAppointment = (doctorId: string, slot: string) => {
    alert(`Booking appointment with ${doctorId} at ${slot}`);
  };

  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-br from-green-900/40 to-green-950/40 backdrop-blur-sm rounded-2xl p-6 border border-green-700/30">
        <h2 className="text-2xl text-white mb-6">Book an Appointment</h2>
        <p className="text-green-200 mb-6">
          Select a specialty to view available doctors and their appointment slots.
        </p>

        {/* Specialties List */}
        <div className="space-y-4">
          {clinic.specialties.map((specialty: any) => (
            <div key={specialty.id} className="border border-green-700/30 rounded-xl overflow-hidden">
              {/* Specialty Header */}
              <button
                onClick={() => setSelectedSpecialty(selectedSpecialty === specialty.id ? null : specialty.id)}
                className="w-full px-6 py-4 bg-black/30 hover:bg-black/50 transition-colors flex items-center justify-between"
              >
                <div className="flex items-center gap-3">
                  <div className="bg-gradient-to-br from-green-400 to-green-600 p-2 rounded-lg">
                    <Award className="w-5 h-5 text-white" />
                  </div>
                  <div className="text-left">
                    <h3 className="text-white">{specialty.name}</h3>
                    <p className="text-sm text-green-300">{specialty.doctors.length} doctor(s) available</p>
                  </div>
                </div>
                <div className={`text-green-400 transform transition-transform ${selectedSpecialty === specialty.id ? 'rotate-180' : ''}`}>
                  ▼
                </div>
              </button>

              {/* Doctors List - Expanded */}
              {selectedSpecialty === specialty.id && (
                <div className="bg-black/20 p-4 space-y-4">
                  {specialty.doctors.map((doctor: any) => (
                    <div key={doctor.id} className="bg-green-900/20 rounded-lg p-4 border border-green-700/30">
                      {/* Doctor Info */}
                      <div className="flex items-start gap-4 mb-4">
                        <div className="bg-gradient-to-br from-green-400 to-green-600 rounded-full p-3">
                          <User className="w-6 h-6 text-white" />
                        </div>
                        <div className="flex-1">
                          <h4 className="text-white mb-1">{doctor.name}</h4>
                          <p className="text-sm text-green-300 mb-1">{doctor.title}</p>
                          <div className="flex items-center gap-2 text-sm text-green-200">
                            <Award className="w-4 h-4" />
                            <span>{doctor.experience} experience</span>
                          </div>
                        </div>
                      </div>

                      {/* Availability Slots */}
                      <div className="border-t border-green-700/30 pt-4">
                        <div className="flex items-center gap-2 mb-3">
                          <Clock className="w-4 h-4 text-green-400" />
                          <span className="text-sm text-green-300">Available Time Slots</span>
                        </div>
                        <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                          {doctor.availability.map((slot: string, index: number) => (
                            <button
                              key={index}
                              onClick={() => handleBookAppointment(doctor.id, slot)}
                              className="px-4 py-2 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg hover:shadow-lg hover:shadow-green-500/30 transition-all text-sm flex items-center justify-center gap-2"
                            >
                              <Calendar className="w-4 h-4" />
                              <span>{slot}</span>
                            </button>
                          ))}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
