#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scorebot
Telegram bot using python-telegram-api
It can manage scoreboeard interactively and display interesting statistics.
Everything is under GNU-GPL.

@author: Stefano Della Morte

This is a debug function, not listed in the menus.
Instanciate a random table with three players.
If any argument is passed along with /debug the table is time tracking.
In this case udpates doesn't work because index is not initialized.
"""

import pandas as pd
import datetime
import numpy as np
import telegram.ext as ex

def debug(update, context) :
    
    time = len(context.args) != 0
    
    chat_data = context.chat_data
    
    columns = ['Tizio', 'Caio', 'Sempronio']
    now = datetime.datetime.now()
    hour = datetime.timedelta(hours=1)
    index = [1, 2, 3] if time else [now, now + hour, now + 2*hour]
    
    chat_data['table'] = pd.DataFrame(np.random.randint(10, size=(3,3)),
                                      index=index,
                                      columns=columns)
    chat_data['players'] = columns
    chat_data['index'] = None if time else (datetime.datetime.now() for i in range(30))
    
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Debug scoreboard loaded.')
    
    
handler = ex.CommandHandler('debug', debug, pass_args=True)