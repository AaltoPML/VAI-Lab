import sys
from . import run_pipeline

rc = 1
try:
    run_pipeline()
    rc = 0
except Exception as e:
    print('Error: %s' % e, file=sys.stderr)
sys.exit(rc)