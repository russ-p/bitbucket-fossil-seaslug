# -*- coding: utf-8 -*-
"""
console messenger with file input source

@copyright: (c) 2011 Ruslan Penkrat
@author: Ruslan Penkrat <penkrat@gmail.com>
@license: GPLv3 <http://www.gnu.org/licenses/gpl-3.0.html>
"""

from seaslug.messengers.dummy import DummyMessenger, DummyChat
from seaslug.core.user import User
from seaslug.core.message import Message

class FileInputMessenger (DummyMessenger):
    
    def start (self):
        print "Started"
        chat = DummyChat ('console', 'Console')
        user = User ('file source', 'File  Source')
        for line in open ('input.txt').readlines():
            self.do_message_receive(Message (line.rstrip().decode ('utf-8'), user, chat))
        self.do_exit()
        
    def connect (self):
        print "Connected"
        
    def disconnect (self):
        print "Disconnected"
