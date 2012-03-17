# -*- coding: utf-8 -*-
"""
Handler for message process

@copyright: (c) 2012 Ruslan Penkrat
@author: Ruslan Penkrat <penkrat@gmail.com>
@license: GPLv3 <http://www.gnu.org/licenses/gpl-3.0.html>
"""
import logging

log = logging.getLogger('handlers')

class Handler (object):
    """
    Базовый класс для всех обработчиков
    """
    
    def __init__(self, application):
        self._application = application
        self.data = {}
        self.nextHandler = None
 
    def __add__ (self, newHandler):
        """
        Метод, используемый для комбинации классов
        """
        if not isinstance(newHandler, Handler):
            raise TypeError('Handler.__iadd__() expects Handler, not '+str (Handler.__class__))
        if self.nextHandler:
            self.nextHandler += newHandler
        else:
            log.debug ('Added handler '+str(newHandler.__class__))
            self.nextHandler = newHandler
            while newHandler:
                newHandler.data = self.data
                newHandler = newHandler.nextHandler
        return self
        
    def useHook(self, msg):
        """
        Применить обработчик
        """
        log.debug ('useHook '+str(self.__class__))
        if self.hook(msg):
            if self.nextHandler:
                if not self.nextHandler.useHook(msg):
                    log.debug ('Message processed.')
                    return False
        else:
            self.data.clear( )
        return True
 
    def hook(self, msg):
        """
        Обработчик по умолчанию
        """
        return True
