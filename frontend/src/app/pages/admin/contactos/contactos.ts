import { DatePipe } from '@angular/common';
import { Component, computed, signal } from '@angular/core';
import { Contacto } from '../../../models/contacto.model';
import { ContactoService } from '../../../services/contactos/contacto.service';


type FiltroContacto = 'todos' | 'pendientes' | 'revisados';
type OrdenContacto = 'prioridad' | 'recientes' | 'antiguos';


@Component({
  selector: 'app-contactos-admin',
  imports: [DatePipe],
  templateUrl: './contactos.html',
  styleUrl: './contactos.css'
})
export class ContactosAdmin {
  contactos = signal<Contacto[]>([]);
  contactoSeleccionado = signal<Contacto | null>(null);
  filtro = signal<FiltroContacto>('todos');
  orden = signal<OrdenContacto>('prioridad');
  cargando = signal(true);
  error = signal('');

  pendientes = computed(
    () => this.contactos().filter(contacto => !contacto.tracked).length
  );

  contactosVisibles = computed(() => {
    const filtro = this.filtro();
    const orden = this.orden();
    const filtrados = this.contactos().filter(contacto => {
      if (filtro === 'pendientes') return !contacto.tracked;
      if (filtro === 'revisados') return contacto.tracked;
      return true;
    });

    return filtrados.sort((a, b) => {
      const fechaA = new Date(a.fecha_creacion).getTime();
      const fechaB = new Date(b.fecha_creacion).getTime();
      if (orden === 'recientes') return fechaB - fechaA;
      if (orden === 'antiguos') return fechaA - fechaB;
      if (a.tracked !== b.tracked) return Number(a.tracked) - Number(b.tracked);
      return fechaB - fechaA;
    });
  });

  constructor(private contactoService: ContactoService) {
    this.cargarContactos();
  }

  cargarContactos(): void {
    this.cargando.set(true);
    this.contactoService.obtenerTodos().subscribe({
      next: contactos => {
        this.contactos.set(contactos);
        this.cargando.set(false);
      },
      error: () => {
        this.error.set('No se pudieron cargar los mensajes de contacto.');
        this.cargando.set(false);
      }
    });
  }

  cambiarFiltro(event: Event): void {
    this.filtro.set((event.target as HTMLSelectElement).value as FiltroContacto);
  }

  cambiarOrden(event: Event): void {
    this.orden.set((event.target as HTMLSelectElement).value as OrdenContacto);
  }

  abrirDetalle(id: number): void {
    this.contactoService.obtenerPorId(id).subscribe({
      next: contacto => this.contactoSeleccionado.set(contacto),
      error: () => this.error.set('No se pudo recuperar el mensaje seleccionado.')
    });
  }

  cerrarDetalle(): void {
    this.contactoSeleccionado.set(null);
  }

  cambiarSeguimiento(contacto: Contacto, tracked: boolean): void {
    this.contactoService.actualizarTracked(contacto.id, tracked).subscribe({
      next: actualizado => {
        this.contactos.update(contactos =>
          contactos.map(item => item.id === actualizado.id ? actualizado : item)
        );
        this.contactoSeleccionado.set(actualizado);
      },
      error: () => this.error.set('No se pudo actualizar el seguimiento.')
    });
  }
}
