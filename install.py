from crontab import CronTab
import os

cwd = os.getcwd()

my_cron = CronTab(user='pi')
job = my_cron.new(command='cd '+cwd+' && python client.py')
job.minute.every(1)

my_cron.write()

