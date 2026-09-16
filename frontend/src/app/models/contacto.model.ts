export enum MotivoContacto {
  ConsultaGeneral = 'Consulta general',
  ProblemaTecnico = 'Problema técnico',
  Sugerencia = 'Sugerencia',
  Otro = 'Otro'
}

export const MOTIVOS_CONTACTO = Object.values(MotivoContacto);

export interface Contacto {
  id: number;
  nombre_completo: string;
  correo_electronico: string;
  motivo: MotivoContacto;
  mensaje: string;
  tracked: boolean;
  fecha_creacion: string;
}

export interface NuevoContacto {
  nombre_completo: string;
  correo_electronico: string;
  motivo: MotivoContacto;
  mensaje: string;
}
