// Form validation
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Basic validation
            const templateInput = form.querySelector('input[name="template"]');
            const contactsInput = form.querySelector('input[name="contacts"]');

            // At least one file can be empty (uses defaults)
            // But we could add more validation here if needed

            console.log('Form submitted');
        });
    });
});

// Auto-hide error messages after 5 seconds
function autoHideErrors() {
    const errorBoxes = document.querySelectorAll('.error-box');
    errorBoxes.forEach(box => {
        if (box.style.display !== 'none') {
            setTimeout(() => {
                box.style.display = 'none';
            }, 5000);
        }
    });
}

// Call on page load
document.addEventListener('DOMContentLoaded', autoHideErrors);

// Utility: Format file size for display
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// File input labels with file size
document.addEventListener('DOMContentLoaded', function() {
    const fileInputs = document.querySelectorAll('input[type="file"]');

    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const file = this.files[0];
                const sizeText = ' (' + formatFileSize(file.size) + ')';
                console.log('File selected: ' + file.name + sizeText);
            }
        });
    });
});

// Prevent accidental form resubmission
function disableFormOnSubmit(form) {
    form.addEventListener('submit', function() {
        const buttons = form.querySelectorAll('button');
        buttons.forEach(btn => {
            btn.disabled = true;
            btn.textContent = 'Processing...';
        });
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(disableFormOnSubmit);
});
