import { Component, Input, Output, EventEmitter, OnChanges } from '@angular/core';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { UsuarioService } from '../../../../services/usuario/usuario.service';
import Swal from 'sweetalert2';
import { advertenciaEdad } from '../../../../validators/edad.validator';

@Component({
  selector: 'app-usuario-modal',
  imports: [ReactiveFormsModule],
  templateUrl: './usuario-modal.html',
  styleUrl: './usuario-modal.css'
})
export class UsuarioModal implements OnChanges {

  @Input() usuario: any = null;
  @Input() modo: 'ver' | 'editar' | 'eliminar' = 'ver';
  @Output() cerrar = new EventEmitter<void>();
  @Output() actualizar = new EventEmitter<void>();

  editForm: FormGroup;
  cargando = false;
  error = '';
  readonly gruposSanguineos = [
    'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'
  ];

  constructor(
    private fb: FormBuilder,
    private usuarioService: UsuarioService
  ) {
    this.editForm = this.fb.group({
      nombre: ['', Validators.required],
      apellido: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      dni: ['', Validators.required],
      fecha_nacimiento: ['', Validators.required],
      grupo_sanguineo: ['', Validators.required],
    });
  }

  ngOnChanges(): void {
    this.error = '';
    if (this.usuario && this.modo === 'editar') {
      this.editForm.patchValue({
        nombre: this.usuario.nombre,
        apellido: this.usuario.apellido,
        email: this.usuario.email,
        dni: this.usuario.dni,
        fecha_nacimiento: this.usuario.fecha_nacimiento,
        grupo_sanguineo: this.usuario.grupo_sanguineo,
      });
    }
  }

  advertenciaFechaNacimiento(): string {
    return advertenciaEdad(this.editForm.get('fecha_nacimiento')?.value);
  }

  guardar(): void {
    if (this.editForm.invalid) {
      this.editForm.markAllAsTouched();
      return;
    }
    this.cargando = true;
    this.usuarioService.editarUsuario(this.usuario.id, {
      ...this.editForm.value,
      username: this.usuario.username,
    }).subscribe({
      next: () => {

        this.cargando = false;

        Swal.fire({
          icon: 'success',
          title: 'Usuario actualizado',
          text: 'Los datos fueron modificados correctamente',
          confirmButtonText: 'Aceptar'
        });

        this.actualizar.emit();
        this.cerrar.emit();
      },
      error: () => {
        this.cargando = false;
        this.error = 'Error al guardar los cambios.';
      }
    });
  }

  confirmarEliminar(): void {
    this.cargando = true;
    this.usuarioService.eliminarUsuario(this.usuario.id).subscribe({
      next: () => {
        this.cargando = false;
        Swal.fire({
          icon: 'success',
          title: 'Usuario eliminado',
          text: 'El usuario fue eliminado correctamente',
          confirmButtonText: 'Aceptar'
        });
        this.actualizar.emit();
        this.cerrar.emit();
      },
      error: () => {
        this.cargando = false;
        this.error = 'Error al eliminar el usuario.';
      }
    });
  }
}
