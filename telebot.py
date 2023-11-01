import logging
from aiogram import Bot,Dispatcher,types,executor
from dotenv import load_dotenv
import os
import openai
import sys



class Reference :
    '''
    A class to store previouly response from chatGPT API 
    '''
    
    def __init__(self)-> None:
        self.response=""
        
        
        


load_dotenv()
openai.api_key=os.getenv("OPENAI_API_KEY")
reference=Reference()

TOKEN=os.getenv("TOKEN")

#model name
MODEL_NAME="gpt-3.5-turbo"

#Initialize bot and dispatcher

bot=Bot(token=TOKEN)
dispatcher=Dispatcher(bot)

def clear_past():
    '''
    this function clear cprevious context and conversation
    '''
    reference.response=""
    
@dispatcher.message_handler(commands=['start'])
async def welcome(message:types.Message)->None:
    """This handler recieves messages with '/start'  command
    """
    await message.reply("Hi\nI am Tele Bot!\ Created By Rajat.How can i assist you?")

@dispatcher.message_handler(commands=['help'])
async def clear(message:types.Message)->None:
    """This handler display help menu
    """
    help_command='''
    Hi there, I'm chatGPT Telegram bot created by Rajat! Please follow these commands -
    /start - to start the conversation.
    /clear - to clear the past the conversation and context.
    /help - to get this help menu
    I hope this helps. :)
    '''
    await message.reply(help_command)
    

@dispatcher.message_handler(commands=['clear'])
async def clear(message:types.Message)->None:
    """This handler recieves messages with '/start'  command
    """
    clear_past()
    await message.reply("I have cleared past conversation and context")

@dispatcher.message_handler()
async def chatgpt(message:types.Message):
    """
    A handler to process the user's input and generate a response using the chatGPT API.
    """
    print(f">>>USER:\n\t{message.text}")
    response=openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=[
            {"role":"assistant","content":reference.response}, # role assistant
            {"role":"user","content":message.text} #our query
        ]
    )
    reference.response=response['choices'][0]['message']['content']
    print(f">>> chatGPT: \n\t {reference.response}")
    await bot.send_message(chat_id=message.chat.id,text=reference.response)

if __name__ =="__main__":
    executor.start_polling(dispatcher,skip_updates=True)