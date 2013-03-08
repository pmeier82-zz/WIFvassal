# XML parsing for the buildFile of the vassal module

##---IMPORTS

from lxml import etree, objectify

##---CONSTANTS

##---FUNCTIONS

def find_cs_map(tree):
    a = tree.find('VASSAL.build.module.ChartWindow')
    b = a.find('VASSAL.build.widget.TabWidget')
    c = b.find('VASSAL.build.widget.MapWidget')
    d = c.find('VASSAL.build.widget.WidgetMap')
    e = d.find('VASSAL.build.module.map.SetupStack')
    f = e.findall('VASSAL.build.widget.PieceSlot')
    return a, b, c, d, e,f

##---MAIN

if __name__ == '__main__':
    bf = None
    #with open('buildFile', 'r') as f:
        #bf = etree.parse(f)
    bf = objectify.parse(open('buildFile', 'r'))

    print etree.tostring(bf, pretty_print=True)
    print '#' * 20
    #print find_cs_map(bf)
