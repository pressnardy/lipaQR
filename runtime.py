import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lipaqr.settings')
django.setup()

from qrgenerator.models import QrImage

newImg = QrImage.add(2, 4)
print(newImg)
