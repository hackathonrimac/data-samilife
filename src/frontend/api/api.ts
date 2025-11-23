const resolveBaseUrl = () => {
  const envUrl = import.meta.env.VITE_API_URL as string | undefined;
  if (envUrl && envUrl.trim()) {
    return envUrl.trim();
  }

  // Fallback: same host, default backend port
  if (typeof window !== "undefined") {
    return `${window.location.protocol}//${window.location.hostname}:8000`;
  }

  return "http://localhost:8000";
};

const API_BASE_URL = resolveBaseUrl();

export interface EstablishmentSummary {
  nombre: string;
  direccion: string;
  calificacion?: string | null;
  cod_unico?: string | null;
}

export interface ServiceInfo {
  servicio: string;
  profesional?: string | null;
  especialidad?: string | null;
  telefono?: string | null;
}

export interface ProfessionalInfo {
  cmp: string;
  nombre: string;
  profesion: string;
  especialidad?: string | null;
}

export interface InsuranceInfo {
  seguro: string;
  red?: string | null;
  costo_consulta?: number | null;
}

export interface EstablishmentInfo {
  cod_unico: string;
  nombre: string;
  direccion: string;
  institucion: string;
  establecimiento: string;
  clasificacion: string;
  correo?: string | null;
  longitud?: number | null;
  latitud?: number | null;
  pagina?: string | null;
  servicios: ServiceInfo[];
  profesionales: ProfessionalInfo[];
  seguros: InsuranceInfo[];
}

export interface ScheduleEntry {
  dia: number;
  ini: string;
  fin: string;
}

export interface AppointmentSlot {
  profesional: string;
  cmp?: string | null;
  especialidad?: string | null;
  servicio: string;
  horario: ScheduleEntry[];
  telefono?: string | null;
}

export interface PricingInfo {
  precio_normal: number;
  precio_rimac: number;
}

export interface MedicationInfo {
  codigo_med: string;
  nombre: string;
  forma_farmaceutica: string;
  tipo: string;
  stock: number;
  precio: number;
  fecha_vencimiento?: string | null;
  disponible: string;
}

export interface SearchEstablishmentsParams {
  lugar?: string;
  fecha?: string;
  tipo?: string;
  filtros?: Record<string, unknown>;
}

export interface AppointmentFilters {
  especialidad?: string;
  profesional?: string;
  fecha_inicio?: string;
  fecha_fin?: string;
  tipo_servicio?: string;
}

export interface MedicationFilters {
  nombre?: string;
  tipo?: string;
  forma_farmaceutica?: string;
  disponibilidad?: boolean;
  incluir_sin_stock?: boolean;
}

const buildUrl = (path: string, params?: Record<string, string | undefined>) => {
  const url = new URL(path, API_BASE_URL.endsWith("/") ? API_BASE_URL : `${API_BASE_URL}/`);
  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== "") {
        url.searchParams.set(key, value);
      }
    });
  }
  return url.toString();
};

const fetchJson = async <T>(url: string, init?: RequestInit): Promise<T> => {
  const response = await fetch(url, init);
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`Request failed (${response.status}): ${detail || response.statusText}`);
  }
  return response.json() as Promise<T>;
};

export const api = {
  searchEstablishments: (params: SearchEstablishmentsParams = {}) => {
    const query: Record<string, string | undefined> = {
      lugar: params.lugar,
      fecha: params.fecha,
      tipo: params.tipo,
    };

    if (params.filtros) {
      query.filtros = JSON.stringify(params.filtros);
    }

    return fetchJson<EstablishmentSummary[]>(buildUrl("get", query));
  },

  getEstablishmentInfo: (codUnico: string) =>
    fetchJson<EstablishmentInfo>(buildUrl(`get/${codUnico}/informacion`)),

  getAppointments: (codUnico: string, filtros?: AppointmentFilters) => {
    const query: Record<string, string | undefined> = {};
    if (filtros && Object.keys(filtros).length) {
      query.filtros = JSON.stringify(filtros);
    }
    return fetchJson<AppointmentSlot[]>(buildUrl(`get/${codUnico}/citas`, query));
  },

  getMedications: (codUnico: string, filtros?: MedicationFilters) => {
    const query: Record<string, string | undefined> = {};
    if (filtros && Object.keys(filtros).length) {
      query.filtros = JSON.stringify(filtros);
    }
    return fetchJson<MedicationInfo[]>(buildUrl(`get/${codUnico}/farmacos`, query));
  },

  getPricing: (codigo: string, servicio: { servicio: string; cmp?: string; profesion?: string }) => {
    const query: Record<string, string | undefined> = {
      codigo,
      servicio: JSON.stringify(servicio),
    };
    return fetchJson<PricingInfo>(buildUrl("get/precio/cita", query));
  },
};
