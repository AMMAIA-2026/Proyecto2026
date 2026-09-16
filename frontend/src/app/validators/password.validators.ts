import {
  AbstractControl,
  ValidationErrors,
  ValidatorFn,
  Validators
} from '@angular/forms';


const PASSWORD_PATTERN = /^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[^A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9\s]).+$/;


export function validadoresPassword(): ValidatorFn[] {
  return [
    Validators.required,
    Validators.minLength(10),
    Validators.pattern(PASSWORD_PATTERN)
  ];
}


export const passwordsCoinciden: ValidatorFn = (
  control: AbstractControl
): ValidationErrors | null => {
  const password = control.get('password')?.value;
  const confirmacion = control.get('confirmar_password')?.value;

  if (!password || !confirmacion) {
    return null;
  }

  return password === confirmacion ? null : { passwordsNoCoinciden: true };
};
