/**
 * bookings.js — Booking Calendar Alpine.js komponenti
 * LMS Platform | bookings/booking_calendar.html
 *
 * Gözlənilən data atributları (bookingCalendar() çağrılanda):
 *   el.dataset.calendarData  — JSON: { "2026-05-08": [{id, start, end}, ...], ... }
 *   el.dataset.availableDates — JSON: ["2026-05-08", ...]
 *   el.dataset.quickBookUrl   — URL string: /bookings/quick-book/
 *   el.dataset.csrfToken      — CSRF token string
 */

window.bookingCalendar = function bookingCalendar() {
    const el = document.querySelector('[data-calendar]');
    const calendarData = el ? JSON.parse(el.dataset.calendarData || '{}') : {};
    const quickBookUrl = el ? el.dataset.quickBookUrl : '';
    const csrfToken = el ? el.dataset.csrfToken : '';

    const azMonths = [
        'Yanvar', 'Fevral', 'Mart', 'Aprel', 'May', 'İyun',
        'İyul', 'Avqust', 'Sentyabr', 'Oktyabr', 'Noyabr', 'Dekabr'
    ];

    return {
        currentDate: new Date(),
        selectedDate: null,
        selectedSlots: [],
        booking: false,
        successMsg: '',
        calendarCells: [],
        dayNames: ['B.e.', 'Ç.a.', 'Ç.', 'C.a.', 'C.', 'Ş.', 'B.'],

        get monthTitle() {
            return azMonths[this.currentDate.getMonth()] + ' ' + this.currentDate.getFullYear();
        },

        get formattedDate() {
            if (!this.selectedDate) return '';
            const parts = this.selectedDate.split('-');
            const d = new Date(parts[0], parts[1] - 1, parts[2]);
            return d.getDate() + ' ' + azMonths[d.getMonth()] + ' ' + d.getFullYear();
        },

        init() {
            this.buildCalendar();
        },

        buildCalendar() {
            const year = this.currentDate.getFullYear();
            const month = this.currentDate.getMonth();
            const firstDay = new Date(year, month, 1);
            const lastDay = new Date(year, month + 1, 0);
            let startDay = (firstDay.getDay() + 6) % 7;
            const today = new Date();
            today.setHours(0, 0, 0, 0);

            this.calendarCells = [];

            const prevLast = new Date(year, month, 0);
            for (let i = startDay - 1; i >= 0; i--) {
                const day = prevLast.getDate() - i;
                const dateStr = this.formatDate(year, month - 1, day);
                this.calendarCells.push({
                    day, dateStr, currentMonth: false, isToday: false,
                    hasSlots: false, slotCount: 0
                });
            }

            for (let day = 1; day <= lastDay.getDate(); day++) {
                const dateStr = this.formatDate(year, month, day);
                const d = new Date(year, month, day);
                d.setHours(0, 0, 0, 0);
                const slots = calendarData[dateStr] || [];
                this.calendarCells.push({
                    day, dateStr, currentMonth: true,
                    isToday: d.getTime() === today.getTime(),
                    hasSlots: slots.length > 0 && d >= today,
                    slotCount: slots.length
                });
            }

            const remaining = 42 - this.calendarCells.length;
            for (let day = 1; day <= remaining; day++) {
                this.calendarCells.push({
                    day, dateStr: '', currentMonth: false, isToday: false,
                    hasSlots: false, slotCount: 0
                });
            }
        },

        formatDate(y, m, d) {
            const dt = new Date(y, m, d);
            const yy = dt.getFullYear();
            const mm = String(dt.getMonth() + 1).padStart(2, '0');
            const dd = String(dt.getDate()).padStart(2, '0');
            return `${yy}-${mm}-${dd}`;
        },

        prevMonth() {
            this.currentDate = new Date(
                this.currentDate.getFullYear(),
                this.currentDate.getMonth() - 1,
                1
            );
            this.buildCalendar();
        },

        nextMonth() {
            this.currentDate = new Date(
                this.currentDate.getFullYear(),
                this.currentDate.getMonth() + 1,
                1
            );
            this.buildCalendar();
        },

        selectDate(dateStr) {
            this.selectedDate = dateStr;
            this.selectedSlots = calendarData[dateStr] || [];
        },

        async bookSlot(slot) {
            this.booking = true;
            try {
                const formData = new FormData();
                formData.append('slot_id', slot.id);
                formData.append('csrfmiddlewaretoken', csrfToken);

                const res = await fetch(quickBookUrl, {
                    method: 'POST',
                    body: formData,
                    headers: { 'X-CSRFToken': csrfToken }
                });

                const data = await res.json();
                if (res.ok && data.success) {
                    this.successMsg = data.message;
                    this.selectedSlots = this.selectedSlots.filter(s => s.id !== slot.id);
                    delete calendarData[this.selectedDate];
                    if (this.selectedSlots.length > 0) {
                        calendarData[this.selectedDate] = this.selectedSlots;
                    }
                    this.buildCalendar();
                } else {
                    alert(data.error || 'Xəta baş verdi');
                }
            } catch (e) {
                alert('Şəbəkə xətası');
            } finally {
                this.booking = false;
            }
        }
    };
};
