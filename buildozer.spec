[app]
title = TikTokReportBot
package.name = tiktokreportbot
package.domain = org.tiktokreport
source.dir = .
source.include_exts = py
source.main = tiktok_report_bot.py
version = 1.0

# Requirements
requirements = python3, kivy==2.3.0, requests, openssl

# Android settings
android.ndk = 25b
p4a.branch = 2024.05.06  # MUST BE ON SEPARATE LINE

orientation = portrait
android.permissions = INTERNET
android.archs = arm64-v8a, armeabi-v7a
android.minapi = 21
android.api = 33
android.accept_sdk_license = True

[buildozer]
log_level = 2
