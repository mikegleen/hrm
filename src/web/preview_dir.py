"""

"""
import os.path
import subprocess
import sys
from PIL import Image

targetdir = sys.argv[1]

try:
    for target in os.listdir(targetdir):
        filename, extension = os.path.splitext(target)
        if extension.lower() in ('.jpg', '.png'):
            subprocess.run(['open', '-W', os.path.join(targetdir, target)])
        else:
            print('skipping', target)
except KeyboardInterrupt:
    print('\nExiting.')
    sys.exit(1)

