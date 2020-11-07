from Databases import MethodValidationDatabase
import json
from os import chdir, listdir, getcwd
from Packages.Utils import JSONAdaptor
import Computations

global programpath

programpath = r"C:\Users\User\Documents\Programming\Project Validation"


class Project:

    def __init__(self, name, team, datapath, filepath, root):
        self.name = name
        self.team = team
        self.datapath = datapath
        self.filepath = filepath
        self.root = root
        chdir(filepath)


class Validation(Project):

    def recovery(self):
        pass

    def matrixmatch(self):
        pass

    def set_advanced_validation_settings(self):
        try:
            if self.settings['advanced_validation_settings'] is None:
                try:
                    cwd = getcwd()
                    chdir(programpath)
                    with open('Settings-User.json', 'r') as settings:
                        self.settings = JSONAdaptor.jsontopython(
                            json.load(settings))
                    chdir(cwd)
                except FileNotFoundError:
                    print('No user settings found')
                    try:
                        with open('Settings-Default.json', 'r') as settings:
                            self.settings = JSONAdaptor.jsontopython(
                                json.load(settings))
                    except FileNotFoundError:
                        print('Could not load any settings')
        except KeyError:
            print('Key access violation')
        return None

    def __init__(self, settings=None, root=None):
        #Look into breaking this up
        super().__init__(settings['project_parameters']['name'], settings['project_parameters']['team'],
                         settings['project_parameters']['datapath'], settings['project_parameters']['filepath'], root)
        self.settings = settings
        self.to_do = []
        for task in self.settings['basic_settings']:
            if task.Curve is "STD":
                self.std = task
            elif task.Curve is "Spike":
                self.Curve = task
            elif task.Curve is "Matrix":
                self.matrix = task
            self.to_do.append(task)
        self.set_advanced_validation_settings()
        self.database = MethodValidationDatabase(
            self.name, self.team, self.datapath, self.filepath, other=self)
        #Continue with computations here
        self.computations = Computations.Validation( self.name, self.filepath, self.datapath, self.database.getDatasheets(), self.to_do, self.settings )
    
    @staticmethod
    def Save(settings=None, filepath=None):
        settings = JSONAdaptor.pythontojson(settings)
        with open("Settings-User.json", "w") as file:
            json.dump(settings, file, indent=4)
        return None
