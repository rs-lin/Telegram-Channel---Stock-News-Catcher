telegram_token={YOUR TOKEN}

import telegram
import logging
import pandas as pd
import json
import datetime
import urllib.request

import schedule,time

import datetime

import smtplib

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename = '{ROOT PATH}/newsCatcher.log',
                     level=logging.INFO)

logger = logging.getLogger(__name__)

# list of news that's already sent
sent_list=[]
# dict to record like and dislike
like_dict={}

def listToString(s):

    str1 = " "
    return (str1.join(s))

def make_alert(context):
    job = context.job
    with open({PATH TO THE SCRAPED NEWS FILE}) as f:
        latest_news = json.load(f)

    for news in latest_news['data']:
        if news['news_url'] not in sent_list:
            try:
                keyboard = telegram.InlineKeyboardMarkup([[InlineKeyboardButton('\N{thumbs up sign}',callback_data='\N{thumbs up sign} '+news['news_url']), InlineKeyboardButton('\N{thumbs down sign}',callback_data='\N{thumbs down sign} '+news['news_url'])]])
                like_dict['\N{thumbs up sign} '+news['news_url']]=0
                like_dict['\N{thumbs down sign} '+news['news_url']]=0
                context.bot.send_message(
                    job.context, text="<b>"+listToString(news['tickers'])+"</b>"+"\n"+"[Sentiment] "+news['sentiment']+"\n"+"[Title] "+news['title']+":\n"+"[Summary] "+news['text']+'\n'+news['news_url'],parse_mode=telegram.ParseMode.HTML,reply_markup=keyboard)
                sent_list.append(news['news_url'])
                context.bot.send_message(chat_id={TELEGRAM CHANNEL ID},text="<b>"+listToString(news['tickers'])+"</b>"+"\n"+"[Sentiment] "+news['sentiment']+"\n"+"[Title] "+news['title']+":\n"+"[Summary] "+news['text']+'\n'+news['news_url'],parse_mode=telegram.ParseMode.HTML,reply_markup=keyboard)
            except:
                keyboard = telegram.InlineKeyboardMarkup([[InlineKeyboardButton('\N{thumbs up sign}',callback_data='\N{thumbs up sign} '+news['news_url']), InlineKeyboardButton('\N{thumbs down sign}',callback_data='\N{thumbs down sign} '+news['news_url'])]])
                like_dict['\N{thumbs up sign} '+news['news_url']]=0
                like_dict['\N{thumbs down sign} '+news['news_url']]=0
                context.bot.send_message(
                    job.context, text="<b>"+listToString(news['tickers'])+"</b>"+"\n"+"[Sentiment] "+news['sentiment']+"\n"+"[Title] "+news['title']+":\n"+news['news_url'],parse_mode=telegram.ParseMode.HTML)
                sent_list.append(news['news_url'])
                context.bot.send_message(chat_id={TELEGRAM CHANNEL ID},text="<b>"+listToString(news['tickers'])+"</b>"+"\n"+"[Sentiment] "+news['sentiment']+"\n"+"[Title] "+news['title']+":\n"+news['news_url'],parse_mode=telegram.ParseMode.HTML)

def promote(context):
    job = context.job
    context.bot.send_message(chat_id={TELEGRAM CHANNEL ID},text="Welcome to Stock News Catcher Series! Nothing but the excitement of realtime market news in you!\n\nKnow someone who would benefit from the content? Invite them over /n https://t.me/USstockNews")
    context.bot.send_message(chat_id={TELEGRAM CHANNEL ID},text="If you have preferences over a few sectors of the stock market, check out the following channels, each dedicated to the sector of\n"+
    '\N{white right pointing backhand index} Basic Materials (https://t.me/basicMaterialsNews)\n'+
    '\N{white right pointing backhand index} Conglomerates (https://t.me/conglomeratesSector)\n'+
    '\N{white right pointing backhand index} Consumer Goods (https://t.me/ConsumerGoodsNews)\n'+
    '\N{white right pointing backhand index} Financial (https://t.me/FinancialSectorNews)\n'+
    '\N{white right pointing backhand index} Healthcare (https://t.me/HealthcareStockNews)\n'+
    '\N{white right pointing backhand index} Industrial Goods (https://t.me/IndustrialGoodsNews)\n'+
    '\N{white right pointing backhand index} Real Estate (https://t.me/realEstateSectorNews)\n'+
    '\N{white right pointing backhand index} Services (https://t.me/StockNewsServices)\n'+
    '\N{white right pointing backhand index} Technology (https://t.me/TechnologyStockNews)\n'+
    '\N{white right pointing backhand index} Utilities (https://t.me/utilitiesSector)'+
    '\n\nYou can rate your experience with this channel and provide feedback at @Listen_to_feedback_bot 🤖'+
    '\n\nJoin the discussion group chat at @StockNewsCatcher'+
    '\n\nIf you like this channel, please with anyone that might be interested in\N{person raising both hands in celebration}'+
    '\n\nHave a good one!')
