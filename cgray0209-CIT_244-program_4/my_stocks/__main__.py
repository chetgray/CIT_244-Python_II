import sys

if __package__:
    from . import main
else:
    from __init__ import main

try:
    rc = main(sys.argv)
except Exception as e:  # pylint: disable=broad-except
    print(f"Error: {e}", file=sys.stderr)
    rc = 1
sys.exit(rc)
