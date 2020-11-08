import re
import os
from itertools import chain, tee,cycle
from collections.abc import Iterable
from functools import wraps, reduce


lcNegFiles = ['Spike_spike_2_D1_2.xlsx', 'Matrix_spike_100_D1_1.xlsx', 'Matrix_spike_20_D1_1.xlsx', 'Matrix_spike_2_D1_1.xlsx', 'Matrix_spike_50_D1_1.xlsx', 'Matrix_spike_5_D1_1.xlsx', 'Spike_spike_100_D1_1.xlsx', 'Spike_spike_100_D1_2.xlsx', 'Spike_spike_100_D1_3.xlsx', 'Spike_spike_100_D2_1.xlsx', 'Spike_spike_100_D2_2.xlsx', 'Spike_spike_100_D2_3.xlsx', 'Spike_spike_20_D1_1.xlsx', 'Spike_spike_20_D1_2.xlsx', 'Spike_spike_20_D1_3.xlsx', 'Spike_spike_20_D2_1.xlsx', 'Spike_spike_20_D2_2.xlsx', 'Spike_spike_20_D2_3.xlsx', 'Spike_spike_2_D1_1.xlsx', 'Spike_spike_2_D1_3.xlsx', 'Spike_spike_2_D2_1.xlsx', 'Spike_spike_2_D2_2.xlsx', 'Spike_spike_2_D2_3.xlsx', 'Spike_spike_50_D1_1.xlsx', 'Spike_spike_5_D1_1.xlsx', 'STD_spike_100_D1_1.xlsx', 'STD_spike_20_D1_1.xlsx', 'STD_spike_2_D1_1.xlsx', 'STD_spike_50_D1_1.xlsx', 'STD_spike_5_D1_1.xlsx']

trimmedSettings = {'advanced_settings': {'advanced_curve_settings': {'STD': [{'spike_index': 1, 'spike_level': 2.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [True, 3], 'InterLabReproducibilityandRepeats': [True, 3]}, {'spike_index': 2, 'spike_level': 5.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [False, None], 'InterLabReproducibilityandRepeats': [False, None]}, {'spike_index': 3, 'spike_level': 20.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [True, 3], 'InterLabReproducibilityandRepeats': [True, 3]}, {'spike_index': 4, 'spike_level': 50.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [False, None], 'InterLabReproducibilityandRepeats': [False, None]}, {'spike_index': 5, 'spike_level': 100.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [True, 3], 'InterLabReproducibilityandRepeats': [True, 3]}], 'Spike': [{'spike_index': 1, 'spike_level': 2.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [True, 3], 'InterLabReproducibilityandRepeats': [True, 3]}, {'spike_index': 2, 'spike_level': 5.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [False, None], 'InterLabReproducibilityandRepeats': [False, None]}, {'spike_index': 3, 'spike_level': 20.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [True, 3], 'InterLabReproducibilityandRepeats': [True, 3]}, {'spike_index': 4, 'spike_level': 
50.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [False, None], 'InterLabReproducibilityandRepeats': [False, None]}, {'spike_index': 5, 'spike_level': 100.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [True, 3], 
'InterLabReproducibilityandRepeats': [True, 3]}], 'Matrix': [{'spike_index': 1, 'spike_level': 2.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [True, 3], 'InterLabReproducibilityandRepeats': [True, 3]}, {'spike_index': 2, 'spike_level': 5.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [False, None], 'InterLabReproducibilityandRepeats': [False, None]}, {'spike_index': 3, 'spike_level': 20.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [True, 3], 'InterLabReproducibilityandRepeats': [True, 3]}, {'spike_index': 4, 'spike_level': 50.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [False, None], 'InterLabReproducibilityandRepeats': [False, None]}, {'spike_index': 5, 'spike_level': 100.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [True, 3], 'InterLabReproducibilityandRepeats': [True, 3]}]}}}


