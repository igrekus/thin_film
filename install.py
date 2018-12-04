# -*- coding: UTF-8 -*-
import subprocess

subprocess.run(['pyinstaller', '--onefile', 'film.py', '--clean'])
