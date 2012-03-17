# -*- coding: utf-8 -*-
"""
Base classes for user

@copyright: (c) 2012 Ruslan Penkrat
@author: Ruslan Penkrat <penkrat@gmail.com>
@license: GPLv3 <http://www.gnu.org/licenses/gpl-3.0.html>
"""

class User:
    id = None
    name = None
    full_name = None
    
    def __init__(self,id, name=None, full_name=None):
        self.id = id
        if name:
            self.name = name
        else:
            self.name = id
        if full_name:
            self.full_name = full_name
        else:
            self.full_name = id
            
    def __str__ (self):
        return 'User %s with name %s' % (self.id,self.full_name)
        
    def send_message (self, text):
        """Send message to user"""
        raise NotImplementedError()

    def __unicode__ (self):
        return u'User %s with name %s' % (self.id,self.full_name)
