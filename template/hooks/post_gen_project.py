import os
import sys

GIT = {{ cookiecutter.git }}

if GIT:
    os.system("git init")
else:
    os.remove(".gitignore")

sys.exit(0)
