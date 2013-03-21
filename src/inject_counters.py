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
CSrange = [1, 2, 3, 4, 5, 6, 24, # WIF FE
           7, 8, 9, # PiF
           14, # AfA
           15, # AsA
           18, 19, 20, 21, 22, # SiF
           23, # MiF
]

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


def cs_pos(cs_no, cs_row, _cs_col):
    return etree.Element(
        'VASSAL.build.widget.MapWidget',
        target='VASSAL.build.module.ChartWindow:Counter Sheets/'
               'VASSAL.build.widget.TabWidget:tabs/'
               'VASSAL.build.widget.MapWidget:CS {:02d}/'
               'VASSAL.build.widget.WidgetMap:Counter Sheet 1/'
               'VASSAL.build.module.map.SetupStack:lala'.
        format(cs_no))


def get_cs_parent(cs_no):
    global BF, EXT

    # tab widget
    if EXT is None:
        cs_tab = BF.find('/*/VASSAL.build.widget.TabWidget'
                         '[@entryName="cs_tab"]')
    else:
        cs_tab = BF.find(
            'VASSAL.build.module.ExtensionElement[@target="'
            'VASSAL.build.module.ChartWindow:Counter '
            'Sheets/VASSAL.build.widget.TabWidget:cs_tab"]')
        if cs_tab is None:
            cs_tab = etree.SubElement(
                BF.getroot(),
                'VASSAL.build.module.ExtensionElement',
                target='VASSAL.build.module.ChartWindow:Counter Sheets/'
                       'VASSAL.build.widget.TabWidget:cs_tab')

    # map widget
    mw = cs_tab.find(
        'VASSAL.build.widget.MapWidget[@entryName="CS {:02d}"]'
        .format(cs_no))
    if mw is not None:
        return mw.find('VASSAL.build.widget.WidgetMap')
    else:
        mw = etree.SubElement(
            cs_tab,
            'VASSAL.build.widget.MapWidget',
            entryName='CS {:02d}'.format(cs_no))

    # widget map
    mw_wm = etree.SubElement(
        mw,
        'VASSAL.build.widget.WidgetMap',
        allowMultiple='false',
        backgroundcolor='255,255,255',
        buttonName='Map',
        changeFormat='$message$',
        color='204,0,204',
        createFormat='$pieceName$ created in $location$',
        edgeHeight='0',
        edgeWidth='0',
        hotkey='',
        icon='',
        launch='false',
        mapName='Counter Sheet {:d}'.format(cs_no),
        markMoved='Never',
        markUnmovedIcon='',
        markUnmovedText='',
        markUnmovedTooltip='',
        moveKey='67,715',
        moveToFormat='$pieceName$ moves $previousLocation$ -> $location$ *',
        moveWithinFormat='$pieceName$ moves $previousLocation$ -> $location$ *',
        thickness='1')
    # board picker
    mw_wm_bp = etree.SubElement(
        mw_wm,
        'VASSAL.build.module.map.BoardPicker',
        addColumnText='Add column',
        addRowText='Add row',
        boardPrompt='Select board',
        slotHeight='125',
        slotScale='0.2',
        slotWidth='350',
        title='Choose Boards')
    mw_wm_bp_setup = etree.SubElement(mw_wm_bp, 'setup')
    mw_wm_bp_setup.text = 'Counter Sheet 1BoardPicker\t\t0\t0'
    mw_wm_bp_bd = etree.SubElement(
        mw_wm_bp,
        'VASSAL.build.module.map.boardPicker.Board',
        color='204,204,204',
        height='803',
        name='',
        reversible='false',
        width='1603')
    mw_wm_bp_bd_sg = etree.SubElement(
        mw_wm_bp_bd,
        'VASSAL.build.module.map.boardPicker.board.SquareGrid',
        color='0,0,0',
        cornersLegal='false',
        dotsVisible='false',
        dx='80.0',
        dy='80.0',
        edgesLegal='false',
        range='Metric',
        snapTo='true',
        visible='true',
        x0='41',
        y0='41')
    etree.SubElement(
        mw_wm_bp_bd_sg,
        'VASSAL.build.module.map.boardPicker.board.mapgrid.SquareGridNumbering',
        color='0,0,0',
        first='V',
        fontSize='20',
        hDescend='false',
        hDrawOff='0',
        hLeading='0',
        hOff='1',
        hType='N',
        locationFormat='$gridLocation$',
        rotateText='0',
        sep='-',
        vDescend='false',
        vDrawOff='30',
        vLeading='0',
        vOff='1',
        vType='N',
        visible='true')
    # map options
    etree.SubElement(mw_wm, 'VASSAL.build.module.map.ForwardToKeyBuffer')
    etree.SubElement(mw_wm, 'VASSAL.build.module.map.Scroller')
    etree.SubElement(mw_wm, 'VASSAL.build.module.map.ForwardToChatter')
    etree.SubElement(mw_wm, 'VASSAL.build.module.map.MenuDisplayer')
    etree.SubElement(mw_wm, 'VASSAL.build.module.map.MapCenterer')
    etree.SubElement(mw_wm, 'VASSAL.build.module.map.StackExpander')
    etree.SubElement(mw_wm, 'VASSAL.build.module.map.PieceMover')
    etree.SubElement(mw_wm, 'VASSAL.build.module.map.KeyBufferer')
    etree.SubElement(mw_wm, 'VASSAL.build.module.properties.GlobalProperties')
    etree.SubElement(mw_wm, 'VASSAL.build.module.map.SelectionHighlighters')
    etree.SubElement(
        mw_wm,
        'VASSAL.build.module.map.CounterDetailViewer',
        bgColor='255,255,255',
        borderWidth='2',
        counterReportFormat='',
        delay='700',
        display='from top-most layer only',
        emptyHexReportForma='$LocationName$',
        fgColor='0,0,0',
        fontSize='9',
        graphicsZoom='1.5',
        hotkey='32,130',
        layerList='',
        minDisplayPieces='1',
        propertyFilter='',
        showDeck='false',
        showMoveSelectde='false',
        showNoStack='false',
        showNonMovable='false',
        showgraph='true',
        showgraphsingle='false',
        showtext='false',
        showtextsingle='false',
        summaryReportFormat='$LocationName$',
        unrotatePieces='true',
        version='2',
        zoomlevel='2.0')
    etree.SubElement(
        mw_wm,
        'VASSAL.build.module.map.Zoomer',
        inButtonText='',
        inIconName='icn_zoom_in.png',
        inTooltip='Zoom in',
        outButtonText='',
        outIconName='icn_zoom_out.png',
        outTooltip='Zoom out',
        pickButtonText='',
        pickIconName='icn_zoom.png',
        pickTooltip='Select Zoom',
        zoomInKey='',
        zoomLevels='0.5,1.0',
        zoomOutKey='',
        zoomPickKey='',
        zoomStart='2')
    etree.SubElement(
        mw_wm,
        'VASSAL.build.module.map.StackMetrics',
        bottom='40,0',
        disabled='true',
        down='37,0',
        exSepX='6',
        exSepY='18',
        top='38,0',
        unexSepX='2',
        unexSepY='4',
        up='39,0')
    etree.SubElement(
        mw_wm,
        'VASSAL.build.module.map.HighlightLastMoved',
        color='255,0,0',
        enabled='false',
        thickness='2')
    return mw_wm


