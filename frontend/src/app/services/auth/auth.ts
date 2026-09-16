import { inject, Injectable, signal } from '@angular/core';
import { HttpBackend, HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import {
  LoginPayload,
  RecuperarPasswordPayload,
  RegistroPayload,
  TokenResponse,
} from '../../models/auth.model';

@Injectable({ providedIn: 'root' })
export class AuthService {

  private readonly TOKEN_KEY = 'access_token';

  isAuthenticated = signal<boolean>(this.checkToken());

  private readonly apiUrl = 'http://localhost:8000';
  private readonly http = new HttpClient(inject(HttpBackend));

  constructor() {}

  iniciarSesion(payload: LoginPayload): Observable<TokenResponse> {
    return this.http.post<TokenResponse>(
      `${this.apiUrl}/api/token/`,
      payload,
    );
  }

  registrar(payload: RegistroPayload): Observable<{ message: string }> {
    return this.http.post<{ message: string }>(
      `${this.apiUrl}/usuarios/registro/`,
      payload,
    );
  }

  recuperarPassword(
    payload: RecuperarPasswordPayload,
  ): Observable<{ message: string }> {
    return this.http.post<{ message: string }>(
      `${this.apiUrl}/usuarios/recuperar-password/`,
      payload,
    );
  }

  private checkToken(): boolean {
    return !!localStorage.getItem(this.TOKEN_KEY);
  }

  login(token: string): void {
    localStorage.setItem(this.TOKEN_KEY, token);
    this.isAuthenticated.set(true);
  }

  logout(): void {
    localStorage.removeItem(this.TOKEN_KEY);
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('rol');
    this.isAuthenticated.set(false);
  }

  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

}
