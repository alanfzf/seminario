# Proyecto bomberos voluntarios

## TODO
- [X] [Empaquetar la aplicación](https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/)
- [X] Crear worker para realizar guardado de la base de datos

## Setup

```bash
# Debemos de crear el archivo .env

# Aquí se debe colocar la secret key que le servirá a Django.
SECRET_KEY=CHANGE_ME
# Aquí debemos de indicar que el servidor a lanzar no estará en modo de desarrollo.
DEBUG=FALSE
```

```bash
# Ejecutar los siguientes comandos
docker compose exec web python manage.py collectstatic
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
docker compose exec web python manage.py create_default_groups
```

## Backups

```bash
# Dar permisos al script
chmod ugo+rwx ./backup.sh

# Crear carpeta de logs y backups
mkdir -p ~/backups/logs

# Agregar el script de backup al cron
crontab -e

# Editar el archivo, (aquí se ejecutaría cada día el backup a las 11 AM)
0 11 * * * ~/sistema-reportes-ambulancias/backup.sh >> ~/backups/logs/backup_logs.log 2>&1
#- - - - -
#| | | | |
#| | | | +-- Day of the week (0 - 7) [Both 0 and 7 represent Sunday]
#| | | +---- Month (1 - 12)
#| | +------ Day of the month (1 - 31)
#| +-------- Hour (0 - 23)
#+---------- Minute (0 - 59)
```

# Integrantes
- Alan David González López
- José Raúl Botzoc Mérida
- Manuel Miguel Miguel.
