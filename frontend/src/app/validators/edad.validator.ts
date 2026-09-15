export function calcularEdad(fechaNacimiento: string | null): number | null {
  if (!fechaNacimiento) return null;

  const [anio, mes, dia] = fechaNacimiento.split('-').map(Number);
  const hoy = new Date();
  let edad = hoy.getFullYear() - anio;
  if (
    hoy.getMonth() + 1 < mes ||
    (hoy.getMonth() + 1 === mes && hoy.getDate() < dia)
  ) {
    edad--;
  }
  return edad;
}


export function advertenciaEdad(fechaNacimiento: string | null): string {
  const edad = calcularEdad(fechaNacimiento);
  if (edad === null) return '';
  if (edad < 18) return 'Para donar debés tener al menos 18 años.';
  if (edad >= 65) return 'Para donar debés tener menos de 65 años.';
  return '';
}
