import { useState } from 'react';
import { Search, ArrowLeft, Pill, MapPin, Package, DollarSign, Calendar } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';

interface Establishment {
  cod_unico: string;
  nombre: string;
  direccion: string;
  stock: number;
  precio: number;
  fecha_vencimiento: string | null;
  disponible: string;
}

interface Medicine {
  codigo_med: string;
  nombre: string;
  forma_farmaceutica: string;
  tipo: string;
  establecimientos: Establishment[];
}

interface CheckMedicinePageProps {
  onBack: () => void;
}

export function CheckMedicinePage({ onBack }: CheckMedicinePageProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [medicines, setMedicines] = useState<Medicine[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      setError('Por favor ingresa el nombre de un medicamento');
      return;
    }

    setLoading(true);
    setError(null);
    setHasSearched(true);

    try {
      const response = await fetch(
        `http://localhost:8000/get/medicina?nombre=${encodeURIComponent(searchQuery)}`
      );

      if (!response.ok) {
        throw new Error('Error al buscar medicamentos');
      }

      const data = await response.json();
      setMedicines(data);
    } catch (err) {
      setError('Error al buscar medicamentos. Por favor intenta de nuevo.');
      console.error('Error searching medicines:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <div className="min-h-screen px-4 py-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <Button
            onClick={onBack}
            variant="ghost"
            className="mb-4 text-green-100 hover:text-white hover:bg-green-800/50"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Volver
          </Button>
          
          <div className="flex items-center gap-3 mb-4">
            <Pill className="w-10 h-10 text-green-400" />
            <h1 className="text-4xl font-bold text-green-100">
              Buscar Medicamentos
            </h1>
          </div>
          
          <p className="text-green-200 text-lg">
            Encuentra medicamentos disponibles en establecimientos de salud
          </p>
        </div>

        {/* Search Bar */}
        <Card className="mb-8 bg-green-900/30 border-green-700/50">
          <CardContent className="pt-6">
            <div className="flex gap-4">
              <div className="flex-1">
                <Input
                  type="text"
                  placeholder="Ej: Paracetamol, Ibuprofeno, Amoxicilina..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onKeyPress={handleKeyPress}
                  className="bg-green-950/50 border-green-700 text-green-100 placeholder:text-green-400/50"
                />
              </div>
              <Button
                onClick={handleSearch}
                disabled={loading}
                className="bg-green-600 hover:bg-green-700 text-white"
              >
                <Search className="w-4 h-4 mr-2" />
                {loading ? 'Buscando...' : 'Buscar'}
              </Button>
            </div>
            
            {error && (
              <p className="text-red-400 mt-2 text-sm">{error}</p>
            )}
          </CardContent>
        </Card>

        {/* Results */}
        {loading && (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-green-400"></div>
            <p className="text-green-200 mt-4">Buscando medicamentos...</p>
          </div>
        )}

        {!loading && hasSearched && medicines.length === 0 && (
          <Card className="bg-green-900/30 border-green-700/50">
            <CardContent className="py-12 text-center">
              <Pill className="w-16 h-16 text-green-400/50 mx-auto mb-4" />
              <p className="text-green-200 text-lg">
                No se encontraron medicamentos con ese nombre
              </p>
              <p className="text-green-400/70 mt-2">
                Intenta con otro nombre o verifica la ortografía
              </p>
            </CardContent>
          </Card>
        )}

        {!loading && medicines.length > 0 && (
          <div className="space-y-6">
            <p className="text-green-200">
              Se encontraron <span className="font-bold text-green-400">{medicines.length}</span> medicamento(s)
            </p>

            {medicines.map((medicine) => (
              <Card key={medicine.codigo_med} className="bg-green-900/30 border-green-700/50">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div>
                      <CardTitle className="text-2xl text-green-100 mb-2">
                        {medicine.nombre}
                      </CardTitle>
                      <CardDescription className="text-green-300">
                        <div className="flex gap-4 flex-wrap">
                          <span>Código: {medicine.codigo_med}</span>
                          <span>•</span>
                          <span>Forma: {medicine.forma_farmaceutica}</span>
                          <span>•</span>
                          <span>Tipo: {medicine.tipo}</span>
                        </div>
                      </CardDescription>
                    </div>
                    <Badge className="bg-green-600 text-white">
                      {medicine.establecimientos.length} establecimiento(s)
                    </Badge>
                  </div>
                </CardHeader>
                
                <CardContent>
                  <h3 className="text-lg font-semibold text-green-200 mb-4">
                    Disponible en:
                  </h3>
                  
                  <div className="space-y-4">
                    {medicine.establecimientos.map((est, index) => (
                      <div
                        key={`${est.cod_unico}-${index}`}
                        className="bg-green-950/50 rounded-lg p-4 border border-green-700/30"
                      >
                        <div className="flex items-start justify-between mb-3">
                          <div className="flex-1">
                            <h4 className="font-semibold text-green-100 mb-1">
                              {est.nombre}
                            </h4>
                            <div className="flex items-center text-green-300 text-sm">
                              <MapPin className="w-4 h-4 mr-1" />
                              {est.direccion}
                            </div>
                          </div>
                          {est.disponible && (
                            <Badge variant="outline" className="border-green-500 text-green-400">
                              {est.disponible}
                            </Badge>
                          )}
                        </div>
                        
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-3">
                          <div className="flex items-center text-green-200">
                            <Package className="w-4 h-4 mr-2 text-green-400" />
                            <span className="text-sm">
                              Stock: <span className="font-semibold">{est.stock}</span> unidades
                            </span>
                          </div>
                          
                          <div className="flex items-center text-green-200">
                            <DollarSign className="w-4 h-4 mr-2 text-green-400" />
                            <span className="text-sm">
                              Precio: <span className="font-semibold">S/ {est.precio.toFixed(2)}</span>
                            </span>
                          </div>
                          
                          {est.fecha_vencimiento && (
                            <div className="flex items-center text-green-200">
                              <Calendar className="w-4 h-4 mr-2 text-green-400" />
                              <span className="text-sm">
                                Vence: {new Date(est.fecha_vencimiento).toLocaleDateString('es-PE')}
                              </span>
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
