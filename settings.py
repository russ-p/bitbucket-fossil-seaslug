#List of bot admins
ADMINS = []


#MESSENGER = 'seaslug.messengers.dummy.DummyMessenger'
#MESSENGER = 'seaslug.messengers.fileinput.FileInputMessenger'
MESSENGER = 'seaslug.messengers.plugintest.PluginTestMessenger'
#MESSENGER = 'seaslug.messengers.skype.SkypeMessenger'


PLUGINS = (
    'seaslug.plugins.basecommands.BaseCommandsPlugin',
    'seaslug.plugins.basecommands.ListAndHelpCommands',
    'seaslug.plugins.webjokes.WebJokePlugin',
    'seaslug.plugins.bar.BarPlugin',
    'seaslug.plugins.razum.RazumPlugin',
    'seaslug.plugins.slogan.SloganPlugin',
)

HANDLERS = (
    'seaslug.handlers.CommandParser',
    'seaslug.handlers.CommandFilter',
    'seaslug.handlers.ConsoleLogger',
    'seaslug.handlers.AllMessageHandler',
    'seaslug.handlers.AllCommandHandler',
    'seaslug.handlers.CommandExecuter',
)

DATA_DIR = ''
