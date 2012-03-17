# -*- coding: utf-8 -*-

import logging
logging.basicConfig(format='[%(name)s]%(thread)d  %(levelname)s: %(message)s', level=logging.INFO)
logging.getLogger('').setLevel(logging.DEBUG)
logging.getLogger('app').setLevel(logging.DEBUG)
logging.getLogger('handlers').setLevel(logging.DEBUG)
logging.getLogger('SkypeMessenger').setLevel(logging.DEBUG)

from seaslug.core.application import application
