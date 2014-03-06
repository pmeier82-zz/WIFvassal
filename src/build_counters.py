# -*- coding: utf-8 -*-
# counter sheet data for vassal

## IMPORTS

from lxml import etree as ET
# from xml.etree import cElementTree as ET
from froon_ods import (
    get_sheet, read_header, gen_filtered_rowset,
    Counter, LandCounter, AirCounter, NavalCounter)
from vassal_xml import GPIDGenerator, PieceSlot

## CONSTANTS

BF_base = "/home/pmeier/Documents/Games/buildFile_base"
BF_new = "/home/pmeier/Documents/Games/buildFile_new"
SHEET = {}
HEADER = {}
GPID = None
BF = None

CNTR_BACK_COL_NUM = {
    "black": 2,
    "white": 3,
    "aqua": 4,
    "blue": 5,
    "dark blue": 6,
    "dk blue": 6,
    "light blue": 7,
    "lt blue": 7,
    "med blue": 8,
    "brown": 9,
    "light brown": 10,
    "lt brown": 10,
    "med brown": 11,
    "cranberry": 12,
    "dark gray": 13,
    "dark grey": 13,
    "dk gray": 13,
    "dk grey": 13,
    "light gray": 14,
    "light grey": 14,
    "lt gray": 14,
    "lt grey": 14,
    "med gray": 15,
    "med grey": 15,
    "green": 16,
    "dark green": 17,
    "dk green": 17,
    "forest green": 18,
    "light green": 19,
    "lt green": 19,
    "med green": 20,
    "khaki": 21,
    "orange": 22,
    "pink": 23,
    "purple": 24,
    "red": 25,
    "yellow": 26,
}

CNTR_FORE_COL_NUM = {
    "black": 2,
    "white": 3,
    "blue": 4,
    "dark blue": 5,
    "dk blue": 5,
    "light blue": 6,
    "lt blue": 6,
    "med blue": 7,
    "pale blue": 8,
    "brown": 9,
    "dark brown": 10,
    "dk brown": 10,
    "light brown": 11,
    "lt brown": 11,
    "med brown": 12,
    "emerald": 13,
    "dark gray": 14,
    "dark grey": 14,
    "dk gray": 14,
    "dk grey": 14,
    "light gray": 15,
    "light grey": 15,
    "lt gray": 15,
    "lt grey": 15,
    "med gray": 16,
    "green": 17,
    "dark green": 18,
    "dk green": 18,
    "light green": 19,
    "lt green": 19,
    "med green": 20,
    "pale green": 21,
    "olive": 22,
    "orange": 23,
    "light orange": 24,
    "lt orange": 24,
    "pink": 25,
    "light pink": 26,
    "lt pink": 26,
    "red": 27,
    "dark red": 28,
    "dk red": 28,
    "violet": 29,
    "light violet": 30,
    "lt violet": 30,
    "yellow": 31,
    "light yellow": 32,
    "lt yellow": 32,
}

TYPE_NUM_LAND = {
    "SUPP": 2,
    "HQA": 3,
    "HQI": 4,
    "ARM": 5,
    "MECH": 6,
    "MOT": 7,
    "INF": 8,
    "MIL": 9,
    "TERR": 10,
    "GARR": 11,
    "MTN": 12,
    "MAR": 13,
    "PARA": 14,
    "CAV": 15,
    "ACAV": 16,
    "WAR": 17,
    "Arm": 18,
    "Mech": 19,
    "Mot": 20,
    "Eng": 21,
    "Inf": 22,
    "Garr": 23,
    "Mtn": 24,
    "Mar": 25,
    "Para": 26,
    "Ski": 27,
    "Cav": 28,
    "Art": 29,
    "SP": 30,
    "AT": 31,
    "TD": 32,
    "AA": 33,
    "AAA": 34,
    "SAM": 35,
    "FTR": 36,
    "LND": 37,
    "NAV": 38,
    "ATR": 39,
    "CVP": 40,
    "BOMB": 41,
    "SUB": 42,
    "AMPH": 43,
    "TRS": 44,
    "ASW": 45,
    "CX": 46,
    "CV": 47,
    "CVL": 48,
    "BB": 49,
    "CA": 50,
    "CL": 51,
    "FROG": 52,
    "LEAD": 53,
    "SYNTH": 54,
}

