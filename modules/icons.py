"""modules/icons.py — Premium SVG icon system replacing emojis."""


def _svg(path_d: str, size: int = 24, color: str = "currentColor",
         viewbox: str = "0 0 24 24", stroke_width: str = "1.5") -> str:
    """Generate an inline SVG icon."""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="{viewbox}" fill="none" stroke="{color}" '
        f'stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round" '
        f'style="display:inline-block;vertical-align:middle;flex-shrink:0;">'
        f'{path_d}</svg>'
    )


def _svg_filled(path_d: str, size: int = 24, color: str = "currentColor",
                viewbox: str = "0 0 24 24") -> str:
    """Generate a filled SVG icon."""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="{viewbox}" fill="{color}" '
        f'style="display:inline-block;vertical-align:middle;flex-shrink:0;">'
        f'{path_d}</svg>'
    )


# ─── Brand / App ────────────────────────────────────────────────────────────

def graduation_cap(size=24, color="#6C63FF"):
    return _svg(
        '<path d="M22 10v6M2 10l10-5 10 5-10 5z"/>'
        '<path d="M6 12v5c0 1.66 2.69 3 6 3s6-1.34 6-3v-5"/>',
        size, color
    )


def logo_icon(size=40):
    return _svg(
        '<path d="M22 10v6M2 10l10-5 10 5-10 5z"/>'
        '<path d="M6 12v5c0 1.66 2.69 3 6 3s6-1.34 6-3v-5"/>',
        size, "url(#grad)"
    ).replace(
        '</svg>',
        '<defs><linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">'
        '<stop offset="0%" style="stop-color:#6C63FF"/>'
        '<stop offset="100%" style="stop-color:#4ECDC4"/>'
        '</linearGradient></defs></svg>'
    )


# ─── Navigation / Sidebar ───────────────────────────────────────────────────

def dashboard(size=20, color="#E0E0F0"):
    return _svg(
        '<rect x="3" y="3" width="7" height="7" rx="1"/>'
        '<rect x="14" y="3" width="7" height="7" rx="1"/>'
        '<rect x="3" y="14" width="7" height="7" rx="1"/>'
        '<rect x="14" y="14" width="7" height="7" rx="1"/>',
        size, color
    )


def chat(size=20, color="#E0E0F0"):
    return _svg(
        '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>'
        '<path d="M8 10h.01M12 10h.01M16 10h.01"/>',
        size, color
    )


def brain(size=20, color="#E0E0F0"):
    return _svg(
        '<path d="M12 2a7 7 0 0 0-7 7c0 3.5 2.5 6.5 7 10 4.5-3.5 7-6.5 7-10a7 7 0 0 0-7-7z"/>'
        '<path d="M12 2C8.5 2 5 4.5 5 9c0 2 1 4 2.5 5.5M12 2c3.5 0 7 2.5 7 7 0 2-1 4-2.5 5.5"/>'
        '<path d="M9 9h.01M15 9h.01M9.5 13c.83.67 2.17.67 3 0"/>',
        size, color, stroke_width="1.5"
    )


def quiz(size=20, color="#E0E0F0"):
    return _svg(
        '<circle cx="12" cy="12" r="10"/>'
        '<path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>'
        '<path d="M12 17h.01"/>',
        size, color
    )


def exam(size=20, color="#E0E0F0"):
    return _svg(
        '<circle cx="12" cy="12" r="10"/>'
        '<polyline points="12 6 12 12 16 14"/>',
        size, color
    )


def flashcard(size=20, color="#E0E0F0"):
    return _svg(
        '<rect x="2" y="6" width="20" height="12" rx="2"/>'
        '<path d="M12 6v12M2 12h20"/>',
        size, color
    )


def progress(size=20, color="#E0E0F0"):
    return _svg(
        '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
        size, color, stroke_width="2"
    )


def admin(size=20, color="#E0E0F0"):
    return _svg(
        '<path d="M12 15v2m-6 4h12a2 2 0 0 0 2-2v-6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2zm10-10V7a4 4 0 0 0-8 0v4h8z"/>',
        size, color
    )


def faculty(size=20, color="#E0E0F0"):
    return _svg(
        '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>'
        '<circle cx="9" cy="7" r="4"/>'
        '<path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
        size, color
    )


def logout(size=20, color="#FF5252"):
    return _svg(
        '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>'
        '<polyline points="16 17 21 12 16 7"/>'
        '<line x1="21" y1="12" x2="9" y2="12"/>',
        size, color
    )


# ─── Metric / Dashboard Icons ───────────────────────────────────────────────

def clipboard_check(size=28, color="#6C63FF"):
    return _svg(
        '<path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2"/>'
        '<rect x="9" y="3" width="6" height="4" rx="1"/>'
        '<path d="m9 14 2 2 4-4"/>',
        size, color
    )


