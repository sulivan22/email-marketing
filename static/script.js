// ===== FORM VALIDATION & INTERACTION =====
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const buttons = form.querySelectorAll('button');
            buttons.forEach(btn => {
                btn.style.opacity = '0.6';
                btn.style.pointerEvents = 'none';
            });
        });
    });
});

// ===== AUTO-HIDE ERRORS =====
function autoHideErrors() {
    const errorBoxes = document.querySelectorAll('.error-box');
    errorBoxes.forEach(box => {
        if (box.style.display !== 'none') {
            setTimeout(() => {
                box.style.opacity = '0';
                box.style.transform = 'translateY(-10px)';
                setTimeout(() => {
                    box.style.display = 'none';
                }, 300);
            }, 5000);
        }
    });
}

document.addEventListener('DOMContentLoaded', autoHideErrors);

// ===== FILE INPUT ENHANCEMENTS =====
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

document.addEventListener('DOMContentLoaded', function() {
    const fileInputs = document.querySelectorAll('input[type="file"]');

    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const file = this.files[0];
                const label = this.parentElement.querySelector('label');
                if (label) {
                    label.innerHTML = `
                        <span>📎</span> ${file.name}
                        <small style="display: block; margin-top: 0.25rem;">
                            Tamaño: ${formatFileSize(file.size)}
                        </small>
                    `;
                    label.style.color = 'var(--success-color)';
                    label.style.fontWeight = '600';
                }
            }
        });
    });
});

// ===== PREVENT ACCIDENTAL FORM RESUBMISSION =====
function disableFormOnSubmit(form) {
    form.addEventListener('submit', function() {
        const buttons = form.querySelectorAll('button');
        buttons.forEach(btn => {
            btn.disabled = true;
            btn.textContent = '⏳ Procesando...';
            btn.style.opacity = '0.7';
        });
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(disableFormOnSubmit);
});

// ===== SMOOTH PAGE TRANSITIONS =====
function addPageTransition() {
    const links = document.querySelectorAll('a[href^="/"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (!href.includes('#') && !href.startsWith('javascript:')) {
                e.preventDefault();
                document.body.style.opacity = '0.95';
                document.body.style.transform = 'translateY(5px)';
                setTimeout(() => {
                    window.location.href = href;
                }, 150);
            }
        });
    });
}

document.addEventListener('DOMContentLoaded', addPageTransition);

// ===== TABLE ROW HOVER EFFECT =====
document.addEventListener('DOMContentLoaded', function() {
    const rows = document.querySelectorAll('.history-table tbody tr');
    rows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.01)';
        });

        row.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
});

// ===== KEYBOARD SHORTCUTS =====
document.addEventListener('keydown', function(e) {
    // Alt+H: Go to Dashboard
    if (e.altKey && e.key === 'h') {
        window.location.href = '/';
    }
    // Alt+L: Go to History
    if (e.altKey && e.key === 'l') {
        window.location.href = '/history';
    }
});

// ===== STATS ANIMATION =====
function animateStats() {
    const statValues = document.querySelectorAll('.stat-value');
    statValues.forEach((stat, index) => {
        stat.style.animation = `fadeIn 0.6s ease ${index * 0.1}s forwards`;
        stat.style.opacity = '0';
    });
}

document.addEventListener('DOMContentLoaded', animateStats);
