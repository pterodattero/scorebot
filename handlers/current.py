#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scorebot
Telegram bot using python-telegram-api
It can manage scoreboeard interactively and display interesting statistics.
Everything is under GNU-GPL.

@author: Stefano Della Morte

This displays the current scores
"""

import telegram.ext as ex


def current(update, context) :
    """
    Shows the current scores
    """
    
    chat_data = context.chat_data
    
    if 'players' not in chat_data or len(chat_data['players']) == 0 :
        message = 'You have to create a game with /newgame first!'
        
    else :
        message = 'Current scores:'
        for player in chat_data['players'] :
            message += '\n' + player + ' ' 
            message += str(chat_data['table'][player].sum())

    context.bot.send_message(chat_id=update.effective_chat.id, text = message)


handler = ex.CommandHandler('current', current)  

