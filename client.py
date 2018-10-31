import requests
import json
import os.path
import pickle
import time

import thermalPrinter
import config as serverConfig

printer = thermalPrinter.ThermalPrinter()

def mainLoop(config):
        s = requests.session()
        try:
                r = s.post(url=serverConfig.SERVER_URL+'/api/remote/checkIn', json={'callsign':config['callsign'],'code':config['code']})
        except:
                printer.write("Server could not be reached at " + serverConfig.SERVER_URL)
                return
        print(r.text)
        data = json.loads(r.text)
        if data['status'] == 2:
                printer.write("The server doesn't know our callsign. Deleting local config and re-registering")
                os.remove('config.txt')
        else:
                if (len(data['data']['messages'])):
                        needToUpdate = False
                        for m in data['data']['messages']:
                                if m['type'] == 'UPDATE':
                                        needToUpdate = True
                                printer.write(m['timestamp']+"\nFrom:"+m['from']+"\nTo  :"+m['to'])
                                printer.thickBar()
                                printer.write(m['body'])
                                printer.feed(3)
                        if needToUpdate:
                                printer.write("GOING TO UPDATE NOW")

if os.path.isfile('config.txt'):
        config = pickle.load(open('config.txt','rb'))
        mainLoop(config)
else:
        r = requests.get(serverConfig.SERVER_URL+'/api/remote/firstContact')
        data = json.loads(r.text)
        config = data
        pickle.dump(data, open('config.txt','wb'))
        print('Got a response from the server and saved it')
        printer.welcome()
        printer.write("\nYour callsign is\n" + data['callsign'])
        printer.feed(3)
        print(r.text)
        mainLoop(data)