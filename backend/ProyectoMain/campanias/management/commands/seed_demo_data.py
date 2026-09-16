from datetime import date

from django.core.management.base import BaseCommand, CommandError

from campanias.models import Campania, EstadoCampaniaChoices
from centros_salud.models import CentroSalud
from inscripciones.models import Inscripcion
from usuarios.models import RolChoices, Usuario


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

        demo_campaigns = list(Campania.objects.order_by('id')[:10])
        if len(demo_campaigns) < 10:
            raise CommandError('No se pudieron preparar 10 campañas de prueba.')

        demo_users = []
        for index in range(1, 21):
            email = f'demo.usuario{index:02d}@sangreya.test'
            user, _ = Usuario.objects.get_or_create(
                email=email,
                defaults={
                    'username': f'demo_usuario_{index:02d}',
                    'dni': f'{50000000 + index}',
                    'nombre': f'Donante {index:02d}',
                    'apellido': 'Prueba',
                    'fecha_nacimiento': date(1990, 1, 1),
                    'rol': RolChoices.USUARIO_ESTANDAR,
                    'is_active': True,
                },
            )
            user.username = f'demo_usuario_{index:02d}'
            user.dni = f'{50000000 + index}'
            user.nombre = f'Donante {index:02d}'
            user.apellido = 'Prueba'
            user.fecha_nacimiento = date(1990, 1, 1)
            user.rol = RolChoices.USUARIO_ESTANDAR
            user.is_active = True
            user.set_password('DemoSangreYa2026!')
            user.save()
            demo_users.append(user)

        inscription_count = 0
        for index, user in enumerate(demo_users):
            amount = 2 + (index % 4)
            for offset in range(amount):
                campaign = demo_campaigns[(index + offset) % len(demo_campaigns)]
                _, created = Inscripcion.objects.get_or_create(
                    usuario=user,
                    campania=campaign,
                )
                if created:
                    inscription_count += 1

        self.stdout.write(self.style.SUCCESS(
            'Datos de prueba listos: 25 centros, 10 campañas, '
            '20 usuarios estándar y entre 2 y 5 inscripciones por usuario. '
            f'Inscripciones nuevas: {inscription_count}.'
        ))

    @staticmethod
    def calculate_status(start_date, end_date):
        today = date.today()
        if start_date > today:
            return EstadoCampaniaChoices.PROXIMAMENTE
        if end_date >= today:
            return EstadoCampaniaChoices.ACTIVA
        return EstadoCampaniaChoices.FINALIZADA
