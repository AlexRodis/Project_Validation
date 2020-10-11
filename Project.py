from Databases import MethodValidationDatabase
import json
from os import chdir, listdir


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
                        self.validation_settings['advanced_validation_settings'] = json.read(
                            settings)
                except FileNotFoundError:
                    try:
                        with open('Settings-Default.json', 'r') as settings:
                            self.validation_settings['advanced_validation_settings'] = json.read(
                                settings)
                    except FileNotFoundError:
                        print("Validation settings not found")
            else:
                raise ValueError
        except ValueError:
            pass
        return None

    def __init__(self, settings=None, root=None):
        print(settings)
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

# Doesn't work. For some reason settings aren't being written to a file. Look at desktop. Currently writes null
    @staticmethod
    def save(settings=None, filepath=None):
        chdir(filepath)
        print(settings)
        try:
            print('Attempting to open file')
            with open('Settings-User.json', 'w') as file:
                json.dump(settings['advanced_settings'], file)
                print('File opened')
        except:
            try:
                print('Attempting to create file')
                f = open('testsettings.json', 'x')
                f.close()
                print('file created')
                print('Attempting to write to file')
                with open('testsettings.json', 'r+') as file:
                    json.dump(settings['advanced_settings'], file)
                    print('Dumping json')
                print('Wrote to file')
            except:
                print("Failed to create settings file")
