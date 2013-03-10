# counter sheet to vassal

##---IMPORTS

from lxml import etree
from ods_files import counter_sheet_row_idx_set, get_sheet, Unit, LandUnit
from xml_parsing import GPIDGenerator, find_stack, PieceSlot

##---CONSTANTS

indent = '                        '
buildFile_base = '/home/pmeier/Workspace/WIFvassal/mod/buildFile_base'
buildFile_new = '/home/pmeier/Workspace/WIFvassal/mod/WiFdab/buildFile'

##---FUNCTIONS

def get_control(u):
    if u.u_power == 'China':
        return {'Comm China': 'CC',
                'Nat China': 'CN'}[u.u_home]
    else:
        return {'Commonwealth': 'CW',
                'France': 'FR',
                'Germany': 'GE',
                'Italy': 'IT',
                'Japan': 'JP',
                'USSR': 'RU',
                'USA': 'US'}[u.u_power]


def get_type(u):
    rval = u.u_type
    if 'Div' in u.lu_size:
        if u.u_class == 'ART':
            if u.u_type not in ['AT', 'AA', 'AAA']:
                rval = rval[0] + rval[1:].lower()
            if 'mot' in u.lu_other:
                rval = 'Mot ' + rval
            if 'self-prop' in u.lu_other:
                if u.u_class == 'AT':
                    rval = 'TD'
                else:
                    rval = 'SP ' + rval
        else:
            rval = rval[0] + rval[1:].lower()
    if u.u_type in ['CAV', 'FTR', 'LND', 'NAV', 'ATR', 'CVP', 'SYNTH']:
        rval += '-{:d}'.format(u.lu_cost)
    return rval


def inject_land(cs_no):
    """land units"""

    # init build file
    bf = None
    with open(buildFile, 'r') as f:
        bf = etree.parse(f)
    gpid = GPIDGenerator(bf)
    stack = find_stack(bf, cs_no, 'LAND')

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
            cs_no, lu.u_row, lu.u_col)
        ps = PieceSlot(lu.lu_unit, gpid.get(), img_name)
        ps.add_trait('mark', ('kit', lu.u_kit))
        ps.add_trait('mark', ('cs_col', lu.u_col))
        ps.add_trait('mark', ('cs_row', lu.u_row))
        ps.add_trait('mark', ('cs_no', lu.u_cs))
        ps.add_trait('mark', ('MOV', lu.lu_mov))
        if lu.lu_rog:
            ps.add_trait('mark', ('ROG', lu.lu_rog))
        ps.add_trait('mark', ('STR', lu.lu_str))
        ps.add_trait('prototype', (get_type(lu), ''))
        ps.add_trait('prototype', ('Control' + get_control(lu), ''))
        stack.append(ps.get_xml())

    bf.write(buildFile_new, pretty_print=True)

##---MAIN

if __name__ == '__main__':
    inject_land(1)
