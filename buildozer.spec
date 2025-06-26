[app]
title = Meme Town
package.name = memetown
package.domain = org.alimoo.mt
source.dir = .
source.include_exts = py,jpg,png,json
icon.filename = mticon.png
version = 1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 1

# Permissions
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.allow_backup = False

# Presplash and background
android.presplash = coverimage.jpg

# Java version (recommended)
android.api = 31
android.minapi = 21
android.ndk = 23b
android.gradle_dependencies = androidx.appcompat:appcompat:1.2.0

# (Optionally add if you need filechooser)
android.gradle_dependencies += org.apache.commons:commons-io:1.3.2

[buildozer]
log_level = 2
warn_on_root = 1