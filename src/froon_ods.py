# -*- coding: utf-8 -*-
# ODS handling for the counter excel file by Partrice Forno
# changelog:
# * making it unicode safe

## IMPORTS

from ezodf import opendoc

## CONSTANTS

#COUNTER_FILE = "/home/pmeier/Workspace/WIFvassal/res/WiF-AiF-PatiF-Counters.ods"
COUNTER_FILE = "/home/pmeier/Dropbox/Stuff/games/wif/aid-counters-fr.ods"
ROW_HEADER = 3
ROW_LAST_LAND = 2643
ROW_LAST_AIR = 2065
ROW_LAST_NAVAL = 2812

## FUNCTIONS

def get_sheet(sheet_name):
    return opendoc(COUNTER_FILE).sheets[sheet_name].copy()


def read_header(sheet):
    rval = {}
    for i, cell in enumerate(sheet.row(ROW_HEADER)):
        rval[cell.value] = i
    return rval


def xml_ustr(cell):
    try:
        rval = {
            "string": unicode,
            "float": lambda x: unicode(int(x)),
            "percentage": lambda x: u"{:02.2f}".format(x),
            "currency": lambda x: u"{s}{:.2f}".format(x),
            "boolean": unicode,
            "date": unicode,
            "time": unicode,
        }[cell.value_type](cell.value).strip().replace("/", "\/")
    except:
        rval = None
    finally:
        return rval


def xml_int(cell):
    try:
        if cell.value is None:
            return None
        rval = {
            "string": unicode,
            "float": int,
            "boolean": int,
        }[cell.value_type](cell.value)
    except:
        try:
            rval = float(cell.value[1:-1])
        except:
            rval = None
    finally:
        try:
            rval = int(rval)
        except:
            rval = None
    return rval

## row sets

def gen_filtered_rowset(sheet, header=None, filt=None):
    header = header or read_header(sheet)
    MODE = sheet.name[6:]
    last = {
        "Land": ROW_LAST_LAND,
        "Air": ROW_LAST_AIR,
        "Naval": ROW_LAST_NAVAL,
    }[MODE]
    cnt_cls = {
        "Land": LandCounter,
        "Air": AirCounter,
        "Naval": NavalCounter
    }[MODE]
    for rid in xrange(ROW_HEADER, last):
        try:
            u = cnt_cls()
            u.update(sheet, rid, header)
            if filt is not None:
                if filt(u):
                    yield u
        except:
            pass

## CLASSES

class Counter(object):
    """counter base class"""

    def __init__(self):
        # sheet info
        self.sh_name = None
        self.sh_row = None
        # counter info
        self.side = None
        self.power = None
        self.home = None
        self.clas = None
        self.type = None
        self.name = None
        self.name2 = None
        self.year = None
        self.cost = None
        self.time = None
        # game info
        self.info = None
        self.kit = None
        self.options = None
        self.used = None
        self.color = None
        self.color2 = None

    def update(self, sheet, row_no, header=None):
        # header and row
        if header is None:
            header = read_header(sheet)
        row_data = sheet.row(row_no)
        # sheet info
        self.sh_name = sheet.name
        if self.sh_name.startswith("CopyOf"):
            self.sh_name = self.sh_name[6:]
        self.sh_row = row_no
        # counter info
        self.side = {
            u"": u"N",
            u"C": u"C",
            u"L": u"D",
            u"X": u"F",
        }[xml_ustr(row_data[header["SIDE"]])]
        self.power = xml_ustr(row_data[header["POWER"]])
        self.home = xml_ustr(row_data[header["HOME"]])
        self.clas = xml_ustr(row_data[header["CLASS"]])
        self.type = xml_ustr(row_data[header["TYPE"]])
        self.year = xml_ustr(row_data[header["YEAR"]])
        self.time = xml_int(row_data[header["TIME"]])
        # game info
        self.kit = xml_ustr(row_data[header["KIT"]])
        self.option = xml_ustr(row_data[header["OPTION"]])
        # return
        return header, row_data

    def __unicode__(self):
        return u"{sh_name}#{sh_row} {}".format(self.__dict__, **self.__dict__)

    def __str__(self):
        return str(self.__unicode__())

    def __cmp__(self, other):
        def is_num(x):
            try:
                int(x)
                return True
            except (ValueError, TypeError):
                return False

        if self.power != other.power:
            return cmp(self.power, other.power)
        else:
            if self.type != other.type:
                return cmp(self.type, other.type)
            else:
                self_is_num = is_num(self.year)
                other_is_num = is_num(other.year)
                if self_is_num != other_is_num:
                    if self_is_num:
                        return 1
                    if other_is_num:
                        return -1
                else:
                    if self_is_num and other_is_num:
                        return cmp(self.year, other.year)
                    else:
                        if self.year == "Res":
                            return 1
                        return cmp(self.name, other.name)


