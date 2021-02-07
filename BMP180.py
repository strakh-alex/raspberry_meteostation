import time
import datetime
import Adafruit_BMP.BMP085 as BMP085
import logging
from influxdb import InfluxDBClient

sensor = BMP085.BMP085()

logging.basicConfig(filename='/var/log/BMP180.log', filemode='a', format='%(created)f %(message)s', level=logging.INFO) 
 
while True:
    try:
        temperature = sensor.read_temperature()
        pressure = int(sensor.read_pressure() / 133)
        sealevelPressure = int(sensor.read_sealevel_pressure() / 133)
        
        iso = datetime.datetime.utcnow()

        json_body = [
            {
                "measurement": "BMP",
                "tags": {
                    "host": "RPi",
                },
                "time": iso,
                "fields": {
                  "temperature" : temperature,
                  "pressure": pressure,
                  "sealevelPressure": sealevelPressure
                }
            }
        ]

        client = InfluxDBClient('localhost', 8086, '<username>', '<password>', '<database>')
        client.create_database('<database>')
        client.write_points(json_body)
 
    except RuntimeError as error:
        logging.warning(error.args[0])
        time.sleep(10.0)
        continue
    except Exception as error:
        logging.error("Error happens")
        raise error
 
    time.sleep(10.0)
