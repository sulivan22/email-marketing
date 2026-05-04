import smtplib
import re
import time
import os
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from datetime import datetime

try:
    from dotenv import load_dotenv
except ImportError:
    print("❌ Error: Se requiere 'python-dotenv'. Instala con: pip install python-dotenv")
    sys.exit(1)

# Cargar variables de entorno desde .env
load_dotenv()

# === CONFIGURACIÓN SMTP (desde variables de entorno) ===
smtp_server = os.getenv("SMTP_SERVER")
smtp_port = int(os.getenv("SMTP_PORT", "587"))
smtp_user = os.getenv("SMTP_USER")
smtp_password = os.getenv("SMTP_PASSWORD")

# Validar que las credenciales estén configuradas
if not all([smtp_server, smtp_user, smtp_password]):
    print("❌ Error: Variables SMTP no configuradas.")
    print("Por favor:")
    print("  1. Copia .env.example a .env")
    print("  2. Completa tus credenciales SMTP en .env")
    print("  3. Nunca compartas tu .env en Git")
    sys.exit(1)

# === VALIDADOR DE EMAILS MEJORADO ===
def validar_email(email):
    """
    Valida un email usando un patrón más robusto.
    RFC 5322 simplificado para casos prácticos.
    """
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(patron, email.strip()))

# === LEER Y LIMPIAR DESTINATARIOS ===
mail_list_file = os.getenv("MAIL_LIST_FILE", "mails.txt")

try:
    with open(mail_list_file, "r", encoding="utf-8") as f:
        lines = f.read().replace("\n", ",")
        all_recipients = [
            email.strip().strip(",")
            for email in lines.split(",")
            if email.strip() and validar_email(email.strip())
        ]

    if not all_recipients:
        print(f"❌ Error: No se encontraron emails válidos en {mail_list_file}")
        sys.exit(1)

    print(f"✅ Se cargaron {len(all_recipients)} emails válidos")
except FileNotFoundError:
    print(f"❌ Error: Archivo {mail_list_file} no encontrado")
    sys.exit(1)

# === LEER CONTENIDO HTML ===
html_template_file = os.getenv("HTML_TEMPLATE_FILE", "app.html")

try:
    with open(html_template_file, "r", encoding="utf-8") as f:
        html_content = f.read()
    print(f"✅ Plantilla cargada: {html_template_file}")
except FileNotFoundError:
    print(f"❌ Error: Archivo {html_template_file} no encontrado")
    sys.exit(1)

# === FUNCIONES AUXILIARES ===
def dividir_en_bloques(lista, tamano):
    for i in range(0, len(lista), tamano):
        yield lista[i:i + tamano]

def registrar(mensaje, nivel="INFO"):
    """Registra mensajes con timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    prefijo = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️"}
    print(f"[{timestamp}] {prefijo.get(nivel, '•')} {mensaje}")

# === CONFIGURACIÓN DEL CORREO ===
email_from_name = os.getenv("EMAIL_FROM_NAME", "eSimJourney.com")
email_from_address = os.getenv("EMAIL_FROM_ADDRESS", "travel@esimjourney.com")
email_subject = os.getenv("EMAIL_SUBJECT", "Stay connected anywhere — Download the app today")
batch_size = int(os.getenv("BATCH_SIZE", "50"))
batch_delay = int(os.getenv("BATCH_DELAY_SECONDS", "30"))

# === ENVÍO POR BLOQUES ===
enviados = []
fallidos = []

try:
    registrar("Conectando a servidor SMTP...", "INFO")
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)
    registrar("Conexión SMTP exitosa", "SUCCESS")

    total_bloques = (len(all_recipients) + batch_size - 1) // batch_size
    bloque_num = 1

    for bloque in dividir_en_bloques(all_recipients, batch_size):
        msg = MIMEMultipart("alternative")
        msg["Subject"] = Header(email_subject, "utf-8")
        msg["From"] = f"{email_from_name} <{email_from_address}>"
        msg["To"] = email_from_address

        html_part = MIMEText(html_content, "html", "utf-8")
        msg.attach(html_part)

        try:
            server.sendmail(smtp_user, bloque + [smtp_user], msg.as_string())
            enviados.extend(bloque)
            registrar(f"Bloque {bloque_num}/{total_bloques}: Enviados {len(bloque)} correos", "SUCCESS")
        except Exception as e:
            fallidos.extend(bloque)
            registrar(f"Bloque {bloque_num}/{total_bloques}: Error - {str(e)}", "ERROR")

        if bloque_num < total_bloques:
            registrar(f"Esperando {batch_delay}s antes del siguiente bloque...", "INFO")
            time.sleep(batch_delay)

        bloque_num += 1

    server.quit()
    registrar("Conexión SMTP cerrada", "INFO")

except smtplib.SMTPException as e:
    registrar(f"Error SMTP: {str(e)}", "ERROR")
    fallidos.extend(all_recipients)
except Exception as e:
    registrar(f"Error inesperado: {str(e)}", "ERROR")
    fallidos.extend(all_recipients)

# === GUARDAR LOGS ===
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

try:
    with open("enviados.log", "a", encoding="utf-8") as f:
        if enviados:
            f.write(f"\n--- Envío {timestamp} ---\n")
            f.write("\n".join(enviados))
            f.write("\n")

    with open("errores.log", "a", encoding="utf-8") as f:
        if fallidos:
            f.write(f"\n--- Errores {timestamp} ---\n")
            f.write("\n".join(fallidos))
            f.write("\n")

    # Resumen final
    print("\n" + "="*50)
    registrar(f"Envío completado", "SUCCESS")
    registrar(f"Total enviados: {len(enviados)}", "SUCCESS")
    registrar(f"Total fallidos: {len(fallidos)}", "WARNING" if fallidos else "SUCCESS")
    print("="*50)

except Exception as e:
    registrar(f"Error al guardar logs: {str(e)}", "ERROR")