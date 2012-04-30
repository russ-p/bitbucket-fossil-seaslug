# -*- coding: utf-8 -*-
"""
Global configuration data

@copyright: (c) 2012 Ruslan Penkrat
@author: Ruslan Penkrat <penkrat@gmail.com>
@license: GPLv3 <http://www.gnu.org/licenses/gpl-3.0.html>
"""

import os

SEASLUG_SETTINGS_MODULE = 'SEASLUG_SETTINGS_MODULE'

class Settings (object):
    ADMINS = ['pyskypebot']
    WORK_DIR = os.curdir
    
    def __init__ (self):
        self._load_settings()
        
    def _load_settings (self):
        self.setting_module = os.getenv(SEASLUG_SETTINGS_MODULE, None)
        if self.setting_module:
            self._load_from_file(self.setting_module)
        else:
            self._load_from_file('settings.py')
        
    def _load_from_file (self,file_name):

            import imp
            import errno  
            self.settings = imp.new_module('settings')
            self.settings.__file__ = file_name
            try:
                execfile(file_name, self.__dict__)
            except IOError, e:
                e.strerror = 'Unable to load configuration file (%s)' % e.strerror
                raise

settings = Settings()

if __name__ == '__main__':
    print settings
    for k in settings.__dict__:
        print k


