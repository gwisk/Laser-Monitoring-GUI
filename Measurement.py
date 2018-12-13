import Adafruit_ADS1x15
from decimal import Decimal
import time
from guizero import App, Text


#rawRange = 65536 #2^16
#logRange = 5.0
convFactor = 5.0/65536
efficacy = 0.020 #phototopic efficacy for 770 nm laser is around 0.020 lm/W
laserD = 3 # dummy variable, get the exact laser D

#converts from voltage to lux
def rawToLux(voltage): 
	logLux = voltage*convFactor
	return pow(10, logLux)

#converts from lux to milliwatts
def luxTomW(lux): 
	watts = laserD*lux/efficacy
	return watts*(10**-3)

#converts from voltage to milliwatts
def rawTomW(voltage): 
	logLux = voltage*convFactor
	lux = pow(10, logLux)
	watts = laserD*lux/efficacy
	return '%.5f'%(watts*(10**-3))

i = 1
def update():
	global i
	sensor1.value=str(rawTomW(i)) + " mW"
	sensor2.value= str(rawTomW(i)) + " mW"
	i+=1
	if i > 2:
		sensor1.text_color="red"
"""
if abs(sensor1.value) >= range:
	sensor1.text_color="red"
if abs(sensor1.value) < range:
	sensor1.text_color = "green"
"""

app = App(title="Laser Monitoring", layout="grid")
sensor1 = Text(app, text=str(rawTomW(0)) + " mW", grid =[0, 0], size =25)
sensor2 = Text(app, text=str(rawTomW(0)) + " mW", grid = [0, 1], size = 25)
sensor1.repeat(1000, update)
app.display()
