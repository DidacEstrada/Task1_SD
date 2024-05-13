import subprocess
import time

subprocess.Popen(['start', 'cmd', '/k', 'title NameServer && python grpc_nameServer.py'], shell=True)
time.sleep(1)
subprocess.Popen(['start', 'cmd', '/k', 'title RabbitMQServer && python RabbitMQServer.py'], shell=True)