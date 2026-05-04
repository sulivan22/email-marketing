import os
import subprocess
import re
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max upload
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = os.getenv('SECRET_KEY', 'dev-key-change-in-production')

# Allowed file extensions
ALLOWED_EXTENSIONS = {'txt', 'html'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validar_email(email):
    """Validate email format"""
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(patron, email.strip()))

def read_contacts_from_file(filepath):
    """Read and validate contacts from file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.read().replace('\n', ',')
            contacts = [
                email.strip().strip(',')
                for email in lines.split(',')
                if email.strip() and validar_email(email.strip())
            ]
        return contacts
    except Exception as e:
        return None

def read_html_template(filepath):
    """Read HTML template"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/preview', methods=['POST'])
def preview():
    """Display email preview before sending"""
    try:
        # Get template file
        template_file = request.files.get('template')
        if template_file and template_file.filename:
            # Save uploaded template
            filename = secure_filename(template_file.filename)
            template_path = os.path.join(app.config['UPLOAD_FOLDER'], 'templates', filename)
            template_file.save(template_path)
            html_content = read_html_template(template_path)
        else:
            # Use default template
            template_path = 'app.html'
            html_content = read_html_template(template_path)

        if not html_content:
            return redirect(url_for('index'))

        # Get contacts file
        contacts_file = request.files.get('contacts')
        if contacts_file and contacts_file.filename:
            # Save uploaded contacts
            filename = secure_filename(contacts_file.filename)
            contacts_path = os.path.join(app.config['UPLOAD_FOLDER'], 'contacts', filename)
            contacts_file.save(contacts_path)
            contacts = read_contacts_from_file(contacts_path)
        else:
            # Use default contacts
            contacts_path = 'mails.txt'
            contacts = read_contacts_from_file(contacts_path)

        if not contacts:
            return redirect(url_for('index'))

        # Get batch settings
        batch_size = request.form.get('batchSize', '50')
        batch_delay = request.form.get('batchDelay', '30')

        return render_template('preview.html',
                             html_content=html_content,
                             first_contact=contacts[0],
                             total_contacts=len(contacts),
                             email_from=os.getenv('EMAIL_FROM_ADDRESS', 'travel@esimjourney.com'),
                             email_subject=os.getenv('EMAIL_SUBJECT', 'Stay connected anywhere'),
                             template_path=template_path,
                             contacts_path=contacts_path,
                             batch_size=batch_size,
                             batch_delay=batch_delay)

    except Exception as e:
        return f"Error in preview: {str(e)}", 400

@app.route('/send', methods=['POST'])
def send():
    """Launch email sending in background"""
    try:
        template_path = request.form.get('template_path')
        contacts_path = request.form.get('contacts_path')
        batch_size = request.form.get('batch_size', '50')
        batch_delay = request.form.get('batch_delay', '30')

        # Validate files exist
        if not os.path.exists(template_path) or not os.path.exists(contacts_path):
            return "Files not found", 400

        # Build environment for subprocess
        env = os.environ.copy()
        env['HTML_TEMPLATE_FILE'] = template_path
        env['MAIL_LIST_FILE'] = contacts_path
        env['BATCH_SIZE'] = batch_size
        env['BATCH_DELAY_SECONDS'] = batch_delay

        # Launch subprocess in background (non-blocking)
        subprocess.Popen(
            ['python', 'enviar_newsletter.py'],
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        return redirect(url_for('status'))

    except Exception as e:
        return f"Error launching send: {str(e)}", 500

@app.route('/status')
def status():
    # Placeholder: will implement in next task
    return "Status route"

@app.route('/history')
def history():
    # Placeholder: will implement in next task
    return "History route"

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
