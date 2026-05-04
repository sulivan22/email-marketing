# Email Marketing Newsletter

Herramienta segura y configurable para enviar campañas de email masivo mediante SMTP.

## Características

- ✅ **Seguridad Crítica:** Credenciales en `.env`, nunca en el código
- ✅ **Validación Robusta:** Patrones de email mejorados (RFC 5322)
- ✅ **Envío por Lotes:** Configurable para evitar límites de SMTP
- ✅ **Logging Completo:** Timestamps y detalles de cada envío
- ✅ **Manejo de Errores:** SMTP específico y mensajes claros
- ✅ **Flexible:** Todo configurable desde `.env`

## Instalación Rápida

### 1. Clonar el repositorio
```bash
git clone https://github.com/sulivan22/email-marketing.git
cd email-marketing
```

### 2. Crear virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
python3 -m pip install -r requirements.txt
```

### 4. Configurar credenciales
```bash
cp .env.example .env
# Edita .env con tus credenciales SMTP
```

### 5. Ejecutar
```bash
python3 enviar_newsletter.py
```

## Estructura del Proyecto

```
email-marketing/
├── enviar_newsletter.py      # Script principal
├── .env.example              # Template de configuración
├── .env                       # Tus credenciales (NO en Git ⚠️)
├── .gitignore                # Protege secretos
├── requirements.txt          # Dependencias Python
├── SETUP.md                  # Guía detallada de setup
├── app.html                  # Plantilla HTML principal
├── emails/                   # Plantillas HTML adicionales
│   ├── newsletter.html
├── contactos/                # Listas de contactos
│   ├── campaña1.txt
│   └── campaña2.txt
└── mails.txt                 # Destinatarios actuales
```

## Configuración

Todos los parámetros se configuran en `.env`:

```ini
# SMTP
SMTP_SERVER=mail.tudominio.com
SMTP_PORT=587
SMTP_USER=tu_email@tudominio.com
SMTP_PASSWORD=tu_contraseña

# Correo
EMAIL_FROM_NAME=Tu Nombre
EMAIL_FROM_ADDRESS=email@tudominio.com
EMAIL_SUBJECT=Tu Asunto

# Archivos
MAIL_LIST_FILE=mails.txt
HTML_TEMPLATE_FILE=app.html

# Envío
BATCH_SIZE=50              # Emails por bloque
BATCH_DELAY_SECONDS=30     # Pausa entre bloques
```

## Uso

### Envío básico
```bash
python3 enviar_newsletter.py
```

### Output esperado
```
✅ Se cargaron 1500 emails válidos
✅ Plantilla cargada: app.html
[2026-05-04 12:01:37] ℹ️ Conectando a servidor SMTP...
[2026-05-04 12:01:39] ✅ Conexión SMTP exitosa
[2026-05-04 12:01:42] ✅ Bloque 1/30: Enviados 50 correos
...
[2026-05-04 12:15:30] ✅ Envío completado
[2026-05-04 12:15:30] ✅ Total enviados: 1500
[2026-05-04 12:15:30] ✅ Total fallidos: 0
```

## Logs

- **enviados.log** — Emails enviados exitosamente (acumulativo)
- **errores.log** — Emails que fallaron (acumulativo)

Ambos logs incluyen timestamps para auditoría.

## Seguridad

### ⚠️ IMPORTANTE

**NUNCA:**
- ❌ Hagas commit de `.env` a Git
- ❌ Compartas credenciales en repositorios públicos
- ❌ Guardes contraseñas en código

**SIEMPRE:**
- ✅ Usa `.env.example` como template
- ✅ Copia a `.env` localmente
- ✅ Verifica que `.env` está en `.gitignore`
- ✅ Usa variables de entorno para secretos

## Mejoras Futuras

- [ ] Retry logic para fallos temporales
- [ ] CLI interactivo para elegir plantilla y lista
- [ ] Soporte para CSV además de TXT
- [ ] Estadísticas detalladas de envío
- [ ] Integración con webhooks

## Requisitos

- Python 3.7+
- SMTP válido (Outlook, Gmail, Zoho, etc.)
- Lista de emails en formato TXT

## Licencia

MIT

## Soporte

Para problemas o sugerencias, abre un issue en GitHub.

---

**Última actualización:** 2026-05-04
