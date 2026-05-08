/**
 * support.js — Support ticket səhifəsi skriptləri
 * LMS Platform | support/ticket_detail.html
 */

document.addEventListener('DOMContentLoaded', function () {
    const chatEl = document.getElementById('chat-messages');
    if (chatEl) chatEl.scrollTop = chatEl.scrollHeight;
});
