"""
templates.py — Central theme/template configuration for Auto-PPT Agent.
Each template defines background, title, content colors, and font configuration.
Colors are RGB tuples: (R, G, B)
"""

TEMPLATES = {
    "modern_minimal": {
        "display_name": "Modern Minimal",
        "bg_color": (248, 249, 250),          # Very light grey
        "title_bg": (255, 255, 255),           # White title bar
        "title_color": (30, 30, 30),           # Near black
        "content_color": (60, 60, 60),         # Dark grey
        "accent_color": (99, 102, 241),        # Indigo
        "font_title": "Segoe UI",
        "font_body": "Segoe UI",
        "layout": "light",
    },
    "dark_tech": {
        "display_name": "Dark Tech",
        "bg_color": (15, 15, 30),              # Very dark navy
        "title_bg": (20, 20, 40),              # Slightly lighter dark
        "title_color": (0, 240, 200),          # Neon teal
        "content_color": (200, 210, 255),      # Light blue-white
        "accent_color": (120, 80, 255),        # Purple neon
        "font_title": "Consolas",
        "font_body": "Segoe UI",
        "layout": "dark",
    },
    "startup_pitch": {
        "display_name": "Startup Pitch",
        "bg_color": (255, 255, 255),           # White
        "title_bg": (255, 90, 60),             # Vibrant orange-red
        "title_color": (255, 255, 255),        # White on colored bg
        "content_color": (40, 40, 40),         # Dark text
        "accent_color": (255, 90, 60),         # Orange accent
        "font_title": "Arial Black",
        "font_body": "Arial",
        "layout": "bold",
    },
    "education_visual": {
        "display_name": "Education Visual",
        "bg_color": (255, 252, 240),           # Warm cream
        "title_bg": (100, 180, 120),           # Soft green
        "title_color": (255, 255, 255),        # White on green
        "content_color": (50, 50, 50),         # Dark grey text
        "accent_color": (255, 170, 50),        # Warm yellow
        "font_title": "Trebuchet MS",
        "font_body": "Trebuchet MS",
        "layout": "light",
    },
    "corporate_professional": {
        "display_name": "Corporate Professional",
        "bg_color": (255, 255, 255),           # White
        "title_bg": (0, 70, 140),              # Deep corporate blue
        "title_color": (255, 255, 255),        # White
        "content_color": (30, 30, 30),         # Dark text
        "accent_color": (0, 120, 200),         # Lighter blue
        "font_title": "Calibri",
        "font_body": "Calibri",
        "layout": "light",
    },
    "academic_clean": {
        "display_name": "Academic Clean",
        "bg_color": (254, 254, 254),           # Pure white
        "title_bg": (240, 240, 240),           # Light grey
        "title_color": (20, 20, 80),           # Dark blue/navy
        "content_color": (30, 30, 30),         # Dark
        "accent_color": (80, 80, 160),         # Muted blue
        "font_title": "Times New Roman",
        "font_body": "Times New Roman",
        "layout": "light",
    },
}

def get_template(name: str) -> dict:
    """Returns a template config dict by name, defaulting to 'corporate_professional'."""
    return TEMPLATES.get(name, TEMPLATES["corporate_professional"])

def get_template_names() -> list:
    """Returns all available template keys."""
    return list(TEMPLATES.keys())

def get_template_display_names() -> dict:
    """Returns a mapping of key -> display name."""
    return {k: v["display_name"] for k, v in TEMPLATES.items()}
