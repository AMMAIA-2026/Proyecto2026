import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CampaniaService, Campania } from '../../../services/campanias/campania.service';
import { RouterModule } from '@angular/router';


@Component({
  selector: 'app-campanias',
  standalone: true,
  imports: [FormsModule, RouterModule],
  templateUrl: './campanias.html',
  styleUrl: './campanias.css'
})
export class Campanias implements OnInit {

  campanias: Campania[] = [];
  campaniasFiltradas: Campania[] = [];
  cargando: boolean = true;
  error: string = '';
  busqueda: string = '';
  filtroEstado: string = '';

  constructor(private campaniaService: CampaniaService, private cdr: ChangeDetectorRef) { }

  ngOnInit(): void {
    this.campaniaService.getCampanias().subscribe({
      next: (datos: Campania[]) => {
        this.campanias = datos;
        this.filtrar();
        this.cargando = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.error = 'No se pudieron cargar las campañas.';
        this.cargando = false;
      }
    });
  }

  filtrar(): void {
    this.campaniasFiltradas = this.campanias.filter(c => {
      const coincideBusqueda = c.titulo.toLowerCase()
        .includes(this.busqueda.toLowerCase());

      if (!this.filtroEstado) {
        return coincideBusqueda && c.estado_calculado !== 'Finalizada';
      }
      return coincideBusqueda && c.estado_calculado === this.filtroEstado;
    });
    this.cdr.detectChanges();
  }

}
