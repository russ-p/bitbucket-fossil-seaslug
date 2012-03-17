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
from seaslug.messengers.dummy import DummyChat
from seaslug.utils import get_instance_by_classname

import settings

class PluginTestMessenger (Messenger):
    
    cmds = []
    
    def start (self):
        print "Started"
        user = User ('dummy', 'dummy messenger')
        chat = DummyChat ('console', 'Console')
        chat.members = {
        '1':user,
        '2':User ('dummy2', 'User 2'),
        '3':User ('dummy3', 'User 3'),
        '4':User ('dummy4', 'User 4'),
        '5':User ('dummy5', 'User 5')}
        for cmd in self.cmds:
            self.do_message_receive(Message (cmd, user, chat))
        self.do_exit()
        
    def connect (self):
        for plugin in settings.PLUGINS:
            try:
                plugin_instance = get_instance_by_classname(plugin, self)
                if 'commands' in plugin_instance.__dict__:
                    for cmd, hook in plugin_instance.commands.iteritems ():
                        self.cmds.append(cmd)
            except Exception as ex:
                print ex
 
        
    def disconnect (self):
        print "Disconnected"
