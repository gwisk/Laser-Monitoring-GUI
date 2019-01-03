
# -*- coding: utf-8 -*-

from time import sleep
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import sys
import random
import cloud4rpi
import ds18b20
import rpi

convFactor = 5.0/65536
efficacy = 21.856            #phototopic efficacy for 671 nm laser is around 0.020 lm/W http://www.kayelaby.npl.co.uk/general_physics/2_5/2_5_3.html
area = 3.2*(10**-6)         # area of the sensor

i2c = busio.I2C(board.SCL, board.SDA)
ads=ADS.ADS1115(i2c)

chan=AnalogIn(ads, ADS.P0)
def sensor1():
		logLux = chan.voltage * 5.0/3.3 #V
		lux = pow(10, logLux)
		watts = (area*lux)/efficacy
		return '%.3f'%(watts*(10**3))
# Put your device token here. To get the token,
# sign up at https://cloud4rpi.io and create a device.
DEVICE_TOKEN = 'AQ9zBj6KjdR2b761douGif4Ns'

# Constants
LED_PIN = 12
DATA_SENDING_INTERVAL = 30  # secs
DIAG_SENDING_INTERVAL = 60  # secs
POLL_INTERVAL = 0.5  # 500 ms




def listen_for_events():
    # Write your own logic here
    result = random.randint(1, 5)
    if result == 1:
        return 'RING'

    if result == 5:
        return 'BOOM!'

    return 'IDLE'


def main():
    # Put variable declarations here
    # Available types: 'bool', 'numeric', 'string'
    variables = {
        'STATUS': {
            'type': 'string',
            'bind': listen_for_events
        },
        'SENSOR1': {
           'type': 'numeric',
           'bind': sensor1
   } }

    diagnostics = {
       'CPU Temp': rpi.cpu_temp,
        'IP Address': rpi.ip_address,
        'Host': rpi.host_name,
        'Operating System': rpi.os_name
    }
    device = cloud4rpi.connect(DEVICE_TOKEN)

    # Use the following 'device' declaration
    # to enable the MQTT traffic encryption (TLS).
    #
    # tls = {
    #     'ca_certs': '/etc/ssl/certs/ca-certificates.crt'
    # }
    # device = cloud4rpi.connect(DEVICE_TOKEN, tls_config=tls)

    try:
        device.declare(variables)
        device.declare_diag(diagnostics)

        device.publish_config()

        # Adds a 1 second delay to ensure device variables are created
        sleep(1)

        data_timer = 0
        diag_timer = 0

        while True:
            if data_timer <= 0:
                device.publish_data()
                data_timer = DATA_SENDING_INTERVAL

            if diag_timer <= 0:
                device.publish_diag()
                diag_timer = DIAG_SENDING_INTERVAL

            sleep(POLL_INTERVAL)
            diag_timer -= POLL_INTERVAL
            data_timer -= POLL_INTERVAL

    except KeyboardInterrupt:
        cloud4rpi.log.info('Keyboard interrupt received. Stopping...')

    except Exception as e:
        error = cloud4rpi.get_error_message(e)
        cloud4rpi.log.exception("ERROR! %s %s", error, sys.exc_info()[0])

    finally:
        sys.exit(0)


if __name__ == '__main__':
    main()
