# -*- coding: utf-8 -*-
"""
Dummy console messenger

@copyright: (c) 2011 Ruslan Penkrat
@author: Ruslan Penkrat <penkrat@gmail.com>
@license: GPLv3 <http://www.gnu.org/licenses/gpl-3.0.html>
"""

from seaslug.core.messenger import Messenger
from seaslug.core.user import User
from seaslug.core.message import Message
from seaslug.core.chat import Chat

class DummyMessenger (Messenger):
    
    def start (self):
        print "Started"
        chat = DummyChat ('console', 'Console')
        user = User ('dummy', 'dummy messenger')
        msg = Message ('This is message from Dummy messenger', user, chat)
        self.do_message_receive(msg)
        
    def connect (self):
        print "Connected"
        
    def disconnect (self):
        print "Disconnected"
        
class DummyChat(Chat):
    def send_message(self,msg):
        print '\033[94m',msg,'\033[0m'
