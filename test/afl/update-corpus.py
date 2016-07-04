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

    mindir = "stub/%s/minimized" % cls
    if os.path.exists(mindir):
        newsamples = set()
        for fn in os.listdir(mindir):
            if os.path.isfile("%s/%s" % (mindir, fn)):
                with open("%s/%s" % (mindir,fn)) as f:
                    newsamples.add(base64.b64encode(f.read()))
        if len(newsamples) > 0:
            samples = list(newsamples)
    if set(samples) == set([""]):
        print "# %s skipped" % cls
    else:
        print json.dumps([cls,exceptions,samples])
