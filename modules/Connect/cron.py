from crontab import CronTab

cron = CronTab(user="leonardo")
job = cron.new(command="python /home/leonardo/Documentos/Desenvolvimento/whatsapp-framework/modules/Connect/auth.py", comment="Tarefa para autorizar no sigeco")
job.hour.every(2)

for item in cron:
    print item

cron.write()

