# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        stats - модуль ведения статистики
# Purpose:
#
# Author:      Russ
#
# Created:     22.08.2010
# Copyright:   (c)  2010
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import sys
import random
import time
import sqlite3

from seaslug.core.plugin import Plugin
from seaslug.utils import ru, ur, explore

class StatsPlugin(Plugin):
    plugin_name = 'Chat statistic'
    db_connect = None
    commits_count = 0
    
    def get_connection (self):
        if not self.db_connect:
            self.db_connect = sqlite3.connect(self.db_path, check_same_thread = False)
        return self.db_connect
        
    def get_cursor(self):
        return self.get_connection().cursor()
        
    def lazy_commit (self, force = False):
        if force | (self.commits_count > 10):
            self.get_connection().commit()
            self.commits_count = 0
        else:
            self.commits_count += 1
    
    def top(self, botMessage):
        "Топ флудеров"
        self.lazy_commit(True)
        cursor = self.get_cursor()
        cursor.execute("SELECT username, count FROM msgs_count WHERE chatname='%s' ORDER BY count  DESC LIMIT 10" % botMessage.chat.id)
        return botMessage.send_response(ru('Топ-10 флудеров:\n\t * ') + '\n\t * '.join([ '%s (%d)' % (username, count) for (username, count) in cursor]))
    
    def top20(self, botMessage):
        "Топ флудеров, места 11-20"
        self.lazy_commit(True)
        cursor = self.get_cursor()
        cursor.execute("SELECT username, count FROM msgs_count WHERE chatname='%s' ORDER BY count  DESC LIMIT 10 OFFSET 10" % botMessage.chat.id)
        return botMessage.send_response(ru('Топ-20 флудеров, места 11-20:\n\t * ') + '\n\t * '.join([ '%s (%d)' % (username, count) for (username, count) in cursor]))
    
    def antitop(self, botMessage):
        "ТОП молчунов-шпионов"
        self.lazy_commit(True)
        cursor = self.get_cursor()
        cursor.execute("SELECT username, count FROM msgs_count WHERE chatname='%s' ORDER BY count  ASC LIMIT 10" % botMessage.chat.id)
        return botMessage.send_response(ru('Эти подозрительно молчат:\n\t * ') + '\n\t * '.join([ '%s (%d)' % (username, count) for (username, count) in cursor]))
    
    def insert_into_msgs (self,botMessage):
        c = self.get_cursor()
        c.execute('INSERT INTO msgs VALUES (current_timestamp,?,?,?)', (botMessage.chat.id, botMessage.sender.id, botMessage.rawText))
        
    def update_msg_count (self,botMessage):
        c = self.get_cursor()
        c.execute('SELECT * FROM msgs_count  WHERE chatname=? AND uniquename=?', (botMessage.chat.id, botMessage.sender.id))
        if c.fetchone():
            c.execute('UPDATE msgs_count SET count = count + 1, username=?  WHERE chatname=? AND uniquename=?', (botMessage.sender.full_name, botMessage.chat.id, botMessage.sender.id))
        else:
            c.execute('INSERT INTO msgs_count VALUES (?,?,?,1)', (botMessage.chat.id, botMessage.sender.full_name, botMessage.sender.id))
        self.lazy_commit()
    
    def stat_write(self, botMessage):
        if botMessage.sender.id in ['pyskypebot']:
            return
        if len(botMessage.rawText)<4:
            return
        #self.insert_into_msgs(botMessage)
        self.update_msg_count (botMessage)
        
    def clear_stat(self, botMessage):
        "Очищает ТОП от вышедших из чата"
        if not self.is_admin(botMessage.realName):
            return botMessage.send_response( ru('Команда доступна только администратору бота.') )
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT uniquename FROM msgs_count WHERE chatname='%s' ORDER BY count  ASC LIMIT 100" % botMessage.chatName)
        for username in cursor:
            if username[0] in ['pyskypebot']:
                cursor.execute('DELETE FROM msgs_count  WHERE chatname=? AND uniquename=?', (botMessage.chat.id, username[0]))
                return botMessage.send_response(ru('%s удален из статистики') % username[0])
        conn.commit()
        conn.close()        
    
    def init(self):
        self.commands = {
        '!top' : self.top,
        '!top20' : self.top20,
        '!antitop' : self.antitop,
        '!cleartop' : self.clear_stat}
        # список глобальных обработчиков сообщений этого модуля-плагина
        self.globalListeners = [self.stat_write]
        self.db_path = explore('stat.db')
        
    def destroy (self):
        print 'destroy'
        self.get_connection().close()
        
    def __del__(self):
        print 'del'
        self.destroy ()
        
    def create_db (self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''create table msgs (date text, chatname text, username text,msg text)''')
        cursor.execute('''create table msgs_count (chatname text, username text, uniquename text, count int)''')
        conn.commit()
        cursor.close()

if __name__ == '__main__':
        from seaslug.botmessage import BotMessage
        from seaslug.chatbot import CommonBot
        tp = StatsPlugin(CommonBot('/home/ruslan/Документы/pyskypebot/test_config.py'))
        #tp.create_db ()
        start = time.time()
        for i in xrange (100):
            tp.stat_write (BotMessage (rawText = u'this is message',realName=u'Russ', chatName = u'test_chat', displayName=u'Russ'))
            #tp.update_msg_count (BotMessage (rawText = u'this is message',realName=u'Russ', chatName = u'test_chat', displayName=u'Russ'))
        tp.top (BotMessage (rawText = u'this is message',realName=u'Russ', chatName = u'test_chat', displayName=u'Russ'))
        print "Elapsed Time: %s" % (time.time() - start)
        print 'End' 
