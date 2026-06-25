import sys
import os

# Agrega el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(__file__))

from app import app as application
