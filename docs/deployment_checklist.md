# Deployment checklist

## Antes del deploy
- Confirmar que producción use `config.settings.prod`.
- Confirmar `DEBUG=False`.
- Confirmar `SECRET_KEY` por variable de entorno.
- Confirmar `ALLOWED_HOSTS`.
- Confirmar credenciales de base de datos por variables de entorno.
- Confirmar configuración de email si aplica.
- Definir `STATIC_ROOT`.
- Ejecutar migraciones.
- Ejecutar `collectstatic`.
- Ejecutar chequeo de despliegue:
  - `python manage.py check --deploy --settings=config.settings.prod`

## Servidor
- No usar `runserver` en producción.
- Usar servidor WSGI o ASGI real.
- Verificar HTTPS.
- Verificar logging.
- Verificar páginas de error.

## Comando para el futuro

Cuando tengas variables y entorno de producción listos, vas a usar:

    python manage.py check --deploy --settings=config.settings.prod

Django indica explícitamente que parte del checklist puede automatizarse con check --deploy y que debe correrse contra el archivo de settings de producción.