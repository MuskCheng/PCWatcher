import os

def get_version():
    version_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'VERSION')
    if os.path.exists(version_file):
        with open(version_file, 'r', encoding='utf-8') as f:
            return f.read().strip()
    return '1.0.0'

__version__ = get_version()
