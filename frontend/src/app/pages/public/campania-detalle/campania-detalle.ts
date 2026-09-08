import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { ActivatedRoute, Router } from '@angular/router';
import { Campania, CampaniaService } from '../../../services/campanias/campania.service';
import { InscripcionService } from '../../../services/inscripciones/inscripcion.service';
import { AuthService } from '../../../services/auth/auth';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-campania-detalle',
  standalone: true,
  imports: [],
  templateUrl: './campania-detalle.html',
  styleUrl: './campania-detalle.css'
})
export class CampaniaDetalle implements OnInit {

  campania: Campania | null = null;
  cargando: boolean = true;
  error: string = '';
  inscriptosCount = 0;

  constructor(
    private campaniaService: CampaniaService,
    private route: ActivatedRoute,
    private router: Router,
    private cdr: ChangeDetectorRef,
    private inscripcionService: InscripcionService,
    private authService: AuthService
  ) { }

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');

    const obs = this.campaniaService.getCampania(id!);

    obs.subscribe({
      next: (data: Campania) => {
        this.campania = data;
        this.cargando = false;
        this.inscriptosCount = data.total_inscriptos;
        this.cdr.detectChanges();

      },

      error: (err: any) => {
        this.error = 'No se pudo cargar la campaña.';
        this.cargando = false;
        this.cdr.detectChanges();
      }
    });

  }

  getEstado(): string {
    if (!this.campania) return '';
    if (this.campania.estado_calculado === 'Proximamente') return 'Proxima';
    if (this.campania.estado_calculado === 'Activa') return 'En Curso';
    return 'Finalizada';
  }

  formatearFecha(fecha: string): string {
    return new Date(fecha).toLocaleDateString('es-AR', {
      day: 'numeric', month: 'long', year: 'numeric'
    });
  }

  inscribirse() {
    if (!this.campania) {
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

    this.inscripcionService.inscribirse(this.campania.id).subscribe({

      next: (respuesta) => {
        this.inscriptosCount = respuesta.totalInscriptos;
        this.cdr.detectChanges();
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
