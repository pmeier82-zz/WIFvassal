# -*- coding: utf-8 -*-
# counter sheet to vassal

##---IMPORTS

from lxml import etree
from ods_files import counter_sheet_row_idx_set, get_sheet, Unit, LandUnit,\
    AirUnit, NavalUnit
from xml_parsing import GPIDGenerator, find_stack, PieceSlot

##---CONSTANTS

BF_base = '/home/pmeier/Workspace/WIFvassal/mod/'\
          'buildFile_base.xml'
BF_base_ex = '/home/pmeier/Workspace/WIFvassal/mod/'\
             'buildFile_counters_base.xml'
BF_new = '/home/pmeier/Workspace/WIFvassal/mod/'\
         'WiFdab/buildFile'
BF_new_ex = '/home/pmeier/Workspace/WIFvassal/mod/'\
            'WiFdab/WiFdab_counters/buildFile'
CSrange = [1, 2, 3, 4, 5, 6, 7, 8, 9, 14, 15, 18, 19, 20, 21, 22, 23, 24]

SHEET = {}
HEADER = {}
GPID = None
BF = None
EXT = None

##---FUNCTIONS

def start(path=None, ext=False):
    global BF, EXT, GPID, HEADER, SHEET
    if path is None:
        if ext is False:
            path = BF_base
        else:
            path = BF_base_ex
    with open(path, 'r') as f:
        BF = etree.parse(f)
    GPID = GPIDGenerator()
    if 'extensionId' in BF.getroot().attrib:
        EXT = unicode(BF.getroot().attrib['extensionId'])
    else:
        GPID.update_from_tree(BF)
    SHEET['L'] = get_sheet('Land')
    HEADER['L'] = Unit.read_header(SHEET['L'])
    SHEET['A'] = get_sheet('Air')
    HEADER['A'] = Unit.read_header(SHEET['A'])
    SHEET['N'] = get_sheet('Naval')
    HEADER['N'] = Unit.read_header(SHEET['N'])


def finish(path=None, ext=False):
    global BF
    if path is None:
        if ext is False:
            path = BF_base
        else:
            path = BF_base_ex
    BF.write(
        path,
        encoding='UTF-8',
        method='xml',
        xml_declaration=True,
        pretty_print=True)


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


def build_ext_parent(_, cs_no, kind):
    global BF
    rval = etree.Element(
        'VASSAL.build.module.ExtensionElement',
        attrib={
            'target': 'VASSAL.build.module.ChartWindow:Counter Sheets/'
                      'VASSAL.build.widget.TabWidget:tabs/'
                      'VASSAL.build.widget.MapWidget:CS {:02d}/'
                      'VASSAL.build.widget.WidgetMap:Counter Sheet 1/'
                      'VASSAL.build.module.map.SetupStack:{:s}'.
            format(cs_no, kind)})
    BF.append(rval)
    return rval


get_parent = find_stack if EXT is None else build_ext_parent


def inject_land(cs_no, parent):
    # init
    global BF, GPID, HEADER, SHEET
    cs_rids = counter_sheet_row_idx_set(SHEET['L'], cs_no)

    # produce counters and piece slots
    for rid in cs_rids:
        # load unit
        u = LandUnit()
        u.update(SHEET['L'], rid, HEADER['L'])

        # piece slot
        try:
            img = 'cs{:02d}_{:02d}_{:02d}.png'.format(cs_no, u.row, u.col)
        except:
            continue
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
        parent.append(ps.get_xml())


def inject_air(cs_no, parent):
    # init
    global BF, GPID, HEADER, SHEET
    cs_rids = counter_sheet_row_idx_set(SHEET['A'], cs_no)

    # produce counters and piece slots
    for rid in cs_rids:
        # load unit
        u = AirUnit()
        u.update(SHEET['A'], rid, HEADER['A'])

        # piece slot
        try:
            img = 'cs{:02d}_{:02d}_{:02d}.png'.format(cs_no, u.row, u.col)
        except:
            continue
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
        parent.append(ps.get_xml())


def inject_sea(cs_no, parent):
    # init
    global BF, GPID, HEADER, SHEET
    cs_rids = counter_sheet_row_idx_set(SHEET['N'], cs_no)

    # produce counters and piece slots
    for rid in cs_rids:
        # load unit
        u = NavalUnit()
        u.update(SHEET['N'], rid, HEADER['N'])
        if u.type == 'CONV':
            continue

        # piece slot
        try:
            img = 'cs{:02d}_{:02d}_{:02d}.png'.format(cs_no, u.row, u.col)
        except:
            continue
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
        parent.append(ps.get_xml())

##---MAIN

if __name__ == '__main__':
    do_extension = True
    start(ext=do_extension)
    print 'START'
    for cs in [24]:
        print 'CS', cs,
        #print '\tland',
        #inject_land(cs)
        #print '\tair',
        #inject_air(cs)
        print '\tsea',
        p = get_parent(BF, cs, 'SEA')
        inject_sea(cs, p)
        print '\t..done!'
    print 'FINISH'
    finish(ext=do_extension)
