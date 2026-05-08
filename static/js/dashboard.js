/**
 * dashboard.js — Dashboard Alpine.js komponentləri
 * LMS Platform | analytics/dashboard.html + student_dashboard.html
 *
 * Global funksiyalar:
 *   liveClock()  — real-time saat + tarix
 *   counter(val) — animasiyalı KPI sayğac
 */

window.liveClock = function liveClock() {
    const m = ['Yan', 'Fev', 'Mar', 'Apr', 'May', 'İyn', 'İyl', 'Avq', 'Sen', 'Okt', 'Noy', 'Dek'];
    return {
        time: '',
        date: '',
        start() {
            this.tick();
            setInterval(() => this.tick(), 1000);
        },
        tick() {
            const n = new Date();
            this.time = n.toLocaleTimeString('az-AZ', {
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            });
            this.date = n.getDate() + ' ' + m[n.getMonth()] + ' ' + n.getFullYear();
        }
    };
};

window.counter = function counter(target) {
    return {
        display: '0',
        init() {
            const t = parseInt(target) || 0;
            if (!t) { this.display = '0'; return; }
            const dur = 500, st = performance.now();
            const go = (ts) => {
                const p = Math.min((ts - st) / dur, 1);
                this.display = Math.round((1 - Math.pow(1 - p, 3)) * t).toLocaleString('az-AZ');
                if (p < 1) requestAnimationFrame(go);
            };
            requestAnimationFrame(go);
        }
    };
};
