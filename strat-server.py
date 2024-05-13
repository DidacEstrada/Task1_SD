import subprocess
import time

subprocess.Popen(['start', 'cmd', '/k', 'title NameServer && python grpc_nameServer.py'], shell=True)
time.sleep(1)
subprocess.Popen(['start', 'cmd', '/k', 'title RabbitMQServer && python RabbitMQServer.py'], shell=True)

#Para macOS
#subprocess.Popen(['open', '-a', 'Terminal', '-n', '-e', 'python grpc_nameServer.py'])
#subprocess.Popen(['open', '-a', 'Terminal', '-n', '-e', 'python RabbitMQServer.py'])