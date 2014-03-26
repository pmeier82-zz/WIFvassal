# -*- coding: utf-8 -*-
# counter sheet data for vassal

## IMPORTS

from lxml import etree as ET
from froon_ods import (
    get_sheet, read_header, gen_filtered_rowset,
    Counter, LandCounter, AirCounter, NavalCounter)
from vassal_xml import GPIDGenerator, PieceSlot

## CONSTANTS

CW_KIF_ONLY = True

BF_base = "/home/pmeier/Documents/Games/buildFile_base"
BF_new = "/home/pmeier/Documents/Games/buildFile_new"
SHEET = {}
HEADER = {}
GPID = None
BF = None

CONTROL_NUM = {
    "CH": 2,
    "CC": 3,
    "CW": 4,
    "FR": 5,
    "FF": 6,
    "GE": 7,
    "IT": 8,
    "JP": 9,
    "RU": 10,
    "US": 11,
    "OT": 12,
}

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
    "pale blue / red": 27,
    "dark red": 28,
    "dk red": 28,
    "violet": 29,
    "light violet": 30,
    "lt violet": 30,
    "yellow": 31,
    "light yellow": 32,
    "lt yellow": 32,
    "pale yellow": 32,
}

TYPE_NUM_LAND = {
    "SUP": 2,
    "HQA": 3,
    "HQI": 4,
    "ARM": 5,
    "MECH": 6,
    "MOT": 7,
    "INF": 8,
    "MIL": 9,
    "TER": 10,
    "GAR": 11,
    "MTN": 12,
    "MAR": 13,
    "PARA": 14,
    "CAV": 15,
    "ACV": 16,
    "WAR": 17,
    "Arm": 18,
    "Mech": 19,
    "Mot": 20,
    "Eng": 21,
    "Inf": 22,
    "Gar": 23,
    "Mtn": 24,
    "Mar": 25,
    "Para": 26,
    "Ski": 27,
    "Cav": 28,
    "Cdo": 29,
    "Art": 30,
    "SP": 31,
    "AT": 32,
    "TD": 33,
    "AA": 34,
    "AAA": 35,
    "SAM": 36,
    "PART": 37,
}

COL_NUM = {
    "blk": 2,
    "red": 3,
    "blu": 4,
    "whi": 5,
    "gre": 6,
    "yel": 7,
}

COL_CODE = {
    "blk": "#000000",
    "red": "#ff0000",
    "blu": "#00a2ff",
    "whi": "#ffffff",
    "gre": "#99cc33",
    "yel": "#ffff00",
}

CBV_COLOURS = {
    ## CW
    "Athens": ("blu", "blu"),
    "Oslo": ("blu", "whi"),
    ## FR
    "Algiers": ("red", "red"),
    "Damascus": ("gre", "red"),
    "Dakar": ("red", "red"),
    "Antanarivo": ("gre", "whi"),
    "Morocco": ("red", "red"),
    ## GE
    "Ost SS": ("whi", "red"),
    "Frank SS": ("whi", "red"),
    "Vlassov": ("blk", "blk"),
    "Zagreb": ("blu", "red"),
    "Croat": ("blu", "red"),
    "SS America": ("blu", "blu"),
    "SS Pacific": ("blu", "blu"),
    "I Slovak": ("red", "blu"),
    "SS Nordland": ("blu", "blu"),
    "SS Holland": ("whi", "whi"),
    "SS Lettiland": ("whi", "whi"),
    "SS Russland": ("red", "red"),
    "SS Weissr.": ("whi", "whi"),
    "SS Freiwill.": ("red", "red"),
    "SS Kama": ("blu", "blu"),
    ## IT
    "Cairo": ("blk", "red"),
    "Madrid": ("red", "red"),
    ## JP
    "INA": ("whi", "yel"),
    "Saigon": ("yel", "yel"),
    "Manila": ("red", "whi"),
    "Batavia": ("whi", "whi"),
    "Nanking": ("blu", "blu"),
    "Vladivostok": ("red", "red"),
    "Calcutta": ("whi", "whi"),
    "Malaya INA": ("whi", "yel"),
    ## Spain
    "I Hispan.": ("blu", "blu"),
    "II Hispan.": ("blu", "blu"),
    "III Hispan.": ("red", "red"),
    ## US
    "Naples": ("red", "gre"),
    "Rome": ("red", "red"),
    ## RU
    "Sofia": ("red", "red"),
    "Bucharest": ("blu", "red"),
}

