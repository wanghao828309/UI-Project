# -*- coding: UTF-8 -*-

from xml.dom.minidom import parse, parseString


dom = parse('sample.xml')
root=dom.documentElement
print root

for child in root.childNodes:
    print child