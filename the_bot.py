from datetime import datetime, timedelta
import time
import sys
import os
import subprocess 




def get_version():
    filename = 'version.txt'
    startime = time.time()
    while True:
        try:
            with open(filename, 'r') as file:
                current_version = float(file.read())
                return current_version
        except Exception as e:
            if (time.time() - startime) > 100:
                log('Failure on open:' + str(e))
                startime = time.time()
            pass

def version_check():
    global version
    current_version = get_version()
    if current_version > version:
        print('UPDATING NOW')
        log('Update to Version: {}'.format(current_version))
        subprocess.Popen(['start', '/MAX', sys.executable, sys.argv ], shell = True)
        #os.execv(sys.executable, ['python3'] + sys.argv)
    if current_version == version: 
        return 




def log(message):
    with open('log.txt', 'a') as f:
        f.write('\n')
        f.write(datetime.now().isoformat())
        f.write('    :')
        f.write(message)
    return 





 

'''



if __name__ == '__main__':
    version = get_version()

    while True:
        try:
            version_check()
        except Exception as e:
            log('Main Loop Exception' +repr(e))
        pass'''