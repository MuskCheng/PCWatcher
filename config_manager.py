import json
import os

class ConfigManager:
    def __init__(self):
        self.config_dir = os.path.join(os.environ.get('APPDATA', '.'), 'PCWatcher')
        self.config_path = os.path.join(self.config_dir, 'config.json')
        self._ensure_config_dir()
        self.config = self._load()
    
    def _ensure_config_dir(self):
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
    
    def _load(self):
        default_config = {
            "push_key": "",
            "cpu_threshold": 80,
            "memory_threshold": 85,
            "disk_threshold": 90,
            "disk_thresholds": {},
            "network_interface": "",
            "network_upload_threshold": 10485760,
            "network_download_threshold": 10485760,
            "interval": 30,
            "first_run": True
        }
        
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return {**default_config, **config}
        return default_config
    
    def save(self):
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def is_first_run(self):
        return self.config.get("first_run", True)
