Menggunakan sebuah sensor ***selain sensor ultrasonic HC-SR04***, buatlah hal-hal berikut:

1. Wiring diagram untuk sensor tersebut menggunakan fritzing ( upload dalam MD files screenshot wiring diagram tersebut )

    (![Alt text](gambar/IoT_Hardware2.png?raw=true))

2. Script sensor.py dan sebuah fungsi untuk mengambil data dari sensor tersebut

    (from gpiozero import MCP3008, LED, Buzzer
    import time

    #konfigurasi LED dan buzzer

    buzzer = Buzzer(4)
    led_G = LED(6)
    led_R = LED(13)

    # Konfigurasi MCP3008
    WaterLevel = MCP3008(channel=0)  # Saluran ADC MCP3008 yang terhubung

    # Fungsi untuk mengukur ketinggian
    def measure_range():
    adc_value = WaterLevel.value  # Membaca nilai ADC dari MCP3008
    height_adc = adc_value * 10  # dikali 10 Faktor Skala

    return height_adc

    # Loop pengukuran ketinggian
    try:
        while True:
            range = measure_range()
            if range > 3.5:
            led_R.on()
            led_G.off()
            buzzer.on()
            time.sleep(0.1)
            print("WOY AIR MAU PENUH NICH!!!!")
            time.sleep(1)
            led_R.off()
            led_G.off()
        else :
            led_G.on()
            led_R.off()
            buzzer.off()
            time.sleep(1)
            led_G.off()
            print("Ketinggian Bak Saat Ini {:.2f}cm".format(range))
            time.sleep(1)
    except KeyboardInterrupt:
        pass)

3. Sebuah script utama [main.py](http://main.py) yang terdiri dari sebuah logic sederhana yang menjawab sebuah use case sederhana ( jelaskan use case tersebut dalam MD files! )

    (Disini saya akan menjelaskan pengukuran ketinggian bak kamar mandi menggunakan sensor WATER LEVEL

    Tujuan Utama yaitu : Memberitahu jika bak sudah terisi penuh dengan air

    usecase : Karena orang suka lupa mematikan kran air maka saya memberi solusi yaitu dengan membuat
    usecase ini
    
    Cara Kerja : Jika air melebihi batas yang ditentukan maka buzzer akan menyala dan memberi notif kepada
    orang yang lupa mematikan kran air)


4. (Optional) Ambil sekitar 5 - 10 sample data dan tampilkan dalam sebuah grafik matplotlib dan screenshot hasil tersebut dan upload pada MD files.

    (![Alt text](gambar/Matplotlib.jpg?raw=true))