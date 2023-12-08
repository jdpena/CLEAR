# Makefile

# Define shell
SHELL := /bin/bash

# Define the python command.
PYTHON := python

# Define the main script file.
MAIN_SCRIPT := main.py

# Define the server address.
WORKER_SERVER_ADDRESS := http://ait-dev-03:9090
INTERFACE_SERVER_ADDRESS := https://ait-dev-03:7070
ONLINE_INTERFACE_ADDRESS := https://autodroneinterface.azurewebsites.net
ROBOT_PLATFORM := SpotDrone

.PHONY: setup
setup:
	@echo "Setting up the environment..."
	http_proxy=http://llproxy.llan.ll.mit.edu:8080
	ftp_proxy=http://llproxy.llan.ll.mit.edu:8080
	HTTPS_PROXY=http://llproxy.llan.ll.mit.edu:8080
	HTTP_PROXY=http://llproxy.llan.ll.mit.edu:8080
	FTP_PROXY=http://llproxy.llan.ll.mit.edu:8080
	no_proxy=.ll.mit.edu,.mit.edu,localhost,127.0.0.1,172.25.207.73,172.25.207.215,192.168.80.3,ait-dev-03
	
	export https_proxy
	export http_proxy
	export ftp_proxy
	export HTTPS_PROXY
	export HTTP_PROXY
	export FTP_PROXY
	export no_proxy


.PHONY: runll
runll:
	@echo "Running the main script..."
	$(PYTHON) $(MAIN_SCRIPT) --worker_address $(WORKER_SERVER_ADDRESS) --interface_address $(INTERFACE_SERVER_ADDRESS) --platform UnityDrone

.PHONY: runspot
runspot:
	@echo "Running the main script..."
	$(PYTHON) $(MAIN_SCRIPT) --worker_address $(WORKER_SERVER_ADDRESS) --interface_address $(INTERFACE_SERVER_ADDRESS) --platform $(ROBOT_PLATFORM)

.PHONY: rununity
rununity:
	@echo "Running the main script..."
	$(PYTHON) $(MAIN_SCRIPT) --worker_address=$(SERVER_ADDRESS) --interface_address=$(ONLINE_INTERFACE_ADDRESS)


.PHONY: testInterface
testInterface:
	@echo "Running the main script..."
	$(PYTHON) $(MAIN_SCRIPT) --worker_address=$(SERVER_ADDRESS) --interface_address=https://localhost:7070 --platform UnityDrone --manual_control True

.PHONY: rununitySetup
rununitySetup:
	@echo "setting the environment"
	http_proxy=http://llproxy.llan.ll.mit.edu:8080
	ftp_proxy=http://llproxy.llan.ll.mit.edu:8080
	HTTPS_PROXY=http://llproxy.llan.ll.mit.edu:8080
	HTTP_PROXY=http://llproxy.llan.ll.mit.edu:8080
	FTP_PROXY=http://llproxy.llan.ll.mit.edu:8080
	no_proxy=.ll.mit.edu,.mit.edu,localhost,127.0.0.1,172.25.207.73,ait-dev-03
	
	export https_proxy
	export http_proxy
	export ftp_proxy
	export HTTPS_PROXY
	export HTTP_PROXY
	export FTP_PROXY
	export no_proxy

.PHONY: runlocal
runlocal: 
	@echo "Running Locally"
	$(PYTHON) $(MAIN_SCRIPT) --worker_address=http://localhost:9090 --interface_address=https://localhost:7070 --platform UnityDrone