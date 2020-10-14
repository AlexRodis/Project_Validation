from Databases import MethodValidationDatabase
import json
from os import chdir, listdir
from Packages.Utils import JSONAdaptor

class Project:

    def __init__(self, name, team, datapath, filepath, root):
        self.name = name
        self.team = team
        self.datapath = datapath
        self.filepath = filepath
        self.root = root
        self.database = MethodValidationDatabase(
            self.name, self.team, self.datapath, self.filepath, other=self)


class Validation(Project):

    def recovery(self):
        pass

    def matrixmatch(self):
        pass

    def set_advanced_validation_settings(self):
        try:
            if self.validation_settings['advanced_validation_settings'] is None:
                try:
                    with open('Settings-User.json', 'r') as settings:
                        self.validation_settings['advanced_validation_settings'] = JSONAdaptor.jsontopython(json.load(
                            settings))
                except FileNotFoundError:
                    try:
                        with open('Settings-Default.json', 'r') as settings:
                            self.validation_settings['advanced_validation_settings'] = JSONAdaptor.jsontopython(json.load(
                                settings))
                    except FileNotFoundError:
                        print("Validation settings not found")
            else:
                raise ValueError
        except ValueError:
            pass
        return None

    def __init__(self, settings=None, root=None):
        super().__init__(settings['project_parameters']['name'], settings['project_parameters']['team'],
                         settings['project_parameters']['datapath'], settings['project_parameters']['filepath'], root)
        self.validation_settings = settings
        self.to_do = []
        for task in self.validation_settings['basic_settings']:
            if task.Curve is "STD":
                self.std = task
            elif task.Curve is "Spike":
                self.Curve = task
            elif task.Curve is "Matrix":
                self.matrix = task
            self.to_do.append(task)
            self.moveahead()

    def moveahead(self):
        self.set_advanced_validation_settings()
        self.database.create_table(
            table='validation', settings=self.validation_settings, to_do=self.to_do)

    @staticmethod
    def Save(settings=None, filepath=None):
        chdir(filepath)
        settings = JSONAdaptor.pythontojson(settings)
        with open("Settings-User.json", "w") as file:
            json.dump(settings, file, indent=4)
        return None
