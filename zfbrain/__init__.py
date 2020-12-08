print(f'Invoking __init__.py for {__name__}')

from zfbrain.__main__ import *
print("Imported zfbrain.__main__")
from zfbrain.mymath import *
print("Imported zfbrain.mymath")