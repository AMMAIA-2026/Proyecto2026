import { HttpErrorResponse } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import Swal from 'sweetalert2';

import {
  passwordsCoinciden,
  validadoresPassword
} from '../../../validators/password.validators';
import { AuthService } from '../../../services/auth/auth';


@Component({
  selector: 'app-recuperar-password',
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './recuperar-password.html',
  styleUrls: ['../login/login.css', './recuperar-password.css']
})
export class RecuperarPassword {
  form: FormGroup;
  enviando = false;
  error = '';

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private authService: AuthService,
  ) {
    this.form = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', validadoresPassword()],
      confirmar_password: ['', Validators.required]
    }, { validators: passwordsCoinciden });
  }

  onSubmit(): void {
    this.error = '';
    this.form.markAllAsTouched();

    if (this.form.invalid || this.enviando) {
      return;
    }

    this.enviando = true;
    const { confirmar_password, ...datosRecuperacion } = this.form.getRawValue();

    this.authService.recuperarPassword(datosRecuperacion).subscribe({
      next: respuesta => {
        this.enviando = false;
        Swal.fire({
          icon: 'success',
          title: 'Solicitud procesada',
          text: respuesta.message,
          confirmButtonText: 'Ir al login'
        }).then(() => this.router.navigate(['/login']));
      },
      error: (err: HttpErrorResponse) => {
        this.enviando = false;
        const mensajes = Object.values(err.error || {}).flat();
        this.error = String(
          mensajes[0] || 'No se pudo procesar la solicitud. Revisá los datos.'
        );
      }
    });
  }
}
