from pathlib import Path
import os
import json
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

secrets_file = os.path.join(BASE_DIR, 'secrets.json')   # secrets.json path

with open(secrets_file) as f:                           # read file
    secrets = json.loads(f.read())


def get_secret(key_name):                                # get secret or return error_msg
    try:
        return secrets[key_name]
    except KeyError:
        error_msg = 'Set the {} environment variable".format(setting)'
        raise ImproperlyConfigured(error_msg)
