import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DATA_FILE = os.path.join(DATA_DIR, 'data.json')

# Asset Management Constants
BUFFER_TARGET_AMOUNT = 500000  # 500,000 JPY
LIFE_DEFENSE_TARGET_AMOUNT = 1500000 # 1,500,000 JPY (Reference)

import platform

# UI Configuration
# FONT_FAMILY defined below based on OS

# Font Sizes (OS-Dependent)
# Linux often needs larger base sizes if DPI scaling is not automatically handled by CTK/interop.
# Windows/Mac usually handle DPI scaling well, so we use standard sizes.
system = platform.system()
is_desktop_os = system in ["Windows", "Darwin"]

if is_desktop_os:
    # Windows / Mac
    if system == "Windows":
        FONT_FAMILY = "Yu Gothic UI"
    else:
        FONT_FAMILY = "Hiragino Sans" # Mac fallback
        
    FONT_SIZE_SMALL = 12
    FONT_SIZE_NORMAL = 14
    FONT_SIZE_LARGE = 18
    FONT_SIZE_TITLE = 24
    
    # Resizable Frame Base Sizes
    BASE_FONT_TITLE = 28
    BASE_FONT_NORMAL = 16
    BASE_FONT_ENTRIES = 16
    BASE_FONT_BUTTONS = 16
else:
    # Linux (or others) - Keeping the large sizes requested
    FONT_SIZE_SMALL = 16
    FONT_SIZE_NORMAL = 20
    FONT_SIZE_LARGE = 24
    FONT_SIZE_TITLE = 32
    
    # Resizable Frame Base Sizes
    BASE_FONT_TITLE = 42
    BASE_FONT_NORMAL = 28
    BASE_FONT_ENTRIES = 24
    BASE_FONT_BUTTONS = 24

if system == "Linux":
     FONT_FAMILY = "Noto Sans CJK JP"

# Investment Ratio (Reference for future use)
INVESTMENT_RATIO = {
    "Stock": 0.5,
    "Bond": 0.3,
    "Cash": 0.2
}
