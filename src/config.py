import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DATA_FILE = os.path.join(DATA_DIR, 'data.json')

# Asset Management Constants
BUFFER_TARGET_AMOUNT = 500000  # 500,000 JPY
LIFE_DEFENSE_TARGET_AMOUNT = 1500000 # 1,500,000 JPY (Reference)

# UI Configuration
FONT_FAMILY = "Noto Sans CJK JP"

# Investment Ratio (Reference for future use)
INVESTMENT_RATIO = {
    "Stock": 0.5,
    "Bond": 0.3,
    "Cash": 0.2
}
