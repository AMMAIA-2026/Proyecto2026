import { CentroSalud } from './campania.model';

export interface DashboardCampania {
  id: number;
  titulo: string;
  descripcion: string;
  ubicacion: string;
  centro_salud: number | null;
  centro_salud_detalle: CentroSalud | null;
  fecha_inicio: string;
  fecha_fin: string;
  cupo_maximo: number | null;
  total_inscriptos: number;
  estado_campania: string;
  estado_calculado: string;
  estado: string;
}

export interface DashboardSerieMensual {
  anio: number;
  mes: number;
  cantidad: number;
}

export interface CampaniasPorEstado {
  estado: string;
  cantidad: number;
}

export interface Dashboard {
  total_campanias: number;
  total_inscripciones: number;
  total_donantes: number;
  campanias_recientes: DashboardCampania[];
  campanias_por_estado: CampaniasPorEstado[];
  inscripciones_por_mes: DashboardSerieMensual[];
  donantes_por_mes: DashboardSerieMensual[];
}

export interface CampaniaGrafico {
  estado: string;
  count: number;
  porcentaje: number;
  color: string;
}

export interface DonantesGrafico {
  clave: string;
  mes: string;
  donantes: number;
  altura: number;
}

export interface DashboardViewModel extends Dashboard {
  campanias_por_tipo: CampaniaGrafico[];
  conicGradient: string;
  meses: DonantesGrafico[];
}
