import re

class ParameterNameError(Exception):
    def __init__(self, param_name):
        self.param_name = param_name

    def __str__(self):
        return "Parameter Error: {} doesn't exist".format(self.param_name)

class ParamterValueError(Exception):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return "Parameter Value Error: {}: {} is not valid.{}".format(self.key, self.value)

class Process(object):
    unit_regex = {
        "time": re.compile("([0-9]+)\s*(s)"),
        "capacity": re.compile("([0-9]+)\s*(ml|l)"),
        "length": re.compile("([0-9]+)\s*(cm|mm)"),
    }

    params_rules = {}

    def __init__(self):
        self.__params = {}

    def __parse_params(self, params):
        result = {}

        for key, (except_unit, required) in params_rules.items():
            value = params.get(key, None)

            if value is None:
                if required:
                    raise ParameterNameError(key)
                else: 
                    continue

            m = unit_regex[except_unit].match(value)

            if m is None:
                raise ParameterValueError(key, value)
            else:
                number = m.groups(0)
                unit = m.groups(1)
            
            result[key] = (number, unit)

        return result 
