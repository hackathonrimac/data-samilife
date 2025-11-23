import { Search, MapPin, Calendar, Building2, Shield, SlidersHorizontal } from 'lucide-react';
import { useState } from 'react';
import { SearchFilters } from './types';

interface SearchBarProps {
  onSearch: (filters: SearchFilters) => void;
  isLoading?: boolean;
}

export function SearchBar({ onSearch, isLoading = false }: SearchBarProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [location, setLocation] = useState('');
  const [date, setDate] = useState('');
  const [type, setType] = useState('');
  const [insurance, setInsurance] = useState('');
  const [showAdvanced, setShowAdvanced] = useState(false);

  const handleSearch = () => {
    onSearch({
      query: searchQuery,
      location,
      date,
      type,
      insurance,
    });
  };

  return (
    <div className="bg-gradient-to-br from-green-900/40 to-green-950/40 backdrop-blur-sm rounded-2xl p-6 border border-green-700/30">
      {/* Main Search Bar */}
      <div className="flex gap-4 mb-4">
        <div className="flex-1 relative">
          <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-green-400 w-5 h-5" />
          <input
            type="text"
            placeholder="Search for clinics, hospitals, or services..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-black/50 text-white pl-12 pr-4 py-3 rounded-xl border border-green-700/30 focus:border-green-500 focus:outline-none transition-colors"
          />
        </div>
        <button
          onClick={handleSearch}
          disabled={isLoading}
          className="px-8 py-3 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-xl hover:shadow-lg hover:shadow-green-500/30 transition-all"
        >
          {isLoading ? 'Searching...' : 'Search'}
        </button>
      </div>

      {/* Filters */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {/* Location Filter */}
        <div className="relative">
          <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 text-green-400 w-4 h-4" />
          <input
            type="text"
            placeholder="Location"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            className="w-full bg-black/50 text-white pl-10 pr-4 py-2 rounded-lg border border-green-700/30 focus:border-green-500 focus:outline-none transition-colors text-sm"
          />
        </div>

        {/* Date Filter */}
        <div className="relative">
          <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 text-green-400 w-4 h-4" />
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            className="w-full bg-black/50 text-white pl-10 pr-4 py-2 rounded-lg border border-green-700/30 focus:border-green-500 focus:outline-none transition-colors text-sm"
          />
        </div>

        {/* Type Filter */}
        <div className="relative">
          <Building2 className="absolute left-3 top-1/2 transform -translate-y-1/2 text-green-400 w-4 h-4" />
          <select
            value={type}
            onChange={(e) => setType(e.target.value)}
            className="w-full bg-black/50 text-white pl-10 pr-4 py-2 rounded-lg border border-green-700/30 focus:border-green-500 focus:outline-none transition-colors text-sm appearance-none"
          >
            <option value="">All Types</option>
            <option value="Hospital">Hospital</option>
            <option value="Clinic">Clinic</option>
            <option value="Family Practice">Family Practice</option>
            <option value="Specialty">Specialty</option>
          </select>
        </div>

        {/* Insurance Filter */}
        <div className="relative">
          <Shield className="absolute left-3 top-1/2 transform -translate-y-1/2 text-green-400 w-4 h-4" />
          <select
            value={insurance}
            onChange={(e) => setInsurance(e.target.value)}
            className="w-full bg-black/50 text-white pl-10 pr-4 py-2 rounded-lg border border-green-700/30 focus:border-green-500 focus:outline-none transition-colors text-sm appearance-none"
          >
            <option value="">All Insurance</option>
            <option value="Medicare">Medicare</option>
            <option value="Medicaid">Medicaid</option>
            <option value="Blue Cross">Blue Cross</option>
            <option value="Aetna">Aetna</option>
            <option value="United Health">United Health</option>
            <option value="Cigna">Cigna</option>
          </select>
        </div>
      </div>

      {/* Advanced Filters Button */}
      <button
        onClick={() => setShowAdvanced(!showAdvanced)}
        className="mt-4 flex items-center gap-2 text-green-400 hover:text-green-300 transition-colors text-sm"
      >
        <SlidersHorizontal className="w-4 h-4" />
        <span>Advanced Filters</span>
      </button>

      {/* Advanced Filters Panel */}
      {showAdvanced && (
        <div className="mt-4 pt-4 border-t border-green-700/30">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="text-green-300 text-sm mb-2 block">Rating</label>
              <select className="w-full bg-black/50 text-white px-4 py-2 rounded-lg border border-green-700/30 focus:border-green-500 focus:outline-none transition-colors text-sm">
                <option value="">Any Rating</option>
                <option value="4">4+ Stars</option>
                <option value="4.5">4.5+ Stars</option>
                <option value="4.8">4.8+ Stars</option>
              </select>
            </div>
            <div>
              <label className="text-green-300 text-sm mb-2 block">Distance</label>
              <select className="w-full bg-black/50 text-white px-4 py-2 rounded-lg border border-green-700/30 focus:border-green-500 focus:outline-none transition-colors text-sm">
                <option value="">Any Distance</option>
                <option value="5">Within 5 miles</option>
                <option value="10">Within 10 miles</option>
                <option value="25">Within 25 miles</option>
              </select>
            </div>
            <div>
              <label className="text-green-300 text-sm mb-2 block">Availability</label>
              <select className="w-full bg-black/50 text-white px-4 py-2 rounded-lg border border-green-700/30 focus:border-green-500 focus:outline-none transition-colors text-sm">
                <option value="">Any Time</option>
                <option value="today">Available Today</option>
                <option value="week">This Week</option>
                <option value="month">This Month</option>
              </select>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
