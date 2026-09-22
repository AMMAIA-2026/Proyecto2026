# Seed de campañas en PythonAnywhere

El backend ya contiene los 25 centros de salud reales de Córdoba en la migración
`centros_salud.0002_cargar_centros`. El comando `seed_campanias_reales` verifica
los 25 centros, repone los que falten y sincroniza diez campañas asociadas a
centros reales. Es idempotente y no elimina campañas existentes.

Las fechas de las campañas se calculan respecto del día de ejecución para
conservar una mezcla de estados `Finalizada`, `Activa` y `Proximamente`, además
de duraciones cortas y extendidas.

## Comandos

En PythonAnywhere, no ejecutar literalmente valores entre `<` y `>`: son
marcadores de ejemplo y Bash los interpreta como redirecciones. Para el caso
actual, donde el checkout está en `main`, usar:

```bash
PROJECT_ROOT="/home/sangreyaispc/Proyecto2026"
VENV_PATH="/home/sangreyaispc/.virtualenvs/NOMBRE_DEL_VIRTUALENV"
source "$VENV_PATH/bin/activate"
cd "$PROJECT_ROOT"
git pull origin main
python -m pip install -r backend/requirements.txt
cd "$PROJECT_ROOT/backend/ProyectoMain"
python manage.py migrate --noinput
python manage.py seed_campanias_reales
python manage.py seed_campanias_reales --check-only
python manage.py seed_demo_data
```

Reemplazar solamente `NOMBRE_DEL_VIRTUALENV` por el nombre real del virtualenv.
Se puede consultar con `ls -la /home/sangreyaispc/.virtualenvs`. Si todavía no
existe, crearlo una sola vez y luego instalar las dependencias:

```bash
python3.13 -m venv "/home/sangreyaispc/.virtualenvs/sangre-ya"
source "/home/sangreyaispc/.virtualenvs/sangre-ya/bin/activate"
python -m pip install -r "/home/sangreyaispc/Proyecto2026/backend/requirements.txt"
```

El archivo `.env` del servidor debe tener las credenciales de la base remota;
no deben agregarse al repositorio.

`seed_demo_data` agrega los usuarios `usuariomenor18@unmail.com` y
`usuariomayor65@unmail.com`, ambos con contraseña `Qwerty123.`, la campaña
`Campaña de test Cupo` con `cupo_maximo=1` y 11 campañas históricas. Las
inscripciones históricas se distribuyen desde el primer día de cada mes para
que el gráfico del dashboard tenga datos en los 11 meses anteriores.

Si el proyecto se ejecuta desde otra ruta, usar como directorio de trabajo el
que contiene `manage.py`. El primer `--check-only` debe informar `25/25` centros
si la migración ya fue aplicada; si faltan centros, la ejecución normal los
repondrá antes de sincronizar las campañas.
