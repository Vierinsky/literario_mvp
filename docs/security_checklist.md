# Security checklist

## Principios base
- Nunca usar `DEBUG=True` en producción.
- Nunca versionar secretos reales.
- Cargar `SECRET_KEY` desde variables de entorno.
- Configurar `ALLOWED_HOSTS` explícitamente en producción.
- Usar HTTPS en producción.
- Activar `CSRF_COOKIE_SECURE=True` cuando exista HTTPS.
- Activar `SESSION_COOKIE_SECURE=True` cuando exista HTTPS.
- Validar formularios del lado servidor.
- Aplicar rate limiting básico en formularios públicos.
- Mantener dependencias actualizadas.
- Revisar logging y monitoreo de errores.
- Revisar estrategia de backups para base de datos y media.

## Riesgos a vigilar en este proyecto
- abuso de formularios de búsqueda
- abuso de captura de email
- exposición accidental de secretos
- mala calidad de datos por tráfico automatizado
- almacenamiento imprudente de IP o user agent

## Comando para el futuro

Cuando tengas variables y entorno de producción listos, vas a usar:

    python manage.py check --deploy --settings=config.settings.prod

Django indica explícitamente que parte del checklist puede automatizarse con check --deploy y que debe correrse contra el archivo de settings de producción.