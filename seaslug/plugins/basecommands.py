# -*- coding:utf-8 -*-
"""
Additional functions and minimal chat commands

@copyright: (c) 2011 Ruslan Penkrat
@author: Ruslan Penkrat <penkrat@gmail.com>
@license: GPLv3 <http://www.gnu.org/licenses/gpl-3.0.html>
"""

import datetime

from seaslug.about import VERSION, LAST_DATE
from seaslug.core.plugin import Plugin
from seaslug.utils import ru, ur


class BaseCommandsPlugin (Plugin):
    """Класс содержит реализацию базовых команд """
    plugin_name = 'Base commands for bot'
    
    def init(self):
        self.start_time = datetime.datetime.now()
        self.msg_count = 0
        self.cmd_count = 0
        self.commands = {u'!bot': self.main_cmd}
        self.globalListeners = [self.msg_counter]
        self.all_commands = [self.cmd_counter]
    
    def main_cmd (self, botMessage):
        """
Информация о боте, дополнительные параметры команды:
!bot lag - задержка сети и обработки команды ботом;
!bot stat - статистика бота;
!bot about - инфо о авторе;
!bot sysinfo - информация о системе бота
"""
        if len(botMessage.params) > 0:
            if botMessage.params[0] == u'lag':
                self.lagomer(botMessage)
            elif botMessage.params[0] == u'about':
                self.about(botMessage)
            elif botMessage.params[0] == u'sysinfo':
                self.sysinfo(botMessage)
            elif botMessage.params[0] == u'stat':
                self.show_stats(botMessage)
        else:
            self.echo (botMessage)
        
    def echo(self, botMessage):
        """Эхо"""
        resp = '\n'.join( ['I am bot. ((wave))',
                           'version: %s (%s)' % (VERSION, LAST_DATE),
                           'type "!help !bot" for more informaition.'])
        return botMessage.send_response(resp)

    def lagomer(self, botMessage):
        """Лаг"""
        import time
        lag = time.time() - botMessage.sendTime
        resp = ru("%s, твое cообщение долетело за %f секунд") % (botMessage.sender, lag)
        return botMessage.send_response(resp)
    
    def about (self, botMessage):
        """О авторе"""
        resp = '\n'.join( ['"SeaSlug Project" - Chatterbot for Skype and other IMs.',
                           'version: %s (%s)' % (VERSION, LAST_DATE),
                           'Developer: (Skype) ruslan.penkrat'])
        return botMessage.send_response(resp) 
    
    def sysinfo(self, botMessage):    
        """Информация о системе"""
        import platform, time
        resp = '\n'.join( [
                           'OS: %s' % platform.system(),
                           'Local time: %s' % time.strftime('%H:%M:%S')])
        return botMessage.send_response(resp)

    def uptime(self):
        return datetime.datetime.now() - self.start_time

    def strfuptime(self):
        return str(self.uptime())
        
    def show_stats (self, botMessage):
        response = u'Bot stats:\nUptime: %s;\n' % (self.strfuptime())
        response += u'msg count: %d;\n' % self.msg_count
        response += u'cmd exec count: %d;\n' % self.cmd_count
        response += u'plugins: %d;\n' % len(self.app.plugins)
        response += u'users: %d;\n' % len(self.app.messenger.users)
        response += u'chats: %d' % len(self.app.messenger.chats)
        botMessage.send_response(response)
        
    def get_test_command (self):
        return ("!bot","!bot about","!bot sysinfo",)
        
    def msg_counter (self, botMessage):
        self.msg_count += 1
        
    def cmd_counter (self, botMessage):
        self.cmd_count += 1
        
class ListAndHelpCommands (Plugin):
    plugin_name = 'All commands of bot'
    
    bot_commands = None
    bot_plugins = None
    
    def init (self):
        self.commands = {'!list': self.list,
                         '!help': self.help}
    
    def lazy_plugins (self):
        if not self.bot_plugins:
            self.bot_plugins = []
            self.bot_commands = {}
            for plugin in self.app.plugins:
                self.bot_plugins.append (plugin)
                if 'commands' in plugin.__dict__:
                    for cmd, hook in plugin.commands.iteritems():
                        self.bot_commands[cmd] = hook
        return self.bot_plugins
    
    def lazy_commands (self):
        if not self.bot_commands:
            self.lazy_plugins()
        return self.bot_commands
        
    def list(self, botMessage):
        """Вывод списка комманд или плагинов бота.
"!list" - вывод всех комманд,
"!list -plugins" - вывод списка плагинов,
"!list -p" - вывод списка комманд, отсортированых по плагинам,
"!list -v" - вывод списка комманд с описанием.
"""
        if len(botMessage.params) > 0:
            if botMessage.params[0] == u'-v':
                self.list_verbose(botMessage)
            elif botMessage.params[0] == u'-p':
                self.list_by_plugins(botMessage)
            elif botMessage.params[0] == u'-plugins':
                self.list_plugins(botMessage)
        else:
            return botMessage.send_response(u', '.join([cmd for cmd in self.lazy_commands().keys()]))
    
    def list_plugins (self, botMessage):
        resp = ru ('Загруженные плагины:\n* ')
        resp += '\n* '.join ([plugin.plugin_name for plugin in self.lazy_plugins()])
        resp += ru ('\nВсего плагинов: %d') % len (self.lazy_plugins())
        botMessage.send_response(resp)
    
    def list_by_plugins (self, botMessage):
        resp = ru ('Команды бота:\n')
        for plugin in self.lazy_plugins():
            resp += ','.join ([cmd for cmd in plugin.commands.keys ()])
            resp += '\n'
        botMessage.send_response(resp)
        
    def list_verbose (self, botMessage):
        resp = u'\n'.join([u'%s - %s' % (cmd, self._get_command_help(cmd)) for cmd in self.lazy_commands().keys ()])
        botMessage.send_response(resp)

    def _get_command_help(self, cmd):
        if self.lazy_commands()[cmd].func_doc:
            try:
                return ru(self.lazy_commands()[cmd].func_doc)
            except:
                return ru('Ошибка в описании команды %s')
        else:
            return ru('Нет справки для команды %s') % cmd

    def help(self, botMessage):
        """Вывод справки по командам бота"""
        if len(botMessage.params) > 0:
            if botMessage.params[0] in self.lazy_commands():
                return botMessage.send_response(self._get_command_help(botMessage.params[0]))
            else:
                return botMessage.send_response(ru('No commands %s') % botMessage.params[0])
        else:
            return botMessage.send_response(ru('Для получение справки по команде напишите !help <команда>, или !list для списка команд'))    

    def get_test_command(self):
        return ("!list","!help !list", "!list -p",)
