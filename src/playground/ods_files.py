# -*- coding: utf-8 -*-
# ODS handling for the counter excel file by p.forno
# changelog:
# * making it unicode safe

##---IMPORTS

from ezodf import opendoc

##---CONSTANTS

COUNTER_FILE = '/home/pmeier/Workspace/WIFvassal/res/WiF-AiF-PatiF-Counters.ods'

##---FUNCTIONS

def get_sheet(sheet_name):
    """return a copy of a sheet"""

    return opendoc(COUNTER_FILE).sheets[sheet_name].copy()


def counter_sheet_row_idx_set(sheet, cs):
    """yield the row set for a counter sheet"""

    header = Unit.read_header(sheet)
    col_cs = sheet.column(header['CS'])
    return [i for i, cell in enumerate(col_cs) if cell.value == cs]

##----CLASSES

class Unit(object):
    """unit counter"""

    def __init__(self):
        self.sh_name = None
        self.sh_row = None
        self.side = None
        self.power = None
        self.home = None
        self.clas = None
        self.type = None
        self.name = None
        self.year = None
        self.cost = None
        self.time = None
        self.kit = None
        self.cs = None
        self.row = None
        self.col = None
        self.option = None

    @staticmethod
    def read_header(sheet):
        """read the header information from a sheet (from row 3)"""

        rval = {}
        for i, cell in enumerate(sheet.row(3)):
            rval[cell.value] = i
        return rval

    def update(self, sheet, row_no, header=None):
        """update from sheet row"""

        # header and row
        if header is None:
            header = Unit.read_header(sheet)
        row = sheet.row(row_no)

        # set values
        self.sh_name = sheet.name
        self.sh_row = row_no
        self.side = self.xml_ustr(row[header['SIDE']].value)
        self.power = self.xml_ustr(row[header['POWER']].value)
        self.home = self.xml_ustr(row[header['HOME']].value)
        self.clas = self.xml_ustr(row[header['CLASS']].value)
        self.type = self.xml_ustr(row[header['TYPE']].value)
        self.name = self.xml_ustr(row[header['NAME']].value)
        self.year = self.xml_ustr(row[header['YEAR']].value)
        self.cost = self.xml_int(row[header['COST']].value)
        self.time = self.xml_int(row[header['TIME']].value)
        self.kit = self.xml_ustr(row[header['KIT']].value)
        self.cs = self.xml_int(row[header['CS']].value)
        self.row = self.xml_int(row[header['ROW']].value)
        self.col = self.xml_int(row[header['COL']].value)
        self.option = self.xml_ustr(row[header['OPTION']].value)

        return header, row

    def __unicode__(self):
        return u'{sh_name}#{sh_row} {}'.format(self.__dict__, **self.__dict__)

    def __str__(self):
        return str(self.__unicode__())

    def __cmp__(self, other):
        if self.cs != other.cs:
            return cmp(self.cs, other.cs)
        else:
            if self.row != other.row:
                return cmp(self.row, other.row)
            else:
                return cmp(self.col, other.col)

    @classmethod
    def xml_ustr(cls, v):
        try:
            return v.strip()
        except:
            return u''

    @classmethod
    def xml_int(cls, v):
        try:
            return int(v)
        except:
            try:
                return int(v[1:-1])
            except:
                return None


class LandUnit(Unit):
    def __init__(self):
        super(LandUnit, self).__init__()

        self.str = None
        self.rog = None
        self.mov = None
        self.cost = None
        self.size = None
        self.other = None
        self.abilities = None
        self.used_a = None
        self.aif = None
        self.used_p = None
        self.patif = None
        self.used_pa = None
        self.aif_patif = None

    def update(self, sheet, row_no, header=None):
        # super
        header, row = super(LandUnit, self).update(sheet, row_no, header)

        # set values
        self.str = self.xml_int(row[header['STR']].value)
        if row[header['ROG']].value:
            self.rog = self.xml_int(row[header['ROG']].value)
        self.mov = self.xml_int(row[header['MOV']].value)
        self.size = self.xml_ustr(row[header['SIZE']].value)
        self.other = self.xml_ustr(row[header['OTHER']].value)
        self.abilities = self.xml_ustr(row[header['ABILITIES']].value)
        self.used_a = self.xml_ustr(row[header['USED A']].value)
        self.aif = self.xml_ustr(row[header['AIF']].value)
        self.used_p = self.xml_ustr(row[header['USED P']].value)
        self.patif = self.xml_ustr(row[header['PatiF']].value)
        self.used_pa = self.xml_ustr(row[header['USED PA']].value)
        self.aif_patif = self.xml_ustr(row[header['AiF + PatiF']].value)


