import { DatePipe } from '@angular/common';
import { Component, OnInit, signal } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import Swal from 'sweetalert2';

import {
  Inscripcion,
  MisInscripcionesResponse,
  InscripcionService,
} from '../../../services/inscripciones/inscripcion.service';
import { AuthService } from '../../../services/auth/auth';


@Component({
  selector: 'app-mis-inscripciones',
  imports: [DatePipe, RouterLink],
  templateUrl: './mis-inscripciones.html',
  styleUrl: './mis-inscripciones.css',
})
export class MisInscripciones implements OnInit {
  inscripciones = signal<MisInscripcionesResponse | null>(null);
  cargando = signal(true);
  cancelando = signal<number | null>(null);
  error = signal('');

  constructor(
    private inscripcionService: InscripcionService,
    private authService: AuthService,
    private router: Router,
  ) {}

  ngOnInit(): void {
    if (
      !this.authService.isAuthenticated()
      || localStorage.getItem('rol') !== 'Usuario Estandar'
    ) {
      this.router.navigate(['/login']);
      return;
    }

    this.cargar();
  }

  cargar(): void {
    this.cargando.set(true);
    this.inscripcionService.obtenerMias().subscribe({
      next: respuesta => {
        this.inscripciones.set(respuesta);
        this.cargando.set(false);
      },
      error: () => {
        this.error.set('No se pudieron cargar tus inscripciones.');
        this.cargando.set(false);
      },
    });
  }

  cancelar(inscripcion: Inscripcion): void {
    Swal.fire({
      title: '¿Cancelar inscripción?',
      text: `Se cancelará tu inscripción a ${inscripcion.campania.titulo}. Podrás volver a inscribirte mientras la campaña esté disponible.`,
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#C0392B',
      cancelButtonText: 'Volver',
      confirmButtonText: 'Sí, cancelar',
    }).then(resultado => {
      if (!resultado.isConfirmed || this.cancelando() !== null) return;

      this.cancelando.set(inscripcion.id);
      this.inscripcionService.cancelar(inscripcion.id).subscribe({
        next: () => {
          this.inscripciones.update(data => data
            ? {
                ...data,
                actuales: data.actuales.filter(item => item.id !== inscripcion.id),
              }
            : data
          );
          this.cancelando.set(null);
          Swal.fire({
            icon: 'success',
            title: 'Inscripción cancelada',
            text: 'Ya podés volver a inscribirte si la campaña sigue disponible.',
            confirmButtonText: 'Aceptar',
          });
        },
        error: err => {
          this.cancelando.set(null);
          this.error.set(err.error?.mensaje || 'No se pudo cancelar la inscripción.');
        },
      });
    });
  }
}
