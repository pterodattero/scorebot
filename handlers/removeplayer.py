#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scorebot
Telegram bot using python-telegram-api
It can manage scoreboeard interactively and display interesting statistics.
Everything is under GNU-GPL.

@author: Stefano Della Morte

This allows to remove a player in any moment.
"""

import telegram.ext as ex
import telegram as tg


NAME = range(1)

def start(update, context) :
    """
    Prompt a keyboard to select the player to remove.
    """
    
    chat_data = context.chat_data
    
    # Create the keyboard
    cols = 2
    buttons = []
    for i, player in enumerate(chat_data['players']) :
        if i%cols == 0 :
            buttons.append([player])
        else :
            buttons[-1].append(player)   
    
    keyboard = tg.ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True)

    # Mark up the keyboard
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Who?",
                             reply_markup=keyboard)
    
    return NAME


def name(update, context) :
    """
    Collect the response and if present in players list deletes it.
    """
    chat_data = context.chat_data
    
    player = update.message.text
    
    if player not in chat_data['players'] :
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Invalid name.",
                                 reply_markup=tg.ReplyKeyboardRemove())
        
    else :
    
        chat_data['players'].remove(player)
        chat_data['table'].drop(columns=[player], inplace=True)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Removed.') 
    
    return ex.ConversationHandler.END


def cancel(update, context) :
    """
    Fallback function.
    """
    
    context.bot.send_message(chat_id=update.effective_chat.id, text='Aborted.')
    return ex.ConversationHandler.END
    
    
handler = ex.ConversationHandler(
    
    entry_points=[ex.CommandHandler('removeplayer', start)],
    
    states={NAME : [ex.MessageHandler(ex.Filters.text & ~ex.Filters.command, name)]},
    
    fallbacks=[ex.CommandHandler('cancel', cancel)]
    
)
