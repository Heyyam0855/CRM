package com.lms.app.ui.notifications

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.lms.app.data.api.NotificationApi
import com.lms.app.data.model.NotificationResponse
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class NotificationViewModel @Inject constructor(
    private val notificationApi: NotificationApi
) : ViewModel() {

    private val _notifications = MutableLiveData<List<NotificationResponse>>(emptyList())
    val notifications: LiveData<List<NotificationResponse>> = _notifications

    private val _unreadCount = MutableLiveData(0)
    val unreadCount: LiveData<Int> = _unreadCount

    private val _isLoading = MutableLiveData(false)
    val isLoading: LiveData<Boolean> = _isLoading

    fun loadNotifications() {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val response = notificationApi.getNotifications()
                if (response.isSuccessful) {
                    val list = response.body() ?: emptyList()
                    _notifications.value = list
                    _unreadCount.value = list.count { !it.isRead }
                }
            } catch (e: java.net.UnknownHostException) {
                // Offline — sessiz xəta
            } catch (e: Exception) {
                // Sessiz xəta — bildiriş kritik deyil
            } finally {
                _isLoading.value = false
            }
        }
    }

    fun markAsRead(id: String) {
        viewModelScope.launch {
            try {
                notificationApi.markAsRead(id)
                // Lokal state-i dərhal yenilə
                val updated = _notifications.value?.map {
                    if (it.id == id) it.copy(isRead = true) else it
                } ?: emptyList()
                _notifications.value = updated
                _unreadCount.value = updated.count { !it.isRead }
            } catch (e: Exception) {
                // Sessiz xəta
            }
        }
    }

    fun markAllAsRead() {
        viewModelScope.launch {
            _notifications.value?.forEach { notif ->
                if (!notif.isRead) {
                    try { notificationApi.markAsRead(notif.id) } catch (e: Exception) { }
                }
            }
            val updated = _notifications.value?.map { it.copy(isRead = true) } ?: emptyList()
            _notifications.value = updated
            _unreadCount.value = 0
        }
    }
}

