import machine
import dht
import urequests
import time
import bmp180
from machine import ADC
from machine import I2C
from machine import Pin
import blynklib_mp as Blynk

# Replace with your network credentials
SSID = "SSID"
PASSWORD = "PASSWORD"

# Replace with your Blynk project's authentication token
BLYNK_AUTH_TOKEN = "rWbeEHAj5uxK14OBUSAiHq5eMUnHF0NE"

# Temperature thresholds
TEMPERATURE_HIGH_THRESHOLD = 30  
TEMPERATURE_LOW_THRESHOLD = 0   

# Initialize the DHT22 sensor
dht_sensor = dht.DHT22(machine.Pin(4))

# Initialize the BMP180 sensor
i2c = I2C(scl=Pin(22), sda=Pin(21))
bmp = bmp180.BMP180(i2c)

# Initialize the MQ135 gas sensor
adc = ADC(Pin(35))
adc.atten(ADC.ATTN_11DB)
adc.width(ADC.WIDTH_9BIT)

# Initialize Blynk
blynk = Blynk.Blynk(BLYNK_AUTH_TOKEN)

while True:
    try:
        # Read data from DHT22 sensor
        dht_sensor.measure()
        humidity = dht_sensor.humidity()
        temperature_dht = dht_sensor.temperature()

        # Read data from BMP180 sensor
        temperature_bmp = bmp.temperature
        pressure = bmp.pressure

        # Read data from MQ135 gas sensor
        gas_level = adc.read()

        # Send data to Blynk server
        blynk.virtual_write(1, humidity)
        blynk.virtual_write(2, temperature_dht)
        blynk.virtual_write(3, temperature_bmp)
        blynk.virtual_write(4, pressure)

        if temperature_dht > TEMPERATURE_HIGH_THRESHOLD:
            # Raise an alert for high temperature
            blynk.notify("High Temperature Alert!")

        if temperature_dht < TEMPERATURE_LOW_THRESHOLD:
            # Raise an alert for low temperature
            blynk.notify("Low Temperature Alert!")

        if gas_level > threshold_value:
            # Raise an alert for high gas levels
            blynk.notify("High Gas Levels Detected!")

        time.sleep(600)  # Send data every 10 minutes
    except Exception as e:
        print("Error:", e)
        time.sleep(60)
