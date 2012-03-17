# -*- coding:utf-8 -*-
"""
TestPlugin

@copyright: (c) 2012 Ruslan Penkrat
@author: Ruslan Penkrat <penkrat@gmail.com>
@license: GPLv3 <http://www.gnu.org/licenses/gpl-3.0.html>
"""

import random

from seaslug.core.plugin import Plugin
from seaslug.utils import ru, ur

class TestPlugin(Plugin):
    plugin_name = 'Test plugin'
    
    def init (self):
        self.commands = {'!test':self.command}
        self.globalListeners = [self.command]
        print "Test plugin init"
        
    def destroy (self):
        print "Test plugin destroy"
        
    def command (self,msg):
        print self, msg
