import subprocess

subprocess.Popen(['start', 'cmd', '/k', 'title Cliente1 && python Client1.py'], shell=True)
subprocess.Popen(['start', 'cmd', '/k', 'title Cliente2 && python Client2.py'], shell=True)
subprocess.Popen(['start', 'cmd', '/k', 'title Cliente3 && python Client3.py'], shell=True)
subprocess.Popen(['start', 'cmd', '/k', 'title Cliente4 && python Client4.py'], shell=True)
subprocess.Popen(['start', 'cmd', '/k', 'title Cliente5 && python Client5.py'], shell=True)