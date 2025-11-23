import { Heart, Mail, MapPin, Phone } from 'lucide-react';

export function Footer() {
  return (
    <footer className="border-t border-green-700/30 bg-black/50 backdrop-blur-sm py-12 px-4 mt-20">
      <div className="max-w-6xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          {/* Company Info */}
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className="bg-gradient-to-br from-green-400 to-green-600 p-2 rounded-lg">
                <Heart className="w-5 h-5 text-white" fill="white" />
              </div>
              <span className="text-xl text-white">SamiLife</span>
            </div>
            <p className="text-green-300 text-sm leading-relaxed">
              Your trusted intelligent search engine for healthcare services and medications.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-white mb-4">Quick Links</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <a href="#services" className="text-green-300 hover:text-white transition-colors">
                  Services
                </a>
              </li>
              <li>
                <a href="#about" className="text-green-300 hover:text-white transition-colors">
                  About Us
                </a>
              </li>
              <li>
                <a href="#privacy" className="text-green-300 hover:text-white transition-colors">
                  Privacy Policy
                </a>
              </li>
              <li>
                <a href="#terms" className="text-green-300 hover:text-white transition-colors">
                  Terms of Service
                </a>
              </li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h3 className="text-white mb-4">Contact Us</h3>
            <ul className="space-y-3 text-sm">
              <li className="flex items-center gap-2 text-green-300">
                <Mail className="w-4 h-4" />
                <span>info@samilife.com</span>
              </li>
              <li className="flex items-center gap-2 text-green-300">
                <Phone className="w-4 h-4" />
                <span>+1 (555) 123-4567</span>
              </li>
              <li className="flex items-center gap-2 text-green-300">
                <MapPin className="w-4 h-4" />
                <span>Healthcare District, Medical Ave</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Copyright */}
        <div className="pt-8 border-t border-green-700/30 text-center text-green-600 text-sm">
          © 2025 SamiLife. All rights reserved.
        </div>
      </div>
    </footer>
  );
}