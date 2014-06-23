import sys,os
from socket import *
import struct
import requests
import xmltodict
import json

WEMO_SWITCH=[]
WEMO_SENSOR=[]
MCAST_GRP = '239.255.255.250'
MCAST_PORT = 1900

######################### SSDP DISCOVERY #############################

#Creating the SSDP request packet
#---------------------------------
headers = 	"""MX:2\r\nMAN:"ssdp:discover"\r\n\r\n"""
request = """M-SEARCH * HTTP/1.1\r\nHOST:239.255.255.250:1900\r\nST:upnp:rootdevice\r\n"""
soapRequest = request + ('%s' % headers)
print soapRequest

# Create the reusable socket
#---------------------------
try:
	sock = socket(AF_INET,SOCK_DGRAM,IPPROTO_UDP)
	sock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
	sock.bind((gethostbyname(gethostname()),1900))
except:
	print  'could not create sock'
# Send Discovery packets 
#------------------------
try:
	sock.sendto(soapRequest,(MCAST_GRP,MCAST_PORT))	
except Exception, e:
	print "SendTo method failed : %s"%e
# Receive SSDP replies
#---------------------
replies = []
try:
	while True:
		rep = sock.recv(10000)
		print rep,'\n'
		d = dict(item.split(":", 1) for item in rep.splitlines() if ":" in item)
		replies.append(dict((k.lower(), v) for k, v in d.iteritems()))
except KeyboardInterrupt:
	print 'bye'

############################ SSDP END ###############################

######################## PROCESS REPLIES ############################
Locations = []

for i,item in enumerate(replies):
	instances=replies[i]['location']

	
	if instances[0]==' ':
		instances = ''.join(instances[1:])


	# check = list(instances)

	# if check[0]==' ':
	# 	instances = ''.join(check[1:])

	if instances in Locations:
		pass
	else:
		Locations.append(instances)
print Locations

for item in Locations:
	try:
		r = requests.get("%s"%item)
		reply = xmltodict.parse(r.text)
		if reply['root']['device']['friendlyName']=="WeMo Switch":
			WEMO_SWITCH.append(item)
		elif reply['root']['device']['friendlyName']=="WeMo Motion":
			WEMO_SENSOR.append(item)	
	except Exception,e:
		print e
		pass
print '\n\n################################################################\nWemo switch is located at : %s'%WEMO_SWITCH
print 'Wemo Motion is located at : %s\n################################################################\n'%WEMO_SENSOR

device_dict={}

for item in Locations:
	try:
		r = requests.get("%s"%item)
		reply = xmltodict.parse(r.text)
		device_dict[reply['root']['device']['friendlyName']]=item
	except Exception,e:
		print e
		pass

print '\n\nDevices in the Network:\n\n',json.dumps(device_dict,indent=4)

