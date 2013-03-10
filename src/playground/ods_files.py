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
        self.loc = None
        self.side = None
        self.power = None
        self.home = None
        self.clas = None
        self.type = None
        self.year = None
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
        self.side = str(row[header['SIDE']].plaintext())
        self.power = str(row[header['POWER']].plaintext())
        self.home = str(row[header['HOME']].plaintext())
        self.clas = str(row[header['CLASS']].plaintext())
        self.type = str(row[header['TYPE']].plaintext())
        self.year = str(row[header['YEAR']].plaintext())
        self.time = int(row[header['TIME']].plaintext())
        self.kit = str(row[header['KIT']].plaintext())
        self.cs = int(row[header['CS']].value)
        self.row = int(row[header['ROW']].value)
        self.col = int(row[header['COL']].value)
        self.option = str(row[header['OPTION']].plaintext())

        return header, row

    def __str__(self):
        return '{sh_name}#{sh_row} {}'.format(self.__dict__, **self.__dict__)

    def __cmp__(self, other):
        if self.cs != other.u_cs:
            return cmp(self.cs, other.u_cs)
        else:
            if self.row != other.u_row:
                return cmp(self.row, other.u_row)
            else:
                return cmp(self.col, other.u_col)


class LandUnit(Unit):
    """land unit"""

    def __init__(self):
        super(LandUnit, self).__init__()

        self.unit = None
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
        self.col_f = None
        self.col_b = None

    def update(self, sheet, row_no, header=None):
        # super
        header, row = super(LandUnit, self).update(sheet, row_no, header)

        # set values
        self.unit = str(row[header['UNIT']].plaintext())
        self.str = int(row[header['STR']].value)
        if row[header['ROG']].value:
            self.rog = int(row[header['ROG']].value)
        self.mov = int(row[header['MOV']].value)
        self.cost = int(row[header['COST']].value)
        self.size = str(row[header['SIZE']].plaintext())
        self.other = str(row[header['OTHER']].plaintext())
        self.abilities = str(row[header['ABILITIES']].plaintext())
        self.used_a = str(row[header['USED A']].plaintext())
        self.aif = str(row[header['AIF']].plaintext())
        self.used_p = str(row[header['USED P']].plaintext())
        self.patif = str(row[header['PatiF']].plaintext())
        self.used_pa = str(row[header['USED PA']].plaintext())
        self.aif_patif = str(row[header['AiF + PatiF']].plaintext())
        self.col_f = str(row[header['FORE COLOR']].plaintext())
        self.col_b = str(row[header['BACK COLOR']].plaintext())

##---MAIN

if __name__ == '__main__':
    LAND = get_sheet('Land')
    header = Unit.read_header(LAND)
    cs1rid = counter_sheet_row_idx_set(LAND, 3)
    CS1 = []
    for rid in cs1rid:
        lu = LandUnit()
        lu.update(LAND, rid, header)
        CS1.append(lu)

    def pp_cs(cs):
        for u in cs:
            print '({r:02d}-{c:02d}) {name}'.format(r=u.u_row,
                                                    c=u.u_col,
                                                    name=u.lu_unit)

    pp_cs(CS1)
    print '#' * 20

    CS1.sort()
    pp_cs(CS1)
