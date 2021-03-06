from crontab import CronTab
import os

cwd = os.getcwd()

SERVER_URL = ""
REPO_URL = "https://github.com/Schoolboy215/teletype-client"

print("Enter the full address of the server you'd like to connect to.")
userInput = raw_input()
if userInput:
    SERVER_URL = userInput
else:
    quit()

print("Enter the url of the repository to pull updates from")
print("(Leave blank to use the default of " + REPO_URL + ")")
userInput = raw_input()
if userInput:
    REPO_URL = userInput

my_cron = CronTab(user='pi')
job = my_cron.new(command='cd '+cwd+' && python client.py')
job.minute.every(1)

my_cron.write()

f= open("config.py","w")
f.write('SERVER_URL = "'+SERVER_URL+'"\nREPO_URL = "'+REPO_URL+'"')
f.close()

