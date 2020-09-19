#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scorebot
Telegram bot using python-telegram-api
It can manage scoreboeard interactively and display interesting statistics.
Everything is under GNU-GPL.

@author: Stefano Della Morte

This allows to initiate a new scoreboard.
"""

import telegram.ext as ex
import telegram as tg
import pandas as pd
import datetime as dt


# Conversation states
PLAYER, TIME = range(2)


def start(update, context) :
    """
    Initiate a scoreboard and ask for players' names.
    """
    
    message = 'Please send players name one by one. '
    message += 'Digit /ok once you have finished.'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    
    chat = context.chat_data
    chat['players'] = []
    
    return PLAYER

    
def newplayer(update, context) :
    """
    Store players names.
    """
    
    chat = context.chat_data
    chat['players'].append(update.message.text)
    
    return PLAYER
    

def ok(update, context) :
    """
    End the collection of names, ask for temporal tracking.
    """    
    chat = context.chat_data
    chat['table'] = pd.DataFrame({player: [] for player in chat['players']})
    
    message = 'Superduper. One last thing: '
    message += 'do you wanna keep track of time the score are modified?'
    
    keyboard = tg.ReplyKeyboardMarkup([['Yes','No']],
                                      resize_keyboard=True,
                                      one_time_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=message,
                             reply_markup=keyboard)

    return TIME


def time(update, context) :
    """
    According to the user choice, set the index generator for the scoreboard.
    """
    
    chat = context.chat_data
    if update.message.text == 'Yes' :
        def now_generator() :
            while True :
                yield dt.datetime.now()
        chat['index'] = now_generator()
    else :   
        chat['index'] = None

                                  
    message = 'Got it! Now you can change scores using /update or /updateall.'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=message,
                             reply_markup=tg.ReplyKeyboardRemove())
    
    return ex.ConversationHandler.END


def cancel(update, context) :
    """
    Fallback function.
    """
    
    context.bot.send_message(chat_id=update.effective_chat.id, text='Aborted.')
    return ex.ConversationHandler.END



handler = ex.ConversationHandler(
    
    entry_points=[ex.CommandHandler('newgame', start)],
    
    states={PLAYER: [ex.MessageHandler(ex.Filters.text & ~ex.Filters.command,
                                       newplayer),
                     ex.CommandHandler('ok', ok)],
            TIME: [ex.MessageHandler(ex.Filters.text(['Yes','No']), time)]},
    
    fallbacks=[ex.CommandHandler('cancel', cancel)]    
)  