CNTR_NO_HOME = {
    "China": None,
}

## FUNCTIONS

def start(buildfile_base=None):
    global BF, GPID, HEADER, SHEET
    if buildfile_base is None:
        buildfile_base = BF_base
    print "reading build file"
    with open(buildfile_base, "r") as fp:
        BF = ET.parse(fp)
    GPID = GPIDGenerator(BF)
    print "reading counter files"
    SHEET["L"] = get_sheet("Land")
    HEADER["L"] = read_header(SHEET["L"])
    SHEET["A"] = get_sheet("Air")
    HEADER["A"] = read_header(SHEET["A"])
    SHEET["N"] = get_sheet("Naval")
    HEADER["N"] = read_header(SHEET["N"])
    print "done!"
    print


def finish(buildfile_new=None):
    global BF, GPID
    if buildfile_new is None:
        buildfile_new = BF_new
    print "writing build file"
    BF.getroot().attrib["nextPieceSlotId"] = u'{:d}'.format(GPID.get())
    BF.write(
        buildfile_new,
        encoding="UTF-8",
        method="xml",
        xml_declaration=True,
        pretty_print=True)
    print "done!"
    print


def get_power(*args):
    if len(args) == 1:
        if isinstance(args[0], Counter):
            pwr, hom = args[0].power, args[0].home
        else:
            pwr = str(args[0])
            hom = None
    else:
        pwr, hom = args[0], args[1]
    try:
        return {
            "Commonwealth": "CW",
            "France": "FR",
            "Germany": "GE",
            "Italy": "IT",
            "Japan": "JP",
            "USSR": "RU",
            "USA": "US"
        }.get(pwr)
    except KeyError:
        if pwr == "China":
            return {
                "Comm China": "CC",
                "Nat China": "CH",
            }.get(hom, "CH")
        else:
            return "Minors"


def get_clas(u):
    return u.clas


def get_type(u):
    ## FIXME: handle double types
    rval = {
        u"HQ-I": "HQI",
        u"HQ-A": "HQA",
        u"Coastal Fort": "COAST",
        u"FLAK (AAA)": "AAA",
        u"FLAK (SAM)": "SAM",
        u"WARLORDS": "WAR",
    }.get(u.type, u.type)
    if u.clas == "ART":
        if u.info is not None and "self-prop" in u.info:
            if u.type == "ART":
                rval = "SP"
            if u.type == "AT":
                rval = "TD"
    return rval


def get_size(u):
    if u.size is not None and "div" in u.size.lower():
        return "XX"
    if "hq" in u.type.lower():
        return "XXXXX"
    rval = "XXX"
    if get_power(u) == "RU":
        if u.type not in ["CAV", "MAR", "MTN", "PARA"]:
            rval += "X"
    if get_power(u) in ["China", "Japan", "Poland"]:
        if u.type in ["INF", "GARR", "MIL", "MOT"]:
            rval += "X"
    if get_power(u) == "JP":
        if u.type in ["INF", "GARR", "MIL", "MOT"]:
            rval += "X"
    if u.power in ["Arabia", "Liberia"]:
        rval += "X"
    return rval


def get_units_parent(remove_units=False):
    # init
    global BF

    # main tab widget in game pieces
    game_pieces = BF.find(
        "/VASSAL.build.module.PieceWindow[@name=\"Game Pieces\"]"
        "/VASSAL.build.widget.TabWidget[@entryName=\"game_pieces_tab\"]"
    )
    if game_pieces is None:
        raise ValueError("could not find PieceWindow[@name=\"Game Pieces\"]")

    # units box widget
    unt_box = game_pieces.find(
        "VASSAL.build.widget.BoxWidget[@entryName=\"Units\"]"
    )
    if unt_box is not None and remove_units is True:
        game_pieces.remove(unt_box)
        game_pieces \
            .find("VASSAL.build.widget.BoxWidget[@entryName=\"General\"]") \
            .addnext(
            ET.Element(
                "VASSAL.build.widget.BoxWidget",
                entryName="Units"
            )
        )
    return game_pieces.find(
        "VASSAL.build.widget.BoxWidget[@entryName=\"Units\"]"
    )


