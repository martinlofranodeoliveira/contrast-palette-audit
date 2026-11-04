"""Implement the exact README contract; no I/O or operational effects."""
__all__ = ["analyze"]
_HEX = frozenset("0123456789abcdefABCDEF")

def _lin(c):
    if c <= 0.04045:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4

def _lum(color):
    h = color[1:]
    if len(h) == 3:
        h = h[0] * 2 + h[1] * 2 + h[2] * 2
    r = int(h[0:2], 16) / 255.0
    g = int(h[2:4], 16) / 255.0
    b = int(h[4:6], 16) / 255.0
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)

def _check_color(s):
    if type(s) is not str:
        raise ValueError("INPUT_INVALID")
    n = len(s)
    if n != 4 and n != 7:
        raise ValueError("INPUT_INVALID")
    if s[0] != "#":
        raise ValueError("INPUT_INVALID")
    for ch in s[1:]:
        if ch not in _HEX:
            raise ValueError("INPUT_INVALID")

def analyze(payload):
    if type(payload) is not dict:
        raise ValueError("INPUT_INVALID")
    try:
        keys = set(payload.keys())
    except Exception:
        raise ValueError("INPUT_INVALID")
    if keys != {"pairs"}:
        raise ValueError("INPUT_INVALID")
    pairs = payload["pairs"]
    if type(pairs) is not list:
        raise ValueError("INPUT_INVALID")
    if len(pairs) > 512:
        raise ValueError("INPUT_INVALID")
    seen = set()
    out = []
    aa_n = 0
    aaa_n = 0
    for e in pairs:
        if type(e) is not dict:
            raise ValueError("INPUT_INVALID")
        try:
            ek = set(e.keys())
        except Exception:
            raise ValueError("INPUT_INVALID")
        if ek != {"id", "foreground", "background"}:
            raise ValueError("INPUT_INVALID")
        pid = e["id"]
        fg = e["foreground"]
        bg = e["background"]
        if type(pid) is not str:
            raise ValueError("INPUT_INVALID")
        n = len(pid)
        if n < 1 or n > 80:
            raise ValueError("INPUT_INVALID")
        for ch in pid:
            o = ord(ch)
            if o < 32 or o > 126:
                raise ValueError("INPUT_INVALID")
        if pid in seen:
            raise ValueError("INPUT_INVALID")
        seen.add(pid)
        _check_color(fg)
        _check_color(bg)
        l1 = _lum(fg)
        l2 = _lum(bg)
        hi = l1 if l1 >= l2 else l2
        lo = l2 if l1 >= l2 else l1
        ratio = (hi + 0.05) / (lo + 0.05)
        aa = ratio >= 4.5
        aa_large = ratio >= 3.0
        aaa = ratio >= 7.0
        aaa_large = ratio >= 4.5
        if aa:
            aa_n += 1
        if aaa:
            aaa_n += 1
        out.append({"id": pid, "ratio": round(ratio, 6), "aa": aa, "aa_large": aa_large, "aaa": aaa, "aaa_large": aaa_large})
    valid = (aa_n == len(out))
    return {"valid": valid, "pairs": out, "summary": {"total": len(out), "aa_pass": aa_n, "aaa_pass": aaa_n}}
