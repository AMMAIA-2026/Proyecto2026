import { Component, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Campania } from '../../../models/campania.model';
import { CampaniaService } from '../../../services/campanias/campania.service';
import { RouterModule } from '@angular/router';


@Component({
  selector: 'app-campanias',
  imports: [FormsModule, RouterModule],
  templateUrl: './campanias.html',
  styleUrl: './campanias.css'
})
export class Campanias implements OnInit {

  campanias = signal<Campania[]>([]);
  campaniasFiltradas = signal<Campania[]>([]);
  cargando = signal(true);
  error = signal('');
  busqueda: string = '';
  filtroEstado: string = '';

  constructor(private campaniaService: CampaniaService) { }

  ngOnInit(): void {
    this.campaniaService.getCampanias().subscribe({
      next: (datos: Campania[]) => {
        this.campanias.set(datos);
        this.filtrar();
        this.cargando.set(false);
      },
      error: (err) => {
        this.error.set('No se pudieron cargar las campañas.');
        this.cargando.set(false);
      }
    });
  }

  filtrar(): void {
    this.campaniasFiltradas.set(this.campanias().filter(c => {
      const coincideBusqueda = c.titulo.toLowerCase()
        .includes(this.busqueda.toLowerCase());

      if (!this.filtroEstado) {
        return coincideBusqueda && c.estado_calculado !== 'Finalizada';
      }
      return coincideBusqueda && c.estado_calculado === this.filtroEstado;
    }));
  }

}
