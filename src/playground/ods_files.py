# ODS handling for the counter excel file by p.forno

##---IMPORTS

from ezodf import opendoc

##---CONSTANTS

COUNTER_FILE = '../../res/WiF-AiF-PatiF-Counters.ods'


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
        self.sheet = None
        self.row = None
        self.u_loc = None
        self.u_side = None
        self.u_power = None
        self.u_home = None
        self.u_class = None
        self.u_type = None
        self.u_year = None
        self.u_time = None
        self.u_kit = None
        self.u_cs = None
        self.u_row = None
        self.u_col = None
        self.u_option = None

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
        self.u_side = str(row[header['SIDE']].plaintext())
        self.u_power = str(row[header['POWER']].plaintext())
        self.u_home = str(row[header['HOME']].plaintext())
        self.u_class = str(row[header['CLASS']].plaintext())
        self.u_type = str(row[header['TYPE']].plaintext())
        self.u_year = str(row[header['YEAR']].plaintext())
        self.u_time = int(row[header['TIME']].plaintext())
        self.u_kit = str(row[header['KIT']].plaintext())
        self.u_cs = int(row[header['CS']].value)
        self.u_row = int(row[header['ROW']].value)
        self.u_col = int(row[header['COL']].value)
        self.u_option = str(row[header['OPTION']].plaintext())

        return header, row

    def __str__(self):
        return '{sh_name}#{sh_row} {}'.format(self.__dict__, **self.__dict__)

    def __cmp__(self, other):
        if self.u_cs != other.u_cs:
            return cmp(self.u_cs, other.u_cs)
        else:
            if self.u_row != other.u_row:
                return cmp(self.u_row, other.u_row)
            else:
                return cmp(self.u_col, other.u_col)


class LandUnit(Unit):
    """land unit"""

    def __init__(self):
        super(LandUnit, self).__init__()

        self.lu_unit = None
        self.lu_str = None
        self.lu_rog = None
        self.lu_mov = None
        self.lu_cost = None
        self.lu_size = None
        self.lu_other = None
        self.lu_abilities = None
        self.lu_used_a = None
        self.lu_aif = None
        self.lu_used_p = None
        self.lu_patif = None
        self.lu_used_pa = None
        self.lu_aif_patif = None
        self.lu_col_f = None
        self.lu_col_b = None

    def update(self, sheet, row_no, header=None):
        # super
        header, row = super(LandUnit, self).update(sheet, row_no, header)

        # set values
        self.lu_unit = str(row[header['UNIT']].plaintext())
        self.lu_str = int(row[header['STR']].value)
        if row[header['ROG']].value:
            self.lu_rog = int(row[header['ROG']].value)
        self.lu_mov = int(row[header['MOV']].value)
        self.lu_cost = int(row[header['COST']].value)
        self.lu_size = str(row[header['SIZE']].plaintext())
        self.lu_other = str(row[header['OTHER']].plaintext())
        self.lu_abilities = str(row[header['ABILITIES']].plaintext())
        self.lu_used_a = str(row[header['USED A']].plaintext())
        self.lu_aif = str(row[header['AIF']].plaintext())
        self.lu_used_p = str(row[header['USED P']].plaintext())
        self.lu_patif = str(row[header['PatiF']].plaintext())
        self.lu_used_pa = str(row[header['USED PA']].plaintext())
        self.lu_aif_patif = str(row[header['AiF + PatiF']].plaintext())
        self.lu_col_f = str(row[header['FORE COLOR']].plaintext())
        self.lu_col_b = str(row[header['BACK COLOR']].plaintext())

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