def inject_land(cs_no):
    # init
    global BF, GPID, HEADER, SHEET
    cs_rids = counter_sheet_row_idx_set(SHEET['L'], cs_no)
    parent = get_cs_parent(cs_no)

    # add at-start-stacks and piece-slots
    for rid in cs_rids:
        try:
            # load unit
            u = LandUnit()
            u.update(SHEET['L'], rid, HEADER['L'])
            assert u.type not in ['FORT'], 'skipped for type {}'.format(u.type)
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

            # at start stack
            loc_str = '{}-{}'.format(u.row, u.col)
            ats = etree.SubElement(
                parent,
                'VASSAL.build.module.map.SetupStack',
                location=loc_str,
                name=loc_str,
                useGridLocation='true',
                x='0',
                y='0')
            ats.append(ps.get_xml())
        except Exception, ex:
            print 'skipping row:', u.sh_row, str(ex)
            continue


def inject_air(cs_no):
    # init
    global BF, GPID, HEADER, SHEET
    cs_rids = counter_sheet_row_idx_set(SHEET['A'], cs_no)
    parent = get_cs_parent(cs_no)

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

            # at start stack
            loc_str = '{}-{}'.format(u.row, u.col)
            ats = etree.SubElement(
                parent,
                'VASSAL.build.module.map.SetupStack',
                location=loc_str,
                name=loc_str,
                useGridLocation='true',
                x='0',
                y='0')
            ats.append(ps.get_xml())
        except Exception, ex:
            print 'skipping row:', u.sh_row, str(ex)
            continue


def inject_naval(cs_no):
    # init
    global BF, GPID, HEADER, SHEET
    cs_rids = counter_sheet_row_idx_set(SHEET['N'], cs_no)
    parent = get_cs_parent(cs_no)

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
            # at start stack
            loc_str = '{}-{}'.format(u.row, u.col)
            ats = etree.SubElement(
                parent,
                'VASSAL.build.module.map.SetupStack',
                location=loc_str,
                name=loc_str,
                useGridLocation='true',
                x='0',
                y='0')
            ats.append(ps.get_xml())
        except Exception, ex:
            print 'skipping row:', u.sh_row, str(ex)
        continue


def build_WIF_FE(csrange=None):
    if csrange is None:
        csrange = CSrange
    print 'START'
    for cs in csrange:
        print 'CS', cs
        print 'land'
        inject_land(cs)
        print 'air'
        inject_air(cs)
        print 'naval'
        inject_naval(cs)
        print '..done!'
    print 'FINISH'


##---MAIN

if __name__ == '__main__':
    # setup
    start(ext=False)

    build_WIF_FE()
    #build_WIF_FE([1])
    #xml_get_cs(1)
    #inject_land(1)

    # finish
    save_path = None
    #save_path = '/home/pmeier/Workspace/WIFvassal/mod/test_bf.xml'
    finish(path=save_path)
