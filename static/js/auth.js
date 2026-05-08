/**
 * auth.js — Qeydiyyat formu Alpine.js komponentləri
 * LMS Platform | auth/register.html
 *
 * Global funksiyalar:
 *   pricingCalc() — həftəlik dərs × 4 × 25 AZN qiymət kalkulyatoru
 */

window.pricingCalc = function pricingCalc() {
    return {
        lessons: 2,
        get monthlyPrice() {
            return this.lessons * 4 * 25;
        },
        setLessons(count) {
            this.lessons = count;
        },
        init() {
            const checked = document.querySelector('input[name="lessons_per_week"]:checked');
            if (checked) this.lessons = parseInt(checked.value);
        }
    };
};

document.addEventListener('DOMContentLoaded', function () {
    const checked = document.querySelector('input[name="course_package"]:checked');
    if (checked && checked.value === 'other') {
        const el = document.querySelector('[x-data]');
        if (el && el.__x) el.__x.$data.selected = 'other';
    }
});
