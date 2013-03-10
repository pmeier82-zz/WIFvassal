# XML parsing for the buildFile of the vassal module

##---IMPORTS

from lxml import etree, objectify

##---CONSTANTS

##---CLASSES

class GPIDGenerator(object):
    def __init__(self, tree=None):
        self.gpid_set = set([])
        if tree:
            self.update_from_tree(tree)

    def update_from_tree(self, tree):
        tree_gpid_set = set(
            [int(ps.attrib['gpid'])
             for ps in tree.iter('VASSAL.build.widget.PieceSlot')])
        if len(self.gpid_set.intersection(tree_gpid_set)) > 0:
            raise ValueError('gpid set has intersection!!')
        self.gpid_set.update(tree_gpid_set)

    def get(self):
        rval = max(self.gpid_set) + 1
        self.gpid_set.add(rval)
        return rval

GPID = GPIDGenerator()

class Trait(object):
    def __init__(self, kind, *params):
        self.kind = str(kind)
        self.params = params

    def definition(self):
        return ';'.join([self.kind] + [str(p[0]) for p in self.params])

    def parameters(self):
        return ';'.join([str(p[1]) for p in self.params])


class PieceSlot(object):
    def __init__(self, name, gpid, img, h=0, w=0):
        self.name = str(name)
        self.gpid = int(gpid)
        self.img = str(img)
        self.height = int(h)
        self.width = int(w)
        self.traits = []

    def get_xml(self):
        rval = etree.Element(
            'VASSAL.build.widget.PieceSlot',
            attrib={
                'entryName': self.name,
                'gpid': str(self.gpid),
                'height': str(self.height),
                'width': str(self.width)})
        rval.text = self.traits_text()
        return rval

    def get_xml_str(self):
        return etree.tostring(self.get_xml(), pretty_print=True)

    def traits_text(self):
        tdef = []
        for i, t in enumerate(self.traits):
            tdef.append(t.definition())
            tdef.append('\\' * i + '\t')
        tdef.append('piece;;;{:s};{:s}'.format(self.img, self.name))
        tpar = []
        for i, t in enumerate(self.traits):
            tpar.append(t.parameters())
            tpar.append('\\' * i + '\t')
        tpar.append('null;0;0;{:d}'.format(self.gpid))
        return ''.join(['+/null/'] + tdef + ['/'] + tpar)

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


def write_land_piece(name='test', gpid=None):
    if gpid is None:
        gpid = GPID
    p = PieceSlot('test', gpid.get(), 'BG_W.png')
    p.add_trait('mark', ('MV', 3))
    p.add_trait('mark', ('ST', 4))
    return p.get_xml_str()


##---MAIN

if __name__ == '__main__':
    bf = None
    with open('/home/pmeier/Workspace/WIFvassal/mod/buildFile_base.xml',
              'r') as f:
        bf = etree.parse(f)
    GPID.update_from_tree(bf)

    print '#' * 20
    stack = find_stack(bf)
    print stack
    print etree.tostring(stack, pretty_print=True)

    print '#' * 20
    print write_land_piece()
