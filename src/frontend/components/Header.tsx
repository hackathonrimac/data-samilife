import { Heart } from 'lucide-react';

interface HeaderProps {
  onNavigate: (page: 'home' | 'search-service' | 'check-medicine') => void;
}

export function Header({ onNavigate }: HeaderProps) {
  return (
    <header className="absolute top-0 left-0 right-0 z-20 px-6 py-6">
      <nav className="max-w-7xl mx-auto flex items-center justify-between">
        {/* Logo */}
        <button onClick={() => onNavigate('home')} className="flex items-center gap-2">
          <div className="bg-gradient-to-br from-green-400 to-green-600 p-2 rounded-lg">
            <Heart className="w-6 h-6 text-white" fill="white" />
          </div>
          <span className="text-2xl text-white">SamiLife</span>
        </button>

        {/* Navigation Links */}
        <div className="hidden md:flex items-center gap-8">
          <button onClick={() => onNavigate('search-service')} className="text-green-200 hover:text-white transition-colors">
            Services
          </button>
          <a href="#about" className="text-green-200 hover:text-white transition-colors">
            About
          </a>
          <a href="#contact" className="text-green-200 hover:text-white transition-colors">
            Contact
          </a>
        </div>
      </nav>
    </header>
  );
}