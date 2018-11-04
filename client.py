import requests
import json
import os.path
import pickle
import time
import subprocess
from PIL import Image
import io

import thermalPrinter
import config as serverConfig

printer = thermalPrinter.ThermalPrinter()

def mainLoop(config):
        s = requests.session()
        try:
                r = s.post(url=serverConfig.SERVER_URL+'/api/remote/checkIn', json={'callsign':config['callsign'],'code':config['code']}, timeout=5)
        except:
                if not 'timedOut' in config or config['timedOut'] == False:
                        printer.write("Server could not be reached at " + serverConfig.SERVER_URL)
                        printer.feed(3)
                        config['timedOut'] = True
                        pickle.dump(config, open('config.txt','wb'))
                return
        if 'timedOut' in config and config['timedOut'] == True:
                config['timedOut'] = False
                pickle.dump(config, open('config.txt','wb'))
        #print(r.text)
        data = json.loads(r.text)
        if data['status'] == 2:
                printer.write("The server doesn't know our callsign. Deleting local config and re-registering")
                printer.feed(3)
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
                                if 'imageData' in m:
                                        b = bytearray()
                                        b.extend(m['imageData']['data'])
                                        image = Image.open(io.BytesIO(b))
                                        printer.printImage(image)
                                        printer.feed(3)
                        if needToUpdate:
                                printer.write("GOING TO UPDATE NOW")
                                printer.feed(3)
                                subprocess.call("sudo bash ./update.sh", shell=True)

if os.path.isfile('config.txt'):
        config = pickle.load(open('config.txt','rb'))
        mainLoop(config)
else:
        try:
                r = requests.get(serverConfig.SERVER_URL+'/api/remote/firstContact', timeout=5)
                data = json.loads(r.text)
                config = data
                pickle.dump(data, open('config.txt','wb'))
                print('Got a response from the server and saved it')
                printer.welcome()
                printer.write("\nYour callsign is\n" + data['callsign'])
                printer.feed(3)
                print(r.text)
                mainLoop(data)
        except:
                printer.write("Server could not be reached at " + serverConfig.SERVER_URL)
                printer.feed(3)
