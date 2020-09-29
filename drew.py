import serial 
import time
import Adafruit_MCP9808.MCP9808 as MCP9808
import smbus2
import board
import busio
import adafruit_bme280
import datetime
import adafruit_sgp30
import sys
import datetime
import time
from influxdb import InfluxDBClient
from tkinter import *
#import tkinter
import curses

# system variables
upTime = 0
global store_timer
store_timer = 0
pollInterval = 5
storeInterval = 1200
storeFile = '/home/pi/codebase/store.txt'

# Configure InfluxDB connection variables
host = "192.168.0.26"
port = 8086 # default port
user = "pi"
password = "gt46u76t"
dbname = "sensor_data"

# Create the InfluxDB client object
client = InfluxDBClient(host, port, user, password, dbname)
measurement = "rpi2"

# SenseAir S8 | co2
ser = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=.5)
ser.flushInput()

# BME280 | humidity, pressure, altitiude
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

# MCP9808 | high accuracy temperature
mcp = MCP9808.MCP9808()
mcp.begin()

# SGP30 | voc, co2
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)         
sgp30.iaq_init()

# SGP30 set saved calibration
store = open(storeFile, 'r')
cBase = int(store.readline())
vBase = int(store.readline())
store.close()
sgp30.set_iaq_baseline(cBase, vBase)


def getCO2():
    ser.flushInput()
    ser.write(b'\xFE\x44\x00\x08\x02\x9F\x25')
    resp = ser.read(7)
    high = resp[3]
    low = resp[4]
    C = (resp[3] * 256) + resp[4]
    return C 

def mbar_to_iMerc(mbar):
    return round((P * 100) / 3386.39, 2)

def c_to_f(c):
    return round(c * 9.0 / 5.0 + 32.0, 1)

def sec_to_time(sec):
    return str(datetime.timedelta(seconds=sec))

def set_baseline():
    global store_timer
    if store_timer >= storeInterval:
        store_timer = 0 
        co2eq_base, tvoc_base = sgp30.baseline_eCO2, sgp30.baseline_TVOC
        temp = open(storeFile, 'w')
        temp.write(str(co2eq_base))
        temp.write('\n')
        temp.write(str(tvoc_base))
        temp.close()
        #print("new baseline")

def send_data(co2, temp, voc, hum, pres):
    iso = time.ctime()
    data = [{
        "measurement":measurement,
        "time":iso,
        "fields": {
            "co2":co2,
            "temp":c_to_f(temp),
            "voc":voc,
            "hum":hum,
            "press":pres
        }
    }]
    client.write_points(data)


def get_data():	    
    hum = int(bme280.humidity)
    pres = int(bme280.pressure) # unit: mbar
    #alt = int(bme280.altitude)
 
    voc = sgp30.TVOC
    #C2 = sgp30.eCO2
        
    co2 = getCO2()
    temp = mcp.readTempC()

    #print('C={0}, T={1}, V={2}, H={3}, P={4}'.format(co2, c_to_f(temp), voc, hum, pres))

    store_timer += pollInterval
    #upTime += pollInterval

    set_baseline()
    send_data(co2, temp, voc, hum, pres)

    time.sleep(pollInterval)


class Application(Frame):

	def __init__(self, master):
		Frame.__init__(self, master)
		self.topFrame = Frame(root)
		self.botFrame = Frame(root)
		
		self.topFrame.pack(side=TOP)
		self.botFrame.pack(side=BOTTOM)
		
		self.create_widgets()
		self.updater()

	def create_widgets(self):
		self.button1 = Button(self.topFrame, text=0)
		self.button2 = Button(self.topFrame, text=0)
		self.button3 = Button(self.botFrame, text=0)
		self.button4 = Button(self.botFrame, text=0)
		
		self.button1.config(height=14, width=47, activebackground=self.button1.cget('background'))
		self.button2.config(height=14, width=47, activebackground=self.button2.cget('background'))
		self.button3.config(height=13, width=47, activebackground=self.button3.cget('background'))
		self.button4.config(height=13, width=47, activebackground=self.button4.cget('background'))

		self.button1.pack(side=LEFT)
		self.button2.pack(side=LEFT)
		self.button3.pack(side=LEFT)
		self.button4.pack(side=LEFT)

	def update_buttons(self):
		hum = int(bme280.humidity)
		pres = int(bme280.pressure)

		voc = sgp30.TVOC
		co2 = getCO2()
		temp = mcp.readTempC()

		#store_timer += pollInterval # fix this
		#set_baseline # fix this
		send_data(co2, temp, voc, hum, pres)

		self.button1["text"] = co2
		self.button2["text"] = voc
		self.button3["text"] = temp
		self.button4["text"] = hum
		time.sleep(pollInterval)
		
	def updater(self):
		self.update_buttons()
		self.after(1, self.updater)



root = Tk()
root.overrideredirect(True)
root.config(cursor="none")

app = Application(root)
root.mainloop()

#except KeyboardInterrupt:
 #   pass


