# counter sheet to vassal

##---IMPORTS

from lxml import etree
from ods_files import counter_sheet_row_idx_set, get_sheet, Unit, LandUnit
from xml_parsing import GPIDGenerator, find_stack, PieceSlot

##---CONSTANTS

indent = '                        '
buildFile_base = '/home/pmeier/Workspace/WIFvassal/mod/buildFile_base.xml'
buildFile_new = '/home/pmeier/Workspace/WIFvassal/mod/WiFdab/buildFile'

##---FUNCTIONS

def get_control(u):
    if u.power == 'China':
        return {'Comm China': 'CC',
                'Nat China': 'CN'}[u.home]
    else:
        return {'Commonwealth': 'CW',
                'France': 'FR',
                'Germany': 'GE',
                'Italy': 'IT',
                'Japan': 'JP',
                'USSR': 'RU',
                'USA': 'US'}[u.power]


def get_type(u):
    rval = u.type
    if 'Div' in u.size:
        if u.clas == 'ART':
            if u.type not in ['AT', 'AA', 'AAA']:
                rval = rval[0] + rval[1:].lower()
            if 'mot' in u.other:
                rval = 'Mot ' + rval
            if 'self-prop' in u.other:
                if u.clas == 'AT':
                    rval = 'TD'
                else:
                    rval = 'SP ' + rval
        else:
            rval = rval[0] + rval[1:].lower()
    if u.type in ['CAV', 'FTR', 'LND', 'NAV', 'ATR', 'CVP', 'SYNTH']:
        rval += '-{:d}'.format(u.cost)
    return rval


def inject_land(cs_no):
    """land units"""

    # init build file
    bf = None
    with open(buildFile_base, 'r') as f:
        bf = etree.parse(f)
    gpid = GPIDGenerator(bf)
    stack = find_stack(bf, cs_no, 'LND')

    # init ods file
    LAND = get_sheet('Land')
    header = Unit.read_header(LAND)
    cs_rids = counter_sheet_row_idx_set(LAND, cs_no)
    for rid in cs_rids:
        # load unit
        lu = LandUnit()
        lu.update(LAND, rid, header)

        # piece slot
        img_name = 'cs{:02d}_{:02d}_{:02d}.png'.format(
            cs_no, lu.row, lu.col)
        ps = PieceSlot(lu.unit, gpid.get(), img_name)
        ps.add_trait('mark', ('kit', lu.kit))
        ps.add_trait('mark', ('cs_col', lu.col))
        ps.add_trait('mark', ('cs_row', lu.row))
        ps.add_trait('mark', ('cs_no', lu.cs))
        ps.add_trait('mark', ('MOV', lu.mov))
        if lu.rog:
            ps.add_trait('mark', ('ROG', lu.rog))
        ps.add_trait('mark', ('STR', lu.str))
        ps.add_trait('prototype', (get_type(lu), ''))
        ps.add_trait('prototype', ('Control' + get_control(lu), ''))
        stack.append(ps.get_xml())

    bf.write(buildFile_new, pretty_print=True)

##---MAIN

if __name__ == '__main__':
    inject_land(1)
