import os

for root, dirs, files in os.walk('stub'):
    if 'crashes' in root:
        if len(files) > 0:
            _,proto,_,_ = root.split('/')
            repros = filter(lambda x: x.startswith('id:'),files)
            for r in repros:
                print "%s(%s)" % (proto, repr(open("%s/%s" % (root, r)).read()) )

      
        

