import os
import sys

def get_version():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)
    
    version_file = os.path.join(base_path, 'VERSION')
    if os.path.exists(version_file):
        with open(version_file, 'r', encoding='utf-8') as f:
            return f.read().strip()
    return '1.0.0'

__version__ = get_version()
