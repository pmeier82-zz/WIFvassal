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

CONTROL_NUM = {
    "CH": 2,
    "CC": 3,
    "CWblue": 4,
    "CW": 5,
    "FR": 6,
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
    "Cdo": 29,
    "Art": 30,
    "SP": 31,
    "AT": 32,
    "TD": 33,
    "AA": 34,
    "AAA": 35,
    "SAM": 36,
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
    "Rep Spain": ("SR", "red", "red", "red", "blk", "blk"),
    "Sweden": ("Swe", "blu", "blu", "blu", "blk", "blk"),
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

    ## CW TERR
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

    ## FR TERR
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

    ## IT TERR
    "It. Somali": (None, "blu", "blu", "blk", "blk", "blk"),
    "AOI": (None, "gre", "red", "blk", "blk", "blk"),

    ## ITALY
    "Italy": (None, "blk", "red", "blk", "blk", "blk"),

    ## JP TERR
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
        }[pwr]
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
        u"Fl.Pz.": "PARA",
    }.get(u.type, u.type)
    if hasattr(u, "size"):
        if u.size == "Div":
            try:
                return {
                    u"MTN / CAV": "Mtn",
                    u"MTN / MAR": "Cdo",
                    u"MAR / PARA": "Cdo",
                    u"ENG ARM": "Eng",
                }[rval]
            except:
                if u.clas not in ["SUPP", "ART"]:
                    rval = rval[0].upper() + rval[1:].lower()
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
    unt_box = game_pieces.find("VASSAL.build.widget.BoxWidget[@entryName=\"Units\"]")

    # build if not present or rebuild if flaged
    if unt_box is None or (unt_box is not None and rebuild is True):
        print "rebuilding unit parent!!"
        game_pieces.remove(unt_box)
        game_pieces \
            .find("VASSAL.build.widget.BoxWidget[@entryName=\"General\"]") \
            .addnext(
            ET.Element(
                "VASSAL.build.widget.BoxWidget",
                entryName="Units"
            ))
        unt_box = game_pieces.find("VASSAL.build.widget.BoxWidget[@entryName=\"Units\"]")

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
            parent_power = ET.SubElement(
                unt_box,
                "VASSAL.build.widget.TabWidget",
                entryName=power_name
            )

            # land
            land_tab = ET.SubElement(
                parent_power,
                "VASSAL.build.widget.TabWidget",
                entryName="LAND",
            )
            arm_tab = ET.SubElement(
                land_tab,
                "VASSAL.build.widget.ListWidget",
                entryName="ARM",
                divider="250"
            )
            for arm_type in ["HQA", "ARM", "Arm", "MECH", "Mech", "Eng"]:
                ET.SubElement(
                    arm_tab,
                    "VASSAL.build.widget.ListWidget",
                    entryName="<<" + arm_type,
                    divider="150"
                )
            cav_tab = ET.SubElement(
                land_tab,
                "VASSAL.build.widget.ListWidget",
                entryName="CAV",
                divider="250"
            )
            for cav_type in ["ACV", "CAV", "Cav", "MTN"]:
                ET.SubElement(
                    cav_tab,
                    "VASSAL.build.widget.ListWidget",
                    entryName="<<" + cav_type,
                    divider="150"
                )
            inf_tab = ET.SubElement(
                land_tab,
                "VASSAL.build.widget.ListWidget",
                entryName="INF",
                divider="250"
            )
            for inf_type in [
                "HQI", "MOT", "Mot", "INF", "Inf", "GARR", "Garr",
                "MTN", "Mtn", "MAR", "Mar", "PARA", "Para",
                "Eng", "Ski", "TERR", "MIL"]:
                ET.SubElement(
                    inf_tab,
                    "VASSAL.build.widget.ListWidget",
                    entryName="<<" + inf_type,
                    divider="150"
                )
            art_tab = ET.SubElement(
                land_tab,
                "VASSAL.build.widget.ListWidget",
                entryName="ART",
                divider="250"
            )
            for art_type in ["ART", "AT", "AA", "FLAK"]:
                ET.SubElement(
                    art_tab,
                    "VASSAL.build.widget.ListWidget",
                    entryName="<<" + art_type,
                    divider="150"
                )
            other_tab = ET.SubElement(
                land_tab,
                "VASSAL.build.widget.ListWidget",
                entryName="OTHER",
                divider="250"
            )

            # air
            air_tab = ET.SubElement(
                parent_power,
                "VASSAL.build.widget.ListWidget",
                entryName="AIR",
                divider="250"
            )
            for air_type in ["FTR", "LND", "NAV", "ATR", "CVP", "BOMB"]:
                ET.SubElement(
                    air_tab,
                    "VASSAL.build.widget.ListWidget",
                    entryName="<<" + air_type,
                    divider="150"
                )
            other_tab = ET.SubElement(
                air_tab,
                "VASSAL.build.widget.ListWidget",
                entryName="<<" + "OTHER",
                divider="150"
            )

            # naval
            land_tab = ET.SubElement(
                parent_power,
                "VASSAL.build.widget.TabWidget",
                entryName="NAVAL",
            )

            # other
            land_tab = ET.SubElement(
                parent_power,
                "VASSAL.build.widget.TabWidget",
                entryName="OTHER",
            )

        # minors
        parent_power = ET.SubElement(
            unt_box,
            "VASSAL.build.widget.BoxWidget",
            entryName="Minors"
        )

    # return
    return game_pieces.find("VASSAL.build.widget.BoxWidget[@entryName=\"Units\"]")


