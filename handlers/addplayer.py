#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scorebot
Telegram bot using python-telegram-api
It can manage scoreboeard interactively and display interesting statistics.
Everything is under GNU-GPL.

@author: Stefano Della Morte

This allows to add a player on the fly when a game is already on.
"""

import telegram.ext as ex
import numpy as np

NAME = range(1)

def start(update, context) :
    """
    Starts the conversation asking for player's name.
    """
    
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Enter new player's name:")
    
    return NAME


def name(update, context) :
    """
    Stores the player's name. If already used ask for a different one.' 
    """    
    chat_data = context.chat_data
    
    new_player = update.message.text
    
    if new_player in chat_data['players'] :
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="This name is already used. Try a different one.")
        
        return NAME
    # Add the player in the list and instance a NaN column for her/him
    chat_data['players'].append(new_player)
    chat_data['table'][new_player] = np.nan
    
    context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Added.')    
    return ex.ConversationHandler.END


def cancel(update, context) :
    """
    Fallback function.
    """
    return ex.ConversationHandler.END
    
    
handler = ex.ConversationHandler(
    
    entry_points=[ex.CommandHandler('addplayer', start)],
    
    states={NAME : [ex.MessageHandler(ex.Filters.text & ~ex.Filters.command, name)]},
    
    fallbacks=[ex.CommandHandler('cancel', cancel)]
    
)