ENTITY_COLOURS = {
    # home : abbrev, col_symb, col_symb_text, col_left, col_top, col_right

    ## PARTITSANS
    "Partisan": (None, "red", "red", "blk", "blk", "blk"),

    ## MINORS
    "Afghanistan": ("Afg", "red", "red", "whi", "whi", "whi"),
    "Albania": ("Alb", "red", "blk", "red", "red", "blk"),
    "Arabia": ("Ara", "blk", "blk", "blk", "blk", "blk"),
    "Argentina": ("Arg", "blu", "blu", "whi", "blu", "blk"),
    "Austria": ("Aut", "red", "red", "red", "red", "blk"),
    "Belgium": ("Bel", "red", "red", "red", "red", "red"),
    "Be. Congo": ("Be. Congo", "red", "gre", "red", "red", "red"),
    "Bolivia": ("Bol", "yel", "yel", "yel", "yel", "blk"),
    "Brazil": ("Bra", "blu", "blu", "blu", "blu", "blk"),
    "Bulgaria": ("Bul", "red", "red", "gre", "gre", "blk"),
    "Cent. America": ("CA", "blk", "blk", "whi", "whi", "blk"),
    "Chile": ("Chi", "blu", "blu", "whi", "whi", "blk"),
    "Colombia": ("Col", "blu", "blu", "red", "red", "blk"),
    "Costa Rica": ("C.R.", "whi", "whi", "blu", "blu", "blk"),
    "Cuba": ("Cub", "red", "red", "whi", "whi", "blk"),
    "Czechoslovakia": ("Cze", "whi", "whi", "whi", "blk", "blk"),
    "Denmark": ("Den", "red", "red", "red", "blk", "blk"),
    "Dom. Rep.": ("D.R.", "red", "red", "red", "red", "blk"),
    "Ecuador": ("Ecu", "red", "whi", "blu", "blu", "blk"),
    "El Salvador": ("E.S.", "blk", "blk", "whi", "whi", "blk"),
    "Ethiopia": ("Eth", "yel", "yel", "gre", "yel", "blk"),
    "Finland": ("Fin", "whi", "blu", "blu", "blu", "blk"),
    "Greece": ("Gre", "whi", "whi", "blu", "whi", "whi"),
    "Guatemala": ("Gua", "whi", "whi", "blu", "blu", "blk"),
    "Haiti": ("Hai", "whi", "whi", "whi", "whi", "blk"),
    "Honduras": ("Hon", "blk", "whi", "blu", "blu", "blk"),
    "Hungary": ("Hun", "gre", "red", "red", "blk", "blk"),
    "Indonesia": ("Indo", "whi", "whi", "whi", "whi", "blk"),
    "Iraq": ("Irq", "blk", "red", "red", "blk", "blk"),
    "Ireland": ("Ire", "red", "red", "red", "blk", "blk"),
    "Israel": ("Isr", "blu", "blu", "blu", "blu", "blk"),
    "Jordan": ("Jor", "red", "red", "gre", "gre", "blk"),
    "North Korea": ("N.Ko.", "whi", "whi", "blu", "blu", "blk"),
    "South Korea": ("S.Ko", "blu", "blu", "whi", "whi", "blk"),
    "Lebanon": ("Leb", "blu", "blu", "red", "red", "blk"),
    "Liberia": ("Lib", "whi", "whi", "blk", "blk", "blk"),
    "Mexico": ("Mex", "gre", "gre", "gre", "gre", "blk"),
    "Mongolia": ("Mon", "red", "red", "blk", "blk", "blk"),
    "Netherlands": ("Net", "whi", "whi", "red", "whi", "blk"),
    "NEI": ("NEI", "whi", "whi", "red", "whi", "blk"),
    "Nicaragua": ("Nic", "blu", "blu", "blu", "blu", "blk"),
    "Norway": ("Nor", "blu", "blu", "blu", "blu", "blk"),
    "Pakistan": ("Pak", "whi", "whi", "whi", "whi", "blk"),
    "Panama": ("Pan", "whi", "whi", "red", "red", "blk"),
    "Paraguay": ("Par", "whi", "whi", "whi", "whi", "blk"),
    "Persia": ("Prs", "red", "red", "red", "blk", "blk"),
    "Peru": ("Per", "blk", "blk", "red", "red", "blk"),
    "Poland": ("Pol", "red", "red", "whi", "blk", "blk"),
    "Portugal": ("Por", "red", "red", "gre", "blk", "blk"),
    "Rumania": ("Rum", "blu", "red", "yel", "blk", "blk"),
    "Siam": ("Sia", "red", "red", "red", "red", "blk"),
    "Nat Spain": ("SN", "red", "red", "red", "blk", "blk"),
    "Spain": ("Sp", "red", "red", "red", "blk", "blk"),
    "Rep Spain": ("SR", "red", "red", "red", "blk", "blk"),
    "Sweden": ("Swe", "blu", "blu", "#005bab", "blk", "blk"),
    "Switzerland": ("Swi", "blk", "blk", "whi", "blk", "blk"),
    "Turkey": ("Tur", "whi", "whi", "whi", "whi", "blk"),
    "Ukraine": ("Ukr", "red", "red", "red", "red", "blk"),
    "Uruguay": ("Uru", "blu", "blu", "whi", "whi", "blk"),
    "Venezuela": ("Ven", "blu", "blu", "blu", "blu", "blk"),
    "Vietnam": ("Vie", "red", "red", "red", "red", "blk"),
    "Yugoslavia": ("Yug", "red", "red", "blu", "blu", "blk"),

    ## CHINA
    "Comm China": (None, "blk", "whi", "blk", "blk", "blk"),
    "Nat China": (None, "blk", "red", "blk", "blk", "blk"),
    "Warlords": (None, "red", "red", "blk", "blk", "blk"),

    ## CW TER
    "A. E. Sudan": (None, "red", "gre", "blk", "blk", "blk"),
    "Aden": (None, "red", "gre", "blk", "blk", "blk"),
    "Br. Guyana": (None, "blk", "red", "blk", "blk", "blk"),
    "Br. Somali": (None, "blu", "blu", "blk", "blk", "blk"),
    "Burma": (None, "whi", "blu", "blk", "blk", "blk"),
    "Egypt": ("Egy", "red", "red", "blk", "blk", "blk"),
    "Eritrea": (None, "gre", "yel", "blk", "blk", "blk"),
    "Kenya": (None, "whi", "gre", "blk", "blk", "blk"),
    "Libya": (None, "blk", "whi", "blk", "blk", "blk"),
    "Nigeria": (None, "gre", "gre", "blk", "blk", "blk"),
    "Nth. Ireland": (None, "red", "red", "blk", "blk", "blk"),
    "Nth. Rhod.": (None, "red", "yel", "blk", "blk", "blk"),
    "Palestine": (None, "gre", "red", "blk", "blk", "blk"),
    "Rhodesia": (None, "whi", "whi", "blk", "blk", "blk"),
    "Sierra Leone": (None, "gre", "blu", "blk", "blk", "blk"),
    "Tanganyika": (None, "gre", "blu", "blk", "blk", "blk"),
    "Uganda": (None, "blk", "red", "blk", "blk", "blk"),

    ## CW DOMINIONS
    "AUS": ("AUS", "red", "blu", "blk", "blk", "blk"),
    "CAN": ("CAN", "red", "blu", "blk", "blk", "blk"),
    "IND": ("IND", "red", "red", "blk", "blk", "blk"),
    "NZ": ("NZ", "red", "whi", "blk", "blk", "blk"),
    "SA": ("SA", "red", "blu", "blk", "blk", "blk"),
    "UK": (None, "blk", "whi", "blk", "blk", "blk"),

    ## FR TER
    "Algeria": (None, "red", "whi", "blk", "blk", "blk"),
    "Cameroons": (None, "yel", "gre", "blk", "blk", "blk"),
    "Fr. Guyana": (None, "blk", "red", "blk", "blk", "blk"),
    "Fr. Somali": (None, "blu", "blu", "blk", "blk", "blk"),
    "Fr. Sudan": (None, "gre", "red", "blk", "blk", "blk"),
    "Gabon": (None, "blu", "gre", "blk", "blk", "blk"),
    "Indo-China": (None, "yel", "yel", "blk", "blk", "blk"),
    "Ivory Coast": (None, "red", "gre", "blk", "blk", "blk"),
    "Madagascar": (None, "gre", "whi", "blk", "blk", "blk"),
    "Mid. Congo": (None, "gre", "yel", "blk", "blk", "blk"),
    "Morocco": (None, "blk", "gre", "blk", "blk", "blk"),
    "New Caled.": (None, "red", "gre", "blk", "blk", "blk"),
    "Niger": (None, "gre", "red", "blk", "blk", "blk"),
    "Senegal": (None, "red", "gre", "blk", "blk", "blk"),
    "Syria": ("Syr", "red", "gre", "blk", "blk", "blk"),
    "Tunisia": (None, "red", "red", "blk", "blk", "blk"),

    ## FRANCE
    "France": (None, "blk", "red", "blk", "blk", "blk"),

    ## GERMANY
    "Germany": (None, "blk", "red", "blk", "blk", "blk"),

    ## IT TER
    "It. Somali": (None, "blu", "blu", "blk", "blk", "blk"),
    "AOI": (None, "gre", "red", "blk", "blk", "blk"),

    ## ITALY
    "Italy": (None, "blk", "red", "blk", "blk", "blk"),

    ## JP TER
    "Formosa": (None, "whi", "blu", "blk", "blk", "blk"),
    "Korea": (None, "blu", "red", "blk", "blk", "blk"),
    "Manchuria": (None, "whi", "red", "blk", "blk", "blk"),
    "Philippines": ("Phi", "red", "red", "blk", "blk", "blk"),

    ## JAPAN
    "Japan": (None, "blk", "red", "blk", "blk", "blk"),

    ## RUSSIA
    "USSR": (None, "blk", "red", "blk", "blk", "blk"),

    ## USA
    "USA": (None, "blk", "red", "blk", "blk", "blk"),
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


def get_control(*args):
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
        }[pwr]
    except KeyError:
        if pwr == "China":
            return {
                "Comm China": "CC",
                "Nat China": "CH",
            }.get(hom, "CH")
        else:
            return "Minors"