def get_minor_proto(power_name):
    rval = ET.Element(
        "VASSAL.build.widget.TabWidget",
        entryName=power_name
    )
    # land
    land_tab = ET.SubElement(
        rval,
        "VASSAL.build.widget.ListWidget",
        entryName="LAND",
        divider="250"
    )
    land_div = ET.SubElement(
        land_tab,
        "VASSAL.build.widget.ListWidget",
        entryName=">>DIV",
        divider="150"
    )
    type_hvy = ET.SubElement(
        land_tab,
        "VASSAL.build.widget.ListWidget",
        entryName=">>HVY",
        divider="150"
    )
    # air
    land_tab = ET.SubElement(
        rval,
        "VASSAL.build.widget.ListWidget",
        entryName="AIR",
        divider="250"
    )
    # naval
    land_tab = ET.SubElement(
        rval,
        "VASSAL.build.widget.ListWidget",
        entryName="NAVAL",
        divider="250"
    )
    return rval


def cw_kif_only(u):
    if u.power == "Commonwealth":
        return u.kit == "KiF"
    else:
        return True


def inject_land():
    """run over all counters and put them in the right place"""

    # init
    global BF, GPID, HEADER, SHEET
    par_units = get_units_parent()
    print "INJECT LAND"

    # fill containers
    print "reading counters",
    for u in gen_filtered_rowset(sheet=SHEET["L"], header=HEADER["L"],
                                 filt=lambda x: x.type not in ["LEAD", "FORT", "FACT", "PART"] and cw_kif_only(x)):
        try:
            # init
            print_item = "."
            u_clas = get_clas(u)
            u_type = get_type(u)
            print_item = "({})".format(u_type)
            tag, col_symb, col_symb_text, col_left, col_top, col_right = ENTITY_COLOURS[u.home]

            # where to place it
            is_minor = False
            hook = None
            if get_power(u) == "Minors":
                is_minor = True
                par_minors = par_units.find("VASSAL.build.widget.BoxWidget[@entryName=\"Minors\"]")
                par_power = par_minors.find("VASSAL.build.widget.TabWidget[@entryName=\"{}\"]".format(u.power))
                if par_power is None:
                    par_power = get_minor_proto(u.power)
                    par_minors.append(par_power)
                hook = par_power.find("VASSAL.build.widget.ListWidget[@entryName=\"LAND\"]")
            else:
                par_power = par_units.find("VASSAL.build.widget.TabWidget[@entryName=\"{}\"]".format(u.power))
                par_land = par_power.find("VASSAL.build.widget.TabWidget[@entryName=\"LAND\"]")
                par_clas = par_land.find("VASSAL.build.widget.ListWidget[@entryName=\"{}\"]".format(u_clas))
                if par_clas is not None:
                    par_type = par_clas.find("VASSAL.build.widget.ListWidget[@entryName=\"<<{}\"]".format(
                        {"AAA": "FLAK", "SAM": "FLAK"}.get(u_type, u_type)))
                    if par_type is not None:
                        hook = par_type
                if hook is None:
                    hook = par_land.find("VASSAL.build.widget.ListWidget[@entryName=\"OTHER\"]")

            # piece slot, trait order in R E V E R S E !!
            ps = PieceSlot(u.name or u.year, GPID.get())
            ps.add_trait("prototype", ("ROTATE", "")) # last!

            # game values and info
            ps.add_trait("mark", ("val_info", ",".join(u.info or [])))
            ps.add_trait("mark", ("val_kit", u.kit))
            ps.add_trait("mark", ("val_year", u.year))
            ps.add_trait("mark", ("val_class", u.clas))
            ps.add_trait("mark", ("val_type", u_type))
            ps.add_trait("mark", ("val_mv", u.mov))
            if u.rog:
                ps.add_trait("mark", ("val_ro", u.rog))
            ps.add_trait("mark", ("val_cf", u.str or 0))

            # labels
            if u.info is not None and "SS" in u.info:
                col_left = col_right = col_top = "whi"
            if u.name is not None and "siberian" in u.name:
                col_left = col_top = "whi"
            if u.name is not None and u.name == "GGFF":
                col_left = col_right = col_top = col_symb = "yel"
            if not is_minor:
                col_left = col_right = col_top = "blk"
            if is_minor is True:
                ps.add_trait("mark", ("val_left", tag))
                ps.add_trait("mark", ("col_left", COL_CODE[col_left]))
                if u.name:
                    ps.add_trait("mark", ("val_right", u.name))
                    ps.add_trait("mark", ("col_right", COL_CODE[col_right]))
            else:
                if u.name:
                    ps.add_trait("mark", ("val_left", u.name))
                    ps.add_trait("mark", ("col_left", COL_CODE[col_left]))
            if get_size(u):
                ps.add_trait("mark", ("val_top", get_size(u)))
                ps.add_trait("mark", ("col_top", COL_CODE[col_top]))

            # counter background and symbol
            if u_type == "Ski":
                col_symb = "blu"
            if u.home == "Comm China" and u.clas == "SUPP":
                col_symb = "red"
            if u.info is not None and "SS" in u.info:
                col_symb = "whi"
            if u.info is not None and "CBV" in u.info and str(u.name) in CBV_COLOURS:
                col_symb = CBV_COLOURS[u.name][0]
                col_symb_text = CBV_COLOURS[u.name][1]
            ps.add_trait("mark", ("cntr_back_num", CNTR_BACK_COL_NUM.get(u.color.lower(), 1)))
            ps.add_trait("mark", ("symb_back_num", CNTR_FORE_COL_NUM.get(u.color2.lower(), 1)))
            if u.info is not None and "mot" in map(unicode.lower, u.info) or u_type.lower() == "mot":
                ps.add_trait("mark", ("symb_wheels_num", COL_NUM[col_symb]))
            if u.size == "H":
                ps.add_trait("mark", ("symb_heavy_num", COL_NUM[col_symb]))
            if u_type in ["MIL", "TERR", "WAR"]:
                ps.add_trait("mark", ("symb_text", u.type[0].upper()))
                if u.color2 == "white" and col_symb_text == "whi":
                    col_symb_text = "red"
                if "red" in u.color2.lower() and col_symb_text == "red":
                    col_symb_text = "whi"
                ps.add_trait("mark", ("col_symb_text", COL_CODE[col_symb_text]))
            else:
                if u_type.lower() in ["arm", "mech", "mot", "inf"]:
                    if u.home in ["AUS", "CAN", "IND"]:
                        ps.add_trait("mark", ("symb_text", u.home[:1].upper()))
                        ps.add_trait("mark", ("col_symb_text", COL_CODE[col_symb_text]))
                    if u.home in ["NZ", "SA"]:
                        ps.add_trait("mark", ("symb_text", u.home[:2].upper()))
                        ps.add_trait("mark", ("col_symb_text", COL_CODE[col_symb_text]))

            # style and colour
            val1 = "#000000"
            val1_bg = "#ffffff"
            val2 = "#000000"
            val2_bg = "#ffffff"
            if u.color.lower() == "black":
                val1 = "#ff0000"
                val1_bg = "#808080"
                val2 = "#ff0000"
                val2_bg = "#808080"
            if u.info is not None:
                if "WP" in u.info:
                    val1 = "#ffffff"
                    val1_bg = "#000000"
                    val2 = "#ffffff"
                    val2_bg = "#000000"
                    if u.color.lower() == "black":
                        val1 = "#ffffff"
                        val1_bg = "#808080"
                        val2 = "#ffffff"
                        val2_bg = "#808080"
                elif u.clas == "ART":
                    if "hvy" in map(unicode.lower, u.info):
                        ps.add_trait("mark", ("symb_aa_hvy_num", 1))
                    val1 = "#ffffff"
                    val1_bg = "#000000"
                    if "grey" in u.info:
                        ps.add_trait("mark", ("art_num", 1))
                    elif "pink" in u.info:
                        ps.add_trait("mark", ("art_num", 2))
                    elif "red" in u.info:
                        ps.add_trait("mark", ("art_num", 3))
                    else:
                        val1 = "#000000"
                        val1_bg = "#ffffff"
            ps.add_trait("mark", ("col_valL", val1))
            ps.add_trait("mark", ("col_valL_bg", val1_bg))
            ps.add_trait("mark", ("col_valR", val2))
            ps.add_trait("mark", ("col_valR_bg", val2_bg))
            ps.add_trait("prototype", ("UNITll", ""))
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


