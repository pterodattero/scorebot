#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scorebot
Telegram bot using python-telegram-api
It can manage scoreboeard interactively and display interesting statistics.
Everything is under GNU-GPL.

@author: Stefano Della Morte

This is the instructions handler.
"""

import telegram.ext as ex


def start(update, context) :
    
    message =  'Hello!\nThis is a scoreboard bot. '
    message += 'I can keep track of any kind of score. These ar my commands:\n'
    message += '/newgame Create a new game scoreboard\n'
    message += '/addplayer Add a player when you want\n'
    message += '/removeplayer Remove a player when you want\n'
    message += '/update Update the scores of a single player\n'
    message += '/updateall Update the scores of all players\n'
    message += '/undo Forget the last update'
    message += '/current See the current scores\n'
    message += '/stats See the stats of the game\n\n'
    message += '/cancel Interrupt the current operation'
    
    message += 'I can also keep track of the time the scores were updated.'
    message += 'If the challenge lasts through time you can see the temporal '
    message += 'trends of the scores in the stats.'
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


handler = ex.CommandHandler('start', start)