def get_clas(unit):
    return unit.clas


def get_kit(unit):
    return {
        "PiFG": "PiF",
        "WiFC": "WiF",
        "WIFC": "WiF",
        "SIF": "SiF",
    }.get(unit.kit, unit.kit)


def get_type(unit):
    ## FIXME: handle double types
    rval = {
        u"HQ-I": "HQI",
        u"HQ-A": "HQA",
        u"Coastal Fort": "COAST",
        u"FLAK (AAA)": "AAA",
        u"FLAK (SAM)": "SAM",
        u"WARLORDS": "WAR",
        u"Fl.Pz.": "PARA",
        u"GARR": "GAR",
        u"TERR": "TER",
        u"PART HQ-I": "PART",
    }.get(unit.type, unit.type)
    if hasattr(unit, "size"):
        if unit.size == "Div":
            try:
                return {
                    u"MTN / CAV": "Mtn",
                    u"MTN / MAR": "Cdo",
                    u"MAR / PARA": "Cdo",
                    u"ENG ARM": "Eng",
                }[rval]
            except:
                if unit.clas not in ["SUPP", "ART"]:
                    rval = rval[0].upper() + rval[1:].lower()
    return rval


def get_size(unit):
    u_type = get_type(unit)
    if unit.size is not None and "div" in unit.size.lower():
        return "XX"
    if "hq" in u_type.lower():
        return "XXXXX"
    rval = "XXX"
    if unit.power == "USSR":
        if u_type not in ["CAV", "MAR", "MTN", "PARA"]:
            rval += "X"
    if unit.power in ["China", "Japan", "Poland"]:
        if u_type in ["INF", "GAR", "MIL", "MOT"]:
            rval += "X"
    if unit.power in ["Arabia", "Liberia"]:
        rval += "X"
    return rval


