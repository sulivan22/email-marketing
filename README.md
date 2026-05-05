# 📧 EmailFlow - Email Marketing Tool

Herramienta moderna y poderosa para enviar newsletters masivas. **Disponible con interfaz web (GUI) o línea de comandos (CLI)**.

## ✨ Características

- ✅ **Interfaz Web Moderna** — Dashboard intuitivo, responsive y atractivo
- ✅ **CLI Tradicional** — Para automatización y scripting
- ✅ **Seguridad Crítica** — Credenciales en `.env`, nunca en el código
- ✅ **Validación Robusta** — Patrones de email mejorados (RFC 5322)
- ✅ **Envío por Lotes** — Configurable para evitar límites de SMTP
- ✅ **Logging Completo** — Timestamps y detalles de cada envío
- ✅ **Manejo de Errores** — SMTP específico y mensajes claros
- ✅ **Vista Previa** — Ve cómo se verá el email antes de enviar
- ✅ **Estadísticas** — Historial completo con tasas de éxito
- ✅ **Flexible** — Todo configurable desde `.env`

## 🚀 Inicio Rápido

Elige tu forma favorita de usar EmailFlow:

### 🎨 Opción 1: Interfaz Web (GUI) - Recomendado

```bash
python3 app.py
```

Luego abre: **http://localhost:5555**

**Características:**
- 📊 Dashboard con estadísticas
- 👁️ Vista previa de emails
- 📤 Envío en background (no bloquea)
- 📜 Historial completo
- 📈 Seguimiento en tiempo real

**Flujo de uso:**
1. Carga tu plantilla HTML
2. Carga tu lista de contactos (TXT)
3. Ajusta configuración de lotes
4. Haz clic en "Ver Previsualización"
5. Revisa el email
6. Haz clic en "Enviar Ahora"
7. Monitorea el progreso

### 💻 Opción 2: Línea de Comandos (CLI) - Para automatización

```bash
python3 enviar_newsletter.py
```

**Para automatizar con cron:**
```bash
crontab -e
# Añade: 0 9 * * * cd /ruta/proyecto && python3 enviar_newsletter.py
```

---

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

## 📁 Estructura del Proyecto

```
email-marketing/
├── app.py                          # Flask app (GUI) ⭐
├── enviar_newsletter.py            # Script CLI
├── log_parser.py                   # Parser de logs
│
├── requirements.txt                # Dependencias Python
├── .env.example                    # Template de configuración
├── .env                            # Tus credenciales (NO en Git ⚠️)
├── .gitignore                      # Protege secretos
│
├── templates/                      # Templates Flask para GUI
│   ├── base.html                   # Layout base
│   ├── index.html                  # Dashboard
│   ├── preview.html                # Vista previa
│   ├── history.html                # Historial
│   └── status.html                 # Estado en tiempo real
│
├── static/                         # Archivos estáticos
│   ├── style.css                   # Estilos modernos
│   └── script.js                   # Interactividad
│
├── uploads/                        # Archivos cargados por GUI
│   ├── templates/                  # Plantillas subidas
│   └── contacts/                   # Contactos subidos
│
├── emails/                         # Plantillas ejemplo
│   ├── app.html
│   ├── newsletter.html
│   ├── newsletter-2.html
│   └── ig.html
│
├── contactos/                      # Listas de contactos ejemplo
│   ├── alboroto.txt
│   └── esimUser.txt
│
├── mails.txt                       # Lista por defecto (CLI)
├── app.html                        # Plantilla por defecto (CLI)
├── enviados.log                    # Log de enviados
├── errores.log                     # Log de errores
│
└── README.md                       # Este archivo
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
