# -*- coding: utf-8 -*-
"""
Some Handlers for message processing

@copyright: (c) 2012 Ruslan Penkrat
@author: Ruslan Penkrat <penkrat@gmail.com>
@license: GPLv3 <http://www.gnu.org/licenses/gpl-3.0.html>
"""

from seaslug.core.handler import Handler, log


class CommandParser(Handler):
    plugins_hooks = {}
    
    def __init__ (self, application):
        Handler.__init__ (self, application)
        for plugin in application.plugins:
            if 'commands' in plugin.__dict__:
                for cmd, hook in plugin.commands.iteritems ():
                    log.info ( 'Added command "%s"' % cmd)
                    self.plugins_hooks[cmd] = hook 
    
    def hook (self, msg):
        wl = msg.rawText.split(' ')
        command = wl[0].lower()
        params = wl[1:]
        if command in self.plugins_hooks:
            self.data['command'] = command
            self.data['params'] = params
            self.data['plugin_cmd_hook'] = self.plugins_hooks[command]
        return True


class CommandFilter (Handler):
    def __init__ (self, app):
        Handler.__init__ (self,app)
        
    def hook (self, msg):
        return True


class CommandExecuter (Handler):
    def hook (self, msg):
        if 'plugin_cmd_hook' in self.data:
            msg.command = self.data['command']
            msg.params = self.data['params']
            try:
                self.data['plugin_cmd_hook'](msg)
            except Exception as e:
                import traceback, sys
                log.error (traceback.print_tb(sys.exc_info()[2]))
                msg.send_response('Error: ' + str(e))
            return False
        else:
             return True


class ConsoleLogger (Handler):
    def hook (self, msg):
        if msg.sender.id == 'pyskypebot':
            print u'\033[92m[%s](%s):\n\033[94m%s\033[0m' % (msg.sender.full_name,msg.chat.topic, msg.rawText)
        else:
            print u'\033[92m[%s](%s):\n\033[91m%s\033[0m' % (msg.sender.full_name,msg.chat.topic, msg.rawText)
        return True
        
class AllMessageHandler(Handler):
    plugins_hooks = []
    plugin_hook_name = 'globalListeners'
    
    def __init__ (self, application):
        Handler.__init__ (self, application)
        for plugin in application.plugins:
            if self.plugin_hook_name in plugin.__dict__:
                for hook in plugin.globalListeners:
                    log.info ('Added global hook %s' % hook)
                    self.plugins_hooks.append(hook)
    
    def hook (self, msg):
        for plugin_hook in self.plugins_hooks: 
            try:
                plugin_hook(msg)
            except Exception as e:
                log.error (e)
        return True
        
class AllCommandHandler(Handler):
    plugins_hooks = []
    plugin_hook_name = 'all_commands'

    def __init__ (self, application):
        Handler.__init__ (self, application)
        for plugin in application.plugins:
            if self.plugin_hook_name in plugin.__dict__:
                for hook in plugin.all_commands:
                    log.info ('Added all command hook %s' % hook)
                    self.plugins_hooks.append(hook)
    
    def hook (self, msg):
        if 'plugin_cmd_hook' in self.data:
            for plugin_hook in self.plugins_hooks: 
                try:
                    plugin_hook(msg)
                except Exception as e:
                    log.error (e)
            return True
