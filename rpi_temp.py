import os
import time
import datetime
from influxdb import InfluxDBClient

bashCommand = "vcgencmd measure_temp | egrep -o '[0-9]*\.[0-9]*'"

while True:
	try:
		command = os.popen((bashCommand)) 
		rpi_temp = float(command.read().strip())
		print(rpi_temp)
		iso = datetime.datetime.utcnow()
		
		json_body = [
			{
				"measurement": "RPi",
				"tags": {
					"host": "RPi",
				},
				"time": iso,
				"fields": {
					"temperature" : rpi_temp
				}
			}
		]

		client = InfluxDBClient('localhost', 8086, '<username>', '<password>>', '<database>')
		client.create_database('<database>')
		client.write_points(json_body)
	
	except RuntimeError as error:
	    time.sleep(2.0)
	    continue
	except Exception as error:
	    raise error

	time.sleep(5.0)
