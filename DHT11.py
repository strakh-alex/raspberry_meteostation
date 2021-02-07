import time
import datetime
import board
import adafruit_dht
import logging
from influxdb import InfluxDBClient

dhtDevice = adafruit_dht.DHT11(board.D26, use_pulseio=False)

logging.basicConfig(filename='/var/log/DHT11.log', filemode='a', format='%(created)f %(message)s', level=logging.INFO) 
 
while True:
    try:
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity
        iso = datetime.datetime.utcnow()

        json_body = [
            {
                "measurement": "DHT",
                "tags": {
                    "host": "RPi",
                },
                "time": iso,
                "fields": {
                  "temperature" : temperature,
                  "humidity": humidity
                }
            }
        ]

        client = InfluxDBClient('localhost', 8086, '<username>', '<influx>', '<database>')
        client.create_database('<database>')
        client.write_points(json_body)
 
    except RuntimeError as error:
        logging.warning(error.args[0])
        time.sleep(5.0)
        continue
    except Exception as error:
        logging.error(dhtDevice.exit())
        raise error
 
    time.sleep(5.0)
