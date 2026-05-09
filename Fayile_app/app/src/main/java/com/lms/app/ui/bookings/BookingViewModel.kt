package com.lms.app.ui.bookings

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.lms.app.data.api.BookingApi
import com.lms.app.data.model.BookingResponse
import com.lms.app.data.model.BookingCreateRequest
import com.lms.app.data.model.SlotResponse
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class BookingViewModel @Inject constructor(
    private val bookingApi: BookingApi
) : ViewModel() {

    private val _bookings = MutableLiveData<List<BookingResponse>>(emptyList())
    val bookings: LiveData<List<BookingResponse>> = _bookings

    private val _slots = MutableLiveData<List<SlotResponse>>(emptyList())
    val slots: LiveData<List<SlotResponse>> = _slots

    private val _isLoading = MutableLiveData(false)
    val isLoading: LiveData<Boolean> = _isLoading

    private val _error = MutableLiveData<String?>(null)
    val error: LiveData<String?> = _error

    private val _bookingSuccess = MutableLiveData(false)
    val bookingSuccess: LiveData<Boolean> = _bookingSuccess

    fun loadMyBookings() {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val response = bookingApi.getMyBookings()
                if (response.isSuccessful) {
                    _bookings.value = response.body() ?: emptyList()
                } else {
                    _error.value = "Dərslər yüklənmədi (${response.code()})"
                }
            } catch (e: java.net.UnknownHostException) {
                _error.value = "İnternet bağlantısı yoxdur"
            } catch (e: java.net.SocketTimeoutException) {
                _error.value = "Server cavab vermir"
            } catch (e: Exception) {
                _error.value = "Xəta: ${e.localizedMessage}"
            } finally {
                _isLoading.value = false
            }
        }
    }

    fun loadAvailableSlots() {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val response = bookingApi.getAvailableSlots()
                if (response.isSuccessful) {
                    _slots.value = response.body()
                        ?.filter { !it.isReserved } ?: emptyList()
                } else {
                    _error.value = "Slotlar yüklənmədi (${response.code()})"
                }
            } catch (e: java.net.UnknownHostException) {
                _error.value = "İnternet bağlantısı yoxdur"
            } catch (e: Exception) {
                _error.value = "Xəta: ${e.localizedMessage}"
            } finally {
                _isLoading.value = false
            }
        }
    }

    fun createBooking(slotId: String, lessonType: String, topic: String) {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val request = BookingCreateRequest(
                    slotId = slotId,
                    lessonType = lessonType,
                    topic = topic
                )
                val response = bookingApi.createBooking(request)
                if (response.isSuccessful) {
                    _bookingSuccess.value = true
                } else {
                    _error.value = when (response.code()) {
                        400 -> "Bu slot artıq rezerv edilib"
                        403 -> "İcazəniz yoxdur"
                        else -> "Rezervasiya uğursuz (${response.code()})"
                    }
                }
            } catch (e: java.net.UnknownHostException) {
                _error.value = "İnternet bağlantısı yoxdur"
            } catch (e: Exception) {
                _error.value = "Xəta: ${e.localizedMessage}"
            } finally {
                _isLoading.value = false
            }
        }
    }

    fun cancelBooking(bookingId: String) {
        viewModelScope.launch {
            try {
                bookingApi.cancelBooking(bookingId)
                loadMyBookings()
            } catch (e: Exception) {
                _error.value = "Ləğvetmə xətası: ${e.localizedMessage}"
            }
        }
    }

    fun resetBookingSuccess() {
        _bookingSuccess.value = false
    }
}

