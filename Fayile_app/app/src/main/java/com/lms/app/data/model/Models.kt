package com.lms.app.data.model

import com.google.gson.annotations.SerializedName

// ==================== AUTH MODELS ====================
data class LoginRequest(
    val email: String,
    val password: String
)

data class LoginResponse(
    val access: String,
    val refresh: String,
    val user: UserResponse
)

data class RegisterRequest(
    val email: String,
    val password: String,
    @SerializedName("first_name") val firstName: String,
    @SerializedName("last_name") val lastName: String,
    val phone: String = ""
)

data class RegisterResponse(
    val access: String,
    val refresh: String,
    val user: UserResponse
)

data class TokenRefreshRequest(
    val refresh: String
)

data class TokenRefreshResponse(
    val access: String
)

// ==================== USER MODELS ====================
data class UserResponse(
    val id: String,
    val email: String,
    @SerializedName("first_name") val firstName: String,
    @SerializedName("last_name") val lastName: String,
    val phone: String,
    val role: String,   // "teacher" | "student"
    val avatar: String?,
    @SerializedName("created_at") val createdAt: String
) {
    fun getFullName() = "$firstName $lastName"
    fun isTeacher() = role == "teacher"
}

data class UpdateUserRequest(
    @SerializedName("first_name") val firstName: String,
    @SerializedName("last_name") val lastName: String,
    val phone: String
)

data class FcmTokenRequest(
    @SerializedName("fcm_token") val fcmToken: String
)

// ==================== BOOKING MODELS ====================
data class SlotResponse(
    val id: String,
    @SerializedName("start_time") val startTime: String,
    @SerializedName("end_time") val endTime: String,
    @SerializedName("is_reserved") val isReserved: Boolean
)

data class BookingCreateRequest(
    @SerializedName("slot_id") val slotId: String,
    @SerializedName("lesson_type") val lessonType: String,
    val topic: String = "",
    val notes: String = ""
)

data class BookingResponse(
    val id: String,
    val student: UserResponse?,
    val slot: SlotResponse?,
    @SerializedName("lesson_type") val lessonType: String,
    val topic: String,
    val status: String,  // scheduled | completed | cancelled | no_show
    @SerializedName("zoom_link") val zoomLink: String,
    val price: String,   // "25.00" AZN — SABİT
    @SerializedName("created_at") val createdAt: String
)

// ==================== COURSE MODELS ====================
data class CourseResponse(
    val id: String,
    val title: String,
    val description: String,
    val slug: String,
    @SerializedName("is_active") val isActive: Boolean,
    @SerializedName("created_at") val createdAt: String
)

// ==================== PAYMENT MODELS ====================
data class PaymentRequest(
    val amount: String = "25.00",  // 25 AZN — SABİT
    @SerializedName("payment_type") val paymentType: String  // monthly | per_lesson
)

data class PaymentInitiateResponse(
    @SerializedName("payment_url") val paymentUrl: String,
    @SerializedName("order_id") val orderId: String
)

data class PaymentResponse(
    val id: String,
    val amount: String,
    val status: String,  // pending | paid | failed | refunded
    @SerializedName("payment_type") val paymentType: String,
    @SerializedName("created_at") val createdAt: String
)

// ==================== NOTIFICATION MODELS ====================
data class NotificationResponse(
    val id: String,
    val title: String,
    val message: String,
    @SerializedName("notification_type") val type: String,
    @SerializedName("is_read") val isRead: Boolean,
    @SerializedName("created_at") val createdAt: String
)

// ==================== ASSESSMENT MODELS ====================
data class AssessmentResponse(
    val id: String,
    val title: String,
    val score: Int?,
    @SerializedName("max_score") val maxScore: Int,
    val feedback: String,
    val status: String,
    @SerializedName("created_at") val createdAt: String
)

// ==================== SUPPORT MODELS ====================
data class TicketResponse(
    val id: String,
    val subject: String,
    val status: String,  // open | in_progress | resolved | closed
    val priority: String,
    @SerializedName("created_at") val createdAt: String
)

data class TicketCreateRequest(
    val subject: String,
    val message: String,
    val priority: String = "medium"
)

