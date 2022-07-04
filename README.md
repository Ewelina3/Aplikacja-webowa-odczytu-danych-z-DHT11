# lab_app
Aplikacja pozyskująca informacje pogodowe z czujnika DHT11 i przedstawiająca je na wykresie - aplikacja webowa

Schemat układu:

![](images/schemat%20układu.png)

Stos aplikacyjny:

![](images/Stos_aplikacyjny.png)

Wymagane instalacje : 

Python3: "sudo apt-get install python3-pip"

rpi.gpio: "pip3 install rpi.gpio"

Instalacja GIT i biblioteki DHT do obsługi czujnika:

GIT: "sudo apt-get install git-core"
DHT klonowanie repozytorium: "git clone https://github.com/adafruit/Adafruit_Python_DHT.git" następnie wchodzimy do utworzonego przez klonowanie projektu "cd Adafruit_Python_DHT" i dokonujemy instalacji pythona wewnątrz "sudo python3 setup.py install
