import sys
import os
import afl
import exceptions
import importlib


def import_by_name(name, root=exceptions):
    if "." in name:
        path, _, name = name.rpartition(".")
        try:
            root = importlib.import_module(path)
        except ImportError:
            raise AttributeError("Module %s not found" % path)

    try:
        return getattr(root, name)
    except AttributeError:
        raise AttributeError("Class %s.%s not found" % (root.__name__, name))

try:
    cls = import_by_name(sys.argv[1])
except AttributeError as e:
    exit(e)
except IndexError:
    exit("Usage: %s <classname> <exception1> <exception2> ...." % sys.argv[0])

try:
    catched_exceptions = tuple(map(import_by_name, sys.argv[2:]))
except AttributeError as e:
    exit(e)

while afl.loop(1000):
    try:
        cls(sys.stdin.read())
    except catched_exceptions as e:
        pass
os._exit(0)
