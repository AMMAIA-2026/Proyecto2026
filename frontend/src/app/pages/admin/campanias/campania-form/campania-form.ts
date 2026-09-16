import { Component, OnInit, inject } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import Swal from 'sweetalert2';
import { forkJoin } from 'rxjs';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { CentroSalud } from '../../../../models/campania.model';
import { CampaniaService } from '../../../../services/campanias/campania.service';


@Component({
  selector: 'app-campania-form',
  imports: [ReactiveFormsModule],
  templateUrl: './campania-form.html',
  styleUrls: ['./campania-form.css']
})
export class CampaniaForm implements OnInit {

  campaniaForm: FormGroup;
  modoEdicion = false;
  campaniaId: number | null = null;
  estadoActual = '';
  mensajeErrorFechaInicio = '';
  mensajeErrorFechaFin = '';
  fechaInicioOriginal: string | null = null;
  readonly fechaMinima = this.formatearFechaParaInput(new Date());
  minFechaInicio = this.fechaMinima;
  centrosSalud: CentroSalud[] = [];
  errorCentros = '';
  totalInscriptosActual = 0;

  mensajesError: any = {
    titulo: {
      required: 'El título es obligatorio.',
      minlength: 'El título debe tener al menos 5 caracteres.',
      maxlength: 'El título no puede superar los 100 caracteres.'
    },
    descripcion: {
      required: 'La descripción es obligatoria.',
      minlength: 'La descripción debe tener al menos 20 caracteres.',
      maxlength: 'La descripción no puede superar los 1500 caracteres.'
    },
    ubicacion: {
      required: 'La ubicación es obligatoria.',
      minlength: 'La ubicación debe tener al menos 5 caracteres.',
      maxlength: 'La ubicación no puede superar los 100 caracteres.'
    },
    centro_salud: {
      required: 'El centro de salud es obligatorio.'
    },
    fecha_inicio: { required: 'La fecha de inicio es obligatoria.' },
    fecha_fin: { required: 'La fecha de finalización es obligatoria.' },
    cupo_maximo: { min: 'El cupo debe ser de al menos 1 donante.' }
  };

  private fb = inject(FormBuilder);
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private campaniaService = inject(CampaniaService);

  constructor() {
    this.campaniaForm = this.fb.group({
      titulo: ['',
        [Validators.required,
        Validators.minLength(5),
        Validators.maxLength(100)]
      ],
      descripcion: ['',
        [Validators.required,
        Validators.minLength(20),
        Validators.maxLength(1500)]],
      ubicacion: ['',
        [Validators.required,
        Validators.minLength(5),
        Validators.maxLength(100)]],
      centro_salud: [null, Validators.required],
      fecha_inicio: ['', Validators.required],
      fecha_fin: ['', Validators.required],
      cupo_maximo: [null, Validators.min(1)],
      estado_campania: [{ value: '', disabled: true }]
    });

    this.campaniaForm.valueChanges.pipe(takeUntilDestroyed()).subscribe(() => {
      this.actualizarEstado();
    });
  }


  ngOnInit(): void {
    this.campaniaId = Number(this.route.snapshot.paramMap.get('id'));

    if (this.campaniaId) {
      this.modoEdicion = true;
      this.cargarDatosEdicion(this.campaniaId);
    } else {
      this.cargarCentrosSalud();
      this.actualizarEstado();
    }
  }

  cargarCentrosSalud(): void {
    this.campaniaService.getCentrosSalud().subscribe({
      next: centros => {
        this.centrosSalud = centros;
      },
      error: () => {
        this.errorCentros = 'No se pudieron cargar los centros de salud.';
      }
    });
  }


  cargarDatosEdicion(id: number): void {
    forkJoin({
      centros: this.campaniaService.getCentrosSalud(),
      campania: this.campaniaService.getCampania(String(id))
    }).subscribe({
      next: ({ centros, campania }) => {
        this.centrosSalud = centros;
        const data = campania;
        this.fechaInicioOriginal = data.fecha_inicio;
        this.totalInscriptosActual = data.total_inscriptos;
        this.minFechaInicio = data.fecha_inicio < this.fechaMinima
          ? data.fecha_inicio
          : this.fechaMinima;
        this.campaniaForm.patchValue({
          titulo: data.titulo,
          descripcion: data.descripcion,
          ubicacion: data.ubicacion,
          centro_salud: data.centro_salud,
          fecha_inicio: data.fecha_inicio,
          fecha_fin: data.fecha_fin,
          cupo_maximo: data.cupo_maximo
        });
        this.actualizarEstado();
      },
      error: () => {
        this.errorCentros = 'No se pudieron recuperar los datos de la campaña.';
      }
    });
  }


