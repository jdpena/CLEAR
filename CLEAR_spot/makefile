# Makefile

# Define shell
SHELL := /bin/bash

# Define the python command.
PYTHON := python

# Define the main script file.
MAIN_SCRIPT := main.py

# Define the server address.
SERVER_ADDRESS := http://172.25.207.73:7070
SPOT_ADDRESS := 192.168.80.3

.PHONY: setup
setup:
	@echo "Setting up the environment..."
	# Put your setup commands here. For instance:
	# pip install -r requirements.txt
	http_proxy=http://llproxy.llan.ll.mit.edu:8080
	ftp_proxy=http://llproxy.llan.ll.mit.edu:8080
	HTTPS_PROXY=http://llproxy.llan.ll.mit.edu:8080
	HTTP_PROXY=http://llproxy.llan.ll.mit.edu:8080
	FTP_PROXY=http://llproxy.llan.ll.mit.edu:8080
	no_proxy=.ll.mit.edu,.mit.edu,localhost,127.0.0.1,172.25.207.73,172.25.207.215,192.168.80.3,172.27.237.206,172.27.237.206,10.0.0.3
	export https_proxy
	export http_proxy
	export ftp_proxy
	export HTTPS_PROXY
	export HTTP_PROXY
	export FTP_PROXY
	export no_proxy

.PHONY: connectToWifi
connectToWifi:
	sudo nmcli dev wifi connect spot-BD-21910001 password 8wiq3jhe0ae5

.PHONY: run
run:
	@echo "Running the main script..."
	$(PYTHON) $(MAIN_SCRIPT) --serverAddress=$(SERVER_ADDRESS) --spotAddress=$(SPOT_ADDRESS)
