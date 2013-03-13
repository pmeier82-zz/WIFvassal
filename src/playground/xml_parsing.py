# -*- coding: utf-8 -*-
# XML parsing for the buildFile of the vassal module
# changelog:
# * making it unicode safe

##---IMPORTS

from lxml import etree

##---CLASSES

class GPIDGenerator(object):
    def __init__(self, tree=None):
        self.gpid_set = set([])
        if tree:
            self.update_from_tree(tree)

    def update_from_tree(self, tree):
        tree_gpid_set = set(
            [int(ps.attrib['gpid'].split(':')[-1])
             for ps in tree.iter('VASSAL.build.widget.PieceSlot')])
        if len(self.gpid_set.intersection(tree_gpid_set)) > 0:
            raise ValueError('gpid set has intersection!!')
        self.gpid_set.update(tree_gpid_set)

    def get(self):
        try:
            rval = max(self.gpid_set) + 1
        except:
            rval = 1
        finally:
            self.gpid_set.add(rval)
            return rval


class Trait(object):
    def __init__(self, kind, *params):
        self.kind = unicode(kind)
        self.params = params

    def definition(self):
        return u';'.join([self.kind] + [unicode(p[0]) for p in self.params])

    def parameters(self):
        return u';'.join([unicode(p[1]) for p in self.params])


class PieceSlot(object):
    def __init__(self, name, gpid, img, h=0, w=0, ext=None):
        self.name = unicode(name)
        self.gpid = u'{}{:d}'.format(
            u'' if ext is None else u'{}:'.format(ext),
            gpid)
        self.img = unicode(img)
        self.height = unicode(h)
        self.width = unicode(w)
        self.traits = []

    def get_xml(self):
        rval = etree.Element(
            'VASSAL.build.widget.PieceSlot',
            attrib={
                'entryName': self.name,
                'gpid': self.gpid,
                'height': self.height,
                'width': self.width})
        rval.text = self.traits_text()
        return rval

    def get_xml_str(self):
        return etree.tostring(self.get_xml(), pretty_print=True)

    def traits_text(self):
        tdef = []
        for i, t in enumerate(self.traits):
            tdef.append(t.definition())
            tdef.append(u'\\' * i + u'\t')
        tdef.append(u'piece;;;{};{}'.format(self.img, self.name))
        tpar = []
        for i, t in enumerate(self.traits):
            tpar.append(t.parameters())
            tpar.append(u'\\' * i + u'\t')
        tpar.append(u'null;0;0;{}'.format(self.gpid))
        return u''.join([u'+/null/'] + tdef + [u'/'] + tpar)

    def add_trait(self, *args, **kwargs):
        self.traits.append(Trait(*args, **kwargs))

##---FUNCTIONS

def find_stack(tree, csno=1, kind='LND'):
    xpath = '/*/VASSAL.build.module.ChartWindow/*/'\
            'VASSAL.build.widget.MapWidget[@entryName="CS {:02d}"]/*/'\
            'VASSAL.build.module.map.SetupStack[@name="{:s}"]'
    try:
        return tree.xpath(xpath.format(csno, kind))[0]
    except:
        return None


def write_land_piece(name, gpid):
    p = PieceSlot('test', gpid.get(), 'BG_W.png')
    p.add_trait('mark', ('MV', 3))
    p.add_trait('mark', ('ST', 4))
    return p.get_xml_str()


##---MAIN

if __name__ == '__main__':
    bf = etree.parse(
        open('/home/pmeier/Workspace/WIFvassal/mod/buildFile_base', 'r'))
    GPID = GPIDGenerator(bf)

    print '#' * 20
    stack = find_stack(bf)
    print stack
    print etree.tostring(stack, pretty_print=True)

    print '#' * 20
    print write_land_piece('test', GPID)

    print '#' * 20
    print etree.tostring(bf.getroot(), pretty_print=True)
