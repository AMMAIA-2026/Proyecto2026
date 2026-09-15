export interface CentroSalud {
  id: number;
  nombre: string;
  direccion: string;
  barrio: string;
  localidad: string;
  telefono: string | null;
  sitio_web: string | null;
  latitud: string;
  longitud: string;
}

export interface Campania {
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
  estado_calculado: string;
  estado?: string;
}

export interface CampaniaPayload {
  titulo: string;
  descripcion: string;
  ubicacion: string;
  centro_salud: number | null;
  fecha_inicio: string;
  fecha_fin: string;
  cupo_maximo: number | null;
  estado_campania?: string;
}
