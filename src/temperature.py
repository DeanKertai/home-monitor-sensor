import json
import re
from threading import Thread
from typing import List
from dotenv import load_dotenv
import os
import requests
import time
import board
import adafruit_dht
import statistics

load_dotenv()

# Connect the data pin to GPIO 4 (or update the value below)
# See README for a circuit diagram
data_pin = board.D4

class TemperatureModule:
    def __init__(self, read_interval=5, post_interval=600):
        self.name = 'Temperature module'
        self.read_interval = read_interval
        self.post_interval = post_interval
        self.last_post = time.time()
        self.temperature_buffer: List[float] = []
        self.humidity_buffer: List[float] = []
        self.dht_device = adafruit_dht.DHT22(data_pin)
        self.thread = Thread(target=self.loop)
        self.thread.name = self.name
        self.thread.daemon = True
        self.thread.start()

        # FIXME: Standardize this accross modules. DRY
        self.api_token = None

    def get_api_url(self, endpoint):
        base_url = os.environ.get('API_URL')
        if base_url is None:
            raise Exception('API_URL environment variable not set')
        return base_url + endpoint

    def get_device_id(self):
        device_id = os.environ.get('DEVICE_ID')
        if device_id is None:
            raise Exception('DEVICE_ID environment variable not set')
        return device_id

    def get_token(self):
        """
        Uses a device password saved in environment variables to 
        retreive an auth token from the API.
        FIXME: This is going to be used in every module... This
               should be standardized, maybe make a paren Module class
        """
        print('Getting token from server')
        password = os.environ.get('API_PASSWORD')
        if password is None:
            raise Exception('API_PASSWORD environment variable not set')
            
        url = self.get_api_url('/auth')
        response = requests.post(url, json.dumps({'password': password }))
        if response.status_code == 403:
            raise Exception('Invalid API password')
        elif response.status_code == 201:
            print('Got token from API')
            response_body = response.json()
            self.api_token = response_body['token']
        else:
            raise Exception(f'Got {response.status_code} from API while getting token')

    def post_values(self):
        """
        Takes the values in the temperature and humidity buffers
        and posts their averages for the current timestamp
        """
        if self.api_token is None:
            self.get_token()
        average_temperature = round(statistics.mean(self.temperature_buffer), 2)
        average_humidity = round(statistics.mean(self.humidity_buffer), 2)
        timestamp = int(time.time() * 1000)
        url = self.get_api_url('/temperature')
        device_id = self.get_device_id()
        response = requests.post(
            url,
            data=json.dumps({
                'deviceId': device_id,
                'timestamp': timestamp,
                'celsius': average_temperature,
            }),
            headers={
                'Authorization': 'Bearer ' + self.api_token
            },
        )
        if response.status_code != 201:
            print(f'Failed to post temperature data: {response.status_code}')
        self.temperature_buffer = []
        self.humidity_buffer = []

    def loop(self):
        print(f'Starting {self.name}')
        try:
            while True:
                try:
                    temperature_c = self.dht_device.temperature
                    self.temperature_buffer.append(temperature_c)
                    
                    humidity = self.dht_device.humidity
                    self.humidity_buffer.append(humidity)

                    if time.time() - self.last_post > self.post_interval:
                        self.last_post = time.time()
                        self.post_values()
                    
                except RuntimeError as error:
                    # Errors happen fairly often when reading from DHT sensors
                    # Don't sweat it, just keep going
                    time.sleep(self.read_interval)
                    continue
                except Exception as error:
                    print(f'Exception in {self.name}: {str(error)}')

                time.sleep(self.read_interval)

        except KeyboardInterrupt:
            print(f'Exiting {self.name} due to keyboard interrupt')

        finally:
            self.dht_device.exit()
            print(f'{self.name} internal loop ended')
