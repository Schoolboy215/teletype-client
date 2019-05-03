import requests
import json
import os.path
import pickle
import time
import subprocess
from PIL import Image
import io
from datetime import datetime
from dateutil import tz

import thermalPrinter
import config as serverConfig

printer = thermalPrinter.ThermalPrinter()

def mainLoop(config):
        s = requests.session()
        try:
                r = s.post(url=serverConfig.SERVER_URL+'/api/remote/checkIn', json={'callsign':config['callsign'],'code':config['code']}, timeout=5)
        except:
                if not 'timedOut' in config or config['timedOut'] == 0:
                        config['timedOut'] = 1
                config['timedOut'] += 1
                if config['timedOut'] == 4:
                        printer.write("Server could not be reached at " + serverConfig.SERVER_URL)
                        printer.feed(1)
                        pickle.dump(config, open('config.txt','wb'))
                return
        if 'timedOut' in config and config['timedOut'] != 0:
                config['timedOut'] = 0
                pickle.dump(config, open('config.txt','wb'))
        #print(r.text)
        data = json.loads(r.text)
        if data['status'] == 2:
                printer.write("The server doesn't know our callsign. Deleting local config and re-registering")
                printer.feed(1)
                os.remove('config.txt')
        else:
                if (len(data['data']['messages'])):
                        needToUpdate = False
                        for m in data['data']['messages']:
                                if m['type'] == 'UPDATE':
                                        needToUpdate = True

                                #This block translates the server's UTC timestamp to our local timezone
                                from_zone = tz.gettz('UTC')
                                to_zone = tz.tzlocal()
                                utc = datetime.strptime(m['timestamp'], '%Y-%m-%d %H:%M:%S')
                                utc = utc.replace(tzinfo=from_zone)
                                localTime = utc.astimezone(to_zone).strftime('%Y-%m-%d %H:%M:%S')

                                printer.write(localTime+"\nFrom:"+m['from']+"\nTo  :"+m['to'])
                                printer.thickBar()
                                if m['body'] != "":
                                        printer.write(m['body'])
                                printer.feed(1)
                                if 'imageData' in m:
                                        b = bytearray()
                                        b.extend(m['imageData']['data'])
                                        if len(b):
                                                image = Image.open(io.BytesIO(b))
                                                printer.printImage(image)
                                                printer.feed(1)
                        if needToUpdate:
                                printer.write("GOING TO UPDATE NOW")
                                printer.feed(1)
                                subprocess.call("sudo bash ./update.sh", shell=True)
                                printer.write(subprocess.check_output(['git','log','-1']))

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
                printer.feed(1)
                print(r.text)
                mainLoop(data)
        except:
                printer.write("Server could not be reached at " + serverConfig.SERVER_URL)
                printer.feed(1)
