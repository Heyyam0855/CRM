package com.lms.app.ui.courses

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.lms.app.data.api.CourseApi
import com.lms.app.data.model.CourseResponse
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class CourseViewModel @Inject constructor(
    private val courseApi: CourseApi
) : ViewModel() {

    private val _courses = MutableLiveData<List<CourseResponse>>(emptyList())
    val courses: LiveData<List<CourseResponse>> = _courses

    private val _isLoading = MutableLiveData(false)
    val isLoading: LiveData<Boolean> = _isLoading

    private val _error = MutableLiveData<String?>(null)
    val error: LiveData<String?> = _error

    fun loadCourses() {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val response = courseApi.getCourses()
                if (response.isSuccessful) {
                    _courses.value = response.body() ?: emptyList()
                } else {
                    _error.value = "Kurslar yüklənmədi (${response.code()})"
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
}