class AirUnit(Unit):
    def __init__(self):
        super(AirUnit, self).__init__()

        self.name2 = None
        self.ata = None
        self.ats = None
        self.tac = None
        self.str = None
        self.rng = None
        self.other = None
        self.used = None
        self.cvp_y1 = None
        self.cvp_s1 = None
        self.cvp_y2 = None
        self.cvp_s2 = None
        self.cvp_y3 = None
        self.cvp_s3 = None

    def update(self, sheet, row_no, header=None):
        # super
        header, row = super(AirUnit, self).update(sheet, row_no, header)

        # set values
        self.name2 = self.xml_ustr(row[header['NAME2']].value)
        self.ata = self.xml_int(row[header['ATA']].value)
        self.ats = self.xml_int(row[header['ATS']].value)
        self.tac = self.xml_int(row[header['TAC']].value)
        self.str = self.xml_int(row[header['STR']].value)
        self.rng = self.xml_int(row[header['RANGE']].value)
        self.other = self.xml_ustr(row[header['OTHER']].value)
        self.used = self.xml_ustr(row[header['USED']].value)
        self.cvp_y1 = self.xml_int(row[header['YR1']].value)
        self.cvp_s1 = self.xml_int(row[header['SIZ1']].value)
        self.cvp_y2 = self.xml_int(row[header['YR2']].value)
        self.cvp_s2 = self.xml_int(row[header['SIZ2']].value)
        self.cvp_y3 = self.xml_int(row[header['YR3']].value)
        self.cvp_s3 = self.xml_int(row[header['SIZ3']].value)


class NavalUnit(Unit):
    def __init__(self):
        super(NavalUnit, self).__init__()

        self.name2 = None
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
        header, row = super(NavalUnit, self).update(sheet, row_no, header)

        # set values
        self.name2 = self.xml_ustr(row[header['NAME2']].value)
        self.att = self.xml_int(row[header['ATT']].value)
        self.dfs = self.xml_int(row[header['DEF']].value)
        self.aa = self.xml_int(row[header['AA']].value)
        self.sb = self.xml_int(row[header['SB']].value)
        self.rng = self.xml_int(row[header['RNG']].value)
        self.mov = self.xml_int(row[header['MOV']].value)
        self.cv = self.xml_int(row[header['CV']].value)
        self.sunk = self.xml_ustr(row[header['SUNK']].value)
        self.used = self.xml_ustr(row[header['USED']].value)

##---MAIN

if __name__ == '__main__':
    MODE = 'Naval'
    CS = 5
    SH = get_sheet(MODE)
    header = Unit.read_header(SH)
    cs_rids = counter_sheet_row_idx_set(SH, CS)
    CS = []
    for rid in cs_rids:
        u = {'Land': LandUnit,
             'Air': AirUnit,
             'Naval': NavalUnit}[MODE]()
        u.update(SH, rid, header)
        CS.append(u)

    def pp_cs(cs):
        for u in cs:
            print u
            name = ' '.join([u.name, getattr(u, 'name2', '')]).strip()
            print u'({cs:02d}:{row:02d}-{col:02d}) [{type:s}] {name:s}'.format(
                cs=u.cs, row=u.row, col=u.col, type=u.type, name=name)#,
            #print '[CV: {}]'.format(u.cv)

    pp_cs(CS)
    print '#' * 20

    CS.sort()
    pp_cs(CS)
