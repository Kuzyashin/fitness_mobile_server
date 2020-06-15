# -*- coding: utf-8 -*-
import os
from .base import BASE_DIR

LANGUAGE_CODE = 'en-us'

LOCALE_FOLDERS = [
    {"path":  BASE_DIR, "args": "--ignore=static --ignore=applications"},
    {"path":  os.path.join(BASE_DIR, "applications", "core")},

]
LOCALE_PATHS = [path['path'] for path in LOCALE_FOLDERS]