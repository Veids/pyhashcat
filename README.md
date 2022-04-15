# pyhashcat

Python C API binding to libhashcat, originally written by @Rich5, updated by @initiate6 and upgraded by @f0cker:
- https://github.com/Rich5/pyhashcat
- https://github.com/initiate6/pyhashcat
- https://github.com/f0cker/pyhashcat

This is a working directory for an attempt to port/fix from Python 3.7 and hashcat 6.1.x to Python 3.8+ and hashcat 6.2.5+. 

Requirements: 
* hashcat 6.2.5
* Python 3.8+

### Install libhashcat and pyhashcat:

```
git https://github.com/securechicken/pyhashcat
cd pyhashcat/pyhashcat
git clone https://github.com/hashcat/hashcat.git
cd hashcat/
sudo make install_library
sudo make install
cd ..
python setup.py build_ext -R /usr/local/lib
sudo python setup.py install
```

### Simple Test:

```
user@host:~/pyHashcat/pyhashcat$ python simple_mask.py
-------------------------------
---- Simple pyhashcat Test ----
-------------------------------
[+] Running hashcat
STATUS:  Cracked
8743b52063cd84097a65d1633f5c74f5  -->  hashcat
```

### Help:

```
import pyhashcat
help(pyhashcat)
```
