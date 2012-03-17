# -*- coding: utf-8 -*-
"""
Skype messenger - skype interface fo seaslug bot

@copyright: (c) 2012 Ruslan Penkrat
@author: Ruslan Penkrat <penkrat@gmail.com>
@license: GPLv3 <http://www.gnu.org/licenses/gpl-3.0.html>
"""

import sys
import time
import logging
import Skype4Py

from seaslug.core.messenger import Messenger
from seaslug.core.user import User
from seaslug.core.message import Message
from seaslug.core.chat import Chat

log = logging.getLogger ('SkypeMessenger')
SKYPE = None
SKYPE_CHATS = {}
SKYPE_USERS = {}

def get_cached_skype_chat(sk4p_chat):
    global SKYPE_CHATS
    if sk4p_chat.Name in SKYPE_CHATS:
        return SKYPE_CHATS[sk4p_chat.Name]
    else:
        new_chat = SkypeChat(sk4p_chat)
        SKYPE_CHATS.update ({sk4p_chat.Name: new_chat})
        return new_chat
    
def get_cached_skype_user(sk4p_user):
    global SKYPE_USERS
    if sk4p_user.Handle in SKYPE_USERS:
        return SKYPE_USERS[sk4p_user.Handle]
    else:
        new_user = SkypeUser(sk4p_user)
        SKYPE_USERS.update ({sk4p_user.Handle: new_user})
        return new_user

class SkypeMessenger (Messenger):
    last_message_id = 0
    
    def __init__ (self):
        global SKYPE
        SKYPE = Skype4Py.Skype()
        SKYPE.OnMessageStatus = self.MessageStatus
        
    def start (self):
        log.info ('start loop')
        
    def connect (self):
        global SKYPE
        if not SKYPE.Client.IsRunning:
            log.info ('Starting Skype..')
            SKYPE.Client.Start()
        log.info ('Connecting to Skype..')
        SKYPE.Attach()
        log.info (u'Your full name: %s' % SKYPE.CurrentUser.FullName)
        log.info (u'MoodText: %s' % SKYPE.CurrentUser.MoodText)
        
    def disconnect (self):
        print "Disconnected"
    
    def MessageStatus(self, SkMessage, status):
        """SkypeAPI onMessageStatus handler"""
        if (self.last_message_id < SkMessage.Id)\
        and (status in [Skype4Py.cmsSent, Skype4Py.cmsRead, Skype4Py.cmsReceived]):
            log.debug("%s: %d/ %s", status, SkMessage.Id, SkMessage.Body)
            self.last_message_id = SkMessage.Id
            msg = SkypeMessage(SkMessage)
            if status == Skype4Py.cmsReceived:
                SkMessage.MarkAsSeen()
            self.do_message_receive(msg)

    def ConnectionStatus(self, status):
        """SkypeAPI onConnectionStatus handler"""
        log.info(status)

    def ChatMembersChanged__(self, SkChat, Members):
        """This event occurs when a list of chat members change."""
        id = SkChat.Name
        if id in self.all_chats:
            self.all_chats[id] = SkypeChat(SKChat)
            log.debug (u"SkypeBot: added new member in %s" % self.all_chats[id])
            
    def get_users(self):
        global SKYPE_USERS
        return SKYPE_USERS
        
    def get_chats (self):
        global SKYPE_CHATS
        return SKYPE_CHATS
        
    chats = property (get_chats)
    users = property (get_users)
        
class SkypeChat(Chat):
    def __init__ (self, sk4p_chat):
        log.debug ('New skype chat %s', sk4p_chat.Name)
        Chat.__init__(self, sk4p_chat.Name, sk4p_chat.Topic)
        self.sk4p_chat = sk4p_chat
        self.members = {}
        for member in sk4p_chat.Members:
            self.members[member.Handle] = get_cached_skype_user(member)
        
    def send_message(self,msg):
        if not msg.startswith(u'/me'):
            msg = u'>>' + msg
        self.sk4p_chat.SendMessage(msg)
        
class SkypeUser(User):
    def __init__ (self, sk4p_user):
        log.debug ('New skype user %s (%s)',sk4p_user.Handle, sk4p_user.FullName)
        User.__init__(self, sk4p_user.Handle, sk4p_user.DisplayName, sk4p_user.FullName)
        self.sk4p_user = sk4p_user
        
    def send_message(self,msg):
        global SKYPE
        SKYPE.SendMessage (self.sk4p_user.Handle, u'>>'+msg)

class SkypeMessage(Message):
    def __init__ (self, sk4p_chat_message):
        log.debug ('New skype message')
        self.sender = get_cached_skype_user(sk4p_chat_message.Sender)
        self.chat = get_cached_skype_chat(sk4p_chat_message.Chat)
        self.rawText = sk4p_chat_message.Body
        self.sk4p_chat_message = sk4p_chat_message
        self.sendTime = sk4p_chat_message.Timestamp
