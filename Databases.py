import sqlite3 as sql
from os import chdir, mkdir, listdir
import Excel


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
                commandstring += "ID INT PRIMARY KEY, ANALYTE TEXT,"
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
##Resume here tomorrow with the syntax for INSERT INTO VALUES
    def load_analytes(self):
        chdir(self.datapath)
        analytes = Excel.get_analytes(workbook=listdir()[1])
        chdir(self.filepath)
        print("{}.sqlite".format(self.name))
        connection = sql.connect("{}.sqlite".format(self.name))
        with connection as con:
            cursor = con.cursor()
            for idx, analyte in enumerate(analytes, start=1):
                cursor.execute(
                    'INSERT INTO validation (ID, ANALYTE) VALUES ({idx},{analyte})')
        return None

    def __init__(self, name, team, filepath, datapath, other=None):
        super().__init__(name, team, filepath, datapath)
        super().create_table(table='validation', settings=other.settings, to_do=other.to_do)
        self.load_analytes()
        return None
