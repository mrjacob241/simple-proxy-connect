# simple-proxy-connect
Simple Proxy Connect  
⚠️ **Work in progress!** ⚠️

# Simple Python HTTPS Proxy (method CONNECT ✅)

This simple (but fully working) plain Python proxy can navigate in all the modern HTTPS sites like: Google, Facebook, Twitter, Youtube, etc.

## Usage

* Run one of the following lines of code:
```
python proxy_connect_working.py
```
```
python proxy_log.py --log_file="logs/logs.txt"
```
```
python proxy_log.py --log_file="logs/logs.txt" --detail="packets"
```
```
python proxy_log.py --log_file="logs/logs.txt" --detail="packets" --analysis="traffic"
```

* Setup your browser/OS proxy settings to listen on adrress *127.0.0.1* and port *8000* 

* Start to navigate! (All your traffic will be visible on Python console)

## Acknowledgments

This project is based on:
* [MinimalPythonProxy](https://github.com/mrprofessor/MinimalPythonProxy)
* [HTTPS CONNECT integration](https://stackoverflow.com/questions/24218058/python-https-proxy-tunnelling)
