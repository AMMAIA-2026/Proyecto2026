import { Component, OnInit, signal } from '@angular/core';
import { UsuarioService } from '../../../services/usuario/usuario.service';
import { UsuarioModal } from './usuario-modal/usuario-modal';
import { FormsModule } from '@angular/forms';
import { Usuario } from '../../../models/usuario.model';

@Component({
  selector: 'app-usuarios',
  imports: [UsuarioModal, FormsModule],
  templateUrl: './usuarios.html',
  styleUrl: './usuarios.css'
})
export class Usuarios implements OnInit {

  usuarios = signal<Usuario[]>([]);
  textoBusqueda = '';
  usuarioSeleccionado: Usuario | null = null;
  usuariosOriginales: Usuario[] = [];
  modoModal: 'ver' | 'editar' | 'eliminar' = 'ver';
  mostrarModal = false;

  constructor(
    private usuarioService: UsuarioService
  ) { }

  ngOnInit(): void {
    this.cargarUsuarios();
  }

  cargarUsuarios(): void {
    this.usuarioService.getUsuarios().subscribe({
      next: (data) => {
        this.usuarios.set(data);
        this.usuariosOriginales = [...data];
      },
      error: (err) => console.error('ERROR:', err)
    });
  }

  abrirModal(usuario: Usuario, modo: 'ver' | 'editar' | 'eliminar'): void {
    this.usuarioSeleccionado = usuario;
    this.modoModal = modo;
    this.mostrarModal = true;
  }

  cerrarModal(): void {
    this.mostrarModal = false;
    this.usuarioSeleccionado = null;
  }

  filtrarUsuarios(): void {

    const texto = this.textoBusqueda.toLowerCase().trim();

    if (!texto) {
      this.usuarios.set([...this.usuariosOriginales]);
      return;
    }

    this.usuarios.set(this.usuariosOriginales.filter(usuario =>
      usuario.nombre?.toLowerCase().includes(texto) ||
      usuario.apellido?.toLowerCase().includes(texto) ||
      usuario.email?.toLowerCase().includes(texto) ||
      usuario.dni?.toString().includes(texto)
    ));
  }
}
