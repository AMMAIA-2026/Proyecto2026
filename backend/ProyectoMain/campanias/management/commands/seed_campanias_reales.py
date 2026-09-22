from datetime import timedelta
from importlib import import_module

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from centros_salud.models import CentroSalud

from campanias.models import Campania


CENTROS_MIGRATION = 'centros_salud.migrations.0002_cargar_centros'
TELEFONOS_MIGRATION = 'centros_salud.migrations.0003_ajustar_longitudes'

# Reutiliza el catálogo oficial de las migraciones para no duplicar los 25
# centros ni sus datos de contacto en el comando.
# Cada campaña apunta a un centro, por lo que se eligen diez centros distribuidos
# geográficamente. El comando verifica y deja disponibles los 25 centros.
CAMPANIAS = [
    {
        'titulo': 'Jornada de donación - Banco Central Córdoba',
        'centro_id': 1,
        'inicio_dias': -180,
        'fin_dias': -173,
        'cupo_maximo': 120,
        'estado': 'Finalizada',
        'descripcion': (
            'Jornada abierta de donación voluntaria para reforzar la disponibilidad '
            'de sangre y hemocomponentes en la red sanitaria de Córdoba.'
        ),
    },
    {
        'titulo': 'Donación voluntaria - Banco de Sangre UNC',
        'centro_id': 3,
        'inicio_dias': -90,
        'fin_dias': -89,
        'cupo_maximo': 80,
        'estado': 'Finalizada',
        'descripcion': (
            'Campaña universitaria de donación voluntaria destinada a sumar nuevos '
            'donantes y sostener las reservas de sangre.'
        ),
    },
    {
        'titulo': 'Campaña regional - Hospital Dr. Arturo Illia',
        'centro_id': 5,
        'inicio_dias': -60,
        'fin_dias': -30,
        'cupo_maximo': 100,
        'estado': 'Finalizada',
        'descripcion': (
            'Campaña regional para facilitar la donación de sangre a vecinos de '
            'Alta Gracia y localidades cercanas.'
        ),
    },
    {
        'titulo': 'Jornada solidaria - Hospital Aurelio Crespo',
        'centro_id': 8,
        'inicio_dias': -7,
        'fin_dias': 1,
        'cupo_maximo': 70,
        'estado': 'Activa',
        'descripcion': (
            'Jornada de donación voluntaria para mantener el abastecimiento del '
            'servicio de hemoterapia de Cruz del Eje.'
        ),
    },
    {
        'titulo': 'Donación comunitaria - Hospital Vicente Agüero',
        'centro_id': 11,
        'inicio_dias': -2,
        'fin_dias': 14,
        'cupo_maximo': 90,
        'estado': 'Activa',
        'descripcion': (
            'Campaña comunitaria de donación de sangre para fortalecer la atención '
            'de pacientes de Jesús María y su zona de influencia.'
        ),
    },
    {
        'titulo': 'Red de donación - Hospital Abel Ayerza',
        'centro_id': 14,
        'inicio_dias': 0,
        'fin_dias': 45,
        'cupo_maximo': 140,
        'estado': 'Activa',
        'descripcion': (
            'Jornada de la red sanitaria regional para incorporar donantes '
            'voluntarios y fortalecer las reservas disponibles.'
        ),
    },
    {
        'titulo': 'Campaña regional - Hospital San Antonio de Padua',
        'centro_id': 16,
        'inicio_dias': -30,
        'fin_dias': 90,
        'cupo_maximo': 180,
        'estado': 'Activa',
        'descripcion': (
            'Campaña extendida de donación voluntaria para acompañar la demanda de '
            'hemoterapia de Río Cuarto y localidades vecinas.'
        ),
    },
    {
        'titulo': 'Jornada de hemoterapia - Hospital J. B. Iturraspe',
        'centro_id': 18,
        'inicio_dias': 1,
        'fin_dias': 2,
        'cupo_maximo': 60,
        'estado': 'Proximamente',
        'descripcion': (
            'Jornada programada de donación voluntaria para ampliar la participación '
            'de la comunidad de San Francisco.'
        ),
    },
    {
        'titulo': 'Donación voluntaria - Hospital Pasteur',
        'centro_id': 24,
        'inicio_dias': 14,
        'fin_dias': 21,
        'cupo_maximo': 150,
        'estado': 'Proximamente',
        'descripcion': (
            'Campaña programada para promover la donación de sangre y sostener la '
            'atención transfusional de Villa María.'
        ),
    },
    {
        'titulo': 'Campaña comunitaria - Hospital San Vicente de Paul',
        'centro_id': 25,
        'inicio_dias': 45,
        'fin_dias': 90,
        'cupo_maximo': 100,
        'estado': 'Proximamente',
        'descripcion': (
            'Campaña programada de donación voluntaria para la comunidad de Villa '
            'del Rosario y localidades cercanas.'
        ),
    },
]