def daily_top_mention(context):
    job=context.job
    with open({PATH TO THE TOP MENTIONED FILE}) as f:
        top_mention=json.load(f)
    msg="Top mentioned tickers today\n"
    for each in top_mention['data']['all']:
        num=top_mention['data']['all'].index(each)+1
        msg=msg+str(num)+". "+each['ticker']+'\t'+each['name']+"\t"+"total mention: "+str(each['total_mentions'])+"\n"
    try:
        context.bot.send_message(
            chat_id={TELEGRAM CHANNEL ID},text=msg
        )
    except:
        pass
def promote_bot(context):
    job = context.job
    context.bot.send_message(chat_id={TELEGRAM CHANNEL ID},text="For more customization, please visit @stockNewsAlert_bot. Subscribe to your favorite tickers and receive alerts. Please spread the word!")
def button(update, context):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    #query.answer()

    # '\N{thumbs up sign} '+news['news_url']
    user_data = query.data.split(' ')
    query.answer(text="You {} this".format(user_data[0]))

    if user_data[0]=='\N{thumbs up sign}':
        like_dict[query.data]+=1
        keyboard=telegram.InlineKeyboardMarkup([[InlineKeyboardButton('\N{thumbs up sign}'+str(like_dict[query.data]),callback_data='\N{thumbs up sign} '+user_data[1]), InlineKeyboardButton('\N{thumbs down sign}'+str(like_dict['\N{thumbs down sign} '+user_data[1]]),callback_data='\N{thumbs down sign} '+user_data[1])]])
        query.edit_message_reply_markup(reply_markup=keyboard)
    if user_data[0]=='\N{thumbs down sign}':
        like_dict[query.data]+=1
        keyboard=telegram.InlineKeyboardMarkup([[InlineKeyboardButton('\N{thumbs up sign}'+str(like_dict['\N{thumbs up sign} '+user_data[1]]),callback_data='\N{thumbs up sign} '+user_data[1]), InlineKeyboardButton('\N{thumbs down sign}'+str(like_dict[query.data]),callback_data='\N{thumbs down sign} '+user_data[1])]])
        query.edit_message_reply_markup(reply_markup=keyboard)
def start(update, context):
    chat_id = update.message.chat_id
    try:
        if 'job' in context.chat_data:
            old_job = context.chat_data['job']
            old_job.schedule_removal()

        new_job = context.job_queue.run_repeating(make_alert,30,context=chat_id)
        t1 = datetime.time(22,20,00,0000)
        t2 = datetime.time(9,25,00,0000)
        daily_job = context.job_queue.run_daily(promote,t2,days=(0,1,2,3,4,5,6),context=chat_id)
        daily_job_2 = context.job_queue.run_daily(promote,t1,days=(0,1,2,3,4,5,6),context=chat_id)
        daily_job_3 = context.job_queue.run_daily(daily_top_mention,t1,days=(0,1,2,3,4,5,6),context=chat_id)
        context.chat_data['job'] = [new_job,daily_job,daily_job_2,daily_job_3]
        #update.message.reply_text('News alerts successfully set!')
    except:
        update.message.reply_text("An error has occured setting up the news alerts")

def main():
    sent_list=[]
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(telegram_token, use_context=True)


    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
