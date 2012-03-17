# -*- coding: utf-8 -*-
"""
Common interface for any protocols and IM client
like ICQ, IRC,Skype, console

@copyright: (c) 2011 Ruslan Penkrat
@author: Ruslan Penkrat <penkrat@gmail.com>
@license: GPLv3 <http://www.gnu.org/licenses/gpl-3.0.html>
"""

class Messenger(object):
    chats = {}
    users = {}
    def connect (self):
        """Connect to interface"""
        raise NotImplementedError()
        
    def disconnect (self):
        """Disconnect from interface"""
        raise NotImplementedError()
        
    def set_message_handler (self, message_handler):
        """set callback function for onMessage"""
        self.on_message_received = message_handler
        
    def set_exit_handler (self, exit_handler):
        """qwe"""
        self.on_exit_handler = exit_handler
        
    def do_exit (self):
        if self.on_exit_handler:
            self.on_exit_handler()
        
    def do_message_receive (self, msg):
        if self.on_message_received:
            self.on_message_received(msg)
            
    def get_chat_list (self):
        """Return list of chats"""
        raise NotImplementedError()
