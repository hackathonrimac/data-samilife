import { User, Clock, Award, Calendar, AlertCircle } from 'lucide-react';
import { useState } from 'react';
import { AppointmentSlot, ScheduleEntry, ServiceInfo } from '../../api/api';

interface BookAppointmentTabProps {
  clinicName: string;
  appointments: AppointmentSlot[];
  services: ServiceInfo[];
}

type AppointmentGroup = {
  name: string;
  slots: AppointmentSlot[];
};

const formatSchedule = (entry: ScheduleEntry) => {
  try {
    const start = new Date(entry.ini.replace(' ', 'T'));
    const end = new Date(entry.fin.replace(' ', 'T'));
    return `${start.toLocaleDateString()} ${start.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })} - ${end.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
  } catch {
    return `${entry.ini} - ${entry.fin}`;
  }
};

export function BookAppointmentTab({ clinicName, appointments, services }: BookAppointmentTabProps) {
  const [selectedGroup, setSelectedGroup] = useState<string | null>(null);

  const groupedAppointments: AppointmentGroup[] = Object.values(
    appointments.reduce((acc, slot) => {
      const key = slot.especialidad || slot.servicio || 'General';
      if (!acc[key]) {
        acc[key] = { name: key, slots: [] };
      }
      acc[key].slots.push(slot);
      return acc;
    }, {} as Record<string, AppointmentGroup>)
  );

  const handleBookAppointment = (slot: AppointmentSlot, schedule: ScheduleEntry) => {
    alert(`Booking ${slot.servicio} with ${slot.profesional} at ${formatSchedule(schedule)}`);
  };

  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-br from-green-900/40 to-green-950/40 backdrop-blur-sm rounded-2xl p-6 border border-green-700/30">
        <h2 className="text-2xl text-white mb-6">Book an Appointment</h2>
        <p className="text-green-200 mb-6">
          Select a specialty to view available professionals and their appointment slots at {clinicName}.
        </p>

        {groupedAppointments.length === 0 && (
          <div className="flex items-center gap-2 text-green-200 bg-black/30 border border-green-700/30 rounded-xl p-4">
            <AlertCircle className="w-5 h-5 text-green-400" />
            <span>No appointment slots published for this clinic yet.</span>
          </div>
        )}

        <div className="space-y-4">
          {groupedAppointments.map((group) => (
            <div key={group.name} className="border border-green-700/30 rounded-xl overflow-hidden">
              {/* Specialty Header */}
              <button
                onClick={() => setSelectedGroup(selectedGroup === group.name ? null : group.name)}
                className="w-full px-6 py-4 bg-black/30 hover:bg-black/50 transition-colors flex items-center justify-between"
              >
                <div className="flex items-center gap-3">
                  <div className="bg-gradient-to-br from-green-400 to-green-600 p-2 rounded-lg">
                    <Award className="w-5 h-5 text-white" />
                  </div>
                  <div className="text-left">
                    <h3 className="text-white">{group.name}</h3>
                    <p className="text-sm text-green-300">{group.slots.length} slot(s) available</p>
                  </div>
                </div>
                <div className={`text-green-400 transform transition-transform ${selectedGroup === group.name ? 'rotate-180' : ''}`}>
                  ▼
                </div>
              </button>

              {/* Professionals List - Expanded */}
              {selectedGroup === group.name && (
                <div className="bg-black/20 p-4 space-y-4">
                  {group.slots.map((slot, index) => (
                    <div key={`${slot.profesional}-${index}`} className="bg-green-900/20 rounded-lg p-4 border border-green-700/30">
                      {/* Professional Info */}
                      <div className="flex items-start gap-4 mb-4">
                        <div className="bg-gradient-to-br from-green-400 to-green-600 rounded-full p-3">
                          <User className="w-6 h-6 text-white" />
                        </div>
                        <div className="flex-1">
                          <h4 className="text-white mb-1">{slot.profesional}</h4>
                          <p className="text-sm text-green-300 mb-1">{slot.especialidad || slot.servicio}</p>
                          <div className="flex items-center gap-2 text-sm text-green-200">
                            <Award className="w-4 h-4" />
                            <span>CMP: {slot.cmp || 'N/A'}</span>
                          </div>
                        </div>
                      </div>

                      {/* Availability Slots */}
                      <div className="border-t border-green-700/30 pt-4">
                        <div className="flex items-center gap-2 mb-3">
                          <Clock className="w-4 h-4 text-green-400" />
                          <span className="text-sm text-green-300">Available Time Slots</span>
                        </div>
                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
                          {slot.horario.map((schedule) => (
                            <button
                              key={`${schedule.ini}-${schedule.fin}`}
                              onClick={() => handleBookAppointment(slot, schedule)}
                              className="px-4 py-2 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg hover:shadow-lg hover:shadow-green-500/30 transition-all text-sm flex items-center justify-center gap-2"
                            >
                              <Calendar className="w-4 h-4" />
                              <span className="text-left">{formatSchedule(schedule)}</span>
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

        {groupedAppointments.length === 0 && services.length > 0 && (
          <div className="mt-6 text-sm text-green-300">
            Services offered: {services.slice(0, 6).map((service) => service.servicio).join(' • ')}
          </div>
        )}
      </div>
    </div>
  );
}