matrixMissingSettings =  {'advanced_settings': {'advanced_curve_settings': {'STD': [{'spike_index': 1, 'spike_level': 2.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [True, 3], 'InterLabReproducibilityandRepeats': [True, 3]}, {'spike_index': 2, 'spike_level': 5.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [False, None], 'InterLabReproducibilityandRepeats': [False, None]}, {'spike_index': 3, 'spike_level': 20.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [True, 3], 'InterLabReproducibilityandRepeats': [True, 3]}, {'spike_index': 4, 'spike_level': 50.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [False, None], 'InterLabReproducibilityandRepeats': [False, None]}, {'spike_index': 5, 'spike_level': 100.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [True, 3], 'InterLabReproducibilityandRepeats': [True, 3]}], 'Spike': [{'spike_index': 1, 'spike_level': 2.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [True, 3], 'InterLabReproducibilityandRepeats': [True, 3]}, {'spike_index': 2, 'spike_level': 5.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [False, None], 'InterLabReproducibilityandRepeats': [False, None]}, {'spike_index': 3, 'spike_level': 20.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [True, 3], 'InterLabReproducibilityandRepeats': [True, 3]}, {'spike_index': 4, 'spike_level': 50.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [False, None], 'InterLabReproducibilityandRepeats': [False, None]}, {'spike_index': 5, 'spike_level': 100.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [True, 3], 'InterLabReproducibilityandRepeats': [True, 3]}], 'Matrix': [{'spike_index': 1, 'spike_level': 2.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [True, 3], 'InterLabReproducibilityandRepeats': [True, 3]}, {'spike_index': 2, 'spike_level': 5.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [False, None], 'InterLabReproducibilityandRepeats': [False, None]}, {'spike_index': 3, 'spike_level': 20.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [True, 3], 'InterLabReproducibilityandRepeats': [True, 3]}]}}}


spikeMissingSettings = {'advanced_settings': {'advanced_curve_settings': {'STD': [{'spike_index': 1, 'spike_level': 2.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [True, 3], 'InterLabReproducibilityandRepeats': [True, 3]}, {'spike_index': 2, 'spike_level': 5.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [False, None], 'InterLabReproducibilityandRepeats': [False, None]}, {'spike_index': 3, 'spike_level': 20.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [True, 3], 'InterLabReproducibilityandRepeats': [True, 3]}, {'spike_index': 4, 'spike_level': 50.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [False, None], 'InterLabReproducibilityandRepeats': [False, None]}, {'spike_index': 5, 'spike_level': 100.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [True, 3], 'InterLabReproducibilityandRepeats': [True, 3]}], 'Spike': [{'spike_index': 1, 'spike_level': 2.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [True, 3], 'InterLabReproducibilityandRepeats': [True, 3]}, {'spike_index': 2, 'spike_level': 5.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [False, None], 'InterLabReproducibilityandRepeats': [False, None]}, {'spike_index': 3, 'spike_level': 20.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [True, 3], 'InterLabReproducibilityandRepeats': [True, 3]}], 'Matrix': [{'spike_index': 1, 'spike_level': 2.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [True, 3], 'InterLabReproducibilityandRepeats': [True, 3]}, {'spike_index': 2, 'spike_level': 5.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [False, None], 'InterLabReproducibilityandRepeats': [False, None]}, {'spike_index': 3, 'spike_level': 20.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [True, 3], 'InterLabReproducibilityandRepeats': [True, 3]}, {'spike_index': 4, 'spike_level': 50.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [False, None], 'InterLabReproducibilityandRepeats': [False, None]}, {'spike_index': 5, 'spike_level': 100.0, 'Is_In_Curve': True, 'RepeatabilityandRepeats': [True, 3], 'InterLabReproducibilityandRepeats': [True, 3]}]}}}