def get_col(col):
    if col.startswith("#"):
        return col
    else:
        return COL_CODE.get(col, "#000000")


def break_name(name):
    rval = []
    for part in name.split():
        parts = {
            "Liberator": ["Liber-", "ator"],
            "Beaufighter": ["Beau-", "fighter"],
            "Sturmovik": ["Sturm-", "ovik"],
            "Maryland": ["Mary-", "land"],
            "Baltimore": ["Balti-", "more"],
            "Marauder": ["Mar-", "auder"],
            "Mitchell": ["Mit-", "chell"],
            "Peacemaker": ["Peace-", "maker"],
            "Invader": ["Inva-", "der"],
            "Dominator": ["Domi-", "nator"],
        }.get(part, part)
        if isinstance(parts, (str, unicode)):
            rval.append(parts)
        else:
            for item in parts:
                rval.append(item)
    return rval


def get_units_parent(rebuild=False):
    # init
    global BF

    print "finding unit parent"

    # main tab widget in game pieces
    game_pieces = BF.find(
        "/VASSAL.build.module.PieceWindow[@name=\"Game Pieces\"]"
        "/VASSAL.build.widget.TabWidget[@entryName=\"game_pieces_tab\"]"
    )
    if game_pieces is None:
        raise ValueError("could not find PieceWindow[@name=\"Game Pieces\"]")

    # units box widget
    units_parent = game_pieces.find("VASSAL.build.widget.BoxWidget[@entryName=\"Units\"]")

    # build if not present or rebuild if flagged
    if units_parent is None or (units_parent is not None and rebuild is True):

        # the structure we want in the end looks like this:
        # UNITS[tab]
        #  |-POWER_NAME[dropdown]
        #  |  |-KIT1 [tab]
        #  |  |  |-UNIT_TYPE1[list]
        #  |  |  |  |-GAME_PIECE1
        #  |  |  |  |-GAME_PIECE2
        #  |  |  |-UNIT_TYPE2[list]
        #  |  |  |  |-GAME_PIECE3
        #  |  |  |  |-GAME_PIECE4
        #  *  *  *  *
        #

        print "rebuilding unit parent!!"
        if units_parent is not None:
            game_pieces.remove(units_parent)

        # build unit parent
        game_pieces \
            .find("VASSAL.build.widget.BoxWidget[@entryName=\"Markers\"]") \
            .addnext(
            ET.Element(
                "VASSAL.build.widget.BoxWidget",
                entryName="Units"
            ))
        units_parent = game_pieces.find("VASSAL.build.widget.BoxWidget[@entryName=\"Units\"]")

        # major powers
        for power_name in [
            "China",
            "Commonwealth",
            "France",
            "Germany",
            "Italy",
            "Japan",
            "USSR",
            "USA",
        ]:
            # build power parent
            power_parent = ET.SubElement(
                units_parent,
                "VASSAL.build.widget.TabWidget",
                entryName=power_name
            )
            build_power_entry(power_parent)

        # minor countries
        ET.SubElement(
            units_parent,
            "VASSAL.build.widget.BoxWidget",
            entryName="Minors")

        # partisans
        partisan_parent = ET.SubElement(
            units_parent,
            "VASSAL.build.widget.ListWidget",
            entryName="Partisans",
            divider="250")
        for kit_name in [
            "WiF", "AiF", "PatiF",
            "PiF", "AfA", "AsA", "SiF", "MiF", "LiF", "CVPiF", "PoliF",
            "CLiF", "CoiF", "FiF", "KiF"
        ]:
            ET.SubElement(
                partisan_parent,
                "VASSAL.build.widget.ListWidget",
                entryName="<<" + kit_name,
                divider="150")

    # return
    return game_pieces.find("VASSAL.build.widget.BoxWidget[@entryName=\"Units\"]")


