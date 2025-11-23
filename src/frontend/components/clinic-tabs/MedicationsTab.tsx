import { Pill, CheckCircle, XCircle, DollarSign, Search } from 'lucide-react';
import { useEffect, useMemo, useState } from 'react';
import { MedicationInfo } from '../../api/api';

interface MedicationsTabProps {
  clinicName: string;
  medications: MedicationInfo[];
}

export function MedicationsTab({ clinicName, medications }: MedicationsTabProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [page, setPage] = useState(1);
  const perPage = 10;

  const categories = useMemo(() => ['All', ...new Set(medications.map((med) => med.tipo))], [medications]);

  const filteredMedications = medications.filter((med) => {
    const matchesSearch = med.nombre.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === 'All' || med.tipo === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const totalPages = Math.max(1, Math.ceil(filteredMedications.length / perPage));
  const paginated = filteredMedications.slice((page - 1) * perPage, page * perPage);

  const handlePageChange = (nextPage: number) => {
    if (nextPage < 1 || nextPage > totalPages) return;
    setPage(nextPage);
  };

  // Reset page when filters/search change
  useEffect(() => {
    setPage(1);
  }, [searchQuery, selectedCategory, medications]);

  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-br from-green-900/40 to-green-950/40 backdrop-blur-sm rounded-2xl p-6 border border-green-700/30">
        <h2 className="text-2xl text-white mb-6">Available Medications</h2>
        <p className="text-green-200 mb-6">
          Browse the medications available at {clinicName}. Contact the pharmacy for more information.
        </p>

        {/* Search and Filter */}
        <div className="mb-6 space-y-4">
          {/* Search Bar */}
          <div className="relative">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-green-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search medications..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-black/50 text-white pl-12 pr-4 py-3 rounded-xl border border-green-700/30 focus:border-green-500 focus:outline-none transition-colors"
            />
          </div>

          {/* Category Filter */}
          <div className="flex flex-wrap gap-2">
            {categories.map((category) => (
              <button
                key={category}
                onClick={() => setSelectedCategory(category)}
                className={`px-4 py-2 rounded-lg transition-all text-sm ${
                  selectedCategory === category
                    ? 'bg-gradient-to-r from-green-500 to-green-600 text-white shadow-lg shadow-green-500/30'
                    : 'bg-black/30 text-green-300 border border-green-700/30 hover:border-green-500/50'
                }`}
              >
                {category}
              </button>
            ))}
          </div>
        </div>

        {/* Medications Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {paginated.map((medication) => {
            const inStock = medication.stock > 0 || (medication.disponible || '').toLowerCase() === 'si';
            return (
            <div
              key={medication.codigo_med}
              className="bg-black/30 rounded-xl p-4 border border-green-700/30 hover:border-green-500/50 transition-all"
            >
              <div className="flex items-start gap-4">
                {/* Icon */}
                <div className="bg-gradient-to-br from-green-400 to-green-600 rounded-lg p-3 flex-shrink-0">
                  <Pill className="w-6 h-6 text-white" />
                </div>

                {/* Info */}
                <div className="flex-1 min-w-0">
                  <h3 className="text-white mb-1">{medication.nombre}</h3>
                  <p className="text-sm text-green-300 mb-2">{medication.tipo} • {medication.forma_farmaceutica}</p>
                  
                  <div className="flex items-center justify-between">
                    {/* Stock Status */}
                    <div className={`flex items-center gap-1 text-sm ${
                      inStock ? 'text-green-400' : 'text-red-400'
                    }`}>
                      {inStock ? (
                        <>
                          <CheckCircle className="w-4 h-4" />
                          <span>In Stock ({medication.stock})</span>
                        </>
                      ) : (
                        <>
                          <XCircle className="w-4 h-4" />
                          <span>Out of Stock</span>
                        </>
                      )}
                    </div>

                    {/* Price */}
                    <div className="flex items-center gap-1 text-white">
                      <DollarSign className="w-4 h-4 text-green-400" />
                      <span>S/. {medication.precio.toFixed(2)}</span>
                    </div>
                  </div>

                  {/* Action Button */}
                  {inStock && (
                    <button className="mt-3 w-full px-4 py-2 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg hover:shadow-lg hover:shadow-green-500/30 transition-all text-sm">
                      Request Information
                    </button>
                  )}
                </div>
              </div>
            </div>
            );
          })}
        </div>

        {/* No Results */}
        {filteredMedications.length === 0 && (
          <div className="text-center py-12">
            <Pill className="w-12 h-12 text-green-700 mx-auto mb-4" />
            <p className="text-green-300">No medications found matching your search.</p>
          </div>
        )}

        {/* Pagination */}
        {filteredMedications.length > 0 && (
          <div className="mt-6 flex items-center justify-center gap-3 text-green-200">
            <button
              onClick={() => handlePageChange(page - 1)}
              disabled={page === 1}
              className="px-3 py-1 rounded-lg border border-green-700/40 bg-black/30 hover:border-green-500/60 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Anterior
            </button>
            <span className="text-sm">
              Página {page} de {totalPages}
            </span>
            <button
              onClick={() => handlePageChange(page + 1)}
              disabled={page === totalPages}
              className="px-3 py-1 rounded-lg border border-green-700/40 bg-black/30 hover:border-green-500/60 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Siguiente
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
