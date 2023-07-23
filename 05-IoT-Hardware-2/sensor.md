    (from gpiozero import MCP3008, LED, Buzzer
    import time

    #konfigurasi LED dan buzzer

    buzzer = Buzzer(4)
    led_G = LED(6)
    led_R = LED(13)

    #Konfigurasi MCP3008
    WaterLevel = MCP3008(channel=0)  # Saluran ADC MCP3008 yang terhubung

    #Fungsi untuk mengukur ketinggian
    def measure_range():
    adc_value = WaterLevel.value  # Membaca nilai ADC dari MCP3008
    height_adc = adc_value * 10  # dikali 10 Faktor Skala

    return height_adc

    #Loop pengukuran ketinggian
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
