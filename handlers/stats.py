#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scorebot
Telegram bot using python-telegram-api
It can manage scoreboeard interactively and display interesting statistics.
Everything is under GNU-GPL.

@author: Stefano Della Morte

This prompts a menu that allows to choose between available statistics.
"""

import telegram as tg
import telegram.ext as ex
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


MENU, CLASSIC2, DISTRIBUTION2 = range(3)


def start(update, context) :
    """
    Check if a game is on. In case prompt a keyboard to choose between stats.
    """
    if 'table' not in context.chat_data :
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Choose an option:")
        return ex.ConversationHandler.END
    
    
    buttons = [['Plots', 'Classic statistics'],
               ['Distribution', 'Dominance']]
    keyboard = tg.ReplyKeyboardMarkup(buttons,
                                      one_time_keyboard=True,
                                      resize_keyboard=True)
    
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Choose an option:",
                             reply_markup=keyboard)
    
    return MENU


def plots(update, context) :
    """
    Send plot of cumsums.
    """
    chat = context.chat_data
    
    df = chat['table'].cumsum()
    
    plt.clf()
    df.plot()
    
    # All images are saved to temp.png to save memory on the server
    plt.savefig('temp.png')
    with open('./temp.png', 'rb') as photo :
        context.bot.send_photo(chat_id=update.effective_chat.id,
                               photo = photo,
                               reply_markup=tg.ReplyKeyboardRemove())
    
    return ex.ConversationHandler.END


def classic1(update, context) :
    """
    Create a keyboard to select the player you want to analyse.
    """
    chat = context.chat_data
    
    # Create keyboard    
    cols = 2
    buttons = []
    playerz = chat['players'].copy()
    playerz.append('All')
    for i, player in enumerate(playerz) :
        if i%cols == 0 :
            buttons.append([player])
        else :
            buttons[-1].append(player)
            
    
    keyboard = tg.ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Choose player:',
                             reply_markup=keyboard)
    
    return CLASSIC2


def classic2(update, context) :  
    """
    Display statistics of chosen player ar all players.
    """
    chat = context.chat_data
    choice = update.message.text
        
    if choice == 'All' :
        choice = 'all players'
        df = chat['table'].cumsum().values.flatten().tolist()
    elif choice not in chat['players'] :
        return ex.ConversationHandler.END
    else :
        df = chat['table'][choice].cumsum()
        
    
    message = f'Statistics for {choice}.\n'
    message += f'Mean: {np.round(np.mean(df))}' + '\n'
    message += f'St. Dev.: {np.round(np.std(df))}' + '\n'
    message += f'Min: {np.min(df)}' + '\n'
    message += f'Max: {np.max(df)}'

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=message,
                             reply_markup=tg.ReplyKeyboardRemove())
    
    return ex.ConversationHandler.END


def distribution1(update, context) :
    """
    Prompt a keyboard to select the player.
    """
    chat = context.chat_data
    
    # Create keyboard    
    cols = 2
    buttons = []
    for i, player in enumerate(chat['players']) :
        if i%cols == 0 :
            buttons.append([player])
        else :
            buttons[-1].append(player)
            
    
    keyboard = tg.ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Choose player',
                             reply_markup=keyboard)
    
    return DISTRIBUTION2


def distribution2(update, context) :
    """
    Plots the histogram of the selected players cumulative points.
    """
    chat = context.chat_data
    choice = update.message.text
    
    if choice not in chat['players'] :
        return ex.ConversationHandler.END
    else :
        df = chat['table'][choice].cumsum()
       
    plt.clf()
    df.plot(kind='hist')
    plt.savefig('temp.png')
        
    with open('./temp.png', 'rb') as photo :
        context.bot.send_photo(chat_id=update.effective_chat.id,
                               photo = photo,
                               reply_markup=tg.ReplyKeyboardRemove())
        
    return ex.ConversationHandler.END
    

def dominance(update, context) :
    """
    Displays how many turns or how much time each player leaded the competition.
    """
    chat = context.chat_data
    df = chat['table']
            
    # We have to calculate time intervals here
    if chat['index'] is not None :
        args = df.idxmax(axis=1)
        difs = -pd.Series(args.index).diff(periods=-1)
        doms = pd.DataFrame([args, difs]).T
        doms = doms.groupby(0).sum()
        unit = ''
    
    # Here it's just a count of turns
    else :
        doms = df.idxmax(axis=1)
        unit = ' turns'   
        
    message = 'Dominators are:'
    for player in doms.index :
        message += '\n' + player + ' ' + str(doms[1].loc[player]) + unit
        
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=message,
                             reply_markup=tg.ReplyKeyboardRemove())    
    
    return ex.ConversationHandler.END


def cancel(update, context) :
    """
    Fallback function.
    """
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Aborted.',
                             reply_markup=tg.ReplyKeyboardRemove())
    
    return ex.ConversationHandler.END


handler = ex.ConversationHandler(
    
    entry_points=[ex.CommandHandler('stats', start)],
    
    states={MENU : [ex.MessageHandler(ex.Filters.text(['Plots']),
                                            plots),
                          ex.MessageHandler(ex.Filters.text(['Classic statistics']),
                                            classic1),
                          ex.MessageHandler(ex.Filters.text(['Distribution']),
                                            distribution1),
                          ex.MessageHandler(ex.Filters.text(['Dominance']),
                                            dominance)
                          ],
            CLASSIC2 : [ex.MessageHandler(ex.Filters.text,
                                          classic2)],
            DISTRIBUTION2 : [ex.MessageHandler(ex.Filters.text,
                                               distribution2)]
            },
    
    fallbacks=[ex.Filters.all, cancel]
)