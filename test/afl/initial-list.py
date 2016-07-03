from scapy.all import *
import sys
import inspect
import json
import base64

''' Quick & dirty hack to get all packet classes implemented in scapy
'''


def print_json(cls, args, samples):
    print(json.dumps([cls.__name__, args, [], samples]))

def get_samples(p):
    r=set()
    r.add(base64.b64encode(str(p)))
    try:
        f=fuzz(p)
        for i in range(0,5):
            r.add(base64.b64encode(str(p)))
    finally:
        return list(r)
             
def print_packet_subclasses():
    ps = []
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj) and issubclass(obj, Packet):
            ps.append(obj)
    fail = set()
    for s in ps:
        try:
            s(str(s()))
            print_json(s, '', get_samples(s()))
        except Exception as e:
            fail.add(s)
    for s in list(fail):
        try:
            s(str(s("a")))
            print_json(s, "'a'",get_samples(s("a")))
            fail.remove(s)
        except:
            pass
    for s in list(fail):
        print("# %s" % s.__name__)


print_packet_subclasses()
