import copy


class JSONAdaptor:
    @staticmethod
    def pythontojson(arg):
        arg_cp = copy.deepcopy(arg)
        del arg_cp['basic_settings']
        del arg_cp['advanced_settings']['advanced_curve_settings']
        del arg_cp['project_parameters']
        arg_cp['basic_settings'] = {}
        arg_cp['advanced_settings']['advanced_curve_settings'] = {}

        for item in arg['basic_settings']:
            arg_cp['basic_settings'][item.Curve] = {}
            arg_cp['basic_settings'][item.Curve]['Curve'] = True
            arg_cp['basic_settings'][item.Curve]['Repeatability'] = item.Repeatability
            arg_cp['basic_settings'][item.Curve]['Reproducibility'] = item.Reproducibility

        for curve in arg['advanced_settings']['advanced_curve_settings']:
            arg_cp['advanced_settings']['advanced_curve_settings'][curve] = {}
            for point in arg['advanced_settings']['advanced_curve_settings'][curve]:
                arg_cp['advanced_settings']['advanced_curve_settings'][curve]['curve_points'] = [x['spike_level']
                                                                                                 for x in arg['advanced_settings']['advanced_curve_settings'][curve] if x['Is_In_Curve']]
                arg_cp['advanced_settings']['advanced_curve_settings'][curve]['RepeatabilityandRepeats'] = [[x['spike_level'], x['RepeatabilityandRepeats'][1]]
                                                                                                            for x in arg['advanced_settings']['advanced_curve_settings'][curve] if x['RepeatabilityandRepeats'][0]]
                arg_cp['advanced_settings']['advanced_curve_settings'][curve]['InterLabReproducibilityandRepeats'] = [[x['spike_level'], x['InterLabReproducibilityandRepeats'][1]]
                                                                                                                      for x in arg['advanced_settings']['advanced_curve_settings'][curve] if x['InterLabReproducibilityandRepeats'][0]]

        return arg_cp

    @staticmethod
    def jsontopython(arg):
        # Convert json to python
        """Receives user input in order Curve Points, Repeatability Points, Within Laboratory Reproducibility Points, Repeatability repeats per level, Within Laboratory Reproducibility repeats"""
        arg_cp = {'basic_settings': [], 'advanced_settings': None}
        arg_cp['advanced_settings'] = None
        arg_cp['advanced_settings'] = {'advanced_curve_settings': None}
        arg_cp['advanced_settings']['advanced_curve_settings'] = {}
        Base_Parameters = namedtuple(
            "Base_Parameters", 'Curve,Repeatability,Reproducibility')

        for item in arg['basic_settings']:
            arg_cp['basic_settings'].append(Base_Parameters(Curve=item, Repeatability=arg['basic_settings']
                                                            [item]['Repeatability'], Reproducibility=arg['basic_settings'][item]['Reproducibility']))

        for curve in arg['advanced_settings']['advanced_curve_settings']:
            arg_cp['advanced_settings']['advanced_curve_settings'] = {
                curve: None}
            x = arg['advanced_settings']['advanced_curve_settings'][curve]['curve_points']
            y = [x[0] for x in arg['advanced_settings']
                 ['advanced_curve_settings'][curve]['Repeatability']]
            z = [x[1] for x in arg['advanced_settings']
                 ['advanced_curve_settings'][curve]['Repeatability']]
            f = [x[0] for x in arg['advanced_settings']
                 ['advanced_curve_settings'][curve]['Reproducibility']]
            o = [x[1] for x in arg['advanced_settings']
                 ['advanced_curve_settings'][curve]['Reproducibility']]
            arg_cp['advanced_settings']['advanced_curve_settings'][curve] = InputUtils.interpret_input(
                x, y, f, z, o)

        arg.update(arg_cp)
        return arg

class InputUtils:

    @staticmethod
    def convert_input(string, typ=None):
        # Takes user input "levels, conc values sepperated by commas and converts them into a list of values"
        # Types to convert int_num,float_num,string
        try:
            if typ is not None:
                if typ is 'int_num':
                    inp = string.replace(" ", "")
                    inp = string.split(",")
                    inp = [int(i) for i in inp]
                elif typ is 'float_num':
                    inp = string.replace(" ", "")
                    inp = string.split(",")
                    inp = [float(i) for i in inp]
                elif typ is 'string':
                    inp = string.split(",")
            else:
                raise TypeError
        except TypeError:
            print("Invalid Input type to convert")
        return tuple(inp)

    @staticmethod
    def input_to_nums(string, typ=None):
        try:
            if typ is not None:
                if typ is 'float':
                    c = [float(x) for x in string.split(',')]
                if typ is 'int':
                    c = [int(x) for x in string.split(',')]
            else:
                raise ValueError
        except ValueError:
            print('Input type not defined')
        return c

    def aggregator(*args):
        final = args[0] + args[1] + args[2]
        final = dict.fromkeys(final)
        final = list(final)
        final.sort()
        return final

    def mapper(c_pts=None, R_pts=None, r_pts=None, R_repeats=None, r_repeats=None, zipR=None, zipr=None, aggregated=None):
        masterlist = []
        for idx, lvl in enumerate(aggregated, start=1):
            c = [idx, lvl]
            if lvl in c_pts:
                c.append(True)
            else:
                c.append(False)
            if lvl in R_pts:
                for item in zipR:
                    if lvl == item['concentration']:
                        c.append([True, item['repeats']])
            else:
                c.append([False, None])
            if lvl in r_pts:
                for item in zipr:
                    if lvl == item['concentration']:
                        c.append([True, item['repeats']])
            else:
                c.append([False, None])
            masterlist.append(c)
        return masterlist

    @staticmethod
    def interpret_input(*args):
        """Receives user input in order Curve Points, Repeatability Points, Within Laboratory Reproducibility Points, Repeatability repeats per level, Within Laboratory Reproducibility repeats"""
        # Replace with clearer keyword arguements. Requires updating JSONAdapter
        finallist = []
        v = []
        c = []
        for i in range(5):
            if i < 3:
                if isinstance(args[i], str):
                    finallist.append(
                        InputUtils.input_to_nums(args[i], typ='float'))
                else:
                    finallist.append(args[i])
            else:
                if isinstance(args[i], str):
                    finallist.append(
                        InputUtils.input_to_nums(args[i], typ='int'))
                else:
                    finallist.append(args[i])
        finallist.append(list(zip(finallist[1], finallist[3])))
        finallist.append(list(zip(finallist[2], finallist[4])))
        for concentration, repeats in finallist[5]:
            v.append({'concentration': concentration, 'repeats': repeats})
        finallist[5] = v
        for concentration, repeats in finallist[6]:
            c.append({'concentration': concentration, 'repeats': repeats})
        finallist[6] = c
        finallist.append(InputUtils.aggregator(
            finallist[0], finallist[1], finallist[2]))
        ret = InputUtils.mapper(c_pts=finallist[0], R_pts=finallist[1], r_pts=finallist[2], R_repeats=finallist[3],
                                r_repeats=finallist[4], zipR=finallist[5], zipr=finallist[6], aggregated=finallist[7])
        masterlist = []
        for item in ret:
            masterlist.append({'spike_index': item[0], 'spike_level': item[1], 'Is_In_Curve': item[2],
                               'RepeatabilityandRepeats': item[3], 'InterLabReproducibilityandRepeats': item[4]})
        return masterlist
