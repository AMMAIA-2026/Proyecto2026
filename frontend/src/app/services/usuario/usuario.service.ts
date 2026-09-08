import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class UsuarioService {

  private apiUrl = 'http://127.0.0.1:8000/usuarios/';

  constructor(private http: HttpClient) {}

  private headers(): HttpHeaders {
    const token = localStorage.getItem('access_token');
    return new HttpHeaders().set('Authorization', `Bearer ${token}`);
  }

  getUsuarios() {
    return this.http.get<any[]>(this.apiUrl, { headers: this.headers() });
  }

  editarUsuario(id: number, datos: any) {
    return this.http.put(`${this.apiUrl}${id}/`, datos, { headers: this.headers() });
  }

  eliminarUsuario(id: number) {
    return this.http.delete(`${this.apiUrl}${id}/`, { headers: this.headers() });
  }
}
