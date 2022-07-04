# lab_app
Aplikacja pozyskująca informacje pogodowe z czujnika DHT11 i przedstawiająca je na wykresie - aplikacja webowa

Do stworzenia aplikacji w celu poszerzenia wiedzy z zajęć na dane tematy, starałam sie wybierać nowe usługi realizujące tematy omawiane na zajęciach takie jak aplikacja webowa, baza danych, Python, crontab. Projekt ukazuje jak wiele ciekawych usług można stworzyć na niewielkim dostępnym sprzęcie jakim jest DHT11. Korzystając jedynie z tego czujnika oraz wielu usług dostepnych dla raspberry PI, powstała kompletna fukcjonalna aplikacja pozwalająca monitorować naszą życiową przestrzeń poprzez stronę internetową.

## Schemat układu:

![](images/schemat%20układu.png)

## Stos aplikacyjny :

1.Framework aplikacji - wykorzystano **Flask** - mikro framework aplikacji webowych napisany w języku Python

2.Serwer aplikacyjny - wykorzystano **uWSGI** - serwer aplikacyjny

3.Serwer webowy (www) - wykorzystano **nginx** - serwer WWW oraz serwer proxy dla HTTP i IMAP/POP3

Dodatkowo stworzono **wirtualne środowisko Python**

Rysunek poglądowy stosu aplikacyjnego:

![](images/Stos_aplikacyjny.png)

Baza danych: **SQLite3**

Style i frontend : **jQuery, HTML, CSS, Skeleton**

Automatyzacja procesu : **CRON** (crontab -e)

Wykresy i widgety: **Google Charts, Datetime widgets**

Dodatkowe aplikacje: **Plotly** 

## Wymagane instalacje : 

Python3: 
```
sudo apt-get install python3-pip
```
rpi.gpio: 
```
pip3 install rpi.gpio
```

Instalacja GIT i biblioteki DHT do obsługi czujnika:

GIT: 
```
sudo apt-get install git-core
```
DHT klonowanie repozytorium: 
```
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
```
następnie wchodzimy do utworzonego przez klonowanie projektu 
```
cd Adafruit_Python_DHT
```
i dokonujemy instalacji pythona wewnątrz 
```
sudo python3 setup.py install
```
### Wirtualne środowisko Python

Wirtualne środowisko Pythona pozwala nam na brak konfliktów pomiędzy zainstalowanymi modułami i pakietami.

Poglądowy rysunek ukazujący różnicę pomiędzy wirtualnym środowiskiem Pythona a jego brakiem:

![](images/wirtualne_środowisko_python.png)

#### Instalacja

build-essential:
```
sudo apt-get install build-essential
```
```
sudo apt-get install libncurses5-dev libncursesw5-dev libreadline6-dev libffi-dev 
```
```
sudo apt-get install libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libsqlite3-dev libgdbm-dev tk8.5-dev libssl-dev openssl
```
```
sudo apt-get install libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libsqlite3-dev libgdbm-dev tk8.5-dev libssl-dev openssl
```
```
sudo apt-get install libpulse-dev
```
python development:
```
sudo apt-get install libboost-python-dev
```
```
sudo apt-get install python-dev
```
Instalacja edytora tekstu vim:
```
sudo apt-get install vim
```

Stworzenie folderu projektowego pod wirtualne środowisko w katalogu var/:
```
mkdir /var/www
mkdir /var/www/lab_app/
cd /var/www/lab_app/
```
Instalacja wirtualnego środowiska w folderze lab_app (ściezka do pythona -m venv .):
```
/usr/bin/python-3.7 -m venv .
```
Nastepnie logujemy sie na roota komendą 
```
sudo su
```
**Ważna komenda do aktywacji środowiska:**
```
. bin/activate
```
Po tej komendzie na początku terminala powinna pojawić się nazwa wirutalnego środowiska (lab_app) - wszystkie instalacje pakietów będą instalowane z tego wirtualnego środowiska

Dezaktywacja środowiska wirtualnego nastepuje przez komendę
```
deactivate
```

### Instalacja serwera www (nginx) oraz frameworka aplikacji (Flask)
Wejść w wirtualne środowisko przechodząc do folderu lab_app i wprowadzając komendę
```
. bin/activate
```
Komenda instalacyjna serwera:
```
apt-get install nginx
```
Usunięcie obecnej konfiguracji nginx i ustawienie nowej konfiguracji z symbolic linkiem
```
rm /etc/nginx/sites-enabled
```

Komenda instalacyjna frameworka Flask:
```
pip install flask
```
### Instalacja serwera aplikacyjnego (uWSGI) 
Wejść w wirtualne środowisko przechodząc do folderu lab_app i wprowadzając komendę
```
. bin/activate
```
Komenda instalacyjna serwera:
```
pip install uwsgi
```
