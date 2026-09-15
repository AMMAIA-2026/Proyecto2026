export interface LoginPayload {
  email: string;
  password: string;
}

export interface TokenResponse {
  access: string;
  refresh: string;
  user: {
    id: number;
    email: string;
    rol: string;
  };
}

export interface RegistroPayload {
  username: string;
  email: string;
  password: string;
  dni: string;
  nombre: string;
  apellido: string;
  fecha_nacimiento: string;
  grupo_sanguineo: string;
}

export interface RecuperarPasswordPayload {
  email: string;
  password: string;
}
