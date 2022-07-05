import django
import os
import sys

sys.path.append(
    os.path.join(os.path.dirname(__file__), '')
)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

django.setup()

from object.models import Object

print(Object.choose().id)
