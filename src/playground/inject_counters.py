# counter sheet to vassal

##---IMPORTS

from lxml import etree
from ods_files import counter_sheet_row_idx_set, get_sheet, Unit, LandUnit,\
    AirUnit, NavalUnit
from xml_parsing import GPIDGenerator, find_stack, PieceSlot

##---CONSTANTS

indent = '                        '
BF_base = '/home/pmeier/Workspace/WIFvassal/mod/buildFile_base.xml'
BF_new = '/home/pmeier/Workspace/WIFvassal/mod/WiFdab/buildFile'

##---FUNCTIONS

def start(path=None):
    global BF, GPID
    with open(path or BF_base, 'r') as f:
        BF = etree.parse(f)
    GPID = GPIDGenerator(BF)


def finish(path=None):
    global BF
    BF.write(path or BF_new, pretty_print=True)


def get_control(u):
    try:
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
    except:
        return 'Minor'


def get_type(u):
    rval = u.type
    if 'Div' in getattr(u, 'size', ''):
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
    if u.type in ['CAV', 'SYNTH', 'ATR', 'CVP', 'FTR', 'LND', 'NAV']:
        rval += '-{:d}'.format(u.cost)
    if u.type in ['ASW', 'CV', 'CVL']:
        rval += '-{:d}'.format(u.time)
    return rval


def inject_land(cs_no):
    # init
    global BF, GPID
    stack = find_stack(BF, cs_no, 'LND')
    sheet = get_sheet('Land')
    header = Unit.read_header(sheet)
    cs_rids = counter_sheet_row_idx_set(sheet, cs_no)
    assert stack is not None and\
           sheet is not None and\
           header is not None and\
           cs_rids is not None, 'setup error cs_no: %d' % cs_no

    # produce counters and piece slots
    for rid in cs_rids:
        # load unit
        u = LandUnit()
        u.update(sheet, rid, header)

        # piece slot
        img = 'cs{:02d}_{:02d}_{:02d}.png'.format(
            cs_no, u.row, u.col)
        ps = PieceSlot(u.name, GPID.get(), img)
        ps.add_trait('mark', ('kit', u.kit))
        ps.add_trait('mark', ('cs_col', u.col))
        ps.add_trait('mark', ('cs_row', u.row))
        ps.add_trait('mark', ('cs_no', u.cs))
        ps.add_trait('mark', ('YEAR', u.year))
        ps.add_trait('mark', ('MOV', u.mov))
        if u.rog:
            ps.add_trait('mark', ('ROG', u.rog))
        ps.add_trait('mark', ('STR', u.str))
        ps.add_trait('prototype', (get_type(u), ''))
        ps.add_trait('prototype', ('Control' + get_control(u), ''))
        stack.append(ps.get_xml())


def inject_air(cs_no):
    # init
    global BF, GPID
    stack = find_stack(BF, cs_no, 'AIR')
    sheet = get_sheet('Air')
    header = Unit.read_header(sheet)
    cs_rids = counter_sheet_row_idx_set(sheet, cs_no)
    assert stack is not None and\
           sheet is not None and\
           header is not None and\
           cs_rids is not None, 'setup error cs_no: %d' % cs_no

    # produce counters and piece slots
    for rid in cs_rids:
        # load unit
        u = AirUnit()
        u.update(sheet, rid, header)

        # piece slot
        img = 'cs{:02d}_{:02d}_{:02d}.png'.format(
            cs_no, u.row, u.col)
        ps = PieceSlot(' '.join([u.name, u.name2]).strip(), GPID.get(), img)
        ps.add_trait('mark', ('kit', u.kit))
        ps.add_trait('mark', ('cs_col', u.col))
        ps.add_trait('mark', ('cs_row', u.row))
        ps.add_trait('mark', ('cs_no', u.cs))
        ps.add_trait('mark', ('YEAR', u.year))
        if u.cvp_y1 is not None:
            ps.add_trait('mark', ('CVP_Y1', u.cvp_y1))
        if u.cvp_y1 is not None:
            ps.add_trait('mark', ('CVP_Y2', u.cvp_y2))
        if u.cvp_y1 is not None:
            ps.add_trait('mark', ('CVP_Y3', u.cvp_y3))
        if u.cvp_s1 is not None:
            ps.add_trait('mark', ('CVP_S1', u.cvp_s1))
        if u.cvp_s2 is not None:
            ps.add_trait('mark', ('CVP_S2', u.cvp_s2))
        if u.cvp_s3 is not None:
            ps.add_trait('mark', ('CVP_S3', u.cvp_s3))
        if u.str is not None:
            ps.add_trait('mark', ('STR', u.str))
        if u.str is not None:
            ps.add_trait('mark', ('STR', u.str))
        if u.tac is not None:
            ps.add_trait('mark', ('TAC', u.tac))
        if u.ats is not None:
            ps.add_trait('mark', ('ATS', u.ats))
        if u.ata is not None:
            ps.add_trait('mark', ('ATA', u.ata))
        ps.add_trait('prototype', (get_type(u), ''))
        ps.add_trait('prototype', ('Control' + get_control(u), ''))
        stack.append(ps.get_xml())


def inject_sea(cs_no):
    # init
    global BF, GPID
    stack = find_stack(BF, cs_no, 'SEA')
    sheet = get_sheet('Naval')
    header = Unit.read_header(sheet)
    cs_rids = counter_sheet_row_idx_set(sheet, cs_no)
    assert stack is not None and\
           sheet is not None and\
           header is not None and\
           cs_rids is not None, 'setup error cs_no: %d' % cs_no

    # produce counters and piece slots
    for rid in cs_rids:
        # load unit
        u = NavalUnit()
        u.update(sheet, rid, header)
        if u.type == 'CONV':
            continue

        # piece slot
        img = 'cs{:02d}_{:02d}_{:02d}.png'.format(
            cs_no, u.row, u.col)
        ps = PieceSlot(' '.join([u.name, u.name2]).strip(), GPID.get(), img)
        ps.add_trait('mark', ('kit', u.kit))
        ps.add_trait('mark', ('cs_col', u.col))
        ps.add_trait('mark', ('cs_row', u.row))
        ps.add_trait('mark', ('cs_no', u.cs))
        ps.add_trait('mark', ('YEAR', u.year))
        ps.add_trait('mark', ('RNG', u.rng))
        ps.add_trait('mark', ('MOV', u.mov))
        if u.cv is not None:
            ps.add_trait('mark', ('CV', u.cv))
        if u.sb is not None:
            ps.add_trait('mark', ('SB', u.sb))
        ps.add_trait('mark', ('AA', u.aa))
        ps.add_trait('mark', ('DEF', u.dfs))
        ps.add_trait('mark', ('ATT', u.att))
        ps.add_trait('prototype', (get_type(u), ''))
        ps.add_trait('prototype', ('Control' + get_control(u), ''))
        stack.append(ps.get_xml())

##---MAIN

if __name__ == '__main__':
    # init
    CS = 1

    # process
    start()
    inject_land(CS)
    inject_air(CS)
    inject_sea(CS)
    finish()
