#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scorebot
Telegram bot using python-telegram-api
It can manage scoreboeard interactively and display interesting statistics.
Everything is under GNU-GPL.

@author: Stefano Della Morte

This is for updating all players scores.
"""

import telegram.ext as ex
import pandas as pd


UPDATEALL_POINTS = range(1)

def updateall_start(update, context) :
    """
    Check if a game is on, in case sends the name of the first player to update.
    """
    chat = context.chat_data

    if 'table' not in chat or chat['table'] is None :
        message = "You have to create a game with /newgame first!"
        context.bot.send_message(chat_id=update.effective_chat.id, text = message)
        
        return ex.ConversationHandler.END
    
    
    message = 'Enter the point to add ("-" to subtract) for each player:'
    context.bot.send_message(chat_id=update.effective_chat.id, text = message)

    chat['scorelist'] = []
    chat['cursor2'] = 0
    
    context.bot.send_message(chat_id=update.effective_chat.id, text = chat['players'][chat['cursor2']])
    
    return UPDATEALL_POINTS


def updateall_points(update, context) :
    """
    Store the previous response after checking and asks for the next. If the
    previous response was about the last player stores the info.
    """
    chat = context.chat_data
    
    score = update.message.text
    if score.isdigit() :
        score = int(score)
    elif score[0] == '-' and len(score) > 1 and score[1:].isdigit() :
        score = - int(score[1:])
    else :
        context.bot.send_message(chat_id=update.effective_chat.id, text='Insert a number please')
        return UPDATEALL_POINTS
    
    chat['scorelist'].append(score)
    chat['cursor2'] += 1
    
    # Last player case
    if chat['cursor2'] == len(chat['players']) :
        # Store the data!!        
        score_update = pd.DataFrame([chat['scorelist']],
                                    columns=chat['players'],
                                    index=[None if chat['index'] is None else next(chat['index'])])
        chat['table'] = chat['table'].append(score_update)
        if chat['index'] is None :
            chat['table'].reset_index()
        
        context.bot.send_message(chat_id=update.effective_chat.id, text='Updated.')
        return ex.ConversationHandler.END
    
    context.bot.send_message(chat_id=update.effective_chat.id, text = chat['players'][chat['cursor2']])
    return UPDATEALL_POINTS


def updateall_cancel(update, context) :
    """
    Fallback function.
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text='Aborted.')
    return ex.ConversationHandler.END


    
handler = ex.ConversationHandler(

    entry_points=[ex.CommandHandler('updateall', updateall_start)],
    
    states={UPDATEALL_POINTS : [ex.MessageHandler(~ex.Filters.command & ex.Filters.text, updateall_points)]},
    
    fallbacks=[ex.CommandHandler('cancel', updateall_cancel)]
    
)