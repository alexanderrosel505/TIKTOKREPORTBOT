[app]
title = TikTokReportBot
package.name = tiktokreportbot
package.domain = org.tiktokreport
source.dir = .
source.include_exts = py
source.main = tiktok_report_bot.py
version = 1.0

# Requirements
requirements = python3, kivy==2.3.0, requests

# Android settings
android.minapi = 21
android.api = 33
orientation = portrait
android.permissions = INTERNET
