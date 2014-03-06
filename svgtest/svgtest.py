## crop stuff from svg files.
## assume a large svg file with 1000+ nodes and you want to extract
## a minimal svg including the nodes that fall (even partially) into
## a given bounding box.

## copy kill of a js script done by Joel Uckelman


## IMPORTS

from lxml import etree
import shapely

## CONSTANTS

NS = "http://www.w3.org/2000/svg"

##

## MAIN

if __name__ == "__main__":
    #etree.register_namespace()
    svg = etree.parse("./test.svg")
    root = svg.getroot()
    print "####"
    etree.dump(root)
    print "####"
    for child in root:
        print child.tag
    print "####"
