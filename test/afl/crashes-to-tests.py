import os
from scapy.all import *
import traceback

for root, dirs, files in os.walk('stub'):
    if 'crashes' in root:
        if len(files) > 0:
            _,proto,_,_ = root.split('/')
            repros = filter(lambda x: x.startswith('id:'),files)
            for r in repros:
                with  open("%s/%s" % (root, r)) as f:
                    repro = f.read()
                print "%s(%s)" % (proto, repr(repro) )
                try:
                    getattr(scapy.all, proto)(repro)
                except Exception as e:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
#                    traceback.print_exc(file=sys.stdout)
#                print "---"


      
        

