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

# Fix: Force specific NDK version
android.ndk = 25b
android.api = 33
android.minapi = 21
android.sdk = 33
android.private_storage = True
android.accept_sdk_license = True

# Build optimization
p4a.bootstrap = sdl2
android.allow_backup = False
android.verbose = True

[buildozer]
log_level = 2
