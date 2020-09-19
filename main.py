#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scorebot
Telegram bot using python-telegram-api
It can manage scoreboeard interactively and display interesting statistics.
Everything is under GNU-GPL.

@author: Stefano Della Morte

This is the main script of the program. Main guidelines:
    * the table is a pd.DataFrame, each update is a row
    * if the update is asynchronous (one player) the others' values are NaN
    * Menus are implemented as tg.ReplyKeyboardMarkup objects
"""

import telegram.ext as ex
import logging


# Set up the logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot's token
TOKEN = "YOUR_TOKEN"

# Instanciate the main agents:

# The persistance cares about storing files permanently to dicts
# This bot only makes use of data related to the chat were it is used.
persistence = ex.DictPersistence(store_bot_data=False,
                                 store_chat_data=True,
                                 store_user_data=False)

# The updater is a front-end for Telegram, continuosly fetching updates
updater = ex.Updater(token=TOKEN, use_context=True, persistence=persistence)

# The dispatcher is the front-end for the programmer, based on handlers
dispatcher = updater.dispatcher

# This turns on the updater using Polling (alternative to WebHook)
updater.start_polling()


#%% Handlers importation

# Each file .py contains an object handler of type telegram.ext.Handler
from handlers import start, newgame, addplayer, removeplayer, current, update,\
    updateall, undo, stats, debug

# All handlers must be added to the dispatcher
# Each one is documented in its file
    
dispatcher.add_handler(start.handler)
dispatcher.add_handler(newgame.handler)
dispatcher.add_handler(addplayer.handler)
dispatcher.add_handler(removeplayer.handler)
dispatcher.add_handler(current.handler)
dispatcher.add_handler(update.handler)
dispatcher.add_handler(updateall.handler)
dispatcher.add_handler(undo.handler)
dispatcher.add_handler(stats.handler)
dispatcher.add_handler(debug.handler)


#%% Stopping and restarting the updater

"""
One important feature of this bot is its persistence through time. To achieve
this the updater must never be reinitiated, but at least stopped and restarted.
It can be stopped using udpater.idle() in the same console main.py is running
and then using Keyboard Interruption.
Remember to flush the dispatcher's handlers list to avoid duplicates using
dispatcher.clear().
"""