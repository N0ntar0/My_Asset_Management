import sys
import os

# Add project root to sys.path to allow imports from src
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import customtkinter as ctk
from src.ui.app import App

def main():
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    
    app = App()
    try:
        app.run()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
