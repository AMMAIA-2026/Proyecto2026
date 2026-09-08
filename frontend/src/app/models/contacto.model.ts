export interface Contacto {
  id: number;
  email: string;
  asunto: string;
  mensaje: string;
  tracked: boolean;
  fecha_creacion: string;
}

export interface NuevoContacto {
  email: string;
  asunto: string;
  mensaje: string;
}