def centros_configurados():
    centros_migration = import_module(CENTROS_MIGRATION)
    telefonos_migration = import_module(TELEFONOS_MIGRATION)
    telefonos = telefonos_migration.TELEFONOS_PRINCIPALES

    return [
        {
            **centro,
            'telefono': telefonos.get(centro['id'], centro['telefono']),
        }
        for centro in centros_migration.CENTROS
    ]


class Command(BaseCommand):
    help = (
        'Verifica los 25 centros de salud y crea diez campañas de donación '
        'con estados y duraciones variadas.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--check-only',
            action='store_true',
            help='Verifica centros y campañas sin modificar la base de datos.',
        )

    def handle(self, *args, **options):
        centros = centros_configurados()
        ids_centros = [centro['id'] for centro in centros]
        centros_existentes = CentroSalud.objects.in_bulk(ids_centros)
        centros_faltantes = [
            centro for centro in centros if centro['id'] not in centros_existentes
        ]

        titulos = [campania['titulo'] for campania in CAMPANIAS]
        campanias_existentes = Campania.objects.filter(titulo__in=titulos).count()

        if options['check_only']:
            self.stdout.write(
                f'Centros de salud: {len(centros_existentes)}/{len(centros)}.'
            )
            self.stdout.write(
                f'Campañas del seed: {campanias_existentes}/{len(CAMPANIAS)}.'
            )
            if centros_faltantes:
                ids_faltantes = ', '.join(
                    str(centro['id']) for centro in centros_faltantes
                )
                raise CommandError(
                    f'Faltan centros de salud con ID: {ids_faltantes}.'
                )
            if campanias_existentes != len(CAMPANIAS):
                raise CommandError(
                    f'Se esperaban {len(CAMPANIAS)} campañas del seed y '
                    f'se encontraron {campanias_existentes}.'
                )
            return

        with transaction.atomic():
            for centro in centros_faltantes:
                CentroSalud.objects.create(**centro)

            centros_por_id = CentroSalud.objects.in_bulk(ids_centros)
            hoy = timezone.localdate()
            creadas = 0
            actualizadas = 0

            for datos in CAMPANIAS:
                defaults = {
                    'descripcion': datos['descripcion'],
                    'ubicacion': centros_por_id[datos['centro_id']].nombre,
                    'centro_salud': centros_por_id[datos['centro_id']],
                    'fecha_inicio': hoy + timedelta(days=datos['inicio_dias']),
                    'fecha_fin': hoy + timedelta(days=datos['fin_dias']),
                    'cupo_maximo': datos['cupo_maximo'],
                    'estado_campania': datos['estado'],
                }
                _, creada = Campania.objects.update_or_create(
                    titulo=datos['titulo'],
                    defaults=defaults,
                )
                if creada:
                    creadas += 1
                else:
                    actualizadas += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Centros de salud verificados: {len(centros)}/25 '
                f'(repuestos: {len(centros_faltantes)}).'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'Campañas sincronizadas: {len(CAMPANIAS)} '
                f'(creadas: {creadas}, actualizadas: {actualizadas}).'
            )
        )
