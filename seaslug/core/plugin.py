# -*- coding: utf-8 -*-
"""
Abstract class for "Sea Slug Project" plugins.

@copyright: (c) 2012 Ruslan Penkrat
@author: Ruslan Penkrat <penkrat@gmail.com>
@license: GPLv3 <http://www.gnu.org/licenses/gpl-3.0.html>
"""
#
# заготовка для нового модуля плагина
#from skypebot.plugin import SeaSlugPlugin, ru, ur
#from skypebot.botmessage import BotMessagepython
#
#class NewPlugin(SeaSlugPlugin):
#    plugin_name = 'New plugin name'
#    
#    def init(self):
#        self.commands = {}
#        self.globalListeners = []
#
#    def destroy(self):
#        pass

import os.path
import sys
        
class Plugin():
    """Base class for all plugins"""
    ADMINS = [] # спискок администраторов бота
    RES_DIR = '' # папка со всеми ресурсами доступными плагинам
    explore = lambda self,path: os.path.join(self.RES_DIR, path)  
    is_admin = lambda self,name: name in self.ADMINS
    plugin_name = 'SeaSlugPlugin'
    
    commands = None # словарь ключевое слово - функция
    globalListeners = None # список функций обрабатывающих сообщения
    command_handlers = None # список функций обрабатывающих команды вообще
    init = None #
    destroy = None #

    def __init__(self, bot, *args, **kwargs):
        #work_dir = self.config.WORK_DIR, admins = self.config.ADMINS, datastore = self.datastore
        #self.RES_DIR = bot.config.__dict__.get('WORK_DIR','')
        #self.ADMINS = bot.config.__dict__.get('ADMINS',[])
        #self.global_datastore = bot.__dict__.get('datastore',{})
        #self.datastore = self.global_datastore.get (self.plugin_name, None)
        #if not self.datastore:
        #    self.global_datastore[self.plugin_name] = {'enabled':True}
        #    self.datastore = self.global_datastore[self.plugin_name]
            #print self.datastore, self.plugin_name
        self.app = bot
        if self.init:
            try:
                self.init()
            except :
                print self.plugin_name,': initialization F-F-A-I-L-L',sys.exc_info()[1]
    
    def get_test_command(self):
        """ Тестирует команды плагина"""
        return "Test string for plugin. Using for testing"

    def __del__(self):
        if self.destroy:
            try:
                self.destroy()
            except :
                print self.plugin_name,': finalization F-F-A-I-L-L',sys.exc_info()[1]
                
    #def restore_data (self, key, value):
        #print 'Saved data', key, value, self.datastore.get (key, value)
        #if not (key in self.datastore):
            #self.datastore[key] = value
        #return self.datastore.get (key, value)
#        self.globalListeners = []
