@echo off
pygbag --disable-sound-format-error --template autorun.tmpl .
powershell -Command "Copy-Item -Path 'build/web/*' -Destination 'docs' -Recurse -Force"

