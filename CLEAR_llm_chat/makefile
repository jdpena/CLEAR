# Makefile

# Define shell
SHELL := /bin/bash

# Define the python command.
PYTHON := python

# Define the main script file.
MAIN_SCRIPT := main.py

# Define the server address.
SERVER_ADDRESS := http://ait-dev-03:9090

.PHONY: setup
setup:
	@echo "Setting up the environment..."
	http_proxy=http://llproxy.llan.ll.mit.edu:8080
	ftp_proxy=http://llproxy.llan.ll.mit.edu:8080
	HTTPS_PROXY=http://llproxy.llan.ll.mit.edu:8080
	HTTP_PROXY=http://llproxy.llan.ll.mit.edu:8080
	FTP_PROXY=http://llproxy.llan.ll.mit.edu:8080
	no_proxy=.ll.mit.edu,.mit.edu,localhost,127.0.0.1,172.25.207.73,ait-dgx-01,ait-dev-03
	export https_proxy
	export http_proxy
	export ftp_proxy
	export HTTPS_PROXY
	export HTTP_PROXY
	export FTP_PROXY
	export no_proxy

.PHONY: run
run:
	@echo "Running the main script..."
	$(PYTHON) $(MAIN_SCRIPT) --address $(SERVER_ADDRESS)
