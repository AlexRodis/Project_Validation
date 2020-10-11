import GUI_V2
import json
import pickle
import sqlite3


class Database:

    def __init__(self, name, filepath, exportpath, members, task, params, c_settings):
        self.name = name
        self.set_filepath(filepath)
        self.set_exportpath(exportpath)
        try:
            self.set_project_team(members)
        finally:
            self.to_do = to_do
            self.set_validation_params(params, c_settings)
            self.create_database()

    def set_filepath(self, filepath):
        self.filepath = filepath

    def create_database(self, root):
        # self.create_databse(params,c_settings,self.name)
        # to_do
        msg = "Table with the same name exists"
        print(c_settings)
        sql = "CREATE TABLE data(id INT PRIMARY KEY, analyte TEXT,"
        for task in to_do:
            for elem in c_settings["Validation_Parameters"]['{curve}_Curve'.format(curve=task[0])]:
                for j in range(1, elem["Points_In_Curve"] + 1):
                    sql += "{curve}_spike_lvl_{j}_D1_1 REAL,".format(
                        curve=task[0], j=j)
                    sql += "{curve}_Curve_Slope REAL,{curve}_Curve_Intercept REAL, {curve}_Curve_Intercept_Standard_Error REAL, {curve}_Curve_LOD REAL, {curve}_Curve_LOQ REAL,".format(
                        curve=task[0])
                if task[1]:
                    for lvl in c_settings['Validation_Parameters']['{curve}_Curve'.format(curve=task[0])]['Repeatability_Sampling']:
                        for k in range(2, lvl[1] + 1):
                            sql += "{curve}_spike_lvl_{j}_D1_{k} REAL,".format(
                                curve=task[0], j=lvl[0], k=k)
                        sql += "Repeatability_spike_lvl{j}_%RSD_".format(
                            j=lvl[0])
                if task[2]:
                    for lvl in c_settings["Validation_Parameters"]["{curve}_Curve".format(curve=curve)]["Within_Laboratory_Reproducibility_Sampling"]:
                        for k in range(2, lvl[1] + 1):
                            sql += "{curve}_spike_lvl_{j}_D2_{k} REAL,".format(
                                curve=task[0], j=lvl[0], k=k)
                        sql += "Repeatability_%RSD_Spike_lvl_{j}_D2 REAL,".format(
                            j=lvl[0])
# What if there's a spike lvl difference WRL and Repeat?????
                if task[1] and task[2]:
                    for samplings in zip(c_settings['Validation_Parameters']['{curve}_Curve'.format(curve=task[0])]['Repeatability_Sampling'], c_settings['Validation_Parameters']['{curve}_Curve'.format(curve=task[0])]['Within_Laboratory_Reproducibility_Sampling']):
                        try:
                            if samplings[0][0] == samplings[1][0]:
                                sql = "Within_Laboratory_Reproducibility_%RSD_Spike_lvl_{j} REAL,".format(
                                    j=quadr[0][0])
                            else:
                                raise MismatchException
                        except MismatchException:
                            msg = "Warning, spiking level in reproducibility and within laboratory reproducibility mismatch. Will ignore mismatches"
                            Warning_Window(root, msg)
                        finally:
                            connection = sqlite3.connect()
                            with conection:
                                cursor = connection.cursor()
                                cursor.execute(sql[:-1] + ")")

    def set_exportpath(self, exp_path):
        self.exportpath = exp_path
        return None

    def set_project_team(self, p_team):
        self.project_team = p_team
        return None

    def set_validation_params(self, params, c_settings):
        self.params = params
        self.c_settings = c_settings
        return None

    def get_filepath(self, root):
        msg = "Database filepath not found"
        try:
            return self.filepath
        except:
            GUI_V2.Err_Window(root, msg)

    def get_exportpath(self, root):
        msg = "Export path not found"
        try:
            return self.exportpath
        except:
            GUI_V2.Err_Window(root, msg)

    def get_project_team(self, root):
        msg = "Project team not set"
        try:
            return self.project_team
        except:
            GUI_V2.Err_Window(self, root)

    def load_analyte_names(self, names):
        pass
        # Create workbook with xlwings, load analyte names and call format.

    def display(self):
        pass

    def inquire(self):
        pass


class Project:

    def __init__(self):
        GUI_V2.main(self)

    def extend(self, params):
        self.name = params["base_params"]['name']
        self.filepath = params["base_params"]['filepath']
        self.exportpath = params["base_params"]['export_path']
        self.members = params["base_params"]['team_members']
        self.to_do = params["base_params"]['to_do']
        try:
            self.c_settings = params['c_settings']
        except AttributeError:
            try:
                with open("Settings-User.json", 'r') as file:
                    self.c_settings = json.load(file)['c_settings']
            except:
                with open("Settings-Default.json", 'r') as file:
                    self.c_settings = json.load(file)['c_settings']
        finally:
            self.save()
            Database(self.name, self.filepath, self.exportpath, self.members,
                     self.to_do, params, self.c_settings, other, autodetect)

    def save(self):
        with open("{}.pk1".format(self.name), "wb") as save:
            pickle.dump(self, save, pickle.HIGHEST_PROTOCOL)
        return None


def main():
    try:
        Proj = Project()
    except:
        return None


if __name__ == '__main__':
    main()
