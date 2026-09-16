import { DatePipe } from '@angular/common';
import { Component, computed, OnInit, signal } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { Campania } from '../../../models/campania.model';
import { CampaniaService } from '../../../services/campanias/campania.service';
import {
  InscripcionesCampaniaResponse,
  InscripcionService,
} from '../../../services/inscripciones/inscripcion.service';

@Component({
  selector: 'app-dashboard',
  imports: [DatePipe],
  templateUrl: './inscripciones.html',
  styleUrls: ['./inscripciones.css']
})

export class AdminInscripciones implements OnInit {
  campanias = signal<Campania[]>([]);
  seleccion = signal<InscripcionesCampaniaResponse | null>(null);
  busqueda = signal('');
  cargandoCampanias = signal(true);
  cargandoDetalle = signal(false);
  error = signal('');

  usuariosVisibles = computed(() => {
    const detalle = this.seleccion();
    const busqueda = this.busqueda().trim().toLowerCase();
    if (!detalle || !busqueda) return detalle?.usuarios || [];

    return detalle.usuarios.filter(usuario => [
      usuario.nombre,
      usuario.apellido,
      usuario.dni,
      usuario.email,
    ].some(valor => valor.toLowerCase().includes(busqueda)));
  });

  constructor(
    private campaniaService: CampaniaService,
    private inscripcionService: InscripcionService,
    private route: ActivatedRoute,
  ) {}

  ngOnInit(): void {
    this.campaniaService.getCampanias().subscribe({
      next: campanias => {
        this.campanias.set(campanias);
        this.cargandoCampanias.set(false);
        const campaniaId = this.route.snapshot.queryParamMap.get('campania');
        if (campaniaId) this.seleccionar(Number(campaniaId));
      },
      error: () => {
        this.error.set('No se pudieron cargar las campañas.');
        this.cargandoCampanias.set(false);
      },
    });
  }

  seleccionar(campaniaId: number): void {
    this.error.set('');
    this.busqueda.set('');
    this.cargandoDetalle.set(true);
    this.inscripcionService.obtenerPorCampania(campaniaId).subscribe({
      next: detalle => {
        this.seleccion.set(detalle);
        this.cargandoDetalle.set(false);
      },
      error: () => {
        this.error.set('No se pudieron cargar los inscriptos de la campaña.');
        this.cargandoDetalle.set(false);
      },
    });
  }

  actualizarBusqueda(event: Event): void {
    this.busqueda.set((event.target as HTMLInputElement).value);
  }
}