def get_hook(unit, units_parent=None):
    if units_parent is None:
        units_parent = get_units_parent()
    is_minor = False
    if get_control(unit) == "Minors":
        is_minor = True
        u_power = unit.power
        if u_power is None and get_type(unit) == "PART":
            partisan_parent = units_parent.find("VASSAL.build.widget.ListWidget[@entryName=\"Partisans\"]")
            print partisan_parent.getchildren()
            hook = partisan_parent.find("VASSAL.build.widget.ListWidget[@entryName=\"<<{}\"]".format(get_kit(unit)))
            return hook, is_minor
        else:
            minors_parent = units_parent.find("VASSAL.build.widget.BoxWidget[@entryName=\"Minors\"]")
            power_parent = minors_parent.find("VASSAL.build.widget.TabWidget[@entryName=\"{}\"]".format(u_power))
            if power_parent is None:
                power_parent = ET.SubElement(
                    minors_parent,
                    "VASSAL.build.widget.TabWidget",
                    entryName=u_power)
                build_power_entry(power_parent)
    else:
        power_parent = units_parent.find("VASSAL.build.widget.TabWidget[@entryName=\"{}\"]".format(unit.power))
    kit_parent = power_parent.find("VASSAL.build.widget.ListWidget[@entryName=\"{}\"]".format(get_kit(unit)))
    hook = kit_parent.find("VASSAL.build.widget.ListWidget[@entryName=\"<<{}\"]".format(get_type(unit)))
    if hook is None:
        hook = kit_parent.find("VASSAL.build.widget.ListWidget[@entryName=\"<<Misc.\"]")
    return hook, is_minor


def build_power_entry(node):
    for kit_name in [
        "WiF", "AiF", "PatiF",
        "PiF", "AfA", "AsA", "SiF", "MiF", "LiF", "CVPiF", "PoliF",
        "CLiF", "CoiF", "FiF", "KiF"
    ]:
        kit_parent = ET.SubElement(
            node,
            "VASSAL.build.widget.ListWidget",
            entryName=kit_name,
            divider="250")
        for type_name in [
            "HQA", "ARM", "Arm", "MECH", "Mech", # ARM class
            "ACV", "CAV", "Cav", # CAV class
            "HQI", "MOT", "Mot", "INF", "Inf", "GAR", "Gar",
            "MTN", "Mtn", "MAR", "Mar", "PARA", "Para",
            "Eng", "Ski", "TER", "MIL", # INF class
            "ART", "AT", "AA", "AAA", "SAM", # ART class
            "FTR", "LND", "NAV", "ATR", "CVP", "BOMB", # AIR class
            "SUB", # SUB class
            "TRS", "AMPH", "ASW", "CX", "CV", "CVL",
            "BB", "CA", "CL", # SHIP class
            "Misc.", # MISC entry
        ]:
            ET.SubElement(
                kit_parent,
                "VASSAL.build.widget.ListWidget",
                entryName="<<" + type_name,
                divider="150")


def cw_kif_only(u):
    if u.power == "Commonwealth":
        return u.kit == "KiF"
    else:
        return True


