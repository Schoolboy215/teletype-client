import requests
import json
import os.path
import pickle
import time

import thermalPrinter

printer = thermalPrinter.ThermalPrinter()

def mainLoop(config):
        s = requests.session()
        while True:
                r = s.post(url='https://teleType.personalspaceshow.lawyer/api/remote/checkIn', json={'callsign':config['callsign'],'code':config['code']})
                print(r.text)
                data = json.loads(r.text)
                if (len(data['data']['messages'])):
                        for m in data['data']['messages']:
                                printer.write(m['timestamp']+"\nFrom:"+m['from']+"\nTo  :"+m['to'])
                                printer.thickBar()
                                printer.write(m['body'])
                                printer.feed(3)
                time.sleep(30)

time.sleep(15)

if os.path.isfile('config.txt'):
        config = pickle.load(open('config.txt','rb'))
        mainLoop(config)
        #s = requests.session()
        #r = s.post(url='https://teleType.personalspaceshow.lawyer/api/remote/checkIn', json={'callsign':config['callsign'],'code':config['code']})
        #print(r.text)
        #data = json.loads(r.text)
        #if (len(data['data']['messages'])):
        #       for m in data['data']['messages']:
        #               printer.write(m['body'])
        #               printer.feed(3)

else:
        r = requests.get('https://teletype.personalspaceshow.lawyer/api/remote/firstContact')
        data = json.loads(r.text)
        config = data
        pickle.dump(data, open('config.txt','wb'))
        print('Got a response from the server and saved it')
        printer.welcome()
        printer.write("\nYour callsign is\n" + data['callsign'])
        printer.feed(3)
        print(r.text)
        mainLoop(data)
