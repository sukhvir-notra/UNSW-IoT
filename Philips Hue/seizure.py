import requests
import json
import time


# Change hue IP to ip address of your philips Hue 
hueIP = '129.94.5.95'
# Find this by capturing traffic between your app and the philips hue when in the same
# LAN. I recommend using tPacketCapture app for android users.
authentication = '000000007cf4a42fffffffffb82c643e'

r=requests.get('http://'+hueIP+'/api/'+authentication)
print(r.text)
sample = r.text

time.sleep(1)


# light control
url = 'http://'+hueIP+'/api/'+authentication+'/lights/1/state'


i=1

while i in range(1,20):
    
    data = {"bri":254,"ct":50,"on":True,"transitiontime":0}
    r=requests.put(url,json.dumps(data))

    r=requests.put(url,json.dumps({"on":False,"transitiontime":0}))
    time.sleep(0.15)
    
    i= i + 1
    print(sample),  
    


#print status of the lights
j = json.loads(sample)
light = j["lights"]["1"]
print "\n\n\n\n Current Status of the Lights\n-------------------------------\n\n"
print '"name":" %s"'%light["name"]
print '"state": '+json.dumps(light["state"],sort_keys=True,indent =4, separators=(",",": "))


#print the whitelist
k =  j["config"]["whitelist"]
print "\n\n\n\n Whitelist\n-----------\n\nwhitelist = " + json.dumps(k,sort_keys=True,indent =4, separators=(",",": ")) + '\n\n\n\n\n'


#for key,value in j.iteritems():
#    print key

data = {"bri":254,"hue":10000,"on":True,"transitiontime":0}
r=requests.put(url,json.dumps(data))
print sample,


data = {"bri":254,"hue":10000,"transitiontime":0}
r=requests.put(url,json.dumps(data))
print sample,
time.sleep(0.5)

data = {"bri":54,"hue":5000,"transitiontime":0}
r=requests.put(url,json.dumps(data))
print sample,
time.sleep(0.5)

data = {"bri":204,"hue":20000,"transitiontime":0}
r=requests.put(url,json.dumps(data))
print sample,
time.sleep(0.5)

data = {"bri":254,"ct":50,"transitiontime":0}
r=requests.put(url,json.dumps(data))
print sample,
time.sleep(0.5)

data = {"bri":254,"hue":50,"transitiontime":0}
r=requests.put(url,json.dumps(data))
print sample,
time.sleep(0.5)

data = {"bri":254,"hue":50000,"transitiontime":0}
r=requests.put(url,json.dumps(data))
print sample,
time.sleep(0.5)

data = {"bri":153,"hue":25654,"sat":253,"xy":[0.4083,0.5162],"ct":290,"colormode":"xy","transitiontime":0}
r=requests.put(url,json.dumps(data))
print sample,
time.sleep(0.5)

data = {"bri":254,"hue":65527,"sat":253,"xy":[0.6736,0.3221],"ct":500,"colormode":"xy","transitiontime":0}
r=requests.put(url,json.dumps(data))
print sample,
time.sleep(0.5)

r=requests.put(url,json.dumps({"on":False,"transitiontime":0}))

j = json.loads(sample)
light = j["lights"]["1"]
print "\n\n\n\n Current Status of the Lights\n-------------------------------\n\n"
print '"name":" %s"'%light["name"]
print '"state": '+json.dumps(light["state"],sort_keys=True,indent =4, separators=(",",": "))


#print the whitelist
k =  j["config"]["whitelist"]
print "\n\n\n\n Whitelist\n-----------\n\nwhitelist = " + json.dumps(k,sort_keys=True,indent =4, separators=(",",": ")) + '\n\n\n\n\n'

