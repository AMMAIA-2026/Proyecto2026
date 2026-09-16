import { Component } from '@angular/core';
import {
  BeneficioHero,
  ExclusionTemporal,
  PasoProcedimiento,
  RequisitoBasico,
  RequisitoDia,
} from '../../../models/informate.model';


@Component({
  selector: 'app-informate',
  imports: [],
  templateUrl: './informate.html',
  styleUrls: ['./informate.css']
})
export class Informate {


  readonly tituloPrincipal = '1 Donación';
  readonly tituloSecundario = 'Salva 3 Vidas.';

  readonly beneficiosHero: BeneficioHero[] = [
    { texto: 'Reservas seguras para cirugías y emergencias', conIcono: true },
    { texto: 'Licencia especial de estudio o trabajo (según ley nacional)', conIcono: true },
    { texto: 'Seguro de Sangre Solidario para familiares.', conIcono: true },
  ];


  readonly tituloSeccionDonante = '¿Puedo ser Donante?';

  readonly requisitosBasicos: RequisitoBasico[] = [
    { texto: 'Personas entre 18 y 65 años.', icono: 'check' },
    { texto: 'Peso mayor a 50 kg.', icono: 'check' },
    { texto: 'Buen estado general de salud.', icono: 'check' },
    { texto: 'Haber descansado correctamente.', icono: 'check' },
  ];

  readonly tituloExclusiones = 'Exclusiones temporales';

  readonly exclusionesTemporales: ExclusionTemporal[] = [
    { texto: 'Embarazo o lactancia.' },
    { texto: 'Tatuajes o piercings recientes.' },
    { texto: 'Síntomas de fiebre o infecciones.' },
  ];


  readonly tituloRequisitos = 'Requisitos (Día de la donación)';

  readonly requisitosDia: RequisitoDia[] = [
    { texto: 'Traer DNI o documento.', icono: 'dni' },
    { texto: 'Beber abundante agua.', icono: 'agua' },
    { texto: 'Evitar el ayuno prolongado (ropa cómoda).', icono: 'noAyuno' },
    { texto: 'Entrevista médica confidencial.', icono: 'entrevista' },
  ];


  readonly tituloProcedimiento = 'Procedimiento de Donación';

  readonly pasosProcedimiento: PasoProcedimiento[] = [
    { numero: 1, titulo: 'Registro y',       subtitulo: 'Presentación DNI',   icono: 'registro'         },
    { numero: 2, titulo: 'Entrevista Médica', subtitulo: 'y Control Salud',    icono: 'entrevistaMedica' },
    { numero: 3, titulo: 'Extracción',        subtitulo: '(10-15 minutos)',    icono: 'extraccion'       },
    { numero: 4, titulo: 'Descanso',          subtitulo: 'y Refrigerio',       icono: 'descanso'         },
  ];

  readonly pieProcedimiento   = 'Tiempo Total: ~45 mins';
  readonly avisoPostDonacion  = 'Evitar esfuerzos intensos después.';
}

