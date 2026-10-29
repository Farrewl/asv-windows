"""PixhawkCheck — baca parameter failsafe dari cache MAVLink (read-only).

Modul ini tidak membuka koneksi sendiri: `MavlinkTelemetry.poll()` yang
membaca PARAM_VALUE, lalu `evaluate()` membandingkan nilai cache dengan
spec di config/pixhawk_required*.txt.
"""
import os
from struct import pack, unpack

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_SPEC_PATH = os.path.join(_REPO_ROOT, "config", "pixhawk_required.txt")

# MAV_PARAM_TYPE integer -> (format struct, ukuran byte).
_PARAM_FMT = {1: ("B", 1), 2: ("b", 1), 3: ("H", 2), 4: ("h", 2),
              5: ("I", 4), 6: ("i", 4)}

AUTOPILOT_FW = {
    3: ("ArduPilot", "pixhawk_required.txt"),
    12: ("PX4", "pixhawk_required_px4.txt"),
}


def decode_param(msg):
    """Nilai numerik PARAM_VALUE; integer di-decode dari bit float."""
    val = float(getattr(msg, "param_value", 0.0))
    ptype = int(getattr(msg, "param_type", 0) or 0)
    spec = _PARAM_FMT.get(ptype)
    if spec:
        fmt, size = spec
        try:
            return float(unpack("<" + fmt, pack("<f", val)[:size])[0])
        except Exception:
            return val
    return val


def firmware_name(autopilot):
    try:
        if autopilot is None:
            return "?"
        return AUTOPILOT_FW.get(int(autopilot), ("?", None))[0]
    except Exception:
        return "?"


def spec_path_for(autopilot=None):
    name = "pixhawk_required.txt"
    try:
        if autopilot is not None:
            name = AUTOPILOT_FW.get(int(autopilot), (None, name))[1] or name
    except Exception:
        pass
    return os.path.join(_REPO_ROOT, "config", name)


def _as_float(x):
    return None if x in ("-", "inf", "") else float(x)


def load_spec(path=None):
    path = path or _DEFAULT_SPEC_PATH
    spec = []
    with open(path, encoding="utf-8") as f:
        for raw in f:
            line = raw.split("#", 1)[0].strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) < 3:
                continue
            critical = (len(parts) > 3
                        and parts[3].strip().lower() in ("y", "yes", "1"))
            spec.append({
                "name": parts[0],
                "min": _as_float(parts[1]),
                "max": _as_float(parts[2]),
                "critical": critical,
            })
    return spec


def evaluate(spec, values):
    """Bandingkan spec dengan dict {nama: nilai}; hasil ala check_params."""
    out = []
    for p in spec:
        if p["name"] not in values:
            out.append(dict(p, value=None, status="unread"))
            continue
        val = values[p["name"]]
        ok = True
        if p["min"] is not None and val < p["min"] - 1e-9:
            ok = False
        if p["max"] is not None and val > p["max"] + 1e-9:
            ok = False
        out.append(dict(p, value=val, status="ok" if ok else "violation"))
    return out


def summarize(results):
    bad = [r for r in results if r["status"] != "ok"]
    if not bad:
        return "OK"
    parts = []
    for r in bad:
        tag = "KRITIS" if r["critical"] else "advisory"
        if r["status"] == "unread":
            parts.append(f"{r['name']} TIDAK DIJAWAB ({tag})")
        else:
            parts.append(
                f"{r['name']}={r['value']} luar [{r['min']}..{r['max']}] ({tag})")
    return "; ".join(parts)