def inject_land(units_parent=None):
    """run over all counters and put them in the right place"""

    # init
    global BF, GPID, HEADER, SHEET
    print "INJECT LAND"
    if units_parent is None:
        units_parent = get_units_parent(False)

    # fill containers
    print "reading counters",
    for u in gen_filtered_rowset(sheet=SHEET["L"], header=HEADER["L"]):
        try:
            # init
            print_item = "."
            u_type = get_type(u)
            print_item = "({})".format(u_type)
            tag, col_symb, col_symb_text, col_left, col_top, col_right = ENTITY_COLOURS[u.home or "Partisan"]
            hook, is_minor = get_hook(u, units_parent)

            # piece slot, trait order in R E V E R S E !!
            ps = PieceSlot(u.name or u.year, GPID.get())
            ps.add_trait("prototype", ("ROTATE", "")) # last!

            # game values and info
            ps.add_trait("mark", ("val_info", ",".join(u.info or [])))
            ps.add_trait("mark", ("val_kit", get_kit(u)))
            ps.add_trait("mark", ("val_year", u.year))
            ps.add_trait("mark", ("val_class", u.clas))
            ps.add_trait("mark", ("val_type", u_type))
            ps.add_trait("mark", ("val_cost", u.cost))
            ps.add_trait("mark", ("val_time", u.time))
            # land values
            ps.add_trait("mark", ("val_mv", u.mov))
            if u.rog:
                ps.add_trait("mark", ("val_ro", u.rog))
            ps.add_trait("mark", ("val_cf", u.str or 0))

            # labels
            if u.name is not None and "siberian" in u.name:
                col_left = col_top = "whi"
            if u.name is not None and u.name == "GGFF":
                col_left = col_right = col_top = col_symb = "yel"
            if not is_minor:
                col_left = col_right = col_top = "blk"
                if u.info is not None and "SS" in u.info:
                    col_left = col_right = col_top = "whi"
            if is_minor is True:
                if u_type == "PART":
                    ps.add_trait("mark", ("val_right", u.name))
                else:
                    ps.add_trait("mark", ("val_left", tag))
                    ps.add_trait("mark", ("col_left", get_col(col_left)))
                    if u.name:
                        ps.add_trait("mark", ("val_right", u.name))
                        ps.add_trait("mark", ("col_right", get_col(col_right)))
            else:
                if u.name:
                    ps.add_trait("mark", ("val_left", u.name))
                    ps.add_trait("mark", ("col_left", get_col(col_left)))
            if get_size(u):
                ps.add_trait("mark", ("val_top", get_size(u)))
                ps.add_trait("mark", ("col_top", get_col(col_top)))

            # counter background and symbol
            ps.add_trait("mark", ("cntr_back_num", CNTR_BACK_COL_NUM.get(u.color.lower(), 1)))
            ps.add_trait("mark", ("symb_back_num", CNTR_FORE_COL_NUM.get(u.color2.lower(), 1)))
            if u_type == "Ski":
                col_symb = "blu"
            if u.home == "Comm China" and u.clas == "SUPP":
                col_symb = "red"
            if u.info is not None:
                if "SS" in u.info:
                    col_symb = "whi"
                if "CBV" in u.info and str(u.name) in CBV_COLOURS:
                    col_symb = CBV_COLOURS[u.name][0]
                    col_symb_text = CBV_COLOURS[u.name][1]
                if "mot" in map(unicode.lower, u.info) or u_type.lower() == "mot":
                    ps.add_trait("mark", ("symb_wheels_num", COL_NUM[col_symb]))
            if u.size == "H":
                ps.add_trait("mark", ("symb_heavy_num", COL_NUM[col_symb]))
            if u_type in ["MIL", "TER", "WAR", "PART"]:
                ps.add_trait("mark", ("symb_text", u_type[0].upper()))
                if u.color2 == "white" and col_symb_text == "whi":
                    col_symb_text = "red"
                if "red" in u.color2.lower() and col_symb_text == "red":
                    col_symb_text = "whi"
                ps.add_trait("mark", ("col_symb_text", get_col(col_symb_text)))
            else:
                if u_type.lower() in ["arm", "mech", "mot", "inf"]:
                    if u.home in ["AUS", "CAN", "IND"]:
                        ps.add_trait("mark", ("symb_text", u.home[:1].upper()))
                        ps.add_trait("mark", ("col_symb_text", get_col(col_symb_text)))
                    if u.home in ["NZ", "SA"]:
                        ps.add_trait("mark", ("symb_text", u.home[:2].upper()))
                        ps.add_trait("mark", ("col_symb_text", get_col(col_symb_text)))

            # style and colour
            val1 = "#000000"
            val2 = "#000000"
            if u.color.lower() == "black":
                val1 = "#ff0000"
                val2 = "#ff0000"
            if u.info is not None:
                if "WP" in u.info:
                    val1 = "#ffffff"
                    val2 = "#ffffff"
                    if u.color.lower() == "white":
                        val1 = "#eeeeee"
                        val2 = "#eeeeee"
                if u.clas == "ART":
                    if "hvy" in map(unicode.lower, u.info):
                        ps.add_trait("mark", ("symb_aa_hvy_num", 1))
                    val1 = "#ffffff"
                    if "grey" in u.info:
                        ps.add_trait("mark", ("art_num", 1))
                    elif "pink" in u.info:
                        ps.add_trait("mark", ("art_num", 2))
                    elif "red" in u.info:
                        ps.add_trait("mark", ("art_num", 3))
                    else:
                        val1 = "#000000"
            ps.add_trait("mark", ("col_valL", val1))
            ps.add_trait("mark", ("col_valR", val2))
            ps.add_trait("prototype", ("UNITlendlease", ""))
            ps.add_trait("prototype", ("LANDvalues", ""))
            if u.clas == "ART":
                ps.add_trait("prototype", ("LANDart", ""))
            if u.home == "Comm China" and u.clas == "SUPP":
                col_symb = "red"
            ps.add_trait("prototype", ("LAND" + col_symb, ""))
            ps.add_trait("prototype", ("LANDbase", ""))

            # add to xml tree
            hook.append(ps.get_xml())
        except Exception, ex:
            print_item = "!"
            raise
        finally:
            print print_item,
    print "(done)"


