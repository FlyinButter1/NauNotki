# system-agnostic c-compiler (windows and linux)
import os
import sys

if sys.platform.startswith('win'):
    os.system("x86_64-w64-mingw32-gcc -shared -o src/static/c/bmp64lib.dll src/static/c/bmp64lib.c -O3 -std=c11")
elif sys.platform.startswith('linux'):
    os.system("gcc -shared -o src/static/c/bmp64lib.so -fPIC src/static/c/bmp64lib.c -O3 -Wno-unused-result -std=c11")
else:
    print("stop using this javastation")