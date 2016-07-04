import json
import sys
import os
import base64

for l in open(sys.argv[1]).readlines():
    if l.startswith("#"):
        sys.stdout.write(l)
        continue
    try:
        cls, exceptions, samples = json.loads(l)
    except ValueError:
        exit("Bad JSON line: %s" % l)

    wrkdir = "stub/%s" % cls
    for d in (wrkdir, "%s/in" % wrkdir, "%s/out" % wrkdir):
        if not os.path.exists(d):
            os.mkdir(d)
    for i, s in enumerate(samples):     
        f=open("%s/in/%d" % (wrkdir, i), "w")
        f.write(base64.b64decode(samples[i]))
        f.close()
    f = open("%s/aflstub.py" % wrkdir, "w")
    f.write("""
import sys, afl
from scapy.all import *
afl.init()
try:
""")
    f.write("    %s(sys.stdin.read())\n" % (cls))
    if len(exceptions) > 0: 
        f.write("except (%s) as e:\n    pass\n" % ','.join(exceptions))
    else:
        f.write("finally:\n    pass\n")
    f.close()
    