def inject_air():
    # init
    global BF, GPID, HEADER, SHEET
    par_units = get_units_parent()
    print "INJECT AIR"

    # fill containers
    print "reading counters",
    for u in gen_filtered_rowset(sheet=SHEET["A"], header=HEADER["A"],
                                 filt=lambda x: x.type not in ["PILOT"] and cw_kif_only(x)):
        try:
            # init
            print_item = "."
            u_clas = get_clas(u)
            u_type = get_type(u)
            print_item = "({})".format(u_type)
            tag, col_symb, col_symb_text, col_left, col_top, col_right = ENTITY_COLOURS[u.home]

            # where to place it
            is_minor = False
            hook = None
            if get_power(u) == "Minors":
                is_minor = True
                par_minors = par_units.find("VASSAL.build.widget.BoxWidget[@entryName=\"Minors\"]")
                par_power = par_minors.find("VASSAL.build.widget.TabWidget[@entryName=\"{}\"]".format(u.power))
                if par_power is None:
                    par_power = get_minor_proto(u.power)
                    par_minors.append(par_power)
                hook = par_power.find("VASSAL.build.widget.ListWidget[@entryName=\"AIR\"]")
            else:
                par_power = par_units.find("VASSAL.build.widget.TabWidget[@entryName=\"{}\"]".format(u.power))
                par_air = par_power.find("VASSAL.build.widget.ListWidget[@entryName=\"AIR\"]")
                par_type = par_air.find("VASSAL.build.widget.ListWidget[@entryName=\"<<{}\"]".format(u_type))
                if par_type is not None:
                    hook = par_type
                else:
                    hook = par_air.find("VASSAL.build.widget.ListWidget[@entryName=\"<<OTHER\"]")

            # piece slot, trait order in R E V E R S E !!
            ps = PieceSlot(u.name or u.year, GPID.get())
            ps.add_trait("prototype", ("ROTATE", "")) # last!

            # game values and info
            ps.add_trait("mark", ("val_info", ",".join(u.info or [])))
            ps.add_trait("mark", ("val_kit", u.kit))
            ps.add_trait("mark", ("val_year", u.year))
            ps.add_trait("mark", ("val_class", u.clas))
            ps.add_trait("mark", ("val_type", u_type))
            ps.add_trait("mark", ("val_ata", u.ata if u.ata is not None else "*"))
            ps.add_trait("mark", ("val_ats", u.ats if u.ats is not None else "*"))
            ps.add_trait("mark", ("val_tac", u.tac if u.tac is not None else "*"))
            ps.add_trait("mark", ("val_str", u.str if u.str is not None else "*"))
            ps.add_trait("mark", ("val_rng", u.rng))

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
                    ps.add_trait("mark", ("col_top", COL_CODE[col_left]))
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
                    col = COL_CODE[col_left]
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

            ps.add_trait("prototype", ("AIRrng" + base, ""))
            if not is_ll:
                ps.add_trait("prototype", ("UNITll", ""))
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


def inject_naval(cs_no):
    pass


def tidy_tree():
    def recursively_empty(e):
        if e.text:
            return False
        return all((recursively_empty(c) for c in e.iterchildren()))

    print "tidy up"
    par_units = get_units_parent()
    for action, elem in ET.iterwalk(par_units):
        if elem.tag == "VASSAL.build.widget.ListWidget":
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
    get_units_parent(True)

    # inject counters
    inject_land()
    inject_air()

    # finish by writing file back to the archive
    tidy_tree()
    finish(buildfile_new=os.path.join(WORKING_DIR, "buildFile"))
    print "ALL DONE!"
