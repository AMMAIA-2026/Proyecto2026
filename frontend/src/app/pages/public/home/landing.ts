import { Component, OnInit, signal } from '@angular/core';
import { RouterModule } from '@angular/router';
import { Campania } from '../../../models/campania.model';
import { CampaniaService } from '../../../services/campanias/campania.service';



@Component({
  selector: 'app-root',
  imports: [RouterModule],
  templateUrl: './landing.html',
  styleUrl: './landing.css',
})
export class Landing implements OnInit {
  campanias = signal<Campania[]>([]);
  cargando = signal(true);
  error = signal('');

  constructor(
    private campaniaService: CampaniaService
  ) {}
  
  ngOnInit(): void {
    this.campaniaService.getCampanias().subscribe({
      next: (datos: Campania[]) => {
        this.campanias.set(datos.filter(
          campania => campania.estado_calculado !== 'Finalizada'
        ));

        this.cargando.set(false);
      },
      error: (err) => {
        this.error.set('No se pudieron cargar las campañas.');
        this.cargando.set(false);
      }
    });
  }
  formatearFecha(fecha: string): string {
      return new Date(fecha).toLocaleDateString('es-AR', {
        day: 'numeric', month: 'long'
      });
    }
}
