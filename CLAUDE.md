# CLAUDE.md

Este archivo proporciona orientación a Claude Code (claude.ai/code) al trabajar con código en este repositorio.

## Descripción General del Proyecto

Esta es una herramienta de marketing por correo electrónico masivo escrita en Python que envía boletines a listas de contactos utilizando SMTP. El script principal procesa destinatarios de correo electrónico desde archivos de texto y envía correos electrónicos con formato HTML en lotes.

## Distribución de Modelos Claude

Para optimizar tokens y velocidad, usa la siguiente estrategia:

### Haiku 4.5 — Tareas rápidas y sencillas
- Validar direcciones de email (regex, formato)
- Buscar/filtrar contactos en `contactos/` o `mails.txt`
- Responder preguntas puntuales sobre logs
- Contar líneas, verificar duplicados
- Procesar lotes pequeños de datos

### Sonnet 4.6 — Lógica, código y mejoras
- Escribir/refactorizar `enviar_newsletter.py`
- Crear/optimizar plantillas HTML en `emails/`
- Implementar nuevas features (rate limiting, retry logic, etc.)
- Debugging y troubleshooting
- Decisiones de arquitectura normales

### Opus 4.6 — NO usar (innecesario)
- Este proyecto no requiere revisión crítica de arquitectura
- Sonnet es suficiente para todas las decisiones

---

## Archivos y Directorios Clave

- **enviar_newsletter.py** — Script principal que gestiona la conexión SMTP, envío de correos y registro de eventos
- **app.html** — Plantilla HTML principal utilizada para el contenido del boletín
- **emails/** — Directorio que contiene plantillas HTML alternativas (newsletter.html, newsletter-2.html, ig.html)
- **contactos/** — Directorio con listas de contactos (alboroto.txt, esimUser.txt)
- **mails.txt** — Lista actual de destinatarios de correo electrónico (utilizada por el script)
- **enviados.log** — Registro de direcciones de correo electrónico enviadas exitosamente
- **errores.log** — Registro de direcciones de correo electrónico que fallaron
- **REDME.txt** — Referencia rápida para ejecutar el script

## Instalación y Configuración

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar credenciales
```bash
# Copiar el template de variables de entorno
cp .env.example .env

# Editar .env con tus credenciales SMTP
nano .env  # o tu editor preferido
```

**⚠️ IMPORTANTE:** Nunca compartas el archivo `.env` o subas credenciales a Git. El archivo está en `.gitignore`.

## Ejecución del Script

```bash
python3 enviar_newsletter.py
```

El script:
1. Lee direcciones de correo electrónico de `mails.txt` (separadas por comas o saltos de línea)
2. Valida correos electrónicos utilizando el patrón regex `[^@]+@[^@]+\.[^@]+`
3. Carga contenido HTML de `app.html`
4. Envía correos electrónicos en bloques de 50 destinatarios
5. Pausa 30 segundos entre bloques para evitar límites de velocidad SMTP
6. Registra resultados en `enviados.log` y `errores.log`

## Configuración de Correo Electrónico

El script lee todas las configuraciones del archivo `.env`:

```ini
SMTP_SERVER=mail.privateemail.com
SMTP_PORT=587
SMTP_USER=tu_email@ejemplo.com
SMTP_PASSWORD=tu_contraseña
EMAIL_FROM_NAME=eSimJourney.com
EMAIL_FROM_ADDRESS=travel@esimjourney.com
EMAIL_SUBJECT=Stay connected anywhere — Download the app today
```

Las credenciales están **completamente separadas del código** en variables de entorno (nunca en Git).

## Estructura de Directorios
.
├── enviar_newsletter.py      # Script principal
├── app.html                  # Plantilla de correo primaria
├── mails.txt                 # Lista de destinatarios actual
├── enviados.log              # Registro de correos enviados
├── errores.log               # Registro de correos fallidos
├── contactos/                # Archivos de listas de contactos
│   ├── alboroto.txt
│   └── esimUser.txt
└── emails/                   # Plantillas HTML adicionales
├── newsletter.html
├── newsletter-2.html
└── ig.html

## Mejoras de Seguridad Implementadas

- ✅ **Credenciales en `.env`** — No están en el código fuente
- ✅ **Validación de emails robusta** — Patrón RFC 5322 simplificado
- ✅ **`.gitignore`** — Previene que `.env` se suba accidentalmente
- ✅ **Manejo de errores mejorado** — Errores SMTP específicos y detallados
- ✅ **Logging con timestamps** — Seguimiento completo de cada envío

## Notas Importantes

- Los correos electrónicos se envían en lotes (configurables) para evitar sobrecargar el servidor SMTP
- Las pausas entre lotes (configurables) permiten que el servidor de correo procese
- Todos los parámetros pueden personalizarse desde el archivo `.env`
- El contenido HTML se incrusta directamente (no como adjunto)
- Los logs son **acumulativos** (se añaden con timestamp, no se sobrescriben)

## Mejoras Futuras

- [ ] Mover credenciales SMTP a `.env`
- [ ] Implementar retry logic para fallos temporales
- [ ] Agregar CLI para seleccionar template
- [ ] Soportar CSV además de TXT
- [ ] Agregar estadísticas (tasa de error, tiempo total)