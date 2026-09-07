import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';


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


@Injectable({ providedIn: 'root' })
export class ContactoService {
  private readonly apiUrl = 'http://localhost:8000/contactos/';

  constructor(private http: HttpClient) {}

  crear(contacto: NuevoContacto): Observable<Contacto> {
    return this.http.post<Contacto>(this.apiUrl, contacto);
  }

  obtenerTodos(): Observable<Contacto[]> {
    return this.http.get<Contacto[]>(this.apiUrl);
  }

  obtenerPorId(id: number): Observable<Contacto> {
    return this.http.get<Contacto>(`${this.apiUrl}${id}/`);
  }

  actualizarTracked(id: number, tracked: boolean): Observable<Contacto> {
    return this.http.put<Contacto>(`${this.apiUrl}${id}/`, { tracked });
  }
}
