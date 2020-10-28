import sqlite3 as sql
from os import chdir, mkdir, listdir
import Excel
from Packages.Utils import FileUtils
from collections import namedtuple
import re
import pprint
import warnings


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


    def _normalise_to_floats(files):
        # Convert non-float concentration on filenames to floats, for consistency
            out = []
            x = re.compile("[0-9]+(?=_D)")
            for file in files:
                y = re.search(x, file).group(0)
                z = re.sub("[0-9]+(?=_D)", str(float(y)), file)
                out.append(z)
            return out

    def crossValidateFiles(files, settings):
    # Accesses a list of files, given a list of tasks and settings for these tasks, and returns True if files have been found for all settings, and
    # no files found and unaccounted for.
    # This linear algorithm doesn't scale well. Possibly implement binary search
        tasks = settings["basic_settings"]
        Reg_files = []
        files = sorted(MethodValidationDatabase._normalise_to_floats(files))
        try:    
            for task in tasks:
                for point in settings["advanced_settings"]["advanced_curve_settings"][task.Curve]:
                        i = 0
                        sentinel_fnf_err = True
                        for file in files:
                            searchstring = "{curve}_spike_{level}_D1_1".format(curve=task.Curve, level= point["spike_level"])
                            if "{curve}_spike_{level}_D1_1".format(curve=task.Curve, level= point["spike_level"]) in file:
                                sentinel_fnf_err = False
                                Reg_files.append(file)
                                i += 1
                        
                        if sentinel_fnf_err:
                            msg = searchstring
                            raise FileNotFoundError
                        
                        if i>1:
                            msg = searchstring
                            raise NameError
                        
                if task.Repeatability:
                    for point in settings["advanced_settings"]["advanced_curve_settings"][task.Curve]:
                        if point["RepeatabilityandRepeats"][0]:
                            for repeat in range(1, point["RepeatabilityandRepeats"][1] + 1):    
                                sentinel_fnf_err = True
                                i = 0
                                for file in files:
                                    searchstring = "{curve}_spike_{level}_D1_{repeat}".format(curve =task.Curve ,level = point["spike_level"], repeat = repeat)
                                    if "{curve}_spike_{level}_D1_{repeat}".format(curve =task.Curve ,level = point["spike_level"], repeat = repeat) in file:
                                        sentinel_fnf_err = False
                                        Reg_files.append(file)
                                        i += 1
                                
                                if sentinel_fnf_err:
                                    msg = searchstring
                                    raise FileNotFoundError("Missing specified file: " + msg)
                                
                                if i>1:
                                    msg = searchstring
                                    warnings.warn("Possible duplicate found: " + msg)
                
                if task.Reproducibility:
                    for point in settings["advanced_settings"]["advanced_curve_settings"][task.Curve]:
                        if point["InterLabReproducibilityandRepeats"][0]:
                            for repeat in range(1, point["InterLabReproducibilityandRepeats"][1] + 1):
                                sentinel_fnf_err = True
                                i = 0
                                for file in files:
                                    searchstring = "{curve}_spike_{level}_D2_{repeat}".format(curve = task.Curve, level = point["spike_level"], repeat = repeat)
                                    if "{curve}_spike_{level}_D2_{repeat}".format(curve = task.Curve, level = point["spike_level"], repeat = repeat) in file:
                                        sentinel_fnf_err = False
                                        Reg_files.append(file)
                                        i += 1
                                
                                if sentinel_fnf_err:
                                    msg = searchstring
                                    raise FileNotFoundError
                                
                                if i>1:
                                    msg = searchstring
                                    raise NameError
        
        except FileNotFoundError:
            print("File specified in settings not found: \n" + msg)
        
        except NameError:
            print("Duplicate file found: \n" + msg)
        
        finally:
            unaccounted_files = []
            sentinel_extra_files = True
            Reg_files = sorted(list(dict.fromkeys(Reg_files)))
            for file in files:
                if file in Reg_files:
                    continue
                else:
                    sentinel_extra_files = False
                    unaccounted_files.append(file)
            if not  sentinel_extra_files:
                warnings.warn("Warning: Found files unaccounted for in settings: ")
                pprint.pprint(unaccounted_files)
                return False
                
            if sentinel_extra_files:
                return True
    
    def parse_files(self):
        D = namedtuple("Spreadsheets", ["DirectoryPath", "Spreadsheets", "Method" ])
        chdir(self.datapath)
        dirs = listdir()
        datasheets = []
        for folder in dirs:
            t_dir = self.datapath + "\\" + folder
            chdir(t_dir)
            wbs = FileUtils.select_xlsx(listdir())
            if wbs != []:
                datasheets.append(D(DirectoryPath = t_dir, Spreadsheets = wbs , Method = folder))
            
            else:
                raise AttributeError("Attempted to open workbook - found nothing")
        return datasheets,dirs
    
    # For data of multiple instruments, create a data folder and aim datapath var to said folder. Inside create sublfolders, per data batch i.i. ESI+, ESI-,GC Check dirs logic. Need to collect ESI Excel exports to check.
    #This needs testing. Lack files
    def load_analytes(self):
        idx = 0
        datasheets,dirs = self.parse_files()
        for folder in [next(x.Method for x in datasheets)]:
            dirpath,excels = next(([x.DirectoryPath, x.Spreadsheets] for x in datasheets if x.Method == folder), None)
            x = MethodValidationDatabase.crossValidateFiles(excels, self.settings)
            if MethodValidationDatabase.crossValidateFiles(excels, self.settings):
                for excel in excels:    
                    chdir(dirpath)
                    analytes = Excel.get_analytes(workbook = excel)
                    chdir(self.filepath)
                    connection = sql.connect("{}.sqlite".format(self.name))
                    cursor = connection.cursor()
                    for analyte in analytes:
                        with connection:
                            cursor.execute("SELECT ANALYTE,METHOD FROM validation WHERE ANALYTE = :analyte AND METHOD = :method" ,{'analyte': analyte, 'method': folder})
                            if cursor.fetchone() is None:
                                cursor.execute("INSERT INTO validation (ID, ANALYTE,METHOD) VALUES (:idx , :analyte,:method)",{'idx': idx, 'analyte':analyte ,'method':folder} )
                            idx +=1
        return datasheets

    def load_base_values(self, workbooks = None):
        
        return None

    def __init__(self, name, team, filepath, datapath, other=None):
        super().__init__(name, team, filepath, datapath)
        super().create_table(table='validation', settings=other.settings, to_do=other.to_do)
        self.settings = other.settings
        datasheets = self.load_analytes()
        self.load_base_values(workbooks = datasheets)
        return None
