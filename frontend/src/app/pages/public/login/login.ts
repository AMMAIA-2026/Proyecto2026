import { Component } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../../services/auth/auth';
import {
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators
} from '@angular/forms';


@Component({
  selector: 'app-login',


  imports: [
    ReactiveFormsModule,
    RouterLink
  ],

  templateUrl: './login.html',

  styleUrl: './login.css'
})

export class Login {

  loginForm: FormGroup;

  mensaje = '';

  constructor(

    private fb: FormBuilder,
    private router: Router,
    private authService: AuthService

  ) {

    this.loginForm = this.fb.group({

      email: [
        '',
        [
          Validators.required,
          Validators.email
        ]
      ],

      password: [
        '',
        [
          Validators.required,
          Validators.minLength(4),
          Validators.maxLength(100)
        ]
      ]

    });

  }

  onSubmit() {

    this.mensaje = '';

    if (this.loginForm.invalid) {
      this.loginForm.markAllAsTouched();
      return;
    }

    this.authService.iniciarSesion({
      email: this.loginForm.value.email,
      password: this.loginForm.value.password,
    }).subscribe({

      next: (response: any) => {
        
        localStorage.setItem('refresh_token', response.refresh);
        localStorage.setItem('rol', response.user.rol);

        this.authService.login(response.access);

        if (response.user.rol === 'Administrador') {
          this.router.navigate(['/admin/dashboard']);
        } else {
          this.router.navigate(['/']);
        }

      },
      error: (error) => {

        this.mensaje = 'Credenciales incorrectas';
        this.loginForm.get('password')?.reset();
        this.loginForm.markAsUntouched();

      }

    });

  }

}