def target(size=28, color="#6C63FF"):
    return _svg(
        '<circle cx="12" cy="12" r="10"/>'
        '<circle cx="12" cy="12" r="6"/>'
        '<circle cx="12" cy="12" r="2"/>',
        size, color
    )


def trophy(size=28, color="#6C63FF"):
    return _svg(
        '<path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/>'
        '<path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/>'
        '<path d="M4 22h16"/>'
        '<path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20 7 22"/>'
        '<path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20 17 22"/>'
        '<path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/>',
        size, color
    )


def book_open(size=28, color="#6C63FF"):
    return _svg(
        '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>'
        '<path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>',
        size, color
    )


# ─── Action Icons ────────────────────────────────────────────────────────────

def upload(size=20, color="#6C63FF"):
    return _svg(
        '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>'
        '<polyline points="17 8 12 3 7 8"/>'
        '<line x1="12" y1="3" x2="12" y2="15"/>',
        size, color
    )


def lightning(size=20, color="#FFB700"):
    return _svg(
        '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
        size, color, stroke_width="1.5"
    )


def sparkles(size=20, color="#4ECDC4"):
    return _svg(
        '<path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/>'
        '<path d="M5 3v4M19 17v4M3 5h4M17 19h4"/>',
        size, color
    )


def search(size=20, color="#9E9EC0"):
    return _svg(
        '<circle cx="11" cy="11" r="8"/>'
        '<line x1="21" y1="21" x2="16.65" y2="16.65"/>',
        size, color
    )


def check_circle(size=20, color="#4ECDC4"):
    return _svg(
        '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>'
        '<polyline points="22 4 12 14.01 9 11.01"/>',
        size, color
    )


def x_circle(size=20, color="#FF5252"):
    return _svg(
        '<circle cx="12" cy="12" r="10"/>'
        '<line x1="15" y1="9" x2="9" y2="15"/>'
        '<line x1="9" y1="9" x2="15" y2="15"/>',
        size, color
    )


def bar_chart(size=20, color="#6C63FF"):
    return _svg(
        '<line x1="12" y1="20" x2="12" y2="10"/>'
        '<line x1="18" y1="20" x2="18" y2="4"/>'
        '<line x1="6" y1="20" x2="6" y2="16"/>',
        size, color, stroke_width="2"
    )


def trending_up(size=20, color="#4ECDC4"):
    return _svg(
        '<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/>'
        '<polyline points="17 6 23 6 23 12"/>',
        size, color, stroke_width="2"
    )


def alert_triangle(size=20, color="#FFB700"):
    return _svg(
        '<path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>'
        '<line x1="12" y1="9" x2="12" y2="13"/>'
        '<line x1="12" y1="17" x2="12.01" y2="17"/>',
        size, color
    )


def star(size=20, color="#FFB700"):
    return _svg(
        '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
        size, color
    )


def users(size=20, color="#6C63FF"):
    return _svg(
        '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>'
        '<circle cx="9" cy="7" r="4"/>'
        '<path d="M23 21v-2a4 4 0 0 0-3-3.87"/>'
        '<path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
        size, color
    )


def file_text(size=20, color="#9E9EC0"):
    return _svg(
        '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>'
        '<polyline points="14 2 14 8 20 8"/>'
        '<line x1="16" y1="13" x2="8" y2="13"/>'
        '<line x1="16" y1="17" x2="8" y2="17"/>'
        '<polyline points="10 9 9 9 8 9"/>',
        size, color
    )


def wave_hand(size=48, color="#6C63FF"):
    """Animated waving hand icon."""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.5" '
        f'stroke-linecap="round" stroke-linejoin="round" '
        f'style="display:inline-block;vertical-align:middle;animation:wave 1.5s ease-in-out infinite;">'
        '<path d="M7 15c-1-1-3.5-2-5-1s-1 4 1 6 6 3 8 2 2-3 1-5"/>'
        '<path d="M19.5 8.5c.5-1 .5-2-.5-3s-2.5-.5-3 .5l-4 6"/>'
        '<path d="M14 10.5c.5-1 .5-2-.5-3s-2.5-.5-3 .5"/>'
        '<path d="M10.5 13c.5-1 .5-2-.5-3s-2.5-.5-3 .5l-1 1.5"/>'
        '<path d="M22 11.5c.5-1 .5-2-.5-3s-2.5-.5-3 .5l-5.5 8.5"/>'
        '</svg>'
    )


def robot(size=24, color="#6C63FF"):
    return _svg(
        '<rect x="3" y="11" width="18" height="10" rx="2"/>'
        '<circle cx="12" cy="5" r="2"/>'
        '<path d="M12 7v4"/>'
        '<line x1="8" y1="16" x2="8" y2="16"/>'
        '<line x1="16" y1="16" x2="16" y2="16"/>',
        size, color
    )
