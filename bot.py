import logging
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import requests
import re 
from datetime import datetime
from decouple import config

# Enable logging -------------------------------------------------------------------------
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


# Setting Answers for Keyboard -----------------------------------------------------------
CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)
reply_keyboard = [
    ['Yes', 'No'],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


# Fetch data from API --------------------------------------------------------------------
videoName = 'Falcon Heavy Test Flight (Hosted Webcast)-wbSwFU6tY1c'
urlAPI = 'https://framex-dev.wadrid.net/api/video/{}/?format=json'.format(videoName)
encodedURL = urlAPI.replace(" ", "%20")

resp = requests.get(url=encodedURL)
videoData = resp.json()

# Global Variables ------------------------------------------------------------------------
left = 0
n = videoData['frames'] # Where n is the total of frames
right = n - 1
val=0
mid=0
alreadyStarted = False # Avoids the mid recalculation on the first iteration

# Prepare Data Functions ------------------------------------------------------------------
def getFrame(value):
    specificFrame = encodedURL.replace("?format=json", "frame/{}".format(value))
    return specificFrame

def askQuestion(update, context):
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=getFrame(val))
    update.message.reply_text(
    "Did the rocket launch yet?",
    reply_markup=markup,
    )
    return CHOOSING
    

def calculateMid():
    mid = int((left + right) / 2)
    return mid

def takeOffInfo(frame, update, context):
     return update.message.reply_text("Take of at Frame "+str(frame)+" - "+datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

# Handlers Functions ----------------------------------------------------------------------
def start(update, context):
    global alreadyStarted, right, mid, val, left, n
    val = calculateMid()
    return askQuestion(update, context)
    


def Affirmative_choice(update: Update, context: CallbackContext):
    global alreadyStarted, right, mid, val, left, n
    
    if not alreadyStarted:
        right = mid
        alreadyStarted = True
    elif (right>left+1):
        right = mid
        mid = int((left + right) / 2)
        val = mid
    else:
        return takeOffInfo(right, update, context)

    return askQuestion(update, context)

            
def Negative_choice(update: Update, context: CallbackContext) -> int:
    global alreadyStarted, right, mid, val, left, n
    if(not alreadyStarted):
        left = mid
        alreadyStarted = True
    elif (right>left+1):
        left = mid
        mid = int((left + right) / 2)
        val = mid
    else:
        return takeOffInfo(right, update, context)

    return askQuestion(update, context)


def done(update: Update, context: CallbackContext) -> int:
    return 'Ended'

def main():
    
    updater = Updater(config('BOT_TOKEN'), use_context=True)
    dispatcher = updater.dispatcher
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                MessageHandler(Filters.regex('^(Yes)$'), Affirmative_choice),
                MessageHandler(Filters.regex('^(No)'), Negative_choice),
                
            ],
            TYPING_CHOICE: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Done$')), done
                )
            ]
        },
        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)],
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()


if __name__ == '__main__':
    main()