# -*- coding: utf-8 -*-
import hashlib
f = open("/home/ego/mpg/Rossana_hh.wmv", "rb")
h = hashlib.md5()
h.update(f.read())
hash = h.hexdigest()
f.close()
