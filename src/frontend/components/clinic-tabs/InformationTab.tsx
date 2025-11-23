import { MapPin, Phone, Mail, Clock, Star } from 'lucide-react';
import { ImageWithFallback } from '../figma/ImageWithFallback';

interface InformationTabProps {
  clinic: any;
}

export function InformationTab({ clinic }: InformationTabProps) {
  return (
    <div className="space-y-6">
      {/* Clinic Image */}
      <div className="bg-gradient-to-br from-green-900/40 to-green-950/40 backdrop-blur-sm rounded-2xl p-6 border border-green-700/30">
        <div className="aspect-video w-full rounded-xl overflow-hidden bg-green-800/30 mb-4">
          <ImageWithFallback
            src="https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=800&h=500&fit=crop"
            alt={clinic.name}
            className="w-full h-full object-cover"
          />
        </div>
        
        <div className="flex items-center gap-2 mb-4">
          <Star className="w-5 h-5 text-yellow-400" fill="currentColor" />
          <span className="text-white text-lg">{clinic.rating} Rating</span>
        </div>

        <h2 className="text-2xl text-white mb-4">About {clinic.name}</h2>
        <p className="text-green-200 leading-relaxed mb-6">
          {clinic.description}
        </p>
      </div>

      {/* Contact Information */}
      <div className="bg-gradient-to-br from-green-900/40 to-green-950/40 backdrop-blur-sm rounded-2xl p-6 border border-green-700/30">
        <h3 className="text-xl text-white mb-4">Contact Information</h3>
        
        <div className="space-y-4">
          <div className="flex items-start gap-3">
            <MapPin className="w-5 h-5 text-green-400 mt-0.5" />
            <div>
              <p className="text-sm text-green-300 mb-1">Address</p>
              <p className="text-white">{clinic.address}</p>
            </div>
          </div>

          <div className="flex items-start gap-3">
            <Phone className="w-5 h-5 text-green-400 mt-0.5" />
            <div>
              <p className="text-sm text-green-300 mb-1">Phone</p>
              <p className="text-white">{clinic.phone}</p>
            </div>
          </div>

          <div className="flex items-start gap-3">
            <Mail className="w-5 h-5 text-green-400 mt-0.5" />
            <div>
              <p className="text-sm text-green-300 mb-1">Email</p>
              <p className="text-white">{clinic.email}</p>
            </div>
          </div>

          <div className="flex items-start gap-3">
            <Clock className="w-5 h-5 text-green-400 mt-0.5" />
            <div>
              <p className="text-sm text-green-300 mb-1">Hours</p>
              <p className="text-white">{clinic.hours}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Map Placeholder */}
      <div className="bg-gradient-to-br from-green-900/40 to-green-950/40 backdrop-blur-sm rounded-2xl p-6 border border-green-700/30">
        <h3 className="text-xl text-white mb-4">Location</h3>
        <div className="w-full h-64 bg-gradient-to-br from-green-950 to-black rounded-xl border border-green-700/30 flex items-center justify-center relative overflow-hidden">
          {/* Grid overlay */}
          <div className="absolute inset-0 opacity-20" style={{
            backgroundImage: `linear-gradient(rgba(134, 239, 172, 0.3) 1px, transparent 1px), linear-gradient(90deg, rgba(134, 239, 172, 0.3) 1px, transparent 1px)`,
            backgroundSize: '40px 40px'
          }}></div>
          
          {/* Center marker */}
          <div className="relative z-10 bg-green-500 rounded-full p-4">
            <MapPin className="w-8 h-8 text-white" fill="white" />
          </div>
        </div>
      </div>
    </div>
  );
}