def inject_land_major(power=None):
    # init
    global BF, GPID, HEADER, SHEET
    parent = get_units_parent()
    print "injecting land counters for", power

    # power box widget (build new if not present)
    parent_power = parent.find(
        "VASSAL.build.widget.TabWidget[@entryName=\"{}\"]".format(power)
    )
    if parent_power is None:
        if get_power(u) != "Minor":
            # build it and append
            parent_power = ET.SubElement(
                parent,
                "VASSAL.build.widget.TabWidget",
                entryName=power
            )
        else:
            # build it and append
            parent_minors = ET.SubElement(
                parent,
                "VASSAL.build.widget.BoxWidget",
                entryName="Minors"
            )

    # land tab (builds new if not present
    parent_land = parent_power.find("VASSAL.build.widget.TabWidget[@entryName=\"Land\"]")
    if parent_land is None:
        parent_land = ET.SubElement(
            parent_power,
            "VASSAL.build.widget.TabWidget",
            entryName="Land"
        )

    # containers and keys
    cntr_keys = ["ARM", "CAV", "INF", "ART", "SUPP"]
    cntr = {key: {} for key in cntr_keys}
    cntr_unused = {key: {} for key in cntr_keys}
    cntr_unused["FORT"] = {}

    # fill containers
    print "reading counters",
    for u in gen_filtered_rowset(
            sheet=SHEET["L"],
            header=HEADER["L"],
            filt=lambda u: u.power == power):
        try:
            # unused?
            cont = cntr
            if u.clas not in cntr.keys() or not u.used:
                cont = cntr_unused

            # where to add?
            u_clas = get_clas(u)
            u_type = get_type(u)
            if u_type not in cont[u_clas]:
                cont[u_clas][u_type] = []
            cont[u_clas][u_type].append(u)
        except Exception, ex:
            # print "error reading row:", u.sh_row, str(ex)
            continue
        finally:
            print ".",
    print "!"

    # build piece slots
    print "building piece slots",
    for u_clas in cntr_keys:
        # build class tab
        # if u_clas == "UNUSED": continue
        clas_tab = ET.SubElement(
            parent_land,
            "VASSAL.build.widget.TabWidget",
            entryName=u_clas
        )
        for u_type in sorted(cntr[u_clas].keys()):
            type_tab = ET.SubElement(
                clas_tab,
                "VASSAL.build.widget.ListWidget",
                entryName=u_type,
                divider="250"
            )
            type_div_tab = ET.SubElement(
                type_tab,
                "VASSAL.build.widget.ListWidget",
                entryName="Divisions",
                divider="150"
            )
            type_hvy_tab = ET.SubElement(
                type_tab,
                "VASSAL.build.widget.ListWidget",
                entryName="Heavies",
                divider="150"
            )
            for u in sorted(cntr[u_clas][u_type]):
                try:
                    # piece slot, trait order in reverse!!
                    ps = PieceSlot(u.name or u.year, GPID.get())
                    ps.add_trait("prototype", ("TRANSFORM", "")) # last!

                    # counter colours and symbol
                    ps.add_trait("mark", ("cntr_back_num", CNTR_BACK_COL_NUM.get(u.color.lower(), 1)))
                    ps.add_trait("mark", ("symb_back_num", CNTR_FORE_COL_NUM.get(u.color2.lower(), 1)))
                    # ps.add_trait("mark", ("symb_fore_num", u.info))
                    if u.info is not None and "mot" in map(unicode.lower, u.info) or u.type.lower() == "mot":
                        ps.add_trait("mark", ("symb_wheels_num", 1))
                    if u.info is not None and "hvy" in map(unicode.lower, u.info):
                        ps.add_trait("mark", ("symb_aa_hvy_num", 1))
                    if u.size == "H":
                        ps.add_trait("mark", ("symb_heavy_num", 1))

                    # generic information
                    ps.add_trait("mark", ("INFO", ",".join(u.info or [])))
                    ps.add_trait("mark", ("KIT", u.kit))
                    ps.add_trait("mark", ("YEAR", u.year))

                    # labels
                    size = get_size(u)
                    ps.add_trait("mark", ("SIZE", size))
                    # decorate for size
                    ps.add_trait("mark", ("CLASS", u.clas))
                    type = get_type(u)
                    if u.size == "Div" and u.clas not in ["ART", "SUPP"]:
                        type = type[0] + type[1:].lower()
                    ps.add_trait("mark", ("TYPE", type))
                    ps.add_trait("mark", ("MVA", u.mov))
                    ps.add_trait("mark", ("ROG", u"-" if u.rog is None else u"({})".format(u.rog)))
                    ps.add_trait("mark", ("LCF", u.str or 0))
                    # values
                    if u.info is None:
                        ps.add_trait("mark", ("val_style", "color: #000000"))
                        ps.add_trait("mark", ("val_bg_style", "color: #ffffff"))
                        ps.add_trait("prototype", ("LANDvalues", ""))
                    else:
                        if "WP" in u.info:
                            ps.add_trait("mark", ("val_style", "color: #ffffff"))
                            ps.add_trait("mark", ("val_bg_style", "color: #000000"))
                            ps.add_trait("prototype", ("LANDvalues", ""))
                        elif u.clas == "ART":
                            if "grey" in u.info:
                                ps.add_trait("mark", ("art_num", 2))
                                ps.add_trait("prototype", ("LANDart", ""))
                            elif "pink" in u.info:
                                ps.add_trait("mark", ("art_num", 3))
                                ps.add_trait("prototype", ("LANDart", ""))
                            elif "red" in u.info:
                                ps.add_trait("mark", ("art_num", 4))
                                ps.add_trait("prototype", ("LANDart", ""))
                            else:
                                ps.add_trait("mark", ("val_style", "color: #000000"))
                                ps.add_trait("mark", ("val_bg_style", "color: #ffffff"))
                                ps.add_trait("prototype", ("LANDvalues", ""))
                        else:
                            ps.add_trait("mark", ("val_style", "color: #000000"))
                            ps.add_trait("mark", ("val_bg_style", "color: #ffffff"))
                            ps.add_trait("prototype", ("LANDvalues", ""))
                    ps.add_trait("prototype", ("LANDbase", ""))

                    # add piece
                    tab = {
                        None: type_tab,
                        "Div": type_div_tab,
                        "H": type_hvy_tab,
                    }[u.size].append(ps.get_xml())
                finally:
                    print ".",
            if len(type_div_tab) == 0:
                type_tab.remove(type_div_tab)
            if len(type_hvy_tab) == 0:
                type_tab.remove(type_hvy_tab)
    print "!"
    print


