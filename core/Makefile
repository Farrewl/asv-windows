# ============================================================
# core/Makefile — build library C (Linux + Windows/MinGW).
#
# Pemakaian:
#   make -C core linux     # -> core/libaterkia.so     (Linux)
#   make -C core windows   # -> core/aterkia_core.dll  (MinGW)
#   make -C core check     # kompilasi ketat -Wall -Wextra -Werror (tanpa output)
#   make -C core clean
#
# Catatan:
# - gamepad_input.cpp TIDAK masuk library ini (dipakai via CMake).
# - Loader Python: app/aterkia_core.py memuat core/libaterkia.so (Linux)
#   atau core/aterkia_core.dll (Windows).
# - Target windows: di Linux pakai cross mingw (otomatis bila ada),
#   di Windows/MSYS2 gcc native sudah MinGW.
# ============================================================

CC        = gcc
CXX       = g++
CFLAGS    ?= -O2 -Wall -Wextra -Werror
CPPFLAGS  += -Iinclude
SRC_C     := $(wildcard src/*.c)
LM        := -lm

# Cross-compiler Windows bila tersedia; kalau tidak (di Windows/MSYS2)
# pakai gcc native (MinGW).
WIN_CC    ?= $(shell command -v x86_64-w64-mingw32-gcc >/dev/null 2>&1 \
	&& echo x86_64-w64-mingw32-gcc || echo gcc)

.PHONY: linux windows check clean

# --- Linux: shared object ELF (dipakai app/aterkia_core.py) ---
linux: libaterkia.so

libaterkia.so: $(SRC_C) $(wildcard include/*.h)
	$(CC) -shared -fPIC $(CFLAGS) $(CPPFLAGS) $(SRC_C) -o $@ $(LM)

# --- Windows: DLL MinGW (dipakai app/aterkia_core.py saat os.name=="nt") ---
windows: aterkia_core.dll

aterkia_core.dll: $(SRC_C) $(wildcard include/*.h)
	$(WIN_CC) -shared -static-libgcc $(CFLAGS) $(CPPFLAGS) $(SRC_C) -o $@ $(LM)

# --- Verifikasi ketat tanpa menghasilkan file ---
check:
	$(CC) -fsyntax-only $(CFLAGS) $(CPPFLAGS) src/*.c
	$(CXX) -fsyntax-only $(CFLAGS) $(CPPFLAGS) src/gamepad_input.cpp
	@echo "check: lolos -Wall -Wextra -Werror"

clean:
	rm -f libaterkia.so aterkia_core.dll
