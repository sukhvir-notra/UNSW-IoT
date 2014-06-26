import requests
import easygui

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
my_device_list = ['Philips Lighting BV','Nest Labs Inc.','Belkin International Inc.','Wemo Switch']

actions = {'Philips Lighting BV':{"firewall":"Enabled","allow":['129.94.5.87','162.13.15.30'],"direction":"Inbound",'device':"Philips Lighting BV"},
			'Nest Labs Inc.':{"firewall":"Enabled",'allow':['174.129.5.148','50.19.134.217','23.23.239.159'],'direction':"Outbound",'device':'NestLabs Inc.'}, 'Belkin International Inc.':{"firewall":"Enabled",'allow':['129.94.5.87','54.197.246.206','184.73.108.98'],'direction':"Inbound",'device':'Belkin International Inc.'}}

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
user_input = raw_input('\nenter MAC address(you may just enter the first 6 characters): ')

r=requests.get('http://api.macvendors.com/'+user_input) 
print '\n\n',r.text,'\n\n' 
response = r.text.encode('ascii','ignore')

if response in my_device_list: 
    print 'I have info for ',response,':\n' 
    print actions[response],'\n'
    
    easygui.msgbox(msg='firewall = '+str(actions[response]['firewall'])+'\nallow = '+str(actions[response]['allow'])+'\ndirection = '+str(actions[response]['direction'])+'\ndevice = '+str(actions[response]['device']))
 
else: 
    print "I currently don't have any info on this device\n"
    easygui.msgbox(msg='Device = '+response+'\n\nFirewall = N\A'+'\n\nExceptions = N\A'+'\n\nAlert = N\A')