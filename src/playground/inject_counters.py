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
            'WiFdab_ext/WiFdab_counters/buildFile'
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
    GPID = GPIDGenerator(BF)
    if 'extensionId' in BF.getroot().attrib:
        EXT = unicode(BF.getroot().attrib['extensionId'])
    SHEET['L'] = get_sheet('Land')
    HEADER['L'] = Unit.read_header(SHEET['L'])
    SHEET['A'] = get_sheet('Air')
    HEADER['A'] = Unit.read_header(SHEET['A'])
    SHEET['N'] = get_sheet('Naval')
    HEADER['N'] = Unit.read_header(SHEET['N'])


def finish(path=None):
    global BF, GPID
    if path is None:
        if EXT is not None:
            path = BF_new_ex
        else:
            path = BF_new
    BF.getroot().attrib['nextPieceSlotId'] = u'{:d}'.format(GPID.get())
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
                if u.type == 'AT':
                    rval = 'TD'
                else:
                    rval = 'SP ' + rval
        else:
            rval = rval[0] + rval[1:].lower()
    if u.type in ['CAV', 'SYNTH', 'ATR', 'CVP', 'FTR', 'LND', 'NAV']:
        try:
            rval += '-{:d}'.format(u.cost)
        except:
            pass
    if u.type in ['ASW', 'CV', 'CVL']:
        try:
            rval += '-{:d}'.format(u.time)
        except:
            pass
    return rval


def get_parent(cs_no, kind):
    global BF, EXT
    if EXT is None:
        return find_stack(BF, cs_no, kind)
    else:
        return BF.getroot()


def ext_item(cs_no, kind):
    return etree.Element(
        'VASSAL.build.module.ExtensionElement',
        attrib={
            'target': 'VASSAL.build.module.ChartWindow:Counter Sheets/'
                      'VASSAL.build.widget.TabWidget:tabs/'
                      'VASSAL.build.widget.MapWidget:CS {:02d}/'
                      'VASSAL.build.widget.WidgetMap:Counter Sheet 1/'
                      'VASSAL.build.module.map.SetupStack:{:s}'.
            format(cs_no, kind)})


def inject_land(cs_no):
    # init
    global BF, EXT, GPID, HEADER, SHEET
    cs_rids = counter_sheet_row_idx_set(SHEET['L'], cs_no)
    parent = get_parent(cs_no, 'LND')

    # produce counters and piece slots
    for rid in cs_rids:
        try:
            # load unit
            u = LandUnit()
            u.update(SHEET['L'], rid, HEADER['L'])
            assert not u.deleted, 'deleted!'

            # piece slot
            img = 'cs{:02d}_{:02d}_{:02d}.png'.format(cs_no, u.row, u.col)
            ps = PieceSlot(u.name, GPID.get(), img, ext=EXT)
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
            if EXT is None:
                parent.append(ps.get_xml())
            else:
                ei = ext_item(cs_no, 'LND')
                ei.append(ps.get_xml())
                parent.append(ei)
        except Exception, ex:
            print 'skipping row:', u.sh_row, str(ex)
            continue


def inject_air(cs_no):
    # init
    global BF, EXT, GPID, HEADER, SHEET
    cs_rids = counter_sheet_row_idx_set(SHEET['A'], cs_no)
    parent = get_parent(cs_no, 'AIR')

    # produce counters and piece slots
    for rid in cs_rids:
        try:
            # load unit
            u = AirUnit()
            u.update(SHEET['A'], rid, HEADER['A'])
            assert u.type not in ['PILOT'], 'skipped for type {}'.format(u.type)
            assert not u.deleted, 'deleted!'

            # piece slot
            img = 'cs{:02d}_{:02d}_{:02d}.png'.format(cs_no, u.row, u.col)
            ps = PieceSlot(
                ' '.join([u.name, u.name2]).strip(), GPID.get(), img, ext=EXT)
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
            if EXT is None:
                parent.append(ps.get_xml())
            else:
                ei = ext_item(cs_no, 'AIR')
                ei.append(ps.get_xml())
                parent.append(ei)
        except Exception, ex:
            print 'skipping row:', u.sh_row, str(ex)
            continue


def inject_sea(cs_no):
    # init
    global BF, EXT, GPID, HEADER, SHEET
    cs_rids = counter_sheet_row_idx_set(SHEET['N'], cs_no)
    parent = get_parent(cs_no, 'SEA')

    # produce counters and piece slots
    for rid in cs_rids:
        try:
            # load unit
            u = NavalUnit()
            u.update(SHEET['N'], rid, HEADER['N'])
            assert u.type not in ['CONV'], 'skipped for type {}'.format(u.type)
            assert not u.deleted, 'deleted!'

            # piece slot
            img = 'cs{:02d}_{:02d}_{:02d}.png'.format(cs_no, u.row, u.col)
            ps = PieceSlot(
                ' '.join([u.name, u.name2]).strip(), GPID.get(), img, ext=EXT)
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
            if EXT is None:
                parent.append(ps.get_xml())
            else:
                ei = ext_item(cs_no, 'SEA')
                ei.append(ps.get_xml())
                parent.append(ei)
        except Exception, ex:
            print 'skipping row:', u.sh_row, str(ex)
        continue

##---MAIN

if __name__ == '__main__':
    do_extension = False
    start(ext=do_extension)
    print 'START'
    for cs in CSrange:
        print 'CS', cs
        print 'land'
        inject_land(cs)
        print 'air'
        inject_air(cs)
        print 'sea'
        inject_sea(cs)
        print '..done!'
    print 'FINISH'
    finish()
