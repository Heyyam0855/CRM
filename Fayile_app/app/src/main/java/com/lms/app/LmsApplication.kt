package com.lms.app

import android.app.Application
import dagger.hilt.android.HiltAndroidApp

/**
 * LMS Tətbiqinin əsas Application sinifi.
 * Hilt DI burada işə salınır.
 */
@HiltAndroidApp
class LmsApplication : Application()

