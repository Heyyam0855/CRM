/**
 * notifications.js — WebSocket real-time bildiriş sistemi
 * LMS Platform | base.html tərəfindən yüklənir
 */
(function () {
    const wsProtocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const notificationSocket = new WebSocket(
        `${wsProtocol}://${window.location.host}/ws/notifications/`
    );

    notificationSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        if (data.type === 'unread_count') {
            const badge = document.getElementById('notification-badge');
            if (badge) {
                badge.textContent = data.count > 0 ? data.count : '';
                badge.style.display = data.count > 0 ? 'flex' : 'none';
            }
        } else if (data.type === 'notification') {
            window.dispatchEvent(
                new CustomEvent('notify', { detail: { message: data.message } })
            );
        }
    };
})();
