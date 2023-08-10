import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt

# Konfigurasi GPIO untuk sensor ultrasonik
TRIG = 23
ECHO = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Konfigurasi MQTT
mqtt_broker = "broker.hivemq.com"  # Ganti dengan alamat broker HiveMQ
mqtt_topic = "sic/tothreetwo/232/ultrasonic"


def ultrasonic_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.01)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_broker, 1883, 60)

try:
    while True:
        distance = ultrasonic_distance()
        print("Distance:", distance, "cm")
        client.publish(mqtt_topic, str(distance))
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()