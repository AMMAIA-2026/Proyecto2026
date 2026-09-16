import { Component, OnInit, signal } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { ActivatedRoute, Router } from '@angular/router';
import { Campania } from '../../../models/campania.model';
import { CampaniaService } from '../../../services/campanias/campania.service';
import { InscripcionService } from '../../../services/inscripciones/inscripcion.service';
import { AuthService } from '../../../services/auth/auth';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-campania-detalle',
  imports: [],
  templateUrl: './campania-detalle.html',
  styleUrl: './campania-detalle.css'
})
export class CampaniaDetalle implements OnInit {

  campania = signal<Campania | null>(null);
  cargando = signal(true);
  error = signal('');
  inscriptosCount = signal(0);

  constructor(
    private campaniaService: CampaniaService,
    private route: ActivatedRoute,
    private router: Router,
    private inscripcionService: InscripcionService,
    private authService: AuthService
  ) { }

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');

    const obs = this.campaniaService.getCampania(id!);

    obs.subscribe({
      next: (data: Campania) => {
        this.campania.set(data);
        this.cargando.set(false);
        this.inscriptosCount.set(data.total_inscriptos);

      },

      error: (err: any) => {
        this.error.set('No se pudo cargar la campaña.');
        this.cargando.set(false);
      }
    });

  }

  getEstado(): string {
    const campania = this.campania();
    if (!campania) return '';
    if (campania.estado_calculado === 'Proximamente') return 'Proxima';
    if (campania.estado_calculado === 'Activa') return 'En Curso';
    return 'Finalizada';
  }

  formatearFecha(fecha: string): string {
    return new Date(fecha).toLocaleDateString('es-AR', {
      day: 'numeric', month: 'long', year: 'numeric'
    });
  }

  inscribirse() {
    const campania = this.campania();
    if (!campania) {
      return;
    }

    if (!this.authService.isAuthenticated()) {
      Swal.fire({
        icon: 'warning',
        title: 'Atención',
        text: 'Debés iniciar sesión para continuar',
        confirmButtonText: 'Aceptar',
      }).then(() => {
        this.router.navigate(['/login']);
      });
      return;
    };

    this.inscripcionService.inscribirse(campania.id).subscribe({

      next: (respuesta) => {
        this.inscriptosCount.set(respuesta.totalInscriptos);
        Swal.fire({
          icon: 'success',
          title: 'Inscripción exitosa',
          text: 'Te has inscrito correctamente a la campaña',
          showConfirmButton: false,
          timer: 2000
        });
      },

      error: (err: HttpErrorResponse) => {
        const codigo = err.error?.codigo;
        const errorEsperado = [
          'inscripcion_duplicada',
          'edad_no_permitida',
          'cupo_completo',
          'campania_finalizada'
        ].includes(codigo);

        Swal.fire({
          icon: errorEsperado ? 'info' : 'error',
          title: codigo === 'inscripcion_duplicada'
            ? 'Inscripción existente'
            : 'No es posible inscribirse',
          text: errorEsperado
            ? err.error.mensaje
            : 'Hubo un problema al inscribirse a la campaña',
          showConfirmButton: false,
          timer: 2000
        });
      }

    });

  }

  volver(): void {
    this.router.navigate(['/campanias']);
  }

}
