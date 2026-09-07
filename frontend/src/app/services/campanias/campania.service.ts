import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

export const CENTRO_SALUD_MAX_LENGTH = {
  nombre: 100,
  direccion: 200,
  barrio: 50,
  localidad: 50,
  telefono: 10,
  sitio_web: 200
} as const;

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

@Injectable({
  providedIn: 'root'
})
export class CampaniaService {

  private apiUrl = 'http://localhost:8000/campanias/';

  constructor(private http: HttpClient) { }

  getCampanias(): Observable<Campania[]> {
    return this.http.get<Campania[]>(this.apiUrl).pipe(
      map(campanias => campanias.map(c => ({
        ...c,
        estado: c.estado_calculado
      })))
    );
  }

  getCampania(id: string): Observable<Campania> {
    return this.http.get<Campania>(`${this.apiUrl}${id}/`).pipe(
      map(c => ({
        ...c,
        estado: c.estado_calculado,
        fecha_inicio_formateada: this.formatearFecha(c.fecha_inicio),
        fecha_fin_formateada: this.formatearFecha(c.fecha_fin)
      }))
    );
  }

  getCentrosSalud(): Observable<CentroSalud[]> {
    return this.http.get<CentroSalud[]>(
      'http://localhost:8000/centros-salud/'
    );
  }

  private formatearFecha(fecha: string): string {
    return new Date(fecha).toLocaleDateString('es-AR', {
      day: 'numeric', month: 'long', year: 'numeric'
    });
  }
}
