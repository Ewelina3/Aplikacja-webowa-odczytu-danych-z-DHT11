'''
Aplikcja webowa oparta o flask dostępna w przeglądarce użytkownika.
Pierwsza strona aplikacji zawiera obecną temperature i wilgotność pozyskaną z czujnika DHT11. Odswieża się automatycznie co 10 sekund powodując załadowanie aktualnych odczytów na stronę.
Druga strona zawiera archiwum odczytów temperatury i wilgotności, elementy umożliwiające filtrowanie po danach poprzednich odczytów oraz wykresy ukazujące zmiany w czasie danych wartości.
Druga strona zawiera również możliwość importu diagramu do Plotly. Dane prezentowane na tej stronie przechowywane są w bazie SQLite3.
Specyficzne warunki filtrowania po datach są przekazywane przez adres URL.
Użytkownik moze kliknąć w guziki wyboru danych z danego okresu by wybrać odpowiedni zakres danych.
Użytkownik może skorzystać z Jquery Datepickera w celu wybrania interesującego go zakresu danych.
W Plotly użytkownik ma możliwość dalszej konfiguracji diagramu według własnych potrzeb.
'''

from flask import Flask, request, render_template
import time
import datetime
import arrow
import sys
import Adafruit_DHT
import sqlite3
import chart_studio.plotly as py
from plotly.graph_objs import *

app = Flask(__name__)
app.debug = True # ustawienie aplikacji na debbugowanie - False jeśli nie chcemy debuggować

@app.route("/") # ścieżka podstawowa wyświetlająca obecne odczyty sensorów lub informację o braku sensoru
def hello():
    humidity, temperature = Adafruit_DHT.read_retry(11, 17) # odczytanie temperatur z czujnika
    if humidity is not None and temperature is not None:
        return render_template("lab_temp.html",temp=temperature,hum=humidity)
    else:
        return render_template("no_sensor.html")

@app.route("/lab_temp") # ścieżka identyczna jak startowa, prowadzi do tego samego widoku
def lab_temp():
    humidity, temperature = Adafruit_DHT.read_retry(11, 17) # odczytanie temperatur z czujnika
    if humidity is not None and temperature is not None:
        return render_template("lab_temp.html",temp=temperature,hum=humidity)
    else:
        return render_template("no_sensor.html")

@app.route("/lab_env_db", methods=['GET'])  # Dodanie wartości sortowania do linku URL #Argumenty np: from=2015-03-04&to=2015-03-05
def lab_env_db():
    temperatures, humidities, from_date_str, to_date_str = get_records() # wywołanie fukcji get_records() pobierającej dane z bazy

    print ("rendering lab_env_db.html with: %s, %s" % (from_date_str, to_date_str)) # wypisywanie w celu łatwiejszego debuggowania

    # poniżej zwracany widok z pozyskanymi wartościami z bazy
    return render_template("lab_env_db.html",   temp            = temperatures,
                                                hum             = humidities,
                                                from_date       = from_date_str,
                                                to_date         = to_date_str,
                                                temp_items      = len(temperatures),
                                                query_string    = request.query_string[0:len(request.query_string)], #To zapytanie tekstowe używane jest przez Plotly
                                                hum_items       = len(humidities)) 

