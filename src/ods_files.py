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
        self.deleted = None

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
        self.side = self.xml_ustr(row[header['SIDE']])
        self.power = self.xml_ustr(row[header['POWER']])
        self.home = self.xml_ustr(row[header['HOME']])
        self.clas = self.xml_ustr(row[header['CLASS']])
        self.type = self.xml_ustr(row[header['TYPE']])
        self.name = self.xml_ustr(row[header['NAME']])
        self.year = self.xml_ustr(row[header['YEAR']])
        self.cost = self.xml_int(row[header['COST']])
        self.time = self.xml_int(row[header['TIME']])
        self.kit = self.xml_ustr(row[header['KIT']])
        self.cs = self.xml_int(row[header['CS']])
        self.row = self.xml_int(row[header['ROW']])
        self.col = self.xml_int(row[header['COL']])
        self.option = self.xml_ustr(row[header['OPTION']])
        self.deleted = self.xml_ustr(row[header['DELETED']])

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
    def xml_ustr(cls, cell):
        try:
            rval = {'string': unicode,
                    'float': lambda x: unicode(int(x)),
                    'percentage': lambda x: u'{:02.2f}'.format(x),
                    'currency': lambda x: u'{s}{:.2f}'.format(x),
                    'boolean': unicode,
                    'date': unicode,
                    'time': unicode,
                   }[cell.value_type](cell.value).strip().replace('/', '\/')
        except:
            rval = None
        finally:
            return unicode(rval)

    @classmethod
    def xml_int(cls, cell):
        try:
            rval = {'string': unicode,
                    'float': int,
                   }[cell.value_type](cell.value)
        except:
            try:
                rval = int(cell.value[1:-1])
            except:
                rval = None
        finally:
            try:
                rval = int(rval)
            except:
                rval = None
        return rval


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
        self.str = self.xml_int(row[header['STR']])
        if row[header['ROG']].value:
            self.rog = self.xml_int(row[header['ROG']])
        self.mov = self.xml_int(row[header['MOV']])
        self.size = self.xml_ustr(row[header['SIZE']])
        self.other = self.xml_ustr(row[header['OTHER']])
        self.abilities = self.xml_ustr(row[header['ABILITIES']])
        self.used_a = self.xml_ustr(row[header['USED A']])
        self.aif = self.xml_ustr(row[header['AIF']])
        self.used_p = self.xml_ustr(row[header['USED P']])
        self.patif = self.xml_ustr(row[header['PatiF']])
        self.used_pa = self.xml_ustr(row[header['USED PA']])
        self.aif_patif = self.xml_ustr(row[header['AiF + PatiF']])


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
        self.name2 = self.xml_ustr(row[header['NAME2']])
        self.ata = self.xml_int(row[header['ATA']])
        self.ats = self.xml_int(row[header['ATS']])
        self.tac = self.xml_int(row[header['TAC']])
        self.str = self.xml_int(row[header['STR']])
        self.rng = self.xml_int(row[header['RANGE']])
        self.other = self.xml_ustr(row[header['OTHER']])
        self.used = self.xml_ustr(row[header['USED']])
        self.cvp_y1 = self.xml_int(row[header['YR1']])
        self.cvp_s1 = self.xml_int(row[header['SIZ1']])
        self.cvp_y2 = self.xml_int(row[header['YR2']])
        self.cvp_s2 = self.xml_int(row[header['SIZ2']])
        self.cvp_y3 = self.xml_int(row[header['YR3']])
        self.cvp_s3 = self.xml_int(row[header['SIZ3']])


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
        self.name2 = self.xml_ustr(row[header['NAME2']])
        self.att = self.xml_int(row[header['ATT']])
        self.dfs = self.xml_int(row[header['DEF']])
        self.aa = self.xml_int(row[header['AA']])
        self.sb = self.xml_int(row[header['SB']])
        self.rng = self.xml_int(row[header['RNG']])
        self.mov = self.xml_int(row[header['MOV']])
        self.cv = self.xml_int(row[header['CV']])
        self.sunk = self.xml_ustr(row[header['SUNK']])
        self.used = self.xml_ustr(row[header['USED']])

##---MAIN

if __name__ == '__main__':
    MODE = 'Naval'
    CS = 1
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
