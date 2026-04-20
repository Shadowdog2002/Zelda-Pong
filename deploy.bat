@echo off
pygbag --disable-sound-format-error --template autorun.tmpl .
powershell -Command "Copy-Item -Path 'build/web/*' -Destination 'docs' -Recurse -Force"
git add docs
git commit -m "Update build"
git push