def inject_air(cs_no):
    # init
    global BF, GPID, HEADER, SHEET
    cs_rids = counter_sheet_row_idx_set(SHEET['A'], cs_no)
    parent = get_cs_parent(cs_no)

    # produce counters and piece slots
    for rid in cs_rids:
        try:
            # load unit
            u = AirCounter()
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
            ps.add_trait('prototype', ('Control' + get_power(u), ''))

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
            u = NavalCounter()
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
            ps.add_trait('prototype', ('Control' + get_power(u), ''))
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
        inject_land_major(cs)
        print 'air'
        inject_air(cs)
        print 'naval'
        inject_naval(cs)
        print '..done!'
    print 'FINISH'

##---MAIN

if __name__ == '__main__':
    from zipfile import ZipFile
    import os

    # replace buildFile_base with version from the module and parse it
    WORKING_DIR = "/home/pmeier/Documents/Games"
    MODULE_FILE = "/home/pmeier/Dropbox/Stuff/games/vassal/WiFdab.zip"
    with ZipFile(MODULE_FILE, "r") as arc, open(os.path.join(WORKING_DIR, "buildFile_base"), "w") as fp:
        fp.write(arc.read("buildFile"))
    start()

    # new build file
    get_units_parent(True)
    inject_land_major("China")
    inject_land_major("Commonwealth")
    inject_land_major("France")
    inject_land_major("Germany")
    inject_land_major("Italy")
    inject_land_major("Japan")
    inject_land_major("USSR")
    inject_land_major("USA")

    # finish by writing file back to the archive
    finish(buildfile_new=os.path.join(WORKING_DIR, "buildFile"))
    print "ALL DONE!"
