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

    @staticmethod
    def _normalise_to_floats(files):
        # Convert non-float concentration on filenames to floats, for consistency. Possible duplicate code from Utils
            out = []
            x = re.compile("[0-9]+(?=_D)")
            for file in files:
                y = re.search(x, file).group(0)
                z = re.sub("[0-9]+(?=_D)", str(float(y)), file)
                out.append(z)
            return out

    @staticmethod
    def crossValidateFiles(files, settings):
    # Accesses a list of files, given a list of tasks and settings for these tasks, and returns True if files have been found for all settings, and
    # no files found and unaccounted for.
    # This linear algorithm doesn't scale well. Possibly implement binary search.
    #Maximaze code reuse by splitting the concentration-to-index proccess into a sepperate function
        files = [x.name for x in files]
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

    @staticmethod
    def _fetchFileCoords(settings, file):
        FileCoords = namedtuple('FileCoords', 'name,i,j,k,z')
        curve_pattern = re.compile('(STD|Matrix|Spike)(?=_spike_)')
        repeat_pattern = re.compile('(?<=_D[0-9]_)[0-9]+')
        day_pattern = re.compile('(?<=_D)[0-9]+(?=_[0-9])')
        index_pattern = re.compile('(?<=_spike_)([0-9]*\.?[0-9]+)(?=_D[0-9]_[0-9]+)')
        file_ext = re.compile("\.[A-z]+")
        try:
            ext = re.search(file_ext, file).group()
            if ext != '.xlsx':
                raise TypeError
        except AttributeError:
            raise TypeError
        try:
            curve = re.search(curve_pattern, file).group()
        except AttributeError:
            raise NameError
        try:
            day = re.search(day_pattern, file).group()
            day = int(day)
            if (day != 1 and day != 2):
                raise ValueError
        except AttributeError:
            raise TypeError
        try:
            repeat = re.search(repeat_pattern, file).group()
            temp = re.search(index_pattern, file).group()
        except AttributeError:
            raise TypeError
        repeat = int(repeat)
        temp = float(temp)
        idx = [x['spike_index'] for x in settings['advanced_settings']['advanced_curve_settings'][curve] if x['spike_level'] == temp][0]
        if repeat >= 20 or repeat <= 0:
            raise ValueError
        return FileCoords(name=file, i=curve, j=idx, k=repeat, z=day)


    
    def _parse_files(self):
        D = namedtuple("Spreadsheets", ["DirectoryPath", "Spreadsheets", "Method" ])
        chdir(self.datapath)
        dirs = listdir()
        datasheets = []
        for folder in dirs:
            t_dir = self.datapath + "\\" + folder
            chdir(t_dir)
            wbs = FileUtils.select_xlsx(listdir())
            if wbs != []:
                v = []
                for spreadsheet in wbs:
                    v.append(MethodValidationDatabase._fetchFileCoords(self.settings, spreadsheet))
                datasheets.append(D(DirectoryPath = t_dir, Spreadsheets = v , Method = folder))

            else:
                raise AttributeError("Attempted to open workbook - found nothing")
        return datasheets,dirs
    
    # For data of multiple instruments, create a data folder and aim datapath var to said folder. Inside create sublfolders, per data batch i.i. ESI+, ESI-,GC Check dirs logic. Need to collect ESI Excel exports to check.
    #Many functions here can be improved with generators
    def load_analytes(self):
        idx = 0
        datasheets,dirs = self._parse_files()
        for folder in [x.Method for x in datasheets]:
            dirpath,excels = next(([x.DirectoryPath, x.Spreadsheets] for x in datasheets if x.Method == folder), None)
            # x = MethodValidationDatabase.crossValidateFiles(excels, self.settings)
            if MethodValidationDatabase.crossValidateFiles(excels, self.settings):
                for excel in excels:    
                    chdir(dirpath)
                    analytes = Excel.get_analytes(workbook = excel.name)
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

    def _load_base_values(self, datasheets = None):
        connection = sql.connect('{}.sqlite'.format(self.name))
        cursor = connection.cursor()
        for folder in datasheets:
            
        return None

    def __init__(self, name, team, filepath, datapath, other=None):
        super().__init__(name, team, filepath, datapath)
        super().create_table(table='validation', settings=other.settings, to_do=other.to_do)
        self.settings = other.settings
        datasheets = self.load_analytes()
        self._load_base_values(workbooks = datasheets)
        return None
