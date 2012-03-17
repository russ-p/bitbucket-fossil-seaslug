# -*- coding: utf-8 -*-
"""
Base classes for user and chat

@copyright: (c) 2011 Ruslan Penkrat
@author: Ruslan Penkrat <penkrat@gmail.com>
@license: GPLv3 <http://www.gnu.org/licenses/gpl-3.0.html>
"""

import os
import time
import logging

from Queue  import Queue, Empty

from seaslug.conf import settings
from seaslug.utils import get_instance_by_classname

log = logging.getLogger('app')

class Application:
    
    messenger = None
    handler = None
    plugins = []
    running = 1
    
    def __init__ (self, autostart=True):
        log.info ("Starting application...")
        self.Q = Queue()
        self.messenger = get_instance_by_classname(settings.MESSENGER)
        self.messenger.set_message_handler(self.add_task)
        self.messenger.set_exit_handler(self.stop)
        self._init_plugins()
        self._init_handlers_chain()
        if autostart:
            self.connect()
            self.start()
            self.run()
        
    def _init_handlers_chain (self):
        log.info ("Init handlers...")
        handlers = map(lambda h:get_instance_by_classname(h, self), settings.HANDLERS)
        self.handler = reduce (lambda res, h:res+h,handlers[1:],handlers[0])
        
    def _init_plugins (self):
        log.info ("Loading plugins...")
        self.plugins = []
        for plugin in settings.PLUGINS:
            try:
                self.plugins.append(get_instance_by_classname(plugin, self))
                log.info ( str(plugin) + ' loaded.')
            except Exception as ex:
                log.error(plugin+' NOT loaded!')
                log.error(ex)
        
    def connect (self):
        if self.messenger:
            log.info ("Connecting...")
            log.debug('Use messenger '+str(self.messenger.__class__))
            self.messenger.connect()

    def disconnect (self):
        if self.messenger:
            log.info( "Disconnecting...")
            self.messenger.disconnect()
            
    def start (self):
        if self.messenger:
            self.messenger.start ()
    
    def stop (self):
        self.running = 0
        if self.messenger:
            self.messenger.set_message_handler(None)
            
    def add_task (self, msg):
        log.debug('Add new item in Q, Q size %d', self.Q.qsize())
        self.Q.put(msg)
            
    def run (self):
        log.info ("Running.")
        while self.running or not self.Q.empty():
            try:
                item = self.Q.get(block=False)
                self.handler.useHook(item)
                self.Q.task_done()
            except Empty:
                try:
                    time.sleep (0.1)
                except KeyboardInterrupt:
                    self.stop()
        self.disconnect()
        log.info ("Application finished.")
            
application = Application ()
