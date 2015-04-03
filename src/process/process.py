import re
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y', 'z', 'e1', 'e2'])


class Point(object):
    def __init__(self, x=None, y=None, z=None, e1=None, e2=None, f=None):
        self.x = x
        self.y = y
        self.z = z
        self.e1 = e1
        self.e2 = e2
	self.f = f

    def __str__(self):
        return "x:{} y:{} z:{} e1:{} e2:{}".format(self.x, self.y, self.z, self.e1, self.e2)

class Command(object):
    def __init__(self, command, value):
        self.command = command
        self.value = value

    def __str__(self):
        return "command:{} value:{}".format(self.command, self.value)


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
    __x_y = re.compile("\(\s*([0-9\.]+)\s*,\s*([0-9\.]+)\)")
    __temperature = re.compile("([0-9\.]+)\s*degress\s*(C|F)")

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
                    "ml/mm": 1,
                    "ml/step": 1
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
            },

            # (0, 0)
            "x_y_coordinates": {
                "regex": self.__x_y,
                "unit_and_factory": None,
                "handler": self.__x_y_coordinates_handler
            },

            # 70 degress C
            "temperature": {
                "regex": self.__temperature,
                "unit_and_factory": {
                    "C": 1,
                    "F": self.__f_to_c
                },
                "handler": self.__number_with_unit_handler
            }
        }

    def __f_to_c(self, f):
        return (f - 32) * 5 / 9

    def __number_with_unit_handler(self, unit_and_factory, groups):
        value, unit = groups

        if unit is not None and unit in unit_and_factory:
            if type(unit_and_factory[unit]) is int:
                return float(value) * unit_and_factory[unit]
            else:
                return unit_and_factory[unit](float(value))
        else:
            return None

    def __from_to_handler(self, unit_and_factory, groups):
        from_value = self.__number_with_unit_handler(unit_and_factory, (groups[0], groups[1]))
        to_value = self.__number_with_unit_handler(unit_and_factory, (groups[4], groups[5]))

        return (from_value, to_value)

    def __x_y_coordinates_handler(self, unit_and_factory, groups):
        return (float(groups[0]), float(groups[1]))

class Process(object):
    unit = Unit()
    params_rules = {}

    def __init__(self, raw_params):
        for key, value in self.__parse_params(raw_params).items():
            # assign the params as class member
            # e.g
            # Water: 100 ml -> self.__Water = 100
            setattr(self, key.replace(" ", "_").lower(), value)

    def __find_values_by_key(self, params, key):
        result = []

        for item in params:
            if item[0] == key:
                result.append(item[1])

        return result

    def __convert_if_is_number(self, s):
        try:
            return float(s)
        except ValueError:
            return s

    def __parse_params(self, params):
        result = {}
        for key, (except_unit, required, default) in self.params_rules.items():
            values = self.__find_values_by_key(params, key)

            if len(values) == 0:
                if required:
                    raise ParameterNameError(key)
                else:
                    result[key] = default
                    continue

            # Parse the value and convert the unit to minimal unit
            for value in values:

                if except_unit is None:
                    value_result = self.__convert_if_is_number(value)
                else:
                    unit_item = self.unit.regex[except_unit]
                    m = unit_item["regex"].match(value)

                    if m is None:
                        raise ParamterValueError(key, value)
                    else:
                        value_result = unit_item["handler"](unit_item["unit_and_factory"], m.groups())

                # If there are not only one value of this key, save all the
                # value to a list
                if key in result:
                    if type(result[key]) is not list:
                        tmp_value = result[key]
                        result[key] = [tmp_value, value_result]
                    else:
                        result[key].append(value_result)
                else:
                    result[key] = value_result

        return result


    # ==========================================================================
    #
    # Process Interface
    #
    # ==========================================================================
    def points(self):
        return []

    def total_water(self):
        return 0

    def total_length(self):
        return 0
