export interface Clinic {
  id: string;
  name: string;
  address: string;
  classification?: string | null;
  institution?: string | null;
  longitude?: number | null;
  latitude?: number | null;
  distanceKm?: number | null;
}

export interface SearchFilters {
  query?: string;
  location?: string;
  date?: string;
  type?: string;
  insurance?: string;
  latitude?: number;
  longitude?: number;
}
