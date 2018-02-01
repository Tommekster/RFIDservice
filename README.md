# RFIDservice

## Hardware
See https://github.com/ondryaso/pi-rc522.git

## Prerequisities
 - Enable SPI: 
	sudo raspi-config
	lsmod | grep spi

 - Install SPI library
	git clone https://github.com/lthiery/SPI-Py.git
	cd SPI-Py
	sudo python3 setup.py install

 - Install simple MFRCC522 python module
	git clone https://github.com/pimylifeup/MFRC522-python.git

