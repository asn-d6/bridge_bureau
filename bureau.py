from stem.descriptor import parse_file
import sys


def main():
    if len(sys.argv) < 1:
        usage()
        sys.exit(1)

    for desc in parse_file(sys.argv[1], "bridge-extra-info 1.2"):
        print desc.nickname

