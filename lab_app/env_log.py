#!/usr/bin/env python


import sqlite3
import sys
import Adafruit_DHT

#wstawianie odczytanych danych z czujnika do bazy danych - plik używany przez CRONa w celu cyklizacji procesu
def log_values(sensor_id, temp, hum):
	conn=sqlite3.connect('/var/www/lab_app/lab_app.db')  # połączenie z bazą
	curs=conn.cursor()
	curs.execute("""INSERT INTO temperatures values(datetime(CURRENT_TIMESTAMP, 'localtime'),
         (?), (?))""", (sensor_id,temp)) # wstawianie odczytanych wartości do bazy
	curs.execute("""INSERT INTO humidities values(datetime(CURRENT_TIMESTAMP, 'localtime'),
         (?), (?))""", (sensor_id,hum))
	conn.commit()
	conn.close()

humidity, temperature = Adafruit_DHT.read_retry(11, 17) #odczyt z czujnika

if humidity is not None and temperature is not None:
	log_values("1", temperature, humidity)	
else:
    	log_values("1", 0, 0) # jeśli brak czujnika, wstawiamy 0 jako wartość wilgotności i temperatury
