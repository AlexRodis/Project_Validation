import sqlite3 as sql
from os import chdir, mkdir, listdir
import Excel
from Packages.Utils import FileUtils
from collections import namedtuple


class Database:

    # Add sample and blank logic, updating settings and UI

    def create_table_structure(self, *args, **kwargs):
        table = kwargs['table']
        commandstring = kwargs['commandstring']
        if table == 'team':
            commandstring += "ID INT PRIMARY KEY , User TEXT,Action_AUTH TEXT)"
        try:
            if table == 'validation':
                for task in kwargs['to_do']:
                    curve = task.Curve
                    points_index = kwargs['settings']['advanced_settings']['advanced_curve_settings']['{curve}'.format(
                        curve=curve)]
                    for point in [x['spike_index'] for x in points_index if x['Is_In_Curve']]:
                        commandstring += "{curve}_spike_{ith}_D1_1 REAL,".format(
                            curve=curve, ith=point)
                    commandstring += "{curve}_correl_coeff REAL,".format(
                        curve=curve)
                    commandstring += "{curve}_standard_error_interept REAL,".format(
                        curve=curve)
                    commandstring += "{curve}_LOD REAL,".format(curve=curve)
                    commandstring += "{curve}_LOQ REAL,".format(curve=curve)
                    for idx_n_repeats in [[x["spike_index"], x["RepeatabilityandRepeats"][1]] for x in points_index if x["RepeatabilityandRepeats"][0]]:
                        for jth in range(2, idx_n_repeats[1] + 1):
                            commandstring += "{curve}_spike_{ith}_D1_{jth} REAL,".format(
                                curve=curve, ith=idx_n_repeats[0], jth=jth)
                        commandstring += "{curve}_spike_{ith}_D1_RSD_r REAL,".format(
                            curve=curve, ith=idx_n_repeats[0])
                    for idx_n_repeats in [[x["spike_index"], x["InterLabReproducibilityandRepeats"][1]] for x in points_index if x["InterLabReproducibilityandRepeats"][0]]:
                        for jth in range(2, idx_n_repeats[1] + 1):
                            commandstring += "{curve}_spike_{ith}_D2_{jth} REAL,".format(
                                curve=curve, ith=idx_n_repeats[0], jth=jth)
                        commandstring += "{curve}_spike_{ith}_D2_RSD_r REAL,".format(
                            curve=curve, ith=idx_n_repeats[0])
                        commandstring += "{curve}_spike_{ith}_RSD_R REAL,".format(
                            curve=curve, ith=idx_n_repeats[0])
                commandstring = commandstring[:-1] + ")"
        except:
            print(commandstring)

        return commandstring

    def create_table(self, **kwargs):
        try:
            commandstring = "CREATE TABLE IF NOT EXISTS {table_name}(".format(
                table_name=kwargs['table'])
            if kwargs['table'] == 'team':
                commandstring = self.create_table_structure(
                    commandstring=commandstring, table=kwargs['table'])
            elif kwargs['table'] == 'validation':
                commandstring += "ID INT PRIMARY KEY, METHOD TEXT, ANALYTE TEXT,"
                commandstring = self.create_table_structure(
                    commandstring=commandstring, table=kwargs['table'], settings=kwargs['settings'], to_do=kwargs['to_do'])
            connection = sql.connect("{}.sqlite".format(self.name))
            with connection:
                cursor = connection.cursor()
                cursor.execute(commandstring)
            connection.close()
            self.tables.append(kwargs['table'])
        except KeyError:
            print("Create table called without a table arguement")

    def __init__(self, name, team, datapath, filepath):
        self.name = name
        self.tables = []
        self.team = team
        self.filepath = filepath
        self.datapath = datapath
        try:
            chdir(filepath)
        except FileNotFoundError:
            try:
                mkdir(filepath)
            except PermissionError:
                print("Error. Path to files doesn't exist and could't be created")
        connection = sql.connect("{project}.sqlite".format(project=self.name))
        connection.close()
        self.create_table(table='team')
        return None


class MethodValidationDatabase(Database):
    
    def parse_files(self):
        D = namedtuple("Excel Spreadsheets and where to find them", ["DirectoryPath", "Spreadsheets", "Method"])
        chdir(self.datapath)
        dirs = listdir()
        datasheets = []
        for folder in dirs:
            t_dir = self.datapath + "\\" + folder
            chdir(t_dir)
            wbs = FileUtils.select_xlsx(listdir())
            if wbs != []:
                datasheets.append(D(DirectoryPath = t_dir, Spreadsheets = wbs , Method = folder))
        return datasheets
    
    # For data of multiple instruments, create a data folder and aim datapath var to said folder. Inside create sublfolders, per data batch i.i. ESI+, ESI-,GC Check dirs logic. Need to collect ESI Excel exports to check.
    #This needs testing. Lack files
    def load_analytes(self):
        idx = 0
        # chdir(self.datapath)
        datasheets = self.parse_files()
        # dirs = listdir()
        # for folder in dirs:
        #     t_dir = self.datapath + "\\" + folder
        #     chdir(t_dir)
        #     wbs = FileUtils.select_xlsx(listdir())
        #     if wbs != []:
        #         analytes = Excel.get_analytes(
        #             workbook=wbs[0])
        for datasheet in datasheets:
            dirpath, method ,excels = datasheet.DirectoryPath,datasheet.Method, datasheet.Spreadsheets
            analytes = Excel.get_analytes(wrokbook = excels)
            chdir(self.filepath)
            connection = sql.connect("{}.sqlite".format(self.name))
            cursor = connection.cursor()
            for analyte in analytes:
                with connection:
                    cursor.execute("SELECT (ANALYTE,METHOD) FROM validation WHERE VALUES = (?,?)" ,[analyte, method])
                if cursor.fetchone() is None:
                    with connection:
                        cursor.execute(
                            "INSERT INTO validation(ID, ANALYTE,METHOD) VALUES(?,?,?)", [idx, analyte,method])
                    idx += 1
        return datasheets

    def load_base_values(self, workbooks = None):
# Cycle through all excel sheets in folder and all available forlders and load them to the database.
# Possibly use a generator here. Lots of directory changes. Review
#UNTESTED, MUST REVIEW
        for path,method,sheets in workbooks:
            chdir(path)
            connection = sql.connect(self.name + ".sqlite")
            cursor = connection.cursor()
            for sheet in sheets:
                area,analyte = Excel.get_areas(sheet,method)       
                with connection:
                    cursor.execute("SELECT (ANALYTE , METHOD) FROM validation WHERE VALUES = (?,?)" [analyte,method])
                    if c.fetchone() is None:
                        cursor.execute("INSERT INTO validation (?) WHERE ANALYTE = (?)", [sheet,analyte])
        return None

    def __init__(self, name, team, filepath, datapath, other=None):
        super().__init__(name, team, filepath, datapath)
        super().create_table(table='validation', settings=other.settings, to_do=other.to_do)
        datasheets = self.load_analytes()
        self.load_base_values(workbooks = datasheets)
        return None
