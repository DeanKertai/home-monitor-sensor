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

## Run
```bash
python3 main.py
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
