import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import requests
import serial
import pynmea2
import math

# Konfigurasi Ubidots
UBIDOTS_TOKEN = "BBFF-03MEmiXujs99bPymSwqiVXcNo5t545"
DEVICE_LABEL = "raspberry-pi" 
VARIABLE_LABEL_1 = "water-level-device"
VARIABLE_LABEL_2 = "encoder-device"
VARIABLE_LABEL_3 = "position-device"
VARIABLE_LABEL_4 = "speed-device"

# Konfigurasi MCP3008
CLK = 11
MISO = 9
MOSI = 10
CS = 8
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Fungsi untuk membaca data dari MCP3008
def read_adc(channel):
    return mcp.read_adc(channel)

# Fungsi untuk menghitung RPM
def calculate_rpm(pulses, time_elapsed):
    return (pulses / 20) / (time_elapsed / 60)

def convert_to_liters(raw_value):
    # Implementasikan konversi berdasarkan kapasitas total tangki atau wadah Anda
    # Misalnya, jika Anda memiliki kapasitas total 1000 liter, Anda bisa menggunakan rumus:
    # liters = (raw_value / max_raw_value) * total_capacity
    # Di sini max_raw_value adalah nilai maksimal dari sensor dan total_capacity adalah kapasitas total dalam liter.
    
    max_raw_value = 1023  # Nilai maksimal dari sensor
    total_capacity = 30  # Kapasitas total tangki dalam liter  
    
    liters = (raw_value / max_raw_value) * total_capacity
    return liters   

# GPS serial port configuration
SERIAL_PORT = "/dev/ttyS0"
BAUDRATE = 9600

prev_latitude = None
prev_longitude = None
prev_time = None

def read_gps_coordinates():
    ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
    try:
        while True:
            raw_data = ser.readline().decode('utf-8')
            if raw_data.startswith('$GPGGA'):
                msg = pynmea2.parse(raw_data)
                latitude = msg.latitude
                longitude = msg.longitude
                return latitude, longitude
    except KeyboardInterrupt:
        ser.close()
        return None, None

def calculate_speed(curr_latitude, curr_longitude, curr_time):
    global prev_latitude, prev_longitude, prev_time

    if prev_latitude is None or prev_longitude is None or prev_time is None:
        prev_latitude = curr_latitude
        prev_longitude = curr_longitude
        prev_time = curr_time
        return 0.0

    time_diff = (curr_time - prev_time)
    distance = haversine(prev_latitude, prev_longitude, curr_latitude, curr_longitude)

    speed = distance / time_diff  # Speed in meters per second

    prev_latitude = curr_latitude
    prev_longitude = curr_longitude
    prev_time = curr_time

    return speed

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # Radius of the Earth in meters
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

def build_payload(water_level_convert_to_liter, rpm, latitude, longitude, speed):
    payload = {
        VARIABLE_LABEL_1:water_level_convert_to_liter,
        VARIABLE_LABEL_2: rpm,
        VARIABLE_LABEL_3:{"lat": latitude,"lng": longitude},
        VARIABLE_LABEL_4: speed}
    return payload

# Fungsi untuk mengirim data ke Ubidots
def post_request(payload):
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": UBIDOTS_TOKEN, "Content-Type": "application/json"}
    try:
        req = requests.post(url=url, headers=headers, json=payload)
        req.raise_for_status()
        print("[INFO] Data sent successfully")
    except requests.exceptions.RequestException as e:
        print("[ERROR] Failed to send data:", e)

try:
    while True:
        # Baca data dari sensor water level (Channel 0)
        water_level_value = read_adc(0)
        water_level_convert_to_liter = convert_to_liters(water_level_value)

        # Baca data dari sensor IR speed (Channel 1)
        ir_speed_value = read_adc(1)
        
        # Hitung RPM dari data IR speed (asumsi ada disk encoder dengan 20 lubang)
        start_time = time.time()
        start_ir_speed = ir_speed_value
        time.sleep(1)
        end_ir_speed = read_adc(1)
        end_time = time.time()
        
        ir_speed_change = end_ir_speed - start_ir_speed
        rpm = calculate_rpm(ir_speed_change, end_time - start_time)
        
        # Baca data dari GPS
        latitude, longitude = read_gps_coordinates()
        if latitude is not None and longitude is not None:
            curr_time = time.time()
            speed = calculate_speed(latitude, longitude, curr_time)
        else:
            speed = None
        
        # Kirim data ke Ubidots
        payload = build_payload(water_level_convert_to_liter, rpm, latitude, longitude, speed)
        post_request(payload)
        time.sleep(1)

except KeyboardInterrupt:
    print("Proses berhenti oleh pengguna.")
