import pandas as pd
import praw
from datetime import datetime, timedelta
import sqlite3
import string
import commands


def create_table():
    with sqlite3.connect('database.db') as con:
        sql = '''    CREATE TABLE IF NOT EXISTS replied_comments (
            comment_name TEXT PRIMARY KEY NOT NULL
        )'''
        con.execute(sql)
        
    return 

def is_replied(thing):
    create_table()
    name = thing.fullname
    with sqlite3.connect('database.db') as con:
        results = pd.read_sql("select * from replied_comments where comment_name = '{}'".format(name), con)
        if len(results) >= 1:
            return True
    return False
        
def save_replied(thing):
    create_table()
    name = thing.fullname
    with sqlite3.connect('database.db') as con:
        con.execute(" INSERT INTO replied_comments(comment_name) values('{}')".format(name))



def figure_out_command(words):
    words = words.lower()

    if 'abathor:' not in words:
        return False
    
    command_list = commands.command_list
    for command in command_list:
        if command in words.lower():
            
            start = len(command) + words.index(command)
            end = words.find('!')
            arguments = words[int(start): int(end)].split(',')
            final_arguments= []
            
            for arg in arguments:
                arg = arg.strip().upper()
                for punc in string.punctuation:
                    if punc not in '+-/*_':
                        arg = arg.replace(punc, '')
                    
                final_arguments.append(arg)
            return command, final_arguments, end
    return False


def respond_to_text(text):
    command = figure_out_command(text.lower())
    if type(command) == type(False):
        raise ValueError('No valid command')
    command, args, end = command
    return commands.command_list[command](args)

reddit = praw.Reddit('bot1')
subreddit = reddit.subreddit("wallstreetbets+investing+robinhood")



