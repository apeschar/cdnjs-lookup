#!/usr/bin/env python2.7

import time
import os
import os.path
from hashlib import sha256
from base64 import b32encode


ZONE = 'cdnjs.phastcdn.net'
LABEL = '%s.cdnjs.phastcdn.net'
NS = 'sisi.kibohost.com'
HOSTMASTER = '.'.join(['hostmaster'] + NS.split('.')[1:])

if __name__ == '__main__':

    serial = str(int(time.time()))

    print '$ORIGIN .'
    print '%s 1800 IN SOA %s %s %s 1800 1800 604800 300' % (ZONE, NS, HOSTMASTER, serial)
    print '%s 1800 IN NS %s' % (ZONE, NS)

    seen = set()

    for folder, _, files in os.walk('cdnjs/ajax/libs'):
        for filename in files:
            path = os.path.join(folder, filename)

            try:
                path.decode('ascii')
            except UnicodeDecodeError:
                continue

            digest = sha256(open(path, 'r').read()).digest()

            if digest in seen: continue
            seen.add(digest)

            digest32 = b32encode(digest).decode('ascii').rstrip('=').lower()

            url = 'https://cdnjs.cloudflare.com/' + '/'.join(path.split('/')[1:])

            print '%s 86400 IN TXT "%s"' % (LABEL % digest32, url)
