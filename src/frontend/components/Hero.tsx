import { Hospital, Pill } from 'lucide-react';
import { ActionButton } from './ActionButton';

interface HeroProps {
  onNavigate: (page: 'home' | 'search-service' | 'check-medicine') => void;
}

export function Hero({ onNavigate }: HeroProps) {
  return (
    <div className="flex items-center justify-center min-h-screen px-4 py-20">
      <div className="max-w-4xl w-full text-center">
        {/* Logo/Brand */}
        <div className="mb-8">
          <h1 className="text-6xl mb-4 bg-gradient-to-r from-green-300 via-green-100 to-green-300 bg-clip-text text-transparent">
            Welcome to SamiLife
          </h1>
        </div>

        {/* Description */}
        <p className="text-xl text-green-100 mb-12 max-w-2xl mx-auto leading-relaxed">
          Your intelligent search engine for finding the best clinics and medications. 
          Discover healthcare services and get accurate medicine information with ease and confidence.
        </p>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-6 justify-center items-center">
          <ActionButton
            icon={<Hospital className="w-8 h-8" />}
            label="Search Service"
            onClick={() => onNavigate('search-service')}
            variant="primary"
          />
          <ActionButton
            icon={<Pill className="w-8 h-8" />}
            label="Check Medicine"
            onClick={() => onNavigate('check-medicine')}
            variant="secondary"
          />
        </div>
      </div>
    </div>
  );
}