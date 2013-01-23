#!/usr/bin/python
from xml.etree import ElementTree
import sys

#NOTE: this code works except for cases with xsi namespace information
#In these cases, ElementTree seems to be buggy and give up... 

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def main():
#USAGE example
    if len(sys.argv) != 2: 
        print( "Usage: " + sys.argv[0] + " <XML file>")
        sys.exit(1) 
        
    root = ElementTree.parse(sys.argv[1]).getroot()
    #root = ElementTree.parse('/tmp/xmlfile').getroot()
    indent(root)
    print ElementTree.dump(root)

if __name__ == '__main__':
    main()
