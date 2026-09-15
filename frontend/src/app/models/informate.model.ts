export interface BeneficioHero {
  texto: string;
  conIcono: boolean;
}

export interface RequisitoBasico {
  texto: string;
  icono: 'persona' | 'check';
}

export interface ExclusionTemporal {
  texto: string;
}

export interface RequisitoDia {
  texto: string;
  icono: 'dni' | 'agua' | 'noAyuno' | 'entrevista';
}

export interface PasoProcedimiento {
  numero: number;
  titulo: string;
  subtitulo: string;
  icono: 'registro' | 'entrevistaMedica' | 'extraccion' | 'descanso';
}