def inject_air(units_parent=None):
    # init
    global BF, GPID, HEADER, SHEET
    print "INJECT AIR"
    if units_parent is None:
        units_parent = get_units_parent(False)

    # fill containers
    print "reading counters",
    for u in gen_filtered_rowset(sheet=SHEET["A"], header=HEADER["A"],
                                 filt=lambda x: x.type not in ["PILOT"]):
        try:
            # init
            print_item = "."
            u_type = get_type(u)
            print_item = "({})".format(u_type)
            tag, col_symb, col_symb_text, col_left, col_top, col_right = ENTITY_COLOURS[u.home]
            hook, is_minor = get_hook(u, units_parent)

            # piece slot, trait order in R E V E R S E !!
            ps = PieceSlot(u.name or u.year, GPID.get())
            ps.add_trait("prototype", ("ROTATE", "")) # last!

            # game values and info
            ps.add_trait("mark", ("val_info", ",".join(u.info or [])))
            ps.add_trait("mark", ("val_kit", get_kit(u)))
            ps.add_trait("mark", ("val_year", u.year))
            ps.add_trait("mark", ("val_class", u.clas))
            ps.add_trait("mark", ("val_type", u_type))
            ps.add_trait("mark", ("val_cost", u.cost))
            ps.add_trait("mark", ("val_time", u.time))
            # air values
            ps.add_trait("mark", ("val_ata", u.ata if u.ata is not None else "*"))
            ps.add_trait("mark", ("val_ats", u.ats if u.ats is not None else "*"))
            ps.add_trait("mark", ("val_tac", u.tac if u.tac is not None else "*"))
            ps.add_trait("mark", ("val_str", u.str if u.str is not None else "*"))
            ps.add_trait("mark", ("val_rng", u.rng))
            if u_type == "CVP":
                if u.cvp_y1 is not None:
                    ps.add_trait("mark", ("sz1,yr1", u.cvp_s1, u.cvp_y1))
                if u.cvp_y2 is not None:
                    ps.add_trait("mark", ("sz2,yr2", u.cvp_s2, u.cvp_y2))
                if u.cvp_y3 is not None:
                    ps.add_trait("mark", ("sz3,yr3", u.cvp_s3, u.cvp_y3))

            # labels
            if u_type == "FTR":
                name = break_name(u.name)
                if not is_minor:
                    ps.add_trait("mark", ("val_top", name[0]))
                    if len(name) > 1:
                        ps.add_trait("mark", ("val_top2", name[1]))
                    if u.name2 is not None:
                        ps.add_trait("mark", ("val_center3", u.name2))
                else:
                    ps.add_trait("mark", ("val_top", tag))
                    ps.add_trait("mark", ("col_top", get_col(col_left)))
                    ps.add_trait("mark", ("val_center3", u.name))
                if u.info is not None:
                    if "2E" in u.info:
                        ps.add_trait("mark", ("col_valTL", "#fbc834"))
                        ps.add_trait("mark", ("col_valTL_bg", "#808080"))
                    if "NF" in u.info:
                        ps.add_trait("mark", ("valTL_bg_num", 2))
                        if not "2E" in u.info:
                            ps.add_trait("mark", ("col_valTL", "#ffffff"))
            if u_type in ["ATR", "LND"]:
                name = break_name(u.name)
                if len(name) == 1:
                    ps.add_trait("mark", ("val_bottom", name[0]))
                if len(name) == 2:
                    ps.add_trait("mark", ("val_bottom", name[0]))
                    ps.add_trait("mark", ("val_center2", name[1]))
                if u.name2 is not None:
                    name2 = break_name(u.name2)
                    if len(name2) == 1:
                        ps.add_trait("mark", ("val_center2", name2[0]))
                    if len(name2) == 2:
                        ps.add_trait("mark", ("val_center1", name2[0]))
                        ps.add_trait("mark", ("val_center2", name2[1]))
            if u.color.lower() == "black":
                ps.add_trait("mark", ("col_text", "#ff0000"))
                ps.add_trait("mark", ("col_valTL", "#ff0000"))
                ps.add_trait("mark", ("col_valTR", "#ff0000"))
                ps.add_trait("mark", ("col_valBL", "#ff0000"))
            if u_type in ["NAV", "CVP"]:
                name = break_name(u.name)

                if len(name) > 1:
                    ps.add_trait("mark", ("val_top2", name[0]))
                    ps.add_trait("mark", ("val_bottom", name[1]))
                    if u.name2 is not None:
                        ps.add_trait("mark", ("val_top", u.name2))
                else:
                    ps.add_trait("mark", ("val_bottom", name[0]))
                    if u.name2 is not None:
                        ps.add_trait("mark", ("val_top2", u.name2))
            if tag is not None:
                try:
                    col = {
                        "AUS": "#ff0000",
                        "CAN": "#00a2ff",
                        "IND": "#99cc33",
                        "NZ": "#ffffff",
                        "SA": "#fbc834",
                    }[tag]
                    ps.add_trait("mark", ("col_tag", col))
                    ps.add_trait("mark", ("val_center1", tag))
                except:
                    col = get_col(col_left)
                    ps.add_trait("mark", ("col_tag_top", col))
                    ps.add_trait("mark", ("val_top", tag))

            # range and extras
            rng_num = 1
            if u.info is not None and ("ATR" in u.info or "XATR" in u.info):
                rng_num = 3
            if u.info is not None and "EX" in u.info:
                rng_num = 5
            if len(str(u.rng)) > 1:
                rng_num += 1
            ps.add_trait("mark", ("val_rng_num", rng_num))

            # counter background and stripes
            ps.add_trait("mark", ("cntr_back_num", CNTR_BACK_COL_NUM.get(u.color.lower(), 1)))
            if u.info is not None and "FB" in u.info:
                ps.add_trait("mark", ("h_stripe_num", 2))
            is_ll = False
            if u.info is not None:
                for item in u.info:
                    if item.startswith("LL-"):
                        rec = item[3:]
                        ps.add_trait("mark", ("ll_stripe_num", CONTROL_NUM[rec]))
                        is_ll = True
                        break

            # air prototypes
            base = {
                "FTR": "FTR",
                "LND": "LND",
                "ATR": "LND",
                "NAV": "NAV",
                "CVP": "NAV",
                "ABOMB": "FTR",
                "VWEAP": "NAV",
            }[u_type]

            if not is_ll:
                ps.add_trait("prototype", ("UNITlendlease", ""))
            ps.add_trait("prototype", ("AIRrng" + base, ""))
            ps.add_trait("prototype", ("AIRvalues", ""))
            ps.add_trait("prototype", ("AIRbase", ""))

            # add to xml tree
            hook.append(ps.get_xml())
        except Exception, ex:
            print_item = "!"
            raise
        finally:
            print print_item,
    print "(done)"


