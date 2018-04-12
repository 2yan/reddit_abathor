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

def version_check(context):
    version = context['version']
    last_check_time = context['last_check_time']
    if (time.time() - last_check_time) > 60 * 60:
        process = subprocess.Popen(["git", "pull",
                                    "https://github.com/2yan/reddit_abathor"], stdout=subprocess.PIPE)
        log(process.communicate()[0].decode())
        context['last_check_time'] = time.time()
        
    current_version = get_version()
    if current_version > version:
        print('UPDATING NOW')
        log('Update to Version: {}'.format(current_version))
        subprocess.Popen(['start', '/MAX', sys.executable, sys.argv ], shell = True)
        exit()
        #os.execv(sys.executable, ['python3'] + sys.argv)
    if current_version == version: 
        return 




def log(message):
    print(message)
    with open('log.txt', 'a') as f:
        f.write('\n')
        f.write(datetime.now().isoformat())
        f.write('    :')
        f.write(message)
    return 





 



if __name__ == '__main__':
    version = get_version()
    print('Started Bot: __version__ {}'.format(version))
    context = {'version':version, 'last_check_time':0}
    while True:
        try:
            version_check(context)
        except Exception as e:
            log('Main Loop Exception' +repr(e))
        pass