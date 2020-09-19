#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scorebot
Telegram bot using python-telegram-api
It can manage scoreboeard interactively and display interesting statistics.
Everything is under GNU-GPL.

@author: Stefano Della Morte

This contains the conversation for asynchronous update (one player only).
"""

import telegram as tg
import telegram.ext as ex
import pandas as pd


# States of the conversation
PLAYER, POINTS = range(2)

def start(update, context) :
    """
    Starts the conversation asking for the players of the update.
    Also checks if a game is on.
    """
    chat = context.chat_data
    
    if 'table' not in chat or chat['table'] is None \
        or len(chat['players']) == 0 :
        message = "You have to create a game with /newgame first!"
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text = message)
        
        return ex.ConversationHandler.END
    
    # Create keyboard    
    cols = 2
    buttons = []
    for i, player in enumerate(chat['players']) :
        if i%cols == 0 :
            buttons.append([player])
        else :
            buttons[-1].append(player)   
    
    keyboard = tg.ReplyKeyboardMarkup(buttons,
                                      one_time_keyboard=True,
                                      resize_keyboard=True)
    
    
    # Show keyboard of players
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text = 'Choose the player:',
                             reply_markup=keyboard)
    
    return PLAYER


def player(update, context) : 
    """
    Store player info and ask for points to add.
    """
    chat = context.chat_data
    chat['cursor'] = update.message.text
    
    update.message
    
    if chat['cursor'] not in chat['players'] :
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text = 'Insert a valid player!')
        return PLAYER
    
    # Insert points
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Scores to add ("-" to subtract):')
    
    return POINTS


def points(update, context) :
    """
    Interpret the response and store it if valid.
    """    
    chat=context.chat_data
    
    # Store points info
    score = update.message.text
    
    # Positive update case
    if score.isdigit() :
        score = int(score)
    # Negative update case
    elif score[0] == '-' and len(score) > 1 :
        score = - int(score[1:])
    # Not valid case
    else :
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Insert a number please.')
        return POINTS
    
    # Create the row to append
    score_update = pd.DataFrame(columns=chat['players'],
                                index=None if chat['index'] is None else [next(chat['index'])])
    score_update[chat['cursor']] = score
    score_update = score_update.fillna(0)          
      
    # In absence of time tracking the index must be reset
    chat['table'] = chat['table'].append(score_update) 
    if chat['index'] is None :
            chat['table'].reset_index()

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Updated.')
    
    return ex.ConversationHandler.END             

    
def cancel(update, context) :
    """
    Fallback function.
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text='Aborted.')
    
    return ex.ConversationHandler.END
    
    
handler = ex.ConversationHandler(

    entry_points=[ex.CommandHandler('update', start)],

    states={PLAYER: [ex.MessageHandler(~ex.Filters.command & ex.Filters.text, player)],
            POINTS: [ex.MessageHandler(~ex.Filters.reply & ex.Filters.text, points)]},

    fallbacks=[ex.CommandHandler('cancel', cancel)]
)