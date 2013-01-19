#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zipfile, os
import sys
path= os.getcwd()
path = os.path.join(path,sys.argv[1])
zip = zipfile.ZipFile(path+'.zip', 'w', zipfile.ZIP_DEFLATED)
for root, dirs, files in os.walk(path):
    for f in files:
        zip.write(os.path.join(root, f), \
        os.path.join(root,f).replace(path+os.sep, ''))

zip.close()