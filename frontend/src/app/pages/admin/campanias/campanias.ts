import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { signal } from '@angular/core';
import Swal from 'sweetalert2';
import { DatePipe } from '@angular/common';
import { Campania } from '../../../models/campania.model';
import { CampaniaService } from '../../../services/campanias/campania.service';


@Component({
  selector: 'app-campanias-admin',
  imports: [DatePipe],
  templateUrl: './campanias.html',
  styleUrls: ['./campanias.css']
})
export class AdminCampanias implements OnInit {

  campanias = signal<Campania[]>([]);

  error = '';

  constructor(
  private campaniaService: CampaniaService,
  private router: Router
) {}

  ngOnInit(): void {
    this.cargarCampanias();
  }

  cargarCampanias() {
    this.campaniaService.getCampanias().subscribe({

      next: (data) => {
        this.campanias.set(data);
      },

      error: () => {
        this.error = 'No se pudieron cargar las campañas';
      }

    });
  }

  crearCampania() {
    this.router.navigate(['/admin/campanias/nueva']);
  }

  editarCampania(id: number) {
    this.router.navigate(['/admin/campanias/editar', id]);
  }

  
  eliminarCampania(id: number) {

  Swal.fire({
    title: '¿Eliminar campaña?',
    text: 'Esta acción no se puede deshacer',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#C0392B',
    cancelButtonColor: '#7f8c8d',
    confirmButtonText: 'Sí, eliminar',
    cancelButtonText: 'Cancelar'
  }).then((result) => {

    if (!result.isConfirmed) return;

    this.campaniaService.eliminarCampania(id).subscribe({

      next: () => {

        this.campanias.set(this.campanias().filter(c => c.id !== id));

        Swal.fire({
          title: 'Eliminada',
          text: 'La campaña fue eliminada correctamente',
          icon: 'success',
          timer: 1500,
          showConfirmButton: false
        });

      },

      error: () => { Swal.fire('Error', 'No se pudo eliminar la campaña', 'error'); }
    });
  });
}
}
