import json
import sys
import os
import base64

from config import allowed

with open("seen-crashes.json") as f:
    seen_crashes = json.load(f)

for l in open(sys.argv[1]).readlines():
    if l.startswith("#"):
        sys.stdout.write(l)
        continue
    try:
        cls, exceptions, samples = json.loads(l)
    except ValueError:
        print l

    exceptions = sorted(allowed.intersection(set(seen_crashes.get(cls,set()))).union(exceptions))
    print json.dumps([cls,exceptions,samples])
