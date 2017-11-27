import configparser

from qhue import Bridge

config = configparser.ConfigParser()
config.read('config.txt')
hue = Bridge(config.get('hue', 'bridge_ip'), config.get('hue', 'user_token'))


def lights_on(update):
    if hue.lights[1]()['state']['on']:
        # Lights are already on
        return False
    else:
        hue.groups[1].action(on=True)
        return True


def lights_off(update):
    if not hue.lights[1]()['state']['on']:
        # Lights are already off
        return False
    else:
        hue.groups[1].action(on=False)
        return True
