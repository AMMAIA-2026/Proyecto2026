import { Component } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import Swal from 'sweetalert2';

import { MOTIVOS_CONTACTO } from '../../../models/contacto.model';
import { ContactoService } from '../../../services/contactos/contacto.service';


@Component({
  selector: 'app-contactanos',
  imports: [ReactiveFormsModule],
  templateUrl: './contactanos.html',
  styleUrl: './contactanos.css'
})
export class Contactanos {
  contactoForm: FormGroup;
  enviando = false;
  readonly motivos = MOTIVOS_CONTACTO;

  constructor(
    private contactoService: ContactoService,
    private fb: FormBuilder
  ) {
    this.contactoForm = this.fb.group({
      nombre_completo: ['', [Validators.required, Validators.maxLength(100)]],
      correo_electronico: ['', [Validators.required, Validators.email]],
      motivo: ['', Validators.required],
      mensaje: ['', [Validators.required, Validators.maxLength(500)]]
    });
  }

  enviar(): void {
    this.contactoForm.markAllAsTouched();
    if (this.contactoForm.invalid || this.enviando) return;

    this.enviando = true;
    this.contactoService.crear(this.contactoForm.getRawValue()).subscribe({
      next: () => {
        this.enviando = false;
        this.contactoForm.reset();
        Swal.fire({
          icon: 'success',
          title: 'Mensaje enviado',
          text: 'Recibimos tu consulta y la revisaremos a la brevedad.',
          confirmButtonText: 'Aceptar'
        });
      },
      error: () => {
        this.enviando = false;
        Swal.fire({
          icon: 'error',
          title: 'No pudimos enviar el mensaje',
          text: 'Revisá los datos e intentá nuevamente.',
          confirmButtonText: 'Aceptar'
        });
      }
    });
  }
}