def inject_naval(units_parent=None):
    # init
    global BF, GPID, HEADER, SHEET
    print "INJECT NAVAL"
    if units_parent is None:
        units_parent = get_units_parent(False)

    # fill containers
    print "reading counters",
    for u in gen_filtered_rowset(sheet=SHEET["N"], header=HEADER["N"],
                                 filt=lambda x: x.type not in ["CONV", "TANK"]):
        try:
            # init
            print_item = "."
            u_type = get_type(u)
            print_item = "({})".format(u_type)
            tag, col_symb, col_symb_text, col_left, col_top, col_right = ENTITY_COLOURS[u.home]
            hook, is_minor = get_hook(u, units_parent)

            # piece slot, trait order in R E V E R S E !!
            ps = PieceSlot(u.name or u.year, GPID.get())
            ps.add_trait("prototype", ("ROTATE", "")) # last!

            # game values and info
            ps.add_trait("mark", ("val_info", ",".join(u.info or [])))
            ps.add_trait("mark", ("val_kit", get_kit(u)))
            ps.add_trait("mark", ("val_year", u.year))
            ps.add_trait("mark", ("val_class", u.clas))
            ps.add_trait("mark", ("val_type", u_type))
            ps.add_trait("mark", ("val_cost", u.cost))
            ps.add_trait("mark", ("val_time", u.time))
            # naval values
            ps.add_trait("mark", ("val_mov", u.mov if u.aa is not None else "0"))
            ps.add_trait("mark", ("val_rng", u.rng if u.aa is not None else "0"))
            ps.add_trait("mark", ("val_atk", u.atk if u.atk is not None else "0"))
            ps.add_trait("mark", ("val_dfs", u.dfs if u.dfs is not None else "0"))
            ps.add_trait("mark", ("val_aa", u.aa if u.aa is not None else "0"))
            if u.cv is not None:
                ps.add_trait("mark", ("val_sb", u.cv))
                if u_type == "FROG":
                    if "Blue" in u.name2:
                        ps.add_trait("mark", ("val_cv_num", 8))
                    if "Violet" in u.name2:
                        ps.add_trait("mark", ("val_cv_num", 9))
                else:
                    ps.add_trait("mark", ("val_cv_num", u.cv))
            else:
                ps.add_trait("mark", ("val_sb", u.sb or "0"))

            # labels
            if u.name is not None:
                ps.add_trait("mark", ("val_name", u.name))
            if u.color.lower() == "black":
                ps.add_trait("mark", ("col_text", "#ff0000"))
            if tag is not None:
                try:
                    col = {
                        "AUS": "#ff0000",
                        "CAN": "#00a2ff",
                        "IND": "#99cc33",
                        "NZ": "#ffffff",
                        "SA": "#fbc834",
                    }[tag]
                except:
                    col = get_col(col_left)
                ps.add_trait("mark", ("col_tag", col))
                ps.add_trait("mark", ("val_tag", tag))

            # range and extras
            if u_type == "ASW":
                if "pink" in u.info:
                    ps.add_trait("mark", ("val_asw_num", 1))
                if "red" in u.info:
                    ps.add_trait("mark", ("val_asw_num", 2))

            # counter background and stripes
            ps.add_trait("mark", ("cntr_back_num", CNTR_BACK_COL_NUM.get(u.color.lower(), 1)))

            # naval prototypes
            if u.name2 is not None and "LL-FR" in u.name2:
                ps.add_trait("mark", ("ll_stripe_num", "4"))
            else:
                ps.add_trait("prototype", ("UNITlendlease", ""))
            ps.add_trait("prototype", ("NAVALvalues", ""))
            ps.add_trait("prototype", ("NAVALbase", ""))

            # add to xml tree
            hook.append(ps.get_xml())
        except Exception, ex:
            print_item = "!"
            raise
        finally:
            print print_item,
    print "(done)"


def tidy_tree():
    def recursively_empty(e):
        if e.text:
            return False
        return all((recursively_empty(c) for c in e.iterchildren()))

    print "tidy up..",
    par_units = get_units_parent()
    for action, elem in ET.iterwalk(par_units):
        # if elem.tag == "VASSAL.build.widget.ListWidget":
        parent = elem.getparent()
        if recursively_empty(elem):
            parent.remove(elem)

    print "done!"
    print

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

    # remove old units tab
    parent = get_units_parent(True)

    # inject counters
    inject_land(parent)
    inject_air(parent)
    inject_naval(parent)

    # finish by writing file back to the archive
    tidy_tree()
    finish(buildfile_new=os.path.join(WORKING_DIR, "buildFile"))
    print "ALL DONE!"