gcFiles = files = ['AnalysisResult-Matrix_spike_100_D1_1- 30-7_1-2-52_01_35665541148183501248573.xlsx', 'AnalysisResult-Matrix_spike_20_D1_1_2-43_01_3557582426004149730208.xlsx', 'AnalysisResult-Matrix_spike_2_D1_1_1-2-34_01_35482862550978316498435.xlsx', 'AnalysisResult-Matrix_spike_50_D1_1_1-2-45_01_35598471129927513331927.xlsx', 'AnalysisResult-Matrix_spike_5_D1_1_1-2-36_01_35503152321663749397656.xlsx', 'AnalysisResult-Spike_spike_100_D1_1_1-2-46_01_35608776126364816736992.xlsx', 'AnalysisResult-Spike_spike_100_D1_2_1-2-47_01_35614199095694808886407.xlsx', 'AnalysisResult-Spike_spike_100_D1_3_1-2-48_01_35626554624179951736831.xlsx', 'AnalysisResult-Spike_spike_100_D2_1_1-2-49_01_35632558115917325857338.xlsx', 'AnalysisResult-Spike_spike_100_D2_2_1-2-50_01_35645241487278256928596.xlsx', 'AnalysisResult-Spike_spike_100_D2_3_1-2-51_01_35652962624121570074581.xlsx', 'AnalysisResult-Spike_spike_20_D1_1_1-2-37_01_35512173237202547394165.xlsx', 'AnalysisResult-Spike_spike_20_D1_2_1-2-38_01_35523865011057008711745.xlsx', 'AnalysisResult-Spike_spike_20_D1_3_1-2-39_01_35536925864212110396815.xlsx', 'AnalysisResult-Spike_spike_20_D2_1_1-2-40_01_35544942466644801252596.xlsx', 'AnalysisResult-Spike_spike_20_D2_2_1-2-41_01_35556595747401029359498.xlsx', 'AnalysisResult-Spike_spike_20_D2_3_1-2-42_01_35563864764147739279537.xlsx', 'AnalysisResult-Spike_spike_2_D1_1_1-2-28_01_35426846491803724609464.xlsx', 'AnalysisResult-Spike_spike_2_D1_2_1-2-29_01_35432072883938493805894.xlsx', 'AnalysisResult-Spike_spike_2_D1_3_1-2-33_01_35478064630077674041707.xlsx', 'AnalysisResult-Spike_spike_2_D2_1_1-2-31_01_35453095906085641606338.xlsx', 'AnalysisResult-Spike_spike_2_D2_2_1-2-32_01_35468941882868359324648.xlsx', 'AnalysisResult-Spike_spike_2_D2_3_1-2-30_01_35443423844621753603525.xlsx', 'AnalysisResult-Spike_spike_50_D1_1_1-2-44_01_35589117204869249281469.xlsx', 'AnalysisResult-Spike_spike_5_D1_1_1-2-35_01_35496128102324457118870.xlsx', 'AnalysisResult-STD_spike_100_D1_1_1-2-24_01_35387117994604356508227.xlsx', 'AnalysisResult-STD_spike_20_D1_1_01_35363562938905557863539.xlsx', 'AnalysisResult-STD_spike_2_D1_1_1-2-20_01_35348020723252140148841.xlsx', 'AnalysisResult-STD_spike_50_D1_1_1-2-23_01_35372882004211624713877.xlsx', 'AnalysisResult-STD_spike_5_D1_1_1-2-21_01_35358844413992488810065.xlsx']


def __fus(func):
    def wrapper(**kwargs):    
        length = len(kwargs['directories'])
        if not length:
            raise RuntimeError(f'Anomalous directories. Found {length} directories')
        elif length == 1:
            return func(**kwargs)
        else:
            return reduce(lambda x,y: chain(func(files = os.listdir(x), settings=kwargs['settings'] ), func(files = os.listdir(y),settings = kwargs['settings']) ), kwargs['directories']  )
    return wrapper




def __ro(func):
    def wrapper(**kwargs):
        seekMatrix = {x['spike_level'] for x in kwargs['settings']['advanced_settings']['advanced_curve_settings']['Spike']}.difference({x['spike_level'] for x in kwargs['settings']['advanced_settings']['advanced_curve_settings']['Matrix']})
        seekSpike = {x['spike_level'] for x in kwargs['settings']['advanced_settings']['advanced_curve_settings']['Matrix']}.difference({x['spike_level'] for x in kwargs['settings']['advanced_settings']['advanced_curve_settings']['Spike']})
        return chain(func(curve = 'Matrix', files =kwargs['files'] , values=seekMatrix),func(curve='Spike',files=kwargs['files'],values=seekSpike))
    return wrapper
@__fus
@__ro
def __dah(directories = None,curve=None ,files=None, values=None,settings=None):
     expr = map('{}_spike_{}_D1_1'.format, cycle([curve]),(int(x) if x.is_integer() else x for x in values))
     return map(lambda clause : list(filter(lambda x : True if clause in x else False, files))[0], list(expr))



def foo(xs):
    while True:
        try:
            print(next(xs),flush=True)
        except StopIteration:
            print('StopIteration')
            break


def fetchAdditionalRecFiles(settings = None, dirs = None):
    ''' Simple interface to expose private methods to the outside with a simple API.
        settings: A dict of settings encoding task to be done
        dirs: A list of directories to fetch possible files from.
    '''
    return __dah(directories = dirs, settings = settings)

t_dirs = ['/media/alexander/Elements/Pesticides Honey/TEST/GC','/media/alexander/Elements/Pesticides Honey/TEST/LC ESI NEG']
x = fetchAdditionalRecFiles(settings = spikeMissingSettings, dirs = t_dirs)
foo(x)




