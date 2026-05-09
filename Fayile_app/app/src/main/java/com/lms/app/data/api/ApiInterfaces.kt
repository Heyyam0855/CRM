package com.lms.app.data.api

import com.lms.app.data.model.*
import retrofit2.Response
import retrofit2.http.*

// ==================== AUTH API ====================
interface AuthApi {

    @POST("auth/login/")
    suspend fun login(@Body request: LoginRequest): Response<LoginResponse>

    @POST("auth/register/")
    suspend fun register(@Body request: RegisterRequest): Response<RegisterResponse>

    @POST("auth/token/refresh/")
    suspend fun refreshToken(@Body request: TokenRefreshRequest): Response<TokenRefreshResponse>

    @POST("auth/logout/")
    suspend fun logout(): Response<Unit>
}

// ==================== USER API ====================
interface UserApi {

    @GET("users/me/")
    suspend fun getMe(): Response<UserResponse>

    @PATCH("users/me/")
    suspend fun updateMe(@Body request: UpdateUserRequest): Response<UserResponse>

    @GET("users/students/")
    suspend fun getStudents(): Response<List<UserResponse>>

    @POST("users/fcm-token/")
    suspend fun updateFcmToken(@Body request: FcmTokenRequest): Response<Unit>
}

// ==================== BOOKING API ====================
interface BookingApi {

    @GET("bookings/slots/")
    suspend fun getAvailableSlots(): Response<List<SlotResponse>>

    @POST("bookings/create/")
    suspend fun createBooking(@Body request: BookingCreateRequest): Response<BookingResponse>

    @GET("bookings/my/")
    suspend fun getMyBookings(): Response<List<BookingResponse>>

    @GET("bookings/")
    suspend fun getAllBookings(): Response<List<BookingResponse>>

    @POST("bookings/{id}/cancel/")
    suspend fun cancelBooking(@Path("id") id: String): Response<BookingResponse>
}

// ==================== COURSE API ====================
interface CourseApi {

    @GET("courses/")
    suspend fun getCourses(): Response<List<CourseResponse>>

    @GET("courses/{id}/")
    suspend fun getCourseDetail(@Path("id") id: String): Response<CourseResponse>
}

// ==================== PAYMENT API ====================
interface PaymentApi {

    @POST("payments/initiate/")
    suspend fun initiatePayment(@Body request: PaymentRequest): Response<PaymentInitiateResponse>

    @GET("payments/history/")
    suspend fun getPaymentHistory(): Response<List<PaymentResponse>>
}

// ==================== NOTIFICATION API ====================
interface NotificationApi {

    @GET("notifications/")
    suspend fun getNotifications(): Response<List<NotificationResponse>>

    @POST("notifications/{id}/read/")
    suspend fun markAsRead(@Path("id") id: String): Response<Unit>
}

// ==================== ASSESSMENT API ====================
interface AssessmentApi {

    @GET("assessments/")
    suspend fun getAssessments(): Response<List<AssessmentResponse>>
}

// ==================== SUPPORT API ====================
interface SupportApi {

    @GET("support/tickets/")
    suspend fun getTickets(): Response<List<TicketResponse>>

    @POST("support/tickets/")
    suspend fun createTicket(@Body request: TicketCreateRequest): Response<TicketResponse>

    @GET("support/tickets/{id}/")
    suspend fun getTicketDetail(@Path("id") id: String): Response<TicketResponse>
}

