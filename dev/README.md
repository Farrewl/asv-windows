# Dev extras (dipindah dari repo kapal)

Folder ini menampung **perkakas pengembangan** yang sengaja dikeluarkan dari
repo produksi `asv usluk-usluk` agar repo tetap ringan:

- `tests/` — cross-check C↔Python + `_ref/` (oracle Python lama).
- `core-tests/` — unit test C (CMake/CTest).
- `core-CMakeLists.txt` — CMake untuk build/test C (dulu `core/CMakeLists.txt`).
- `weights-pt/` (di folder induk) — bobot `.pt` sumber (runtime pakai `.onnx`).

## Menjalankan test dari sini

Test menghitung root repo dari lokasi file, jadi disediakan **symlink** ke
repo (`app`, `core`, `config`, `weights`). Pastikan repo ada di
`../../asv usluk-usluk` (relatif ke folder ini), lalu:

```bash
./run_tests.sh
# atau:
../../asv usluk-usluk/.venv/bin/python3 -m unittest discover -s tests -p 'test_core_*.py' -v
```

Symlink bersifat **relatif**, jadi aman selama folder ini dan repo tetap
bersaudara di `URDC/`. Bila repo dipindah, perbarui symlink:

```bash
ln -sfn "<path-ke-repo>/app"    app
ln -sfn "<path-ke-repo>/core"   core
ln -sfn "<path-ke-repo>/config" config
ln -sfn "<path-ke-repo>/weights" weights
```

> Repo kapal tidak lagi berisi `tests/`/`docs/`. Dokumentasi lengkap ada di
> `README.md` repo; penjelasan mendalam ada di `../docs/`.
