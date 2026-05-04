# Flask Web Interface Implementation Plan

> **Para trabajadores agentivos:** REQUERIDO: Usar superpowers:subagent-driven-development (recomendado) o superpowers:executing-plans para implementar este plan tarea por tarea. Los pasos usan sintaxis de checkbox (`- [ ]`) para rastrear progreso.

**Objetivo:** Construir una interfaz web Flask para el script de marketing por email que permita cargar plantillas/contactos, previsualizar emails, enviar en background y ver estadísticas desde logs.

**Arquitectura:** App Flask sirve templates HTML y maneja cargas de archivos. Las rutas llaman a `enviar_newsletter.py` como subprocess en background. El log parser lee `enviados.log` y `errores.log` existentes para mostrar estadísticas. Sin base de datos, sin APIs externas.

**Tech Stack:** Flask, Jinja2 templates, HTML/CSS/JS vanilla, módulo subprocess de Python, regex para parsing de logs

---

## Estructura de Archivos

```
EMAILMARKETING/
├── app.py                          # App Flask principal (nuevo)
├── requirements.txt                # Actualizado: +Flask
│
├── templates/                      # Templates Flask (nuevo)
│   ├── base.html
│   ├── index.html
│   ├── preview.html
│   └── history.html
│
├── static/                         # CSS/JS (nuevo)
│   ├── style.css
│   └── script.js
│
├── uploads/                        # Archivos cargados (nuevo)
│   ├── templates/                  # .gitkeep solo
│   └── contacts/                   # .gitkeep solo
│
└── log_parser.py                   # Utilidad log parsing (nueva)
```

---

## Tareas

### Tarea 1: Actualizar `requirements.txt`

**Archivos:**
- Modificar: `requirements.txt`

- [ ] **Paso 1:** Agregar Flask a requirements
- [ ] **Paso 2:** Verificar cambio
- [ ] **Paso 3:** Instalar Flask
- [ ] **Paso 4:** Commit

### Tarea 2: Crear estructura de directorios

**Archivos:**
- Crear: `uploads/templates/.gitkeep`
- Crear: `uploads/contacts/.gitkeep`

- [ ] **Paso 1:** Crear directorio uploads
- [ ] **Paso 2:** Crear archivos .gitkeep
- [ ] **Paso 3:** Verificar estructura
- [ ] **Paso 4:** Commit

### Tarea 3: Crear `app.py` (Flask app principal)

**Archivos:**
- Crear: `app.py`

- [ ] **Paso 1:** Escribir app.py con estructura base
- [ ] **Paso 2:** Verificar sintaxis
- [ ] **Paso 3:** Test de startup
- [ ] **Paso 4:** Commit

### Tarea 4: Crear utilidad `log_parser.py`

**Archivos:**
- Crear: `log_parser.py`

- [ ] **Paso 1:** Escribir log_parser.py
- [ ] **Paso 2:** Test log parser
- [ ] **Paso 3:** Commit

### Tarea 5: Crear template base `templates/base.html`

**Archivos:**
- Crear: `templates/base.html`

- [ ] **Paso 1:** Crear directorio templates
- [ ] **Paso 2:** Escribir base.html
- [ ] **Paso 3:** Verificar archivo
- [ ] **Paso 4:** Commit

### Tarea 6: Crear dashboard template `templates/index.html`

**Archivos:**
- Crear: `templates/index.html`

- [ ] **Paso 1:** Escribir index.html
- [ ] **Paso 2:** Verificar archivo
- [ ] **Paso 3:** Commit

### Tarea 7: Crear template preview `templates/preview.html`

**Archivos:**
- Crear: `templates/preview.html`

- [ ] **Paso 1:** Escribir preview.html
- [ ] **Paso 2:** Verificar archivo
- [ ] **Paso 3:** Commit

### Tarea 8: Crear template history `templates/history.html`

**Archivos:**
- Crear: `templates/history.html`

- [ ] **Paso 1:** Escribir history.html
- [ ] **Paso 2:** Verificar archivo
- [ ] **Paso 3:** Commit

### Tarea 9: Implementar ruta preview y otras rutas principales

**Archivos:**
- Modificar: `app.py`

- [ ] **Paso 1:** Reemplazar ruta preview
- [ ] **Paso 2:** Test sintaxis
- [ ] **Paso 3:** Commit

### Tarea 10: Implementar ruta send (subprocess background)

**Archivos:**
- Modificar: `app.py`

- [ ] **Paso 1:** Reemplazar ruta send
- [ ] **Paso 2:** Test sintaxis
- [ ] **Paso 3:** Commit

### Tarea 11: Implementar ruta status

**Archivos:**
- Crear: `templates/status.html`
- Modificar: `app.py`

- [ ] **Paso 1:** Crear status.html
- [ ] **Paso 2:** Agregar ruta status a app.py
- [ ] **Paso 3:** Test sintaxis
- [ ] **Paso 4:** Commit

### Tarea 12: Implementar ruta history y stats

**Archivos:**
- Modificar: `app.py`

- [ ] **Paso 1:** Reemplazar ruta history
- [ ] **Paso 2:** Test sintaxis
- [ ] **Paso 3:** Commit

### Tarea 13: Crear CSS stylesheet `static/style.css`

**Archivos:**
- Crear: `static/style.css`

- [ ] **Paso 1:** Crear directorio static
- [ ] **Paso 2:** Escribir style.css
- [ ] **Paso 3:** Verificar archivo
- [ ] **Paso 4:** Commit

### Tarea 14: Crear JavaScript `static/script.js`

**Archivos:**
- Crear: `static/script.js`

- [ ] **Paso 1:** Escribir script.js
- [ ] **Paso 2:** Verificar archivo
- [ ] **Paso 3:** Commit

### Tarea 15: Test de app e integración final

**Archivos:**
- Ninguno (testing solo)

- [ ] **Paso 1:** Iniciar Flask app
- [ ] **Paso 2:** Test home page
- [ ] **Paso 3:** Test history route
- [ ] **Paso 4:** Test API stats endpoint
- [ ] **Paso 5:** Abrir browser y verificar localhost:5000
- [ ] **Paso 6:** Detener Flask app
- [ ] **Paso 7:** Commit final
