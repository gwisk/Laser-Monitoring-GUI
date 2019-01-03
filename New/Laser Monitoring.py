import board
from guizero import App, Text
import digitalio
import busio
from adafruit_ads1x15.analog_in import AnalogIn


convFactor = 5.0/65536
efficacy = 21.856            #phototopic efficacy for 671 nm laser is around 0.020 lm/W http://www.kayelaby.npl.co.uk/general_physics/2_5/2_5_3.html
area = 3.2*(10**-6)         # area of the sensor



i2c = busio.I2C(board.SCL, board.SDA)
import adafruit_ads1x15.ads1115 as ADS
ads=ADS.ADS1115(i2c)

def luxTomW():
		logLux = chan.voltage * 5.0/3.3 #V
		lux = pow(10, logLux)
		watts = (area*lux)/efficacy
		return '%.3f'%(watts*(10**3))

def update():
    message.value = luxTomW(chan.voltage)

chan=AnalogIn(ads, ADS.P0)
voltage = chan.voltage
power = luxTomW(voltage)
app = App(title="Laser Monitoring")
message = Text(app, text=power)
message.repeat(1000, update)
app.display()

print(chan.value, chan.voltage)
