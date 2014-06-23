wemoCode
========

SSDP discovery code:
-------------------

ssdp.py conducts a ssdp discovery by broadcasting ssdp discovery packet. It then listens for replies from ssdp enabled clients on the LAN.

To halt the discovery and listening press ctrl+c (Keyboard Interrupt).

This code will then display a list of devices that were discovered


wemoCtrl.py:
---------
This code is for controlling WEMO switch. Change the 'host' and 'port' variable to your wemo IP and port respectively. (This can be found by running ssdp.py in your LAN)

