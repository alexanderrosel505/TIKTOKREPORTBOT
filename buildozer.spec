[app]
title = TikTokReportBot
package.name = tiktokreportbot
package.domain = org.tiktokreport
source.dir = .
source.include_exts = py
source.main = tiktok_report_bot.py
version = 1.0

# CRITICAL CHANGES:
requirements = python3, kivy==2.3.0, requests, openssl, libffi==3.4.4
android.ndk = 25b  # Use NDK 25b
p4a.branch = develop  # Use development branch of python-for-android

orientation = portrait
android.permissions = INTERNET
android.archs = armeabi-v7a, arm64-v8a
android.minapi = 21
android.api = 33
android.accept_sdk_license = True

[buildozer]
log_level = 2
