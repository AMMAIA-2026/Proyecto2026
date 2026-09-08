import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import {
  Campania,
  CampaniaPayload,
  CentroSalud,
} from '../../models/campania.model';

export const CENTRO_SALUD_MAX_LENGTH = {
  nombre: 100,
  direccion: 200,
  barrio: 50,
  localidad: 50,
  telefono: 10,
  sitio_web: 200
} as const;

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

  crearCampania(data: CampaniaPayload): Observable<Campania> {
    return this.http.post<Campania>(this.apiUrl, data);
  }

  editarCampania(id: number, data: CampaniaPayload): Observable<Campania> {
    return this.http.put<Campania>(`${this.apiUrl}${id}/`, data);
  }

  eliminarCampania(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}${id}/`);
  }

  private formatearFecha(fecha: string): string {
    return new Date(fecha).toLocaleDateString('es-AR', {
      day: 'numeric', month: 'long', year: 'numeric'
    });
  }
}
