from decimal import Decimal
from guizero import App, Text
import Adafruit_ADS1x15
import time

adc = Adafruit_ADS1x15.ADS1115()

#rawRange = 65536 #2^16
#logRange = 5.0
convFactor = 5.0/65536
efficacy = 0.02049            #phototopic efficacy for 770 nm laser is around 0.020 lm/W http://www.kayelaby.npl.co.uk/general_physics/2_5/2_5_3.html
area = 3.2*(10**-6)         # dummy variable, get the exact laser D

#converts from voltage to lux
def rawToLux(raw): 
	logLux = raw*convFactor
	return pow(10, logLux)

#converts from lux to milliwatts
def luxTomW(lux): 
	watts = area*lux/efficacy
	return watts*(10**3)

#converts from voltage to milliwatts
def rawTomW(raw): 
	logLux = raw*convFactor
	lux = pow(10, logLux)
	watts = (area*lux)/efficacy
	return '%.3f'%(watts*(10**3))

reading1 = adc.read_adc(0)
reading2 = adc.read_adc(0)

"""
i = 1
def update():
	global i
	sensor1.value=str(rawTomW(i)) + " mW"
	sensor2.value= str(rawTomW(i)) + " mW"
	i+=1
	if i > 2:
		sensor1.text_color="red"

if abs(sensor1.value) >= range:
	sensor1.text_color="red"
if abs(sensor1.value) < range:
	sensor1.text_color = "green"
"""

def update():
	sensor1.value = read_adc(0) + " raw"
	sensor2.value = read_adc(0) + " mW"


app = App(title="Laser Monitoring", layout="grid")
sensor1 = Text(app, text=str(reading1) + " raw", grid =[0, 0], size =25)
sensor2 = Text(app, text=str(reading1) + " mW", grid = [0, 1], size =25)
sensor1.repeat(1000, update)
app.display()
