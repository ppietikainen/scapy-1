import os
from scapy.all import *
import traceback
import json
import struct

from config import allowed
ex = {}

for root, dirs, files in os.walk('stub'):
    if 'crashes' in root:
        if len(files) > 0:
            _,proto,_,_ = root.split('/')
            repros = filter(lambda x: x.startswith('id:'),files)
            for r in repros:
                with  open("%s/%s" % (root, r)) as f:
                    repro = f.read()

                try:
                    getattr(scapy.all, proto)(repro)
                except struct.error:
                    ex.setdefault(proto, set()).add("struct.error")
                except Exception as e:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    exname=exc_type.__name__
                    if exname not in allowed:
                        for l in traceback.format_exc().splitlines()[-5:]:
                            print "# %s" % l
                        print "%s(%s)\n" % (proto, repr(repro))
                    ex.setdefault(proto, set()).add(str(exc_type.__name__))

for k in ex.keys():
    ex[k] = sorted(ex[k])

with open("seen-crashes.json","w") as f:
    json.dump(ex,f)
    

      
        

