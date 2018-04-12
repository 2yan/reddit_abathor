from datetime import datetime
import time
import sys
import subprocess 
import os
import socket
import pandas as pd

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


def get_greeting(comment):
    author = comment.author
    requester_name = author.name
    friend = author.is_friend

    title = ''
    flair = comment.author_flair_text
    if pd.isnull(flair):
        flair = ''
    to_remove = ['the ', 'an ', 'a ']
    for thing in to_remove:
        if flair.lower().strip().startswith(thing):
            flair = flair[len(thing)]
    
    if flair != '':
        flair = "the \'{}\'".format(flair)
    
    if requester_name == '2yan':
        title = 'Yes Sir,'
    
    if requester_name != '2yan':
        title = '{} {} :'.format(requester_name, flair)
    
    if friend:
        title = 'Absolutely {}, {}, Friend of 2yan'.format(requester_name, flair)
    return title

def main_loop():
    subreddit = glue.subreddit
    today = datetime.today()
    
    for comment in subreddit.stream.comments():
        version_check(context)
        
        if datetime.today().day != today.day:
            today = datetime.today()
            glue.delete_cache()
        comment_text = comment.body.lower()
        if 'abathor:' in comment_text:
            print(comment_text)
            if not glue.is_replied(comment):
                try:
                    response = glue.respond_to_text(comment_text)
                except Exception as e:
                    response = 'Error: ' + (str(e))
                    
                greeting = get_greeting(comment)
                    
                text = greeting + '  \n\n\n  ' + response
                text = text + ' \n\n_______________________ ' 
                text = text + ' \n\n Guide: https://github.com/2yan/reddit_abathor/ '
                text = text +  '''\n\n I'm Abathor, a bot that runs on u/2yan's account and serves to provide stats and data.
                Anyone can invoke me in a few specific subreddits.''' 

                comment.reply(text)
                
                print('replied')
                glue.save_replied(comment)
                
                
def allready_running():
    HOST = ''   # Symbolic name, meaning all available interfaces
    PORT = 6613 # Arbitrary non-privileged port
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
    except OSError:
        return False
    return s
    
if __name__ == '__main__':
    print('Starting Up')
    for num in range(0, 5):
        time.sleep(1)
        print(5- num, '.'* (5 - num))


    s = allready_running()
    if not s:
        raise Exception('Only One Version of the Program can be running at a time')

    version = get_version()

    
    print('Started Bot: __version__ {}'.format(version))
    context = {'version':version, 'last_check_time':0}
    while True:
        try:
            import glue
            version_check(context)
            main_loop()
        except Exception as e:
            log('Main Loop Exception' +repr(e))
        pass