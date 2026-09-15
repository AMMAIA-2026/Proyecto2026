
import { Injectable } from '@angular/core';

import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';

import { Campania } from '../../models/campania.model';

export interface Inscripcion {
  id: number;
  campania: Campania;
}

export interface MisInscripcionesResponse {
  actuales: Inscripcion[];
  historicas: Inscripcion[];
}

export interface InscripcionesCampaniaResponse {
  campania: Campania;
  total_inscriptos: number;
  usuarios: {
    id: number;
    nombre: string;
    apellido: string;
    dni: string;
    email: string;
  }[];
}

@Injectable({
  providedIn: 'root'
})

export class InscripcionService {

  private apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  inscribirse(campaniaId: number): Observable<{ data: any, totalInscriptos: number }> {
    return this.http.post<{ data: any, totalInscriptos: number }>(
      `${this.apiUrl}/inscripciones/campanias/${campaniaId}/`,
      null
    );
  }

  obtenerMias(): Observable<MisInscripcionesResponse> {
    return this.http.get<MisInscripcionesResponse>(
      `${this.apiUrl}/inscripciones/mis-inscripciones/`
    );
  }

  cancelar(inscripcionId: number): Observable<void> {
    return this.http.delete<void>(
      `${this.apiUrl}/inscripciones/${inscripcionId}/`
    );
  }

  obtenerPorCampania(
    campaniaId: number,
    buscar = '',
  ): Observable<InscripcionesCampaniaResponse> {
    const query = buscar.trim()
      ? `?buscar=${encodeURIComponent(buscar.trim())}`
      : '';
    return this.http.get<InscripcionesCampaniaResponse>(
      `${this.apiUrl}/inscripciones/campanias/${campaniaId}/${query}`
    );
  }
}



