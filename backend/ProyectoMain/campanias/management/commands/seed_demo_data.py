from datetime import date

from django.core.management.base import BaseCommand, CommandError

from campanias.models import Campania, EstadoCampaniaChoices
from centros_salud.models import CentroSalud


class Command(BaseCommand):
    help = 'Crea 10 campañas de prueba asociadas a centros existentes.'

    def handle(self, *args, **options):
        campaigns = [
            {
                'titulo': 'Donación de Sangre Hospital Central',
                'descripcion': 'Campaña solidaria para pacientes en cirugías y emergencias críticas.',
                'ubicacion': 'Hospital Central Córdoba',
                'fecha_inicio': date(2026, 9, 15),
                'fecha_fin': date(2026, 9, 17),
                'centro_salud_id': 1,
                'cupo_maximo': 40,
            },
            {
                'titulo': 'Jornada Solidaria Barrio Güemes',
                'descripcion': 'Recolección de sangre destinada a hospitales públicos de la ciudad.',
                'ubicacion': 'Centro Cultural Güemes',
                'fecha_inicio': date(2026, 9, 21),
                'fecha_fin': date(2026, 9, 23),
                'centro_salud_id': 4,
                'cupo_maximo': 30,
            },
            {
                'titulo': 'Maratón de Donación Universitaria',
                'descripcion': 'Evento organizado junto a la comunidad universitaria para fomentar la donación voluntaria.',
                'ubicacion': 'Ciudad Universitaria Córdoba',
                'fecha_inicio': date(2026, 9, 25),
                'fecha_fin': date(2026, 9, 27),
                'centro_salud_id': 3,
                'cupo_maximo': 25,
            },
            {
                'titulo': 'Colecta Solidaria Alta Gracia',
                'descripcion': 'Jornada de donación voluntaria para reforzar las reservas de sangre de la región.',
                'ubicacion': 'Hospital Dr. Arturo Illia',
                'fecha_inicio': date(2026, 9, 29),
                'fecha_fin': date(2026, 10, 1),
                'centro_salud_id': 5,
                'cupo_maximo': 35,
            },
            {
                'titulo': 'Donación Comunitaria Bell Ville',
                'descripcion': 'Campaña abierta a la comunidad para promover la donación habitual de sangre.',
                'ubicacion': 'Hospital Dr. José Antonio Ceballos',
                'fecha_inicio': date(2026, 10, 3),
                'fecha_fin': date(2026, 10, 5),
                'centro_salud_id': 6,
                'cupo_maximo': 30,
            },
            {
                'titulo': 'Jornada Regional Cruz del Eje',
                'descripcion': 'Jornada regional para facilitar la donación de sangre a vecinos de localidades cercanas.',
                'ubicacion': 'Hospital Aurelio Crespo',
                'fecha_inicio': date(2026, 10, 7),
                'fecha_fin': date(2026, 10, 9),
                'centro_salud_id': 8,
                'cupo_maximo': 28,
            },
            {
                'titulo': 'Campaña Solidaria Río Cuarto',
                'descripcion': 'Campaña de donación junto al equipo de hemoterapia del sur provincial.',
                'ubicacion': 'Nuevo Hospital San Antonio de Padua',
                'fecha_inicio': date(2026, 10, 12),
                'fecha_fin': date(2026, 10, 14),
                'centro_salud_id': 16,
                'cupo_maximo': 45,
            },
            {
                'titulo': 'Jornada de Donación San Francisco',
                'descripcion': 'Espacio de donación voluntaria para acompañar las necesidades transfusionales locales.',
                'ubicacion': 'Hospital J. B. Iturraspe',
                'fecha_inicio': date(2026, 10, 16),
                'fecha_fin': date(2026, 10, 18),
                'centro_salud_id': 18,
                'cupo_maximo': 32,
            },
            {
                'titulo': 'Colecta Provincial Villa María',
                'descripcion': 'Colecta destinada a fortalecer la disponibilidad de sangre en el centro de la provincia.',
                'ubicacion': 'Hospital Pasteur',
                'fecha_inicio': date(2026, 10, 20),
                'fecha_fin': date(2026, 10, 22),
                'centro_salud_id': 24,
                'cupo_maximo': 40,
            },
            {
                'titulo': 'Jornada de Donación Jesús María',
                'descripcion': 'Campaña abierta para sumar donantes voluntarios en el norte de la provincia.',
                'ubicacion': 'Hospital Vicente Agüero',
                'fecha_inicio': date(2026, 10, 24),
                'fecha_fin': date(2026, 10, 26),
                'centro_salud_id': 11,
                'cupo_maximo': 30,
            },
        ]

        for data in campaigns:
            center_id = data.pop('centro_salud_id')
            try:
                center = CentroSalud.objects.get(pk=center_id)
            except CentroSalud.DoesNotExist as exception:
                raise CommandError(
                    f'No existe el centro de salud con ID {center_id}. '
                    'Ejecutá las migraciones antes del seed.'
                ) from exception

            data['centro_salud'] = center
            data['estado_campania'] = self.calculate_status(
                data['fecha_inicio'],
                data['fecha_fin'],
            )

            title = data.pop('titulo')
            Campania.objects.update_or_create(titulo=title, defaults=data)

        self.stdout.write(self.style.SUCCESS(
            'Datos de prueba creados: 25 centros y 10 campañas.'
        ))

    @staticmethod
    def calculate_status(start_date, end_date):
        today = date.today()
        if start_date > today:
            return EstadoCampaniaChoices.PROXIMAMENTE
        if end_date >= today:
            return EstadoCampaniaChoices.ACTIVA
        return EstadoCampaniaChoices.FINALIZADA
