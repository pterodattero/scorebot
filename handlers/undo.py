#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scorebot
Telegram bot using python-telegram-api
It can manage scoreboeard interactively and display interesting statistics.
Everything is under GNU-GPL.

@author: Stefano Della Morte

This allows to undo last update.
"""

import telegram.ext as ex

def undo(update, context) :
    """
    Checks if there are updates to undo and do it.
    """
    chat_data = context.chat_data
    
    if 'table' not in chat_data or chat_data['table'].shape[0] == 0 :
        
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="There's nothing to undo.")
        
    else:
        
        chat_data['table'] = chat_data['table'].iloc[:-1]

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Last edit undone.")
        

handler = ex.CommandHandler('undo', undo)