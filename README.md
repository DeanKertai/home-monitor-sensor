# Home Monitor Sensor
This is part of my home monitoring system. I run this Python script on a 
few Raspberry Pis equipped with temperature, humidity, water, and gas sensors.
It periodically posts the sensor data to my 
[serverless backend](https://github.com/DeanKertai/home-monitor-api).  


## Install Dependencies
```bash
sudo apt-get install libgpiod2
python3 -m pip install -r requirements.txt
```

## Environment Variables
Before the script can be run, you need to create a `.env` file in the root
directory with the following variables:
```
API_PASSWORD=<The API password for this device>
API_URL=<Base API url>
DEVICE_ID=<Alpha numeric string describing which sensor this is. ie: 'Garage'>

```

## Run
```bash
python3 main.py
```

## Run as Service
1. Create a service file
    ```bash
    sudo vim /etc/systemd/system/sensors.service
    ```
    Contents:
    ```
    [Unit]
    Description=Home Monitor Sensors
    After=multi-user.target
    
    [Service]
    Type=simple
    Restart=always
    ExecStart=/usr/bin/python3 /home<USERNAME>/<PATH TO SCRIPT>
    
    [Install]
    WantedBy=multi-user.target
    ```
1. Enable and start service
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable sensors
    sudo systemctl start sensors
    ```
1. Make sure it's working
    ```bash
    sudo systemctl status sensors
    ```


## Temperature/Humidity Circuit Diagram
1. Connect the `vcc` pin on the DHT22 sensor to a `5v` pin on the Raspberry Pi.
1. Connect the `ground` pin to one of the `ground` pins on the Raspberry Pi.
1. Connect the `data` pin to one of the `GPIO` pins on the Raspberry Pi
1. Connect the `vcc` pin to the `data` pin with a 10k ohm resistor
```
+--------------------+
|                    |
|    DHT22 Sensor    |
|                    |
+--------------------+
 |     |     |      |
vcc   dat   nul    gnd
 |     |            |
 |~10k~|            |
 |     |            |
5v   gpio          gnd
```
