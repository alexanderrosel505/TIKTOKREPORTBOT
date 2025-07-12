[app]
title = TikTok Report Bot
package.name = tiktokreportbot
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0
requirements = python3, kivy==2.3.0, requests, urllib3, chardet, idna, pyjnius==1.5.0
android.permissions = INTERNET
orientation = portrait
android.arch = armeabi-v7a
p4a.branch = master
fullscreen = 0

# Fixed configurations
android.ndk = 25b
android.api = 33
android.minapi = 21
android.sdk = 33
android.private_storage = True
android.accept_sdk_license = True

# Critical fix for jnius
p4a.bootstrap = sdl2
android.allow_backup = False
android.verbose = True
android.ignore_setup_py = True

# Optimizations
p4a.ignore_recipes = openssl,ffmpeg
p4a.allow_java_sdk = True

[buildozer]
log_level = 2
