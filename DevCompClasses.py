from collections import namedtuple

class Validation:
    
    def getCompToDo():
        pass


    def __init__(self,settings,dirs,toDo):
        self.settings = settings
        self.dirs = dirs
        self.toDo = toDo


trimmedSettings = {'advanced_settings': {'advanced_curve_settings': {'STD': [{'spike_index': 1, 'spike_level': 2.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [True, 3], 'InterLabReproducibilityandRepeats': [True, 3]}, {'spike_index': 2, 'spike_level': 5.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [False, None], 'InterLabReproducibilityandRepeats': [False, None]}, {'spike_index': 3, 'spike_level': 20.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [True, 3], 'InterLabReproducibilityandRepeats': [True, 3]}, {'spike_index': 4, 'spike_level': 50.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [False, None], 'InterLabReproducibilityandRepeats': [False, None]}, {'spike_index': 5, 'spike_level': 100.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [True, 3], 'InterLabReproducibilityandRepeats': [True, 3]}], 'Spike': [{'spike_index': 1, 'spike_level': 2.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [True, 3], 'InterLabReproducibilityandRepeats': [True, 3]}, {'spike_index': 2, 'spike_level': 5.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [False, None], 'InterLabReproducibilityandRepeats': [False, None]}, {'spike_index': 3, 'spike_level': 20.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [True, 3], 'InterLabReproducibilityandRepeats': [True, 3]}, {'spike_index': 4, 'spike_level': 
50.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [False, None], 'InterLabReproducibilityandRepeats': [False, None]}, {'spike_index': 5, 'spike_level': 100.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [True, 3], 
'InterLabReproducibilityandRepeats': [True, 3]}], 'Matrix': [{'spike_index': 1, 'spike_level': 2.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [True, 3], 'InterLabReproducibilityandRepeats': [True, 3]}, {'spike_index': 2, 'spike_level': 5.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [False, None], 'InterLabReproducibilityandRepeats': [False, None]}, {'spike_index': 3, 'spike_level': 20.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [True, 3], 'InterLabReproducibilityandRepeats': [True, 3]}, {'spike_index': 4, 'spike_level': 50.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [False, None], 'InterLabReproducibilityandRepeats': [False, None]}, {'spike_index': 5, 'spike_level': 100.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [True, 3], 'InterLabReproducibilityandRepeats': [True, 3]}]}}}


Base_Parameters = namedtuple('Base_Parameters', 'Curve, Repeatability,Reproducibility' )

x1 = Base_Parameters(Curve = 'STD', Repeatability = False, Reproducibility = False)
x2 = Base_Parameters(Curve = 'Spike', Repeatability = True, Reproducibility = True)
x3 = Base_Parameters(Curve = 'Matrix', Repeatability = False, Reproducibility = False)
todo = [x1,x2,x3]

rv = {}

for task in todo:
    rv[task.Curve] = ['LOD', 'LOQ', 'Slope', 'yIntercept' ]
    if task.Repeatability:
        c_settings = trimmedSettings['advanced_settings']['advanced_curve_settings'][task.Curve]
        rsdr =  map('RSDr{}{}'.format, (x['spike_index']  for x in c_settings if x['RepeatabilityandRepeats'][0] ),(x['RepeatabilityandRepeats'][1]  for x in c_settings  if x['RepeatabilityandRepeats'][0]))
        rv[task.Curve].append(list(rsdr))

    if task.Reproducibility:
        c_settings = trimmedSettings['advanced_settings']['advanced_curve_settings'][task.Curve]
        rsdR = map('RSDR{}{}'.format, (x['spike_index'] for x in c_settings if x['InterLabReproducibilityandRepeats'][0]) , (x['InterLabReproducibilityandRepeats'][1] for x in c_settings if x['InterLabReproducibilityandRepeats'][0] ))
        rv[task.Curve].append(list(rsdR))
    

rsdr =  map('RSDr{}{}'.format, (x['spike_index']  for x in c_settings if x['RepeatabilityandRepeats'][0] ),(x['RepeatabilityandRepeats'][1]  for x in c_settings  if x['RepeatabilityandRepeats'][0]))

#pipeline ==> generator_object_1 , generator_object_2, generator_object_3; each generator will yield repetitions

def xrange(num):
    count = num
    if not isinstance(num,int):
        raise TypeError('Arguement must be an integer to be generated')
    elif num < 0:
        raise StopIteration
    else:
        while count>0:
            yield count
            count -= 1


pipeline = map(xrange ,((int(y) for y in (x['RepeatabilityandRepeats'][1]  for x in c_settings  if x['RepeatabilityandRepeats'][0]))))



def devExhaust(iterator):
    while True:
        try:
            print(next(iterator))
        except StopIteration:
            print('StopIteration')
            break



