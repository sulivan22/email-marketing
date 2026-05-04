# Setup de Seguridad

## Paso 1: Instalar dependencias

```bash
pip install -r requirements.txt
```

## Paso 2: Crear archivo .env con tus credenciales

```bash
cp .env.example .env
```

Edita `.env` y completa tus credenciales SMTP:

```ini
SMTP_SERVER=mail.tudominio.com
SMTP_PORT=587
SMTP_USER=tu_email@tudominio.com
SMTP_PASSWORD=tu_contraseña_segura
EMAIL_FROM_NAME=Tu Nombre
EMAIL_FROM_ADDRESS=email@tudominio.com
EMAIL_SUBJECT=Tu Asunto
```

## Paso 3: Verificar que .env está protegido

El archivo `.env` está en `.gitignore`, así que **no se subirá a Git**:

```bash
# Verificar que Git ignora .env
git status
# No debe aparecer .env en la lista
```

## Paso 4: Usar el script

```bash
python3 enviar_newsletter.py
```

El script:
- ✅ Lee credenciales seguras de `.env`
- ✅ Valida todos los emails antes de enviar
- ✅ Registra cada bloque con timestamp
- ✅ Acumula logs (no los sobrescribe)

## Seguridad en Git

Nunca:
- ❌ Hagas `git add .env`
- ❌ Compartas el archivo `.env`
- ❌ Pushs credenciales al repositorio
- ❌ Guardes contraseñas en comentarios del código

Siempre:
- ✅ Usa `.env.example` como template
- ✅ Copia `.env.example` a `.env` localmente
- ✅ Mantén `.env` en `.gitignore`
- ✅ Usa variables de entorno para secretos
