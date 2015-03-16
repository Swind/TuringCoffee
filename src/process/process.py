import re
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y', 'z', 'e1', 'e2'], verbose=True)

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


class Unit(object):
    regex = {
        "time": re.compile("([0-9]+)\s*(s)"),
        "capacity": re.compile("([0-9]+)\s*(ml|l)"),
        "length": re.compile("([0-9]+)\s*(cm|mm)"),
        "extrudate": re.compile("([0-9]+)\s*(ml/mm)"),
        "feedrate": re.compile("([0-9]+)\s*(mm/min)"),
        "high": re.compile()
    }


class Process(object):
    unit = Unit()
    params_rules = {}

    def __init__(self, raw_params):
        for key, value in self.__parse_params(raw_params):
            # assign the params as class member
            # e.g
            # Water: 100 ml -> self.__Water = 100
            setattr(self, "__" + key, value)

    def __parse_params(self, params):
        result = {}

        for key, (except_unit, required, default) in self.params_rules.items():
            value = params.get(key, None)

            if value is None:
                if required:
                    raise ParameterNameError(key)
                else:
                    result[key] = default
                    continue

            m = self.unit.regex[except_unit].match(value)

            if m is None:
                raise ParamterValueError(key, value)
            else:
                number = m.groups(0)
                unit = m.groups(1)

            result[key] = (number, unit)

        return result
