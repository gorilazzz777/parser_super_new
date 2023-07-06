from dotenv import load_dotenv
from pathlib import Path
import os


if os.getenv('DEV', False):
    from .settings_base import *
    from .settings_dev import *
elif os.getenv('PROD', False):
    from .settings_base import *
    from .settings_prod import *
else:
    load_dotenv(f'{Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).parent.parent}/.envs/.django')
    from .settings_base import *
    from .settings_local import *
