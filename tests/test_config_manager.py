import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_load_config():
    from config_manager import ConfigManager
    cm = ConfigManager()
    assert "cpu_threshold" in cm.config
    assert cm.config["cpu_threshold"] == 80

def test_save_config():
    from config_manager import ConfigManager
    cm = ConfigManager()
    cm.config["cpu_threshold"] = 90
    cm.save()
    
    cm2 = ConfigManager()
    assert cm2.config["cpu_threshold"] == 90