class LandCounter(Counter):
    """land counter class"""

    def __init__(self):
        # super
        super(LandCounter, self).__init__()
        # land counter values
        self.str = None
        self.rog = None
        self.mov = None
        self.size = None

    def update(self, sheet, row_no, header=None):
        # super
        header, row_data = super(LandCounter, self).update(sheet, row_no, header)
        # counter values
        self.cost = xml_int(row_data[header["COST"]])
        self.name = xml_ustr(row_data[header["UNIT"]])
        self.info = xml_ustr(row_data[header["OTHER"]])
        if self.info:
            self.info = self.info.replace(",", " ").split()
        abili = xml_ustr(row_data[header["ABILITIES"]])
        if abili:
            self.info.append(u"abilities{}".format(map(int, abili.replace(",", " ").split())))
        self.used = {
            u"Y": True,
            u"N": False,
        }[xml_ustr(row_data[header["USED PA"]])]
        self.color = xml_ustr(row_data[header["BACK COLOR"]])
        self.color2 = xml_ustr(row_data[header["FORE COLOR"]])
        # land counter values
        self.str = xml_int(row_data[header["Strength"]])
        self.rog = xml_int(row_data[header[u"R\xe9org"]])
        self.mov = xml_int(row_data[header["Move"]])
        self.size = xml_ustr(row_data[header["SIZE"]])


class AirCounter(Counter):
    def __init__(self):
        # super
        super(AirCounter, self).__init__()
        # air counter values
        self.ata = None
        self.ats = None
        self.tac = None
        self.str = None
        self.rng = None
        self.cvp_y1 = None
        self.cvp_s1 = None
        self.cvp_y2 = None
        self.cvp_s2 = None
        self.cvp_y3 = None
        self.cvp_s3 = None

    def update(self, sheet, row_no, header=None):
        # super
        header, row_data = super(AirCounter, self).update(sheet, row_no, header)
        # counter values
        self.cost = xml_int(row_data[header["$(ifP)"]])
        self.name = xml_ustr(row_data[header["UNIT"]])
        self.name2 = xml_ustr(row_data[header["NAME"]])
        self.info = xml_ustr(row_data[header["OTHER"]])
        if self.info:
            self.info = self.info.replace(",", " ").split()
        self.used = {
            u"Y": True,
            u"N": False,
        }[xml_ustr(row_data[header["USED1"]])]
        # ait counter values
        self.ata = xml_int(row_data[header["ATA"]])
        self.ats = xml_int(row_data[header["ATS"]])
        self.tac = xml_int(row_data[header["TAC"]])
        self.str = xml_int(row_data[header["STR"]])
        self.rng = xml_int(row_data[header["RANGE"]])
        self.cvp_y1 = xml_int(row_data[header["YR1"]])
        self.cvp_s1 = xml_int(row_data[header["SIZ1"]])
        self.cvp_y2 = xml_int(row_data[header["YR2"]])
        self.cvp_s2 = xml_int(row_data[header["SIZ2"]])
        self.cvp_y3 = xml_int(row_data[header["YR3"]])
        self.cvp_s3 = xml_int(row_data[header["SIZ3"]])


class NavalCounter(Counter):
    def __init__(self):
        # super
        super(NavalCounter, self).__init__()
        # naval counter values
        self.att = None
        self.dfs = None
        self.aa = None
        self.sb = None
        self.rng = None
        self.mov = None
        self.cv = None
        self.cost2 = None
        self.sunk = None
        self.used = None

    def update(self, sheet, row_no, header=None):
        # super
        header, row_data = super(NavalCounter, self).update(sheet, row_no, header)
        # counter values
        self.cost = xml_int(row_data[header["COST1"]])
        self.name = xml_ustr(row_data[header["SHIP1"]])
        self.name2 = xml_ustr(row_data[header["SHIP2"]])
        self.info = xml_ustr(row_data[header["SUNK"]])
        self.used = {
            u"Y": True,
            u"N": False,
        }[xml_ustr(row_data[header["USED2"]])]
        # naval counter values
        self.type = xml_ustr(row_data[header["T2"]])
        self.att = xml_int(row_data[header["ATT"]])
        self.dfs = xml_int(row_data[header["DEF"]])
        self.aa = xml_int(row_data[header["AA"]])
        self.sb = xml_int(row_data[header["SB"]])
        self.rng = xml_int(row_data[header["RNG"]])
        self.mov = xml_int(row_data[header["MOV"]])
        self.cv = xml_int(row_data[header["CV"]])

## MAIN

if __name__ == "__main__":
    MODE = "Land"
    SH = get_sheet(MODE)
    header = read_header(SH)
    CS = []
    us_filt = lambda c: c.power == "USA" and c.used
    for unit in gen_filtered_rowset(sheet=SH, header=header, filt=us_filt):
        CS.append(unit)

    def pp_cs(cs):
        for u in cs:
            name = " ".join([u.name or "", u.name2 or ""]).strip()
            print u"{type:<10s} {name:<10s} {year}".format(type=u.type, name=name, year=u.year or "")

    pp_cs(sorted(CS))
    # CS.sort()
    # pp_cs(CS)
