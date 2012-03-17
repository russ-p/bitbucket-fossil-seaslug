# -*- coding: utf-8 -*-
"""
Base classes for chat

@copyright: (c) 2012 Ruslan Penkrat
@author: Ruslan Penkrat <penkrat@gmail.com>
@license: GPLv3 <http://www.gnu.org/licenses/gpl-3.0.html>
"""

class Chat:
    """Base class for Chat Objects"""
    
    members = {} # dict usr_id:chatmember  
    topic = ''   # chat\chanell topic 
    id = ''      # chat\chanell uniq ID
    chat_admins = [] # list of botadmins in this chat\chanell
    
    def __init__(self, id, topic = None, members = None):
        """Create new instance of chat object"""
        self.id = id
        if not topic: 
            self.topic = self.id
        else:
            self.topic = topic
        if members:
            self.members = members
        
    def kick(self, usr):
        """Kick user @usr from chat """
        raise NotImplementedError()
        
    def ban(self, usr):
        """Ban user @usr"""
        raise NotImplementedError()
        
    def set_topic(self, topic):
        """Set topic"""
        self.topic = topic
        
    def send_message(self,msg):
        """ Send public message to Chat"""
        raise NotImplementedError()
        
    def leave (self):
        """Leave chat"""
        raise NotImplementedError()
        
    def __str__(self):
        return 'Chat %s topic %s' % (self.id, self.topic)
        
if __name__ == '__main__':
    ch = Chat('321', topic = 'Chat topic')
    print ch
    ch.kick(1)