  validarFechas(): string {
    this.mensajeErrorFechaInicio = '';
    this.mensajeErrorFechaFin = '';

    const inicio = this.campaniaForm.value.fecha_inicio;
    const fin = this.campaniaForm.value.fecha_fin;
    const cupo = this.campaniaForm.value.cupo_maximo;

    if (!inicio || !fin) {
      return '';
    }

    if (
      (!this.modoEdicion && inicio < this.fechaMinima) ||
      (this.modoEdicion && inicio < this.fechaMinima && inicio !== this.fechaInicioOriginal)
    ) {
      this.mensajeErrorFechaInicio = 'La fecha de inicio no puede ser anterior a hoy.';
      return this.mensajeErrorFechaInicio;
    }

    if (cupo && this.totalInscriptosActual >= cupo) {
      this.estadoActual = 'Finalizada';
    } else if (fin < this.fechaMinima) {
      this.mensajeErrorFechaFin = 'No se puede crear o editar una campaña finalizada.';
      return this.mensajeErrorFechaFin;
    }

    if (fin < inicio) {
      this.mensajeErrorFechaFin = 'La fecha de fin no puede ser anterior a la fecha de inicio.';
      return this.mensajeErrorFechaFin;
    }

    return '';
  }


  private actualizarEstado(): void {
    const inicio = this.campaniaForm.value.fecha_inicio;
    const fin = this.campaniaForm.value.fecha_fin;

    this.validarFechas();

    if (!inicio || !fin) {
      this.estadoActual = '';
      this.campaniaForm.get('estado_campania')?.setValue('', { emitEvent: false });
      return;
    }

    const cupo = this.campaniaForm.value.cupo_maximo;

    if (cupo && this.totalInscriptosActual >= cupo) {
      this.estadoActual = 'Finalizada';
    } else if (fin < this.fechaMinima) {
      this.estadoActual = 'Finalizada';
    } else if (inicio > this.fechaMinima) {
      this.estadoActual = 'Proximamente';
    } else {
      this.estadoActual = 'Activa';
    }

    this.campaniaForm.get('estado_campania')?.setValue(
      this.estadoActual,
      { emitEvent: false }
    );
  }


  private formatearFechaParaInput(fecha: Date): string {
    const anio = fecha.getFullYear();
    const mes = String(fecha.getMonth() + 1).padStart(2, '0');
    const dia = String(fecha.getDate()).padStart(2, '0');
    return `${anio}-${mes}-${dia}`;
  }


  obtenerError(campo: string): string {
    const control = this.campaniaForm.get(campo);

    if (!control || !control.errors || !control.touched) {
      return '';
    }

    const primerError = Object.keys(control.errors)[0];

    return this.mensajesError[campo]?.[primerError] || '';
  }

  cancelar(): void {
    this.router.navigate(['/admin/campanias']);
  }


  onSubmit() {
    this.campaniaForm.markAllAsTouched();
    if (this.campaniaForm.invalid) {
      return;
    }

    const errorFechas = this.validarFechas();
    if (errorFechas) {
      Swal.fire({
        title: 'Fechas inválidas',
        text: errorFechas,
        icon: 'error'
      });
      return;
    }

    const data = {
      ...this.campaniaForm.value,
      estado_campania: this.estadoActual
    };

    if (this.modoEdicion) {
      this.campaniaService.editarCampania(this.campaniaId!, data).subscribe(() => {
        Swal.fire({
          title: 'Campaña actualizada',
          text: 'La campaña ha sido actualizada correctamente',
          icon: 'success',
          confirmButtonColor: '#2bc055'
        });
        this.router.navigate(['/admin/campanias']);
      }, () => {
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'No se pudo actualizar la campaña.'
        });
      });

    } else {
      this.campaniaService.crearCampania(data).subscribe(() => {
        Swal.fire({
          title: 'Campaña creada',
          text: 'La campaña ha sido creada correctamente',
          icon: 'success',
          confirmButtonColor: '#2bc055'
        });
        this.router.navigate(['/admin/campanias']);
      }, () => {
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'No se pudo crear la campaña.'
        });
      });
    }
  }
}
