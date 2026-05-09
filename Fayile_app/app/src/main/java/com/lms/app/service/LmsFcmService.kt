package com.lms.app.service

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.os.Build
import androidx.core.app.NotificationCompat
import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage
import com.lms.app.R
import com.lms.app.ui.MainActivity

/**
 * Firebase Cloud Messaging servisi.
 * Django backend-dən gələn push bildirişlərini idarə edir.
 *
 * Bildiriş növləri (README_1.md-dən):
 * - BOOKING_CONFIRMED
 * - LESSON_REMINDER
 * - PAYMENT_DUE
 * - REPO_CREATED
 * - GENERAL
 */
class LmsFcmService : FirebaseMessagingService() {

    companion object {
        const val CHANNEL_ID = "lms_notifications"
        const val CHANNEL_NAME = "LMS Bildirişlər"
    }

    override fun onNewToken(token: String) {
        super.onNewToken(token)
        // Yeni FCM token → /api/v1/users/fcm-token/ endpointinə göndər
        saveTokenToPrefs(token)
    }

    override fun onMessageReceived(message: RemoteMessage) {
        super.onMessageReceived(message)

        val title = message.notification?.title ?: message.data["title"] ?: "LMS"
        val body = message.notification?.body ?: message.data["message"] ?: ""
        val notifType = message.data["notification_type"] ?: "GENERAL"

        showNotification(title, body, notifType)
    }

    private fun showNotification(title: String, body: String, type: String) {
        createNotificationChannel()

        val intent = Intent(this, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_CLEAR_TOP
            putExtra("notification_type", type)
        }

        val pendingIntent = PendingIntent.getActivity(
            this, 0, intent,
            PendingIntent.FLAG_ONE_SHOT or PendingIntent.FLAG_IMMUTABLE
        )

        val notification = NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle(title)
            .setContentText(body)
            .setSmallIcon(R.drawable.ic_notification)
            .setAutoCancel(true)
            .setContentIntent(pendingIntent)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .build()

        val manager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        manager.notify(System.currentTimeMillis().toInt(), notification)
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                CHANNEL_NAME,
                NotificationManager.IMPORTANCE_HIGH
            )
            val manager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            manager.createNotificationChannel(channel)
        }
    }

    private fun saveTokenToPrefs(token: String) {
        val prefs = getSharedPreferences("lms_secure_prefs", Context.MODE_PRIVATE)
        prefs.edit().putString("fcm_token", token).apply()
    }
}

