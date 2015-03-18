import re
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y', 'z', 'e1', 'e2'])


class Point(object):
    def __init__(self, x=None, y=None, z=None, e1=None, e2=None):
        self.x = x
        self.y = y
        self.z = z
        self.e1 = e1
        self.e2 = e2

    def __str__(self):
        return "x:{} y:{} z:{} e1:{} e2:{}".format(self.x, self.y, self.z, self.e1, self.e2)


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

    __number_with_unit = re.compile("([0-9\.]+)\s*([a-z\/]+)")
    __from_to = re.compile("([0-9\.]+)\s*([a-z]+)(\s*to\s*(([0-9\.]+)\s*([a-z]+))?)?")

    def __init__(self):
        self.regex = {
            # 10 min
            "time": {
                "regex": self.__number_with_unit,
                "unit_and_factory": {
                    "m": 60,
                    "s": 1
                },
                "handler": self.__number_with_unit_handler
            },

            # 1 ml
            "capacity": {
                "regex": self.__number_with_unit,
                "unit_and_factory": {
                    "l": 1000,
                    "ml": 1
                },
                "handler": self.__number_with_unit_handler
            },

            # 1 mm
            "length": {
                "regex": self.__number_with_unit,
                "unit_and_factory": {
                    "cm": 10,
                    "mm": 1
                },
                "handler": self.__number_with_unit_handler
            },

            # 1 ml/mm
            "extrudate": {
                "regex": self.__number_with_unit,
                "unit_and_factory": {
                    "ml/mm": 1
                },
                "handler": self.__number_with_unit_handler
            },

            # 1 mm/min
            "feedrate": {
                "regex": self.__number_with_unit,
                "unit_and_factory": {
                    "mm/min": 1
                },
                "handler": self.__number_with_unit_handler
            },

            # 1 cm to 2 cm
            "length_from_to": {
                "regex": self.__from_to,
                "unit_and_factory": {
                    "cm": 10,
                    "mm": 1
                },
                "handler": self.__from_to_handler
            }
        }

    def __number_with_unit_handler(self, unit_and_factory, groups):
        value, unit = groups

        if unit is not None and unit in unit_and_factory:
            return float(value) * unit_and_factory[unit]
        else:
            return None

    def __from_to_handler(self, unit_and_factory, groups):
        from_value = self.__number_with_unit_handler(unit_and_factory, (groups[0], groups[1]))
        to_value = self.__number_with_unit_handler(unit_and_factory, (groups[4], groups[5]))

        return (from_value, to_value)


class Process(object):
    unit = Unit()
    params_rules = {}

    def __init__(self, raw_params):
        for key, value in self.__parse_params(raw_params).items():
            # assign the params as class member
            # e.g
            # Water: 100 ml -> self.__Water = 100
            setattr(self, key.replace(" ", "_").lower(), value)

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

            # Parse the value and convert the unit to minimal unit
            if except_unit is None:
                result[key] = float(value)
            else:
                unit_item = self.unit.regex[except_unit]
                m = unit_item["regex"].match(value)

                if m is None:
                    raise ParamterValueError(key, value)
                else:
                    result[key] = unit_item["handler"](unit_item["unit_and_factory"], m.groups())

        return result
