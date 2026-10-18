# Aterkia ASV — Windows (repo lomba)

Backend navigasi & GUI **Autonomous Surface Vehicle** (kompetisi KKCTBN ATSV),
dipindahkan dari repo Linux (`asv usluk-usluk`) supaya bisa jalan di laptop
Windows 64-bit. Deteksi YOLO (ONNX), state machine misi, MAVLink ke Pixhawk,
dan GUI PyQt5 — kode sama dengan versi Linux.

```
Kamera ─▶ YOLO (async, ONNX) ─▶ gate vision + PID/EKF (C core)
                                    │
                                    ▼
      Thruster mixer (differential) ─▶ MAVLink OFFBOARD ─▶ Pixhawk → ESC → Thruster
```

## Persiapan (sekali saja)

Wajib: **Python 3.12+ 64-bit** ([python.org](https://www.python.org/downloads/),
centang *Add python.exe to PATH*). Lalu:

```bat
scripts\setup_windows.bat
```

Buat `.venv`, install dependensi, verifikasi env + model ONNX.

## Menjalankan

```bat
scripts\run_gui.bat
```

Startup mode **HOLD** (aman) → tekan **MULAI** untuk AUTO/OFFBOARD.
Mirror ke QGroundControl lewat UDP (port 14550).

- **Kamera**: tab Settings → Scan, pilih index yang menampilkan gambar.
- **Pixhawk**: colok USB, port COM terdeteksi otomatis (pyserial).
- **Thruster/servo**: uji di lapangan sebelum lomba (tab Settings).

## Isi repo

| Path | Fungsi |
|---|---|
| `main.py` | GUI dashboard (PyQt5) |
| `app/` | navigator, kamera, YOLO ONNX, MAVLink, GUI |
| `core/` | library C (state machine, PID, fuzzy, mixer) + `aterkia_core.dll` |
| `config/` | track, site, parameter tuning |
| `weights/` | 4 model YOLO `.onnx` (ikut git) |
| `scripts/` | `setup_windows.bat`, `run_gui.bat`, `verify_env.py` |

## Catatan teknis Windows

- `core/aterkia_core.dll` sudah di-commit (cross-compile MinGW, dependensi
  hanya UCRT bawaan Windows 10+). Rebuild bila ubah kode C:
  `make -C core windows` (butuh MinGW/MSYS2).
- Kamera pakai backend **DSHOW** (fallback MSMF), port Pixhawk **COM\***
  via pyserial — otomatis lewat `platform.system()`.
- Repo test/latihan terpisah (`asv usluk-usluk` Linux + folder `dev/` di sana);
  repo ini khusus yang dibawa ke lomba.
