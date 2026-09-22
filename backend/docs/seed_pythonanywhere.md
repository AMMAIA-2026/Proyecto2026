# Seed de campañas en PythonAnywhere

El backend ya contiene los 25 centros de salud reales de Córdoba en la migración
`centros_salud.0002_cargar_centros`. El comando `seed_campanias_reales` verifica
los 25 centros, repone los que falten y sincroniza diez campañas asociadas a
centros reales. Es idempotente y no elimina campañas existentes.

Las fechas de las campañas se calculan respecto del día de ejecución para
conservar una mezcla de estados `Finalizada`, `Activa` y `Proximamente`, además
de duraciones cortas y extendidas.

## Comandos

Ejecutar en una consola Bash de PythonAnywhere después de desplegar el branch:

```bash
cd "/home/<usuario>/Sangre Ya back/backend/ProyectoMain"
source "/home/<usuario>/.virtualenvs/sangre-ya/bin/activate"
git pull origin <branch>
python manage.py migrate --noinput
python manage.py seed_campanias_reales
python manage.py seed_campanias_reales --check-only
```

Reemplazar `<usuario>`, `<branch>` y la ruta del virtualenv por los valores de
PythonAnywhere. El archivo `.env` del servidor debe tener las credenciales de la
base remota; no deben agregarse al repositorio.

Si el proyecto se ejecuta desde otra ruta, usar como directorio de trabajo el
que contiene `manage.py`. El primer `--check-only` debe informar `25/25` centros
si la migración ya fue aplicada; si faltan centros, la ejecución normal los
repondrá antes de sincronizar las campañas.