def get_records():
    from_date_str 	= request.args.get('from',time.strftime("%Y-%m-%d 00:00")) #Pozyskanie Daty od ze ścieżki URL
    to_date_str 	= request.args.get('to',time.strftime("%Y-%m-%d %H:%M"))   #Pozyskanie Daty do ze ścieżki URl
    range_h_form	= request.args.get('range_h','');  #Zwróci wartość typu string jeśli pole range_h istnieje w odpowiedzi
    range_h_int 	= "brak"  #zmienna pomocnicza przechowująca zrzutowany integer, na początku jest tekstem, jeśli się nie uda zrzutować będzie zweryfikowana jako błąd

    print ("REQUEST:") # wypiwanie by ułatwić debugowanie
    print (request.args)
    print ("from: %s, to: %s" % (from_date_str, to_date_str))

    # próba rzutowania wyboru okresu na typ liczbowy int
    try:
        range_h_int	= int(range_h_form)
    except:
        print ("range_h_form nie jest numerem") # W przypadku nieudanego rzutowania wysyłamy komunikat o tym informujący


    print ("Received from browser: %s, %s, %s" % (from_date_str, to_date_str, range_h_int))

    if not validate_date(from_date_str):			# Walidowanie daty przed wysłaniem zapytania do bazy danych
        from_date_str 	= time.strftime("%Y-%m-%d 00:00")
    if not validate_date(to_date_str):
        to_date_str 	= time.strftime("%Y-%m-%d %H:%M")		# Walidowanie daty przed wysłaniem zapytania do bazy danych
    print ('2. From: %s, to: %s' % (from_date_str,to_date_str))

    from_date_obj       = datetime.datetime.strptime(from_date_str,'%Y-%m-%d %H:%M')
    to_date_obj         = datetime.datetime.strptime(to_date_str,'%Y-%m-%d %H:%M')

    # Jeśli wartość range_h jest zdefniowana (jest int) to nie potrzebujemy dat od i do
    if isinstance(range_h_int,int):
        time_now     = datetime.datetime.now()
        time_to      = time_now   
        time_from    = time_now - datetime.timedelta(hours = range_h_int)
        from_date_str   = time_from.strftime("%Y-%m-%d %H:%M")
        to_date_str     = time_to.strftime("%Y-%m-%d %H:%M")

    conn = sqlite3.connect('/var/www/lab_app/lab_app.db') # połaczenie z bazą danych
    curs = conn.cursor()
    curs.execute("SELECT * FROM temperatures WHERE rDateTime BETWEEN ? AND ?", (from_date_str, to_date_str)) # pozyskanie temperatur z danych okresów
    temperatures = curs.fetchall()
    curs.execute("SELECT * FROM humidities WHERE rDateTime BETWEEN ? AND ?", (from_date_str, to_date_str)) # pozyskanie wilgotności z danych okresów
    humidities = curs.fetchall()
    conn.close()

    return [temperatures, humidities, from_date_str, to_date_str]

@app.route("/to_plotly", methods=['GET'])  # Fukcja pozyskująca dane i tworząca wykres w Plotly
def to_plotly():
	temperatures, humidities, from_date_str, to_date_str = get_records() # pozyskanie rekordów z bazy

	time_series_adjusted_temperatures   = []
	time_series_adjusted_humidities 	= []
	time_series_temperature_values 	    = []
	time_series_humidity_values 		= []

	for record in temperatures:
		local_timedate = arrow.get(record[0], "YYYY-MM-DD HH:mm:ss")
		time_series_adjusted_temperatures.append(local_timedate.format('YYYY-MM-DD HH:mm:ss')) #Najlepiej przekazywac do Plotly datetime jako text 
		time_series_temperature_values.append(round(record[2],2))

	for record in humidities:
		local_timedate = arrow.get(record[0], "YYYY-MM-DD HH:mm:ss")
		time_series_adjusted_humidities.append(local_timedate.format('YYYY-MM-DD HH:mm:ss')) 
		time_series_humidity_values.append(round(record[2],2))

	temp = Scatter(
        		x     = time_series_adjusted_temperatures,
        		y     = time_series_temperature_values,
        		name  = 'Temperatura'
    				)
	hum = Scatter(
        		x     = time_series_adjusted_humidities,
        		y     = time_series_humidity_values,
        		name  = 'Wilgotność',
        		yaxis = 'y2'
    				)

	data = Data([temp, hum])

	layout = Layout(
					title  = "Temperatura i wilgotność w pomieszczeniu",
				    xaxis  = XAxis(
				        type      = 'date',
				        autorange = True
				    ),
				    yaxis          = YAxis(
				    	title      = 'Stopnie Celciusza',
				        type       = 'linear',
				        autorange  = True
				    ),
				    yaxis2 = YAxis(
				    	title      = 'Procenty',
				        type       = 'linear',
				        autorange  = True,
				        overlaying = 'y',
				        side       = 'right'
				    )

					)
	fig      = Figure(data = data, layout = layout)
	plot_url = py.plot(fig, filename = 'lab_temperatura_wilgotnosc')

	return plot_url

# walidacja poprawności daty
def validate_date(d):  
    try:
        datetime.datetime.strptime(d, '%Y-%m-%d %H:%M')
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
