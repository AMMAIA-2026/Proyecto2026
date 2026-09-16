from datetime import date

from django.core.management.base import BaseCommand

from campanias.models import Campania, CentroSalud, Estado_Campania


class Command(BaseCommand):
    help = 'Crea centros y campañas de prueba sin borrar datos existentes.'

    def handle(self, *args, **options):
        centers = [
            {
                'nombre': 'Banco Central de Sangre de la Provincia de Córdoba',
                'direccion': 'Rosario de Santa Fe 374',
                'barrio': 'Centro',
                'ciudad': 'Córdoba',
                'telefono': '3512480189',
                'sitio_web': 'https://ministeriodesalud.cba.gov.ar/banco-de-sangre/',
                'latitud': '-31.4177671',
                'longitud': '-64.1792522',
            },
            {
                'nombre': 'Banco de Sangre Municipal',
                'direccion': 'Salta 480',
                'barrio': 'Centro',
                'ciudad': 'Córdoba',
                'telefono': '3514276240',
                'sitio_web': 'https://cordoba.gob.ar/donar-sangre-puede-salvar-hasta-cuatro-vidas/',
                'latitud': '-31.4121493',
                'longitud': '-64.1763496',
            },
            {
                'nombre': 'Banco de Sangre de la Universidad Nacional de Córdoba',
                'direccion': 'Enfermera Gordillo Gómez s/n, entre Bv. de la Reforma y Av. Valparaíso',
                'barrio': 'Ciudad Universitaria',
                'ciudad': 'Córdoba',
                'telefono': '3514334121',
                'sitio_web': 'https://bancodesangre.turnos.unc.edu.ar/',
                'latitud': '-31.4379571',
                'longitud': '-64.1878064',
            },
            {
                'nombre': 'Fundación Banco Central de Sangre',
                'direccion': 'Caseros 1576',
                'barrio': 'Quinta Santa Ana',
                'ciudad': 'Córdoba',
                'telefono': '3514807373',
                'sitio_web': 'https://www.donarencordoba.com.ar/',
                'latitud': '-31.4113956',
                'longitud': '-64.2059516',
            },
            {
                'nombre': 'Hospital Dr. Arturo Illia - Servicio de Hemoterapia',
                'direccion': 'Av. del Libertador 1450',
                'barrio': 'Cafferata',
                'ciudad': 'Alta Gracia',
                'telefono': '3547429282/85',
                'sitio_web': 'https://ministeriodesalud.cba.gov.ar/hospitales-y-centros-de-salud/',
                'latitud': '-31.6591224',
                'longitud': '-64.4161881',
            },
            {
                'nombre': 'Hospital Dr. José Antonio Ceballos - Servicio de Hemoterapia',
                'direccion': 'Gerónimo del Barco 1300',
                'barrio': 'Bell Ville',
                'ciudad': 'Bell Ville',
                'telefono': '3534421003/04/06',
                'sitio_web': 'https://ministeriodesalud.cba.gov.ar/hospitales-y-centros-de-salud/',
                'latitud': '-32.6168221',
                'longitud': '-62.7037998',
            },
            {
                'nombre': 'Hospital Dr. Pedro Vella - Servicio de Hemoterapia',
                'direccion': 'Rosario 300',
                'barrio': 'Corral de Bustos',
                'ciudad': 'Corral de Bustos',
                'telefono': '3468433974',
                'sitio_web': 'https://ministeriodesalud.cba.gov.ar/hospitales-y-centros-de-salud/',
                'latitud': '-33.2835410',
                'longitud': '-62.1939697',
            },
            {
                'nombre': 'Hospital Aurelio Crespo - Servicio de Hemoterapia',
                'direccion': 'Félix Cáceres s/n',
                'barrio': 'Cruz del Eje',
                'ciudad': 'Cruz del Eje',
                'telefono': '3549426747',
                'sitio_web': 'https://ministeriodesalud.cba.gov.ar/hospitales-y-centros-de-salud/',
                'latitud': '-30.7437265',
                'longitud': '-64.7874548',
            },
            {
                'nombre': 'Hospital Dr. Ernesto Romagosa - Servicio de Hemoterapia',
                'direccion': 'Colón 247',
                'barrio': 'Deán Funes',
                'ciudad': 'Deán Funes',
                'telefono': '3521479579',
                'sitio_web': 'https://ministeriodesalud.cba.gov.ar/hospitales-y-centros-de-salud/',
                'latitud': '-30.4240135',
                'longitud': '-64.3563512',
            },
            {
                'nombre': 'Hospital René Favaloro - Servicio de Hemoterapia',
                'direccion': 'Uruguay 537',
                'barrio': 'Huinca Renancó',
                'ciudad': 'Huinca Renancó',
                'telefono': '2336494107',
                'sitio_web': 'https://ministeriodesalud.cba.gov.ar/hospitales-y-centros-de-salud/',
                'latitud': '-34.8323721',
                'longitud': '-64.3756257',
            },
            {
                'nombre': 'Hospital Vicente Agüero - Servicio de Hemoterapia',
                'direccion': 'España 121',
                'barrio': 'Vicente Agüero',
                'ciudad': 'Jesús María',
                'telefono': '3525426703',
                'sitio_web': 'https://ministeriodesalud.cba.gov.ar/hospitales-y-centros-de-salud/',
                'latitud': '-30.9769867',
                'longitud': '-64.0900763',
            },
            {
                'nombre': 'Hospital San Antonio - Servicio de Hemoterapia',
                'direccion': 'Enrique Gauna 1251',
                'barrio': 'La Carlota',
                'ciudad': 'La Carlota',
                'telefono': '3584422295',
                'sitio_web': 'https://ministeriodesalud.cba.gov.ar/hospitales-y-centros-de-salud/',
                'latitud': '-33.4240280',
                'longitud': '-63.3033394',
            },
            {
                'nombre': 'Hospital Ramón J. Cárcano - Servicio de Hemoterapia',
                'direccion': 'Av. Juan Domingo Perón 20',
                'barrio': 'La Maitena',
                'ciudad': 'Laboulaye',
                'telefono': '3385453242',
                'sitio_web': 'https://ministeriodesalud.cba.gov.ar/hospitales-y-centros-de-salud/',
                'latitud': '-34.1405091',
                'longitud': '-63.3920740',
            },
            {
                'nombre': 'Hospital Abel Ayerza - Servicio de Hemoterapia',
                'direccion': 'Belgrano 350',
                'barrio': 'Marcos Juárez',
                'ciudad': 'Marcos Juárez',
                'telefono': '3472422820',
                'sitio_web': 'https://ministeriodesalud.cba.gov.ar/hospitales-y-centros-de-salud/',
                'latitud': '-32.6963534',
                'longitud': '-62.0963009',
            },
            {
                'nombre': 'Hospital Dr. Luis M. Bellodi - Servicio de Hemoterapia',
                'direccion': 'Av. Rossel 1800',
                'barrio': 'San Sebastián',
                'ciudad': 'Mina Clavero',
                'telefono': '',
                'sitio_web': 'https://ministeriodesalud.cba.gov.ar/hospitales-y-centros-de-salud/',
                'latitud': '-31.7433298',
                'longitud': '-64.9991184',
            },
            {
                'nombre': 'Nuevo Hospital San Antonio de Padua - Servicio de Hemoterapia',
                'direccion': 'Guardias Nacionales 1051',
                'barrio': 'San Antonio de Padua',
                'ciudad': 'Río Cuarto',
                'telefono': '3584678700/03/72/75',
                'sitio_web': 'https://ministeriodesalud.cba.gov.ar/hospitales-y-centros-de-salud/',
                'latitud': '-33.1098399',
                'longitud': '-64.3556313',
            },
            {
                'nombre': 'Nuevo Hospital Provincial Brig. Gral. Juan Bautista Bustos - Servicio de Hemoterapia',
                'direccion': 'Estanislao del Campo y Amado Nervo',
                'barrio': 'Parque Industrial Leonardo Da Vinci',
                'ciudad': 'Río Tercero',
                'telefono': '3571410210',
                'sitio_web': 'https://ministeriodesalud.cba.gov.ar/hospitales-y-centros-de-salud/',
                'latitud': '-32.1849803',
                'longitud': '-64.1365493',
            },
            {
                'nombre': 'Hospital J. B. Iturraspe - Medicina Transfusional',
                'direccion': 'Dominga Cullen 450',
                'barrio': 'Parque',
                'ciudad': 'San Francisco',
                'telefono': '3564443722/18/19',
                'sitio_web': 'https://ministeriodesalud.cba.gov.ar/hospitales-y-centros-de-salud/',
                'latitud': '-31.4279816',
                'longitud': '-62.0679246',
            },
            {
                'nombre': 'Hospital Eva Perón - Banco de Sangre',
                'direccion': 'Ruta Provincial 5 km 90, esquina Dr. David Bustos',
                'barrio': 'Santa Rosa de Calamuchita',
                'ciudad': 'Santa Rosa de Calamuchita',
                'telefono': '3546426671',
                'sitio_web': 'https://ministeriodesalud.cba.gov.ar/hospitales-y-centros-de-salud/',
                'latitud': '-32.0627076',
                'longitud': '-64.5304128',
            },
            {
                'nombre': 'Hospital Dr. Ramón B. Mestre - Servicio de Hemoterapia',
                'direccion': 'Moisés Quinteros 548',
                'barrio': 'Villa Santa Rosa',
                'ciudad': 'Villa Santa Rosa de Río Primero',
                'telefono': '3574480914',
                'sitio_web': 'https://ministeriodesalud.cba.gov.ar/hospitales-y-centros-de-salud/',
                'latitud': '-31.1572030',
                'longitud': '-63.4087868',
            },
            {
                'nombre': 'Hospital José M. Urrutia - Servicio de Hemoterapia',
                'direccion': '3 de Febrero 324',
                'barrio': 'Unquillo',
                'ciudad': 'Unquillo',
                'telefono': '8005554141',
                'sitio_web': 'https://ministeriodesalud.cba.gov.ar/hospitales-y-centros-de-salud/',
                'latitud': '-31.2346069',
                'longitud': '-64.3206411',
            },
            {
                'nombre': 'Hospital Domingo Funes - Servicio de Hemoterapia',
                'direccion': 'Av. Domingo Funes s/n',
                'barrio': 'Villa Caeiro',
                'ciudad': 'Santa María de Punilla',
                'telefono': '3541489676/73/72/71',
                'sitio_web': 'https://ministeriodesalud.cba.gov.ar/hospitales-y-centros-de-salud/',
                'latitud': '-31.2967838',
                'longitud': '-64.4535742',
            },
            {
                'nombre': 'Hospital Provincial de Villa Dolores - Servicio de Hemoterapia',
                'direccion': 'Av. Belgrano 1800',
                'barrio': 'Villa Dolores',
                'ciudad': 'Villa Dolores',
                'telefono': '3544426437',
                'sitio_web': 'https://ministeriodesalud.cba.gov.ar/hospitales-y-centros-de-salud/',
                'latitud': '-31.9498789',
                'longitud': '-65.1677567',
            },
            {
                'nombre': 'Hospital Pasteur - Servicio de Hemoterapia',
                'direccion': 'Aldo Serrano esquina Buchardo',
                'barrio': 'Ramón Carrillo',
                'ciudad': 'Villa María',
                'telefono': '3534619138/30',
                'sitio_web': 'https://ministeriodesalud.cba.gov.ar/hospitales-y-centros-de-salud/',
                'latitud': '-32.3939013',
                'longitud': '-63.2589614',
            },
            {
                'nombre': 'Hospital San Vicente de Paul - Servicio de Hemoterapia',
                'direccion': 'Bv. Sobremonte 550',
                'barrio': 'Del Molino',
                'ciudad': 'Villa del Rosario',
                'telefono': '3573424704/06',
                'sitio_web': 'https://ministeriodesalud.cba.gov.ar/hospitales-y-centros-de-salud/',
                'latitud': '-31.5630144',
                'longitud': '-63.5417909',
            },
        ]

        center_by_name = {}
        for data in centers:
            center, _ = CentroSalud.objects.update_or_create(
                nombre=data['nombre'],
                defaults=data,
            )
            center_by_name[data['nombre']] = center

        states = {}
        for name in ('Activa', 'Finalizada', 'Proximamente'):
            state, _ = Estado_Campania.objects.get_or_create(estado=name)
            states[name] = state

        campaigns = [
            {
                'titulo': 'Donación de Sangre Hospital Central',
                'descripcion': 'Campaña solidaria para pacientes en cirugías y emergencias críticas.',
                'ubicacion': 'Hospital Central Córdoba',
                'fecha_inicio': date(2026, 9, 18),
                'fecha_fin': date(2026, 9, 20),
                'estado_campania': states['Activa'],
                'centro_salud': center_by_name[
                    'Banco Central de Sangre de la Provincia de Córdoba'
                ],
                'cupo_maximo': 40,
            },
            {
                'titulo': 'Jornada Solidaria Barrio Güemes',
                'descripcion': 'Recolección de sangre destinada a hospitales públicos de la ciudad.',
                'ubicacion': 'Centro Cultural Güemes',
                'fecha_inicio': date(2026, 9, 21),
                'fecha_fin': date(2026, 9, 23),
                'estado_campania': states['Proximamente'],
                'centro_salud': center_by_name['Fundación Banco Central de Sangre'],
                'cupo_maximo': 30,
            },
            {
                'titulo': 'Maratón de Donación Universitaria',
                'descripcion': 'Evento organizado junto a la comunidad universitaria para fomentar la donación voluntaria.',
                'ubicacion': 'Ciudad Universitaria Córdoba',
                'fecha_inicio': date(2026, 9, 25),
                'fecha_fin': date(2026, 9, 27),
                'estado_campania': states['Proximamente'],
                'centro_salud': center_by_name[
                    'Banco de Sangre de la Universidad Nacional de Córdoba'
                ],
                'cupo_maximo': 25,
            },
            {
                'titulo': 'Colecta Solidaria Alta Gracia',
                'descripcion': 'Jornada de donación voluntaria para reforzar las reservas de sangre de la región.',
                'ubicacion': 'Hospital Dr. Arturo Illia',
                'fecha_inicio': date(2026, 9, 29),
                'fecha_fin': date(2026, 10, 1),
                'estado_campania': states['Proximamente'],
                'centro_salud': center_by_name[
                    'Hospital Dr. Arturo Illia - Servicio de Hemoterapia'
                ],
                'cupo_maximo': 35,
            },
            {
                'titulo': 'Donación Comunitaria Bell Ville',
                'descripcion': 'Campaña abierta a la comunidad para promover la donación habitual de sangre.',
                'ubicacion': 'Hospital Dr. José Antonio Ceballos',
                'fecha_inicio': date(2026, 10, 3),
                'fecha_fin': date(2026, 10, 5),
                'estado_campania': states['Proximamente'],
                'centro_salud': center_by_name[
                    'Hospital Dr. José Antonio Ceballos - Servicio de Hemoterapia'
                ],
                'cupo_maximo': 30,
            },
            {
                'titulo': 'Jornada Regional Cruz del Eje',
                'descripcion': 'Jornada regional para facilitar la donación de sangre a vecinos de localidades cercanas.',
                'ubicacion': 'Hospital Aurelio Crespo',
                'fecha_inicio': date(2026, 10, 7),
                'fecha_fin': date(2026, 10, 9),
                'estado_campania': states['Proximamente'],
                'centro_salud': center_by_name[
                    'Hospital Aurelio Crespo - Servicio de Hemoterapia'
                ],
                'cupo_maximo': 28,
            },
            {
                'titulo': 'Campaña Solidaria Río Cuarto',
                'descripcion': 'Campaña de donación junto al equipo de hemoterapia del sur provincial.',
                'ubicacion': 'Nuevo Hospital San Antonio de Padua',
                'fecha_inicio': date(2026, 10, 12),
                'fecha_fin': date(2026, 10, 14),
                'estado_campania': states['Proximamente'],
                'centro_salud': center_by_name[
                    'Nuevo Hospital San Antonio de Padua - Servicio de Hemoterapia'
                ],
                'cupo_maximo': 45,
            },
            {
                'titulo': 'Jornada de Donación San Francisco',
                'descripcion': 'Espacio de donación voluntaria para acompañar las necesidades transfusionales locales.',
                'ubicacion': 'Hospital J. B. Iturraspe',
                'fecha_inicio': date(2026, 10, 16),
                'fecha_fin': date(2026, 10, 18),
                'estado_campania': states['Proximamente'],
                'centro_salud': center_by_name[
                    'Hospital J. B. Iturraspe - Medicina Transfusional'
                ],
                'cupo_maximo': 32,
            },
            {
                'titulo': 'Colecta Provincial Villa María',
                'descripcion': 'Colecta destinada a fortalecer la disponibilidad de sangre en el centro de la provincia.',
                'ubicacion': 'Hospital Pasteur',
                'fecha_inicio': date(2026, 10, 20),
                'fecha_fin': date(2026, 10, 22),
                'estado_campania': states['Proximamente'],
                'centro_salud': center_by_name[
                    'Hospital Pasteur - Servicio de Hemoterapia'
                ],
                'cupo_maximo': 40,
            },
            {
                'titulo': 'Donación de Sangre Centro Córdoba',
                'descripcion': 'Jornada de donación para la comunidad de Córdoba capital.',
                'ubicacion': 'Banco de Sangre Municipal',
                'fecha_inicio': date(2026, 9, 15),
                'fecha_fin': date(2026, 9, 17),
                'estado_campania': states['Activa'],
                'centro_salud': center_by_name['Banco de Sangre Municipal'],
                'cupo_maximo': 50,
            },
            {
                'titulo': 'Jornada de Donación Jesús María',
                'descripcion': 'Campaña abierta para sumar donantes voluntarios en el norte de la provincia.',
                'ubicacion': 'Hospital Vicente Agüero',
                'fecha_inicio': date(2026, 10, 24),
                'fecha_fin': date(2026, 10, 26),
                'estado_campania': states['Proximamente'],
                'centro_salud': center_by_name[
                    'Hospital Vicente Agüero - Servicio de Hemoterapia'
                ],
                'cupo_maximo': 30,
            },
        ]

        for data in campaigns:
            title = data.pop('titulo')
            Campania.objects.update_or_create(titulo=title, defaults=data)

        self.stdout.write(self.style.SUCCESS(
            'Datos de prueba creados: 25 centros y 11 campañas.'
        ))
