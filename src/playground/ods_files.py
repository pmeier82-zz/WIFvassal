# ODS handling for the counter excel file by p.forno

##---IMPORTS

from ezodf import opendoc

##---CONSTANTS

COUNTER_FILE = '/home/pmeier/Workspace/WIFvassal/res/'\
               'WiF-AiF-PatiF-Counters.ods'

##---FUNCTIONS

def get_sheet(sheet_name):
    """return a copy of a sheet"""

    return opendoc(COUNTER_FILE).sheets[sheet_name].copy()


def counter_sheet_row_idx_set(sheet, cs):
    """yield the row set of a counter sheet"""

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
        self.side = self.xml_str(row[header['SIDE']].plaintext())
        self.power = self.xml_str(row[header['POWER']].plaintext())
        self.home = self.xml_str(row[header['HOME']].plaintext())
        self.clas = self.xml_str(row[header['CLASS']].plaintext())
        self.type = self.xml_str(row[header['TYPE']].plaintext())
        self.name = self.xml_str(row[header['NAME']].plaintext())
        self.year = self.xml_str(row[header['YEAR']].plaintext())
        self.cost = self.xml_int(row[header['COST']].plaintext())
        self.time = self.xml_int(row[header['TIME']].plaintext())
        self.kit = self.xml_str(row[header['KIT']].plaintext())
        self.cs = self.xml_int(row[header['CS']].value)
        self.row = self.xml_int(row[header['ROW']].value)
        self.col = self.xml_int(row[header['COL']].value)
        self.option = self.xml_str(row[header['OPTION']].plaintext())

        return header, row

    def __str__(self):
        return '{sh_name}#{sh_row} {}'.format(self.__dict__, **self.__dict__)

    def __cmp__(self, other):
        if self.cs != other.cs:
            return cmp(self.cs, other.cs)
        else:
            if self.row != other.row:
                return cmp(self.row, other.row)
            else:
                return cmp(self.col, other.col)

    @classmethod
    def xml_str(cls, v):
        try:
            return v.strip()
        except:
            return 'ERROR'

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
        self.size = self.xml_str(row[header['SIZE']].plaintext())
        self.other = self.xml_str(row[header['OTHER']].plaintext())
        self.abilities = self.xml_str(row[header['ABILITIES']].plaintext())
        self.used_a = self.xml_str(row[header['USED A']].plaintext())
        self.aif = self.xml_str(row[header['AIF']].plaintext())
        self.used_p = self.xml_str(row[header['USED P']].plaintext())
        self.patif = self.xml_str(row[header['PatiF']].plaintext())
        self.used_pa = self.xml_str(row[header['USED PA']].plaintext())
        self.aif_patif = self.xml_str(row[header['AiF + PatiF']].plaintext())


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
        self.name2 = self.xml_str(row[header['NAME2']].plaintext())
        self.ata = self.xml_int(row[header['ATA']].plaintext())
        self.ats = self.xml_int(row[header['ATS']].plaintext())
        self.tac = self.xml_int(row[header['TAC']].plaintext())
        self.str = self.xml_int(row[header['STR']].plaintext())
        self.rng = self.xml_int(row[header['RANGE']].value)
        self.other = self.xml_str(row[header['OTHER']].plaintext())
        self.used = self.xml_str(row[header['USED']].plaintext())
        self.cvp_y1 = self.xml_int(row[header['YR1']].plaintext())
        self.cvp_s1 = self.xml_int(row[header['SIZ1']].plaintext())
        self.cvp_y2 = self.xml_int(row[header['YR2']].plaintext())
        self.cvp_s2 = self.xml_int(row[header['SIZ2']].plaintext())
        self.cvp_y3 = self.xml_int(row[header['YR3']].plaintext())
        self.cvp_s3 = self.xml_int(row[header['SIZ3']].plaintext())


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
        self.name2 = self.xml_str(row[header['NAME2']].plaintext())
        self.att = self.xml_int(row[header['ATT']].plaintext())
        self.dfs = self.xml_int(row[header['DEF']].plaintext())
        self.aa = self.xml_int(row[header['AA']].plaintext())
        self.sb = self.xml_int(row[header['SB']].plaintext())
        self.rng = self.xml_int(row[header['RNG']].value)
        self.mov = self.xml_int(row[header['MOV']].plaintext())
        self.cv = self.xml_int(row[header['CV']].plaintext())
        self.sunk = self.xml_str(row[header['SUNK']].plaintext())
        self.used = self.xml_str(row[header['USED']].plaintext())

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
            name = ' '.join([u.name, u.name2]).strip()
            print '({cs:02d}:{row:02d}-{col:02d}) [{type}] {name}'.format(
                cs=u.cs, row=u.row, col=u.col, type=u.type, name=name),
            print '[CV: {}]'.format(u.cv)

    pp_cs(CS)
    print '#' * 20

    CS.sort()
    pp_cs(CS)
