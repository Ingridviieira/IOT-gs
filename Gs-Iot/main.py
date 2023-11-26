import network
import time
from machine import Pin
from utime import sleep
import ujson
import random 
from umqtt.simple import MQTTClient

MQTT_CLIENT_ID = "micropython-weather-demo"
MQTT_BROKER    = "broker.mqttdashboard.com"
MQTT_USER      = ""
MQTT_PASSWORD  = ""
MQTT_TOPIC     = "gs-iot-eduarda"

botaocrianca_pin = 35  
botaoadulto_pin = 32  
buzzer_pin = 26  

estadobotaocrianca = 0  
estadobotaoadulto = 0

buzzer = Pin(buzzer_pin, Pin.OUT)
botaocrianca = Pin(botaocrianca_pin, Pin.IN)
botaoadulto = Pin(botaoadulto_pin, Pin.IN)

def setup():
    buzzer.off()

print("conectando ao wifi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
  print(".", end="")
  time.sleep(0.1)
print("Conectou")

print("COnectando ao servidor ", end="")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
client.connect()

print("Conectou")

def loop():
    estadobotaocrianca = botaocrianca.value()
    estadobotaoadulto = botaoadulto.value()

    estado = 0

    if estadobotaocrianca == 1 and estadobotaoadulto == 0:
        sleep(1)
        buzzer.on()
        estado = 1

    message = ujson.dumps({
    "estado": estado,
    })
    client.publish(MQTT_TOPIC,message)
    print(message)

setup()

while True:
    loop()