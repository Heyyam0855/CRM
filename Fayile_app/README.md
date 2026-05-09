# LMS Android Tətbiqi

**LMS Platform** — Django REST API ilə inteqrasiya edilmiş Android tətbiqi.

## 📁 Struktur

```
Fayile_app/
├── app/
│   ├── src/main/
│   │   ├── java/com/lms/app/
│   │   │   ├── data/
│   │   │   │   ├── api/          ← Retrofit API interfeyslər
│   │   │   │   ├── model/        ← Data class-lar (request/response)
│   │   │   │   ├── repository/   ← Repository implementasiyaları
│   │   │   │   └── local/        ← Room DAO + Entity
│   │   │   ├── domain/           ← Business logic (Use Cases)
│   │   │   ├── ui/               ← Fragment-lər, ViewModel-lər
│   │   │   ├── di/               ← Hilt Module-lar
│   │   │   ├── service/          ← FCM Service
│   │   │   └── utils/            ← Extensions, helpers
│   │   ├── res/                  ← Layout, drawable, values
│   │   └── AndroidManifest.xml
│   └── build.gradle.kts
├── gradle/
│   ├── libs.versions.toml        ← Version catalog
│   └── wrapper/
├── build.gradle.kts
└── settings.gradle.kts
```

## 🔗 Backend Bağlantısı

```
Django Backend:  https://your-domain.com/api/v1/
Auth:            JWT Bearer Token
Local Debug:     http://10.0.2.2:8000/api/v1/  (Android Emulator → localhost)
```

## 🚀 Başlamaq üçün

1. Android Studio-da `Fayile_app/` qovluğunu aç
2. `gradle/libs.versions.toml`-da versiyaları yoxla
3. `app/build.gradle.kts`-də `BASE_URL`-i dəyiş
4. `google-services.json` faylını əlavə et (Firebase Console-dan)
5. Sync + Run

## 💰 Biznes Qaydaları

```
LESSON_PRICE = 25 AZN  (DƏYİŞDİRİLMƏZ!)
CANCELLATION_HOURS = 24
Ödəniş: ePoint gateway (WebView)
Video:  Google Meet linki açılır
```

