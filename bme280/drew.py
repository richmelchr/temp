import smbus2
import bme280

port = 1
address = 0x77
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)

data = bme280.sample(bus, address, calibration_params)

print(data.id)
print(data.timestamp)
print(data.temperature)

print(data)








