import os
import sys

def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(__file__)

def get_version():
    base_path = get_base_path()
    version_file = os.path.join(base_path, 'VERSION')
    if os.path.exists(version_file):
        with open(version_file, 'r', encoding='utf-8') as f:
            return f.read().strip()
    return '1.5'

def get_changelog():
    base_path = get_base_path()
    changelog_file = os.path.join(base_path, 'CHANGELOG.md')
    if os.path.exists(changelog_file):
        with open(changelog_file, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

__version__ = get_version()
__changelog__ = get_changelog()
