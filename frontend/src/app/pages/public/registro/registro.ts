import { Component } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import Swal from 'sweetalert2';
import {
  passwordsCoinciden,
  validadoresPassword
} from '../../../validators/password.validators';
import { advertenciaEdad } from '../../../validators/edad.validator';

@Component({
  selector: 'app-registro',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './registro.html',
  styleUrl: './registro.css'
})
export class Registro {

  registroForm: FormGroup;
  grupos = [
    'A+',
    'A-',
    'B+',
    'B-',
    'AB+',
    'AB-',
    'O+',
    'O-'
  ];
  mensaje = '';
  error = '';
  cargando = false;

  constructor(
    private fb: FormBuilder,
    private http: HttpClient,
    private router: Router
  ) {
    this.registroForm = this.fb.group({
      username: ['', [Validators.required, Validators.minLength(3)]],
      email: ['', [Validators.required, Validators.email]],
       password: ['', validadoresPassword()],
       confirmar_password: ['', Validators.required],
      nombre: ['', Validators.required],
      apellido: ['', Validators.required],
      fecha_nacimiento: ['', Validators.required],
      dni: ['', [Validators.required, Validators.minLength(7), Validators.maxLength(8)]],
       rol: ['Usuario Estandar'],
      grupo_sanguineo: ['', Validators.required]
     }, { validators: passwordsCoinciden });
  }

  advertenciaFechaNacimiento(): string {
    return advertenciaEdad(this.registroForm.get('fecha_nacimiento')?.value);
  }

  onSubmit() {
    this.mensaje = '';
    this.error = '';

    if (this.registroForm.invalid) {
      this.registroForm.markAllAsTouched();
      return;
    }

    if (this.cargando) return;
    this.cargando = true;

    const { confirmar_password, ...datosRegistro } = this.registroForm.getRawValue();

    this.http.post('http://localhost:8000/usuarios/registro/', datosRegistro).subscribe({
      next: () => {
        this.cargando = false;
        Swal.fire({
          icon: 'success',
          title: 'Usuario registrado',
          text: 'El usuario fue registrado correctamente',
          confirmButtonText: 'Aceptar'
        });

        setTimeout(() => this.router.navigate(['/login']), 2000);
      },
      error: (err) => {
        this.cargando = false;
        this.error = 'Error al registrar. Verificá los datos.';
      }
    });
  }
}
