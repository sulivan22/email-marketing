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
    # Placeholder: will implement in next task
    return "Preview route"

@app.route('/send', methods=['POST'])
def send():
    # Placeholder: will implement in next task
    return "Send route"

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
