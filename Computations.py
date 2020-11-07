

class Stats:
    pass

class OLS(Stats):
    pass

class Validation(Stats):
    
    
    
    def __init__(self,name,filepath,datapath,datasheets,todo,settings):
        self.name = name
        self.filepath = filepath
        self.datapath = datapath
        self.datasheets = datasheets
        self.todo = todo
        self.settings = settings
        self.recoveries = [] 
        return None
    
    def __call__(self):
        pass

class Recovery(Validation):
    
    def __init__(self,Spike,Matrix):
        self.spike = Spike
        self.matrix = Matrix
        return None

    def __call__(self):
        return (self.matrix/self.spike)*100

class MatrixEffect(Validation):
    pass

class Limits(Validation):
    pass

class Repeatability(Validation):
    pass

class Reproducibility(Validation):
    pass

class Ruggedness(Validation):
    pass