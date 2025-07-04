[app]
# App name
title = TikTokReportBot

# Package name (change if you want a different identifier)
package.name = tiktokreportbot
package.domain = org.tiktokreport

# Main script
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
source.main = tiktok_report_bot.py

# Version
version = 1.0

# Requirements
requirements = python3,kivy,requests

# Icon (optional)
# icon.filename = %(source.dir)s/icon.png

# Presplash (optional)
# presplash.filename = %(source.dir)s/presplash.png

# Orientation
orientation = portrait

# Android Permissions
android.permissions = INTERNET

# Android Arch (support for armeabi-v7a and arm64-v8a)
android.archs = armeabi-v7a, arm64-v8a

# Min SDK Version
android.minapi = 21

# Avoid asking for permissions during install
android.accept_sdk_license = True

# (Optional) Force specific version of Kivy
# kivy_version = 2.3.0

[buildozer]
log_level = 2
warn_on_root = 1

[python]
# Enable if you use SQLite or other native modules
# sqlite3 = 1

