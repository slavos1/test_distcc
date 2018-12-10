#!/usr/bin/env python3
import sys
from pathlib import Path
import os
import re

IGNORED_DIRS = re.compile('/?({})/'.format('|'.join(set('''
nodejs
c\+\+
libspreadsheet.*?
lxappearance
python3\.6m
bits
asm\-generic
.*?_ipv4
linux
openssl
drm
rpcsvc
sys
hfi
rpc
xen
asm
'''.strip().split()))))
#print(IGNORED_DIRS.pattern)

IGNORED_HEADERS = set('''
pcmanfm-modules.h
regexp.h
lib-names-64.h
elf.h
privcmd.h
libio.h
patchkey.h
ip6t_LOG.h
ipt_LOG.h
'''.strip().split())

def list_includes(root=None):
    if root is None:
        root = Path('/usr/include')
    for r,d,files in os.walk(str(root)):
        r = Path(r)
        for f in files:
            if f.startswith('_') or f in IGNORED_HEADERS:
                continue
            yield r.joinpath(f).relative_to(root)

if __name__ == '__main__':
    includes = sorted(list_includes())
    for i in range(1, int(sys.argv[1]) + 1):
        p = Path('test_{:02d}.cpp'.format(i))
        with p.open('w') as out:
            for inc in includes:
                if not IGNORED_DIRS.search(str(inc)):
                    print('#include <{}>'.format(inc), file=out)
            out.write('''
#ifdef MY_GCC
//#error MY_GCC was defined, hey!
#endif
static const int this_is_error = "abc";
int foo_{:02d}(){{return 0;}}
'''.format(i))
        print(str(p))

