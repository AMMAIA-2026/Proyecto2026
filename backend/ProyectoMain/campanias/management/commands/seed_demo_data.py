from datetime import date, datetime, time, timedelta

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from campanias.models import Campania, EstadoCampaniaChoices
from centros_salud.models import CentroSalud
from inscripciones.models import Inscripcion
from usuarios.models import RolChoices, Usuario


class Command(BaseCommand):
    help = (
        'Crea datos de prueba para campañas, edades límite e histórico mensual '
        'del dashboard.'
    )

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

        self.create_manual_test_users()
        self.create_capacity_test_campaign()
        historical_inscriptions = self.create_dashboard_history(demo_users)

        self.stdout.write(self.style.SUCCESS(
            'Datos de prueba listos: 25 centros, 10 campañas base, '
            '1 campaña de cupo y '
            '20 usuarios estándar, 2 usuarios de edad límite y '
            '11 campañas históricas. '
            f'Inscripciones nuevas: {inscription_count + historical_inscriptions}.'
        ))

    def create_manual_test_users(self):
        hoy = timezone.localdate()
        users = [
            {
                'email': 'usuariomenor18@unmail.com',
                'dni': '60160016',
                'nombre': 'Menor',
                'apellido': 'Usuario',
                'fecha_nacimiento': self.birth_date_for_age(hoy, 16),
            },
            {
                'email': 'usuariomayor65@unmail.com',
                'dni': '60700070',
                'nombre': 'Mayor',
                'apellido': 'Usuario',
                'fecha_nacimiento': self.birth_date_for_age(hoy, 70),
            },
        ]

        for data in users:
            email = data['email']
            user, _ = Usuario.objects.get_or_create(
                email=email,
                defaults={
                    **data,
                    'username': email,
                    'rol': RolChoices.USUARIO_ESTANDAR,
                    'is_active': True,
                },
            )
            user.username = email
            user.dni = data['dni']
            user.nombre = data['nombre']
            user.apellido = data['apellido']
            user.fecha_nacimiento = data['fecha_nacimiento']
            user.rol = RolChoices.USUARIO_ESTANDAR
            user.is_active = True
            user.set_password('Qwerty123.')
            user.save()

    def create_capacity_test_campaign(self):
        center = CentroSalud.objects.get(pk=1)
        today = timezone.localdate()
        campaign, _ = Campania.objects.get_or_create(
            titulo='Campaña de test Cupo',
            defaults={
                'descripcion': (
                    'Campaña de prueba para validar el límite de un donante '
                    'y el cambio de estado al completar el cupo.'
                ),
                'ubicacion': center.nombre,
                'centro_salud': center,
                'fecha_inicio': today,
                'fecha_fin': today + timedelta(days=30),
                'cupo_maximo': 1,
                'estado_campania': EstadoCampaniaChoices.ACTIVA,
            },
        )

        total_inscriptos = Inscripcion.objects.filter(campania=campaign).count()
        campaign.descripcion = (
            'Campaña de prueba para validar el límite de un donante '
            'y el cambio de estado al completar el cupo.'
        )
        campaign.ubicacion = center.nombre
        campaign.centro_salud = center
        campaign.fecha_inicio = today
        campaign.fecha_fin = today + timedelta(days=30)
        campaign.cupo_maximo = 1
        campaign.estado_campania = (
            EstadoCampaniaChoices.FINALIZADA
            if total_inscriptos >= 1
            else EstadoCampaniaChoices.ACTIVA
        )
        campaign.save()

    def create_dashboard_history(self, demo_users):
        today = timezone.localdate()
        center = CentroSalud.objects.get(pk=1)
        # Varying counts make the chart useful while keeping the dump small.
        counts_by_month = [1, 2, 3, 2, 4, 1, 3, 2, 5, 3, 4]
        created_inscriptions = 0

        for index, months_ago in enumerate(range(11, 0, -1)):
            month_start = self.month_start(today, months_ago)
            next_month = self.month_start(today, months_ago - 1)
            month_end = next_month - timedelta(days=1)
            title = f'Dump gráfico {month_start:%Y-%m}'
            campaign, _ = Campania.objects.update_or_create(
                titulo=title,
                defaults={
                    'descripcion': 'Datos históricos de prueba para el dashboard.',
                    'ubicacion': center.nombre,
                    'centro_salud': center,
                    'fecha_inicio': month_start,
                    'fecha_fin': month_end,
                    'cupo_maximo': 50,
                    'estado_campania': EstadoCampaniaChoices.FINALIZADA,
                },
            )

            for user_index in range(counts_by_month[index]):
                user = demo_users[user_index]
                inscription, created = Inscripcion.objects.get_or_create(
                    usuario=user,
                    campania=campaign,
                )
                if created:
                    created_inscriptions += 1

                inscription_date = month_start + timedelta(days=5 + user_index)
                inscription_datetime = timezone.make_aware(
                    datetime.combine(inscription_date, time(hour=10 + user_index)),
                    timezone.get_current_timezone(),
                )
                Inscripcion.objects.filter(pk=inscription.pk).update(
                    fecha_inscripcion=inscription_datetime,
                )

        return created_inscriptions

    @staticmethod
    def birth_date_for_age(today, age):
        try:
            return today.replace(year=today.year - age)
        except ValueError:
            return today.replace(year=today.year - age, day=28)

    @staticmethod
    def month_start(today, months_ago):
        month_index = today.year * 12 + today.month - 1 - months_ago
        year, month_index = divmod(month_index, 12)
        return date(year, month_index + 1, 1)

    @staticmethod
    def calculate_status(start_date, end_date):
        today = date.today()
        if start_date > today:
            return EstadoCampaniaChoices.PROXIMAMENTE
        if end_date >= today:
            return EstadoCampaniaChoices.ACTIVA
        return EstadoCampaniaChoices.FINALIZADA
