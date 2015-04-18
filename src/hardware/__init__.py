import mock
import monitor

mock_heater = None


def get_heater(config):
    if config['Emulator']:
        global mock_heater
        heater_emulator = mock.MockHeater(config['HeaterEmulator'])
        mock_heater = heater_emulator
        return heater_emulator
    else:
        import heater
        return heater.Heater(config['Heater']['pin'])


def get_sensors(config):
    if config['Emulator']:
        return map(__get_mock_sensor_monitor, config['Sensors'])
    else:
        return map(__get_sensor_monitor, config['Sensors'])


def get_refill(config):
    if config['Emulator']:
        return mock.MockRefill()
    else:
        import refill
        return refill.Refill()


def __get_mock_sensor_monitor(sensor_config):
    global mock_heater
    return monitor.TemperatureMonitor(mock.MockSensor(mock_heater))


def __get_sensor_monitor(sensor_config):
    if sensor_config['type'] == 'PT100':
        import pt100
        return monitor.TemperatureMonitor(pt100.PT100(sensor_config['ce']))

    return None
