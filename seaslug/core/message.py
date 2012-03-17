# -*- coding: utf-8 -*-
"""
Base classes for message in chat

@copyright: (c) 2012 Ruslan Penkrat
@author: Ruslan Penkrat <penkrat@gmail.com>
@license: GPLv3 <http://www.gnu.org/licenses/gpl-3.0.html>
"""

class Message(object):
    """Class is message sendet to bot"""
    rawText = '' # full message text: "!bot hello"
    command = None # command: "!bot"
    params = None  # params: ["hello",]
    sender = None # User object
    chat = None # Chat object

    def __init__(self, rawText, sender, chat):
        import time
        #print 'Message init'
        self.sender = sender
        self.chat = chat
        self.sendTime = time.time()
        self.rawText = rawText

    def _parse_message (self):
        """Parse command and params from message text"""
        wl = rawText.split(' ')
        self.command = wl[0].lower()
        self.params = wl[1:]
        
    def send_response (self, text):
        """Send text message in chat"""
        self.chat.send_message (text)

    def send_private_response (self, text):
        """Send text message to sender"""
        self.sender.send_message (text)

    def get_param_string (self):
        try:
            return self.rawText.split(' ', 1)[1]
        except IndexError:
            return ''
    
    def get_params (self):
        return self.rawText.split(' ')[1:]

    def msgclb(self, s):
        print s
    
    def __str__ (self):
        return '[%s](%s):\n%s' % (self.sender.full_name,self.chat.topic, self.rawText)

    def __unicode__ (self):
        return u'[%s](%s):\n%s' % (self.sender.full_name,self.chat.topic, self.rawText)
        
    paramString = property (get_param_string)
    #params = property (get_params)

if __name__ == '__main__':
    m = Message('This is text', None, None)
    print m
