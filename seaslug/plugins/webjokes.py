# -*- coding: utf-8 -*-

import urllib
import urllib2
import re
import random
import HTMLParser

from lxml import html

from seaslug.core.plugin import Plugin
from seaslug.utils import ru, ur

class WebJokePlugin(Plugin):
    plugin_name = 'bash.org.ru, ibash.org.ru, anekdot.odessa.ua'
    
    def init(self):
        self.commands = {'!bash': self.bash_org_ru,
            '!ibash': self.ibash_org_ru,
            '!anek': self.anek,
            ru('!анек'): self.anek,
            '!shortik': self.shortiki}
        
    def download_page (self, url):
        try:
            f = urllib2.urlopen(url)
            content = f.read()
            f.close()
            return content
        except IOError:
            print "Could not open document: %s" % url
        
    def ibash_org_ru(self, botMessage, *args, **kwargs):
        """Quote from ibash.org.ru\nibash [number]"""
        url_id = 'http://ibash.org.ru/quote.php?id='
        try: url = url_id + str(int(botMessage.params[0]))
        except: url = 'http://ibash.org.ru/random.php'
        body = self.download_page(url).decode ('cp1251')
        msg =  html.fromstring (body).find_class('quotbody')[0].text_content()
        return botMessage.send_response(msg)
        
    def bash_org_ru(self, botMessage, *args, **kwargs):
        """Random quote from bash.im"""
        url = 'http://bash.im/forweb/'
        reg = re.compile ("""padding: 1em 0;">(.*)<'\s\+\s'/div><""")
        s = urllib2.urlopen(url).read ().decode ('cp1251')
        msg = HTMLParser.HTMLParser().unescape(reg.search(s).group (1).replace("<' + 'br />","\n").replace("<' + 'br>","\n"))
        return botMessage.send_response(msg)

    def anek(self, botMessage):
        'Show random anecdote from anekdot.odessa.ua'
        target = self.download_page('http://anekdot.odessa.ua/rand-anekdot.php').decode ('cp1251')
        od = re.search('background-color:#FFFFFF\'>', target)
        message = target[od.end():]
        message = message[:re.search('<br>', message).start()]
        message = message.replace('<br />', '')
        message = message.strip()
        return botMessage.send_response(message)
        
    def shortiki (self, botmessage):
        """Шутка с shortiki.com"""
        jsondata = urllib.urlopen('http://shortiki.com/export/api.php?format=json&type=random&amount=1').read()
        import json
        j = json.loads(jsondata)
        msg = j[0]['content']
        botmessage.send_response(msg)
