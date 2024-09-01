import os
import sys

ENVIRONMENT = os.environ.get('ENVIRONMENT', '').lower()

if ENVIRONMENT == 'prod':
    from asyncPress.settings.prod import *
elif ENVIRONMENT == 'dev':
    from asyncPress.settings.dev import *
else:
    print(
        'No environment set. Please set ENVIRONMENT to either PROD or DEV.',
        'Using DEV environment by default.',
        sep='\n',
        file=sys.stderr,
    )
    from asyncPress.settings.dev import *
