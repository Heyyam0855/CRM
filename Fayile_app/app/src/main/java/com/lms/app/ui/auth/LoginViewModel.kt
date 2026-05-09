package com.lms.app.ui.auth

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.lms.app.data.api.AuthApi
import com.lms.app.data.model.LoginRequest
import com.lms.app.data.model.UserResponse
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.launch
import javax.inject.Inject

sealed class LoginState {
    object Idle : LoginState()
    object Loading : LoginState()
    data class Success(val user: UserResponse) : LoginState()
    data class Error(val message: String) : LoginState()
}

@HiltViewModel
class LoginViewModel @Inject constructor(
    private val authApi: AuthApi,
    private val prefs: android.content.SharedPreferences
) : ViewModel() {

    private val _loginState = MutableLiveData<LoginState>(LoginState.Idle)
    val loginState: LiveData<LoginState> = _loginState

    fun login(email: String, password: String) {
        // Sadə validasiya
        if (email.isBlank()) {
            _loginState.value = LoginState.Error("Email ünvanını daxil edin")
            return
        }
        if (password.isBlank()) {
            _loginState.value = LoginState.Error("Şifrəni daxil edin")
            return
        }
        if (!android.util.Patterns.EMAIL_ADDRESS.matcher(email).matches()) {
            _loginState.value = LoginState.Error("Düzgün email ünvanı daxil edin")
            return
        }

        viewModelScope.launch {
            _loginState.value = LoginState.Loading
            try {
                val response = authApi.login(LoginRequest(email, password))
                if (response.isSuccessful) {
                    val body = response.body()!!
                    // JWT tokenları təhlükəsiz şəkildə saxla
                    prefs.edit()
                        .putString("access_token", body.access)
                        .putString("refresh_token", body.refresh)
                        .putString("user_role", body.user.role)
                        .putString("user_email", body.user.email)
                        .putString("user_name", body.user.getFullName())
                        .apply()

                    _loginState.value = LoginState.Success(body.user)
                } else {
                    val errorMsg = when (response.code()) {
                        401 -> "Email və ya şifrə yanlışdır"
                        400 -> "Məlumatları düzgün daxil edin"
                        else -> "Server xətası (${response.code()})"
                    }
                    _loginState.value = LoginState.Error(errorMsg)
                }
            } catch (e: java.net.UnknownHostException) {
                _loginState.value = LoginState.Error("İnternet bağlantısı yoxdur")
            } catch (e: java.net.SocketTimeoutException) {
                _loginState.value = LoginState.Error("Server cavab vermir. Yenidən cəhd edin")
            } catch (e: Exception) {
                _loginState.value = LoginState.Error("Xəta: ${e.localizedMessage}")
            }
        }
    }

    fun isAlreadyLoggedIn(): Boolean {
        return prefs.getString("access_token", null) != null
    }

    fun getUserRole(): String {
        return prefs.getString("user_role", "student") ?: "student"
    }
}

