# system-agnostic c-compiler (windows and linux)
import os
import sys

# Get the system's platform from sys.platform
system_platform = sys.platform

# Check the value
if system_platform.startswith('win'):
    os.system("x86_64-w64-mingw32-gcc -shared -o src/static/c/bmp64lib.dll src/static/c/bmp64lib.c -O3")
elif system_platform.startswith('linux'):
    os.system("gcc -shared -o src/static/c/bmp64lib.so -fPIC src/static/c/bmp64lib.c")
else:
    print("stop using this javastation")