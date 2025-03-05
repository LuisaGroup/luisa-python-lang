import sys

# check if is python 3.12 or higher
if sys.version_info < (3, 12):
    raise Exception("luisa_lang requires Python 3.12 or higher")

# from luisa_lang.lang import *
# from luisa_lang.lang_builtins import *