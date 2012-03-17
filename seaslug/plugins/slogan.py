# -*- coding:utf-8 -*-
"""
Slogans

@copyright: (c) 2012 Ruslan Penkrat
@author: Ruslan Penkrat <penkrat@gmail.com>
@license: GPLv3 <http://www.gnu.org/licenses/gpl-3.0.html>
"""
import urllib2, urllib, re

from seaslug.core.plugin import Plugin
from seaslug.utils import ru, ur

class SloganPlugin(Plugin):
    plugin_name = 'Slogan from slogen.ru'
    def getSlogan(self, botMessage, *args, **kwargs):
        "Генератор слоганов: !slogan <текст>"
        if len(botMessage.params) < 1: return botMessage.send_response('Use: !слоган <text>')
        data = urllib.urlencode({"slogan": ur(botMessage.paramString), "submit":"&gt"})
        req = urllib2.Request('http://slogen.ru/pda/index.php', data)
        page = urllib2.urlopen(req)
        source = page.read()
        match = re.search('<div class="slogan1">(.*?)</div>', source)
        return botMessage.send_response(ru(match.group(1)))
    
    def init(self):
        self.commands = {
        '!slogan' : self.getSlogan,
        ru('!слоган') : self.getSlogan}

