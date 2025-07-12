[app]
title = TikTok Report Bot
package.name = tiktokreportbot
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0
requirements = python3,kivy,requests,urllib3,chardet,idna
android.permissions = INTERNET
orientation = portrait
android.arch = armeabi-v7a
p4a.branch = master
fullscreen = 0

# Android specific
android.api = 33
android.minapi = 21
android.sdk = 28
android.ndk = 23b
android.private_storage = True
android.accept_sdk_license = True

[buildozer]
log_level = 2
