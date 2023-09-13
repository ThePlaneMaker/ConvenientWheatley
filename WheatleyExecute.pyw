from wheatley.main import main
from threading import Thread

import os 

pid = os.getpid() 
  
  
# Print the process ID of 
# the current process 

with open("PID.txt", 'w') as f:
    f.write(str(pid))

with open("command.txt", 'r') as f:
    command = []
    for line in f:
        k = line.strip('\n')
        command.append(k)

Thread(target=main, args=(command,)).start()
