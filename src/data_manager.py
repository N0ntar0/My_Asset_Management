import json
import os
from .config import DATA_FILE

class DataManager:
    def __init__(self, filepath=DATA_FILE):
        self.filepath = filepath
        self.data = self._load_data()

    def _load_data(self):
        if not os.path.exists(self.filepath):
            return self._create_default_data()
        
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return self._create_default_data()

    def _create_default_data(self):
        return {
            "assets": {
                "sony_bank": 0,
                "sbi_securities": 0,
                "paypay_bank": 0,
                "sumishin_sbi": 0
            },
            "settings": {
                "buffer_target": 500000
            },
            "logs": []
        }

    def save_data(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def get_asset(self, key):
        return self.data.get("assets", {}).get(key, 0)

    def update_asset(self, key, value):
        if "assets" not in self.data:
            self.data["assets"] = {}
        self.data["assets"][key] = value
        self.save_data()

    def reset_assets(self):
        """Resets all tracked assets to 0"""
        keys = ["sony_bank", "sbi_securities", "paypay_bank", "sumishin_sbi"]
        if "assets" not in self.data:
            self.data["assets"] = {}
            
        for key in keys:
            self.data["assets"][key] = 0
        self.save_data()

    def add_log(self, message):
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        if "logs" not in self.data:
            self.data["logs"] = []
        self.data["logs"].append(log_entry)
        # Keep only last 50 logs to prevent infinite growth
        if len(self.data["logs"]) > 50:
            self.data["logs"] = self.data["logs"][-50:]
        self.save_data()

    def get_settings(self):
        defaults = {
            "living_target": 100000,
            "buffer_target": 500000,
            "life_defense_target": 1500000
        }
        if "settings" not in self.data:
            self.data["settings"] = defaults
            self.save_data()
        
        # Ensure all keys exist (merge defaults)
        settings = self.data.get("settings", {})
        for key, val in defaults.items():
            if key not in settings:
                settings[key] = val
        return settings

    def update_settings(self, new_settings):
        if "settings" not in self.data:
            self.data["settings"] = {}
        self.data["settings"].update(new_settings)
        self.save_data()

    def get_latest_log(self):
        if "logs" in self.data and self.data["logs"]:
            return self.data["logs"][-1]
        return "履歴はありません"

    def get_recent_logs(self, count=1):
        if "logs" in self.data and self.data["logs"]:
            return self.data["logs"][-count:]
        return []
