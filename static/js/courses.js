/**
 * courses.js — Kurs formu Alpine.js komponenti
 * LMS Platform | courses/course_form.html
 *
 * Global funksiyalar:
 *   courseForm() — şəkil önizləmə + drag-drop
 */

window.courseForm = function courseForm() {
    return {
        previewUrl: null,
        dragOver: false,

        handleFileSelect(e) {
            const file = e.target.files[0];
            if (file) this.showPreview(file);
        },

        handleDrop(e) {
            this.dragOver = false;
            const file = e.dataTransfer.files[0];
            if (file && file.type.startsWith('image/')) {
                const input = this.$el.querySelector('input[type=file]');
                const dt = new DataTransfer();
                dt.items.add(file);
                input.files = dt.files;
                this.showPreview(file);
            }
        },

        showPreview(file) {
            const reader = new FileReader();
            reader.onload = (e) => { this.previewUrl = e.target.result; };
            reader.readAsDataURL(file);
        }
    };
};
