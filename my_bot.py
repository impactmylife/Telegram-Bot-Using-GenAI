from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
import logging
import openai

load_dotenv() # To acess the token
TOKEN = os.getenv("TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Connect with OpenAI
openai.api_key = OPENAI_API_KEY

# print("Ok")

MODEL_NAME = "gpt-3.5-turbo"

#Initialize bot 
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot)

# This would act as a memory
class Reference:
    def __init__(self) -> None:
        self.response = "" # This indicate there would be no response in the first statement or task 


reference = Reference()


def clear_past():
    reference.response = "" # This means that if there is something from the first response, it will forget. It empty it



# The function is called clear, which takes the clear command, it calles the clear_past function and then it will reply that 
# it has clear the first response
@dispatcher.message_handler(commands=['clear'])
async def clear(message: types.Message):
    """
    A handler to clear the previous conversation and context.
    """
    clear_past()
    await message.reply("I've cleared the past conversation and context.") # This is where it replies that is has cleat the first conversation context



# It gives messages to welcome the user as starting a new conversation
@dispatcher.message_handler(commands=['start'])
async def welcome(message: types.Message):
    """This handler receives messages with `/start` or  `/help `command

    Args:
        message (types.Message): _description_
    """
    await message.reply("Hi\nI am a Chat Bot! Created by Eric. How can i assist you?")



# It gives messages to as helper functions 
@dispatcher.message_handler(commands=['help'])
async def helper(message: types.Message):
    """
    A handler to display the help menu.
    """
    help_command = """
    Hi There, I'm a bot created by Eric! Please follow these commands - 
    /start - to start the conversation
    /clear - to clear the past conversation and context.
    /help - to get this help menu.
    I hope this helps. :)
    """
    await message.reply(help_command)




@dispatcher.message_handler()
async def main_bot(message: types.Message):
    """
    A handler to process the user's input and generate a response using the openai API.
    """

    print(f">>> USER: \n\t{message.text}")

    response = openai.ChatCompletion.create(
        model = MODEL_NAME,
        messages = [
            {"role": "assistant", "content": reference.response}, # role assistant
            {"role": "user", "content": message.text} #our query 
        ]
    )
    reference.response = response['choices'][0]['message']['content'] # extracting the content from the message
    print(f">>> chatGPT: \n\t{reference.response}")
    await bot.send_message(chat_id = message.chat.id, text = reference.response) # printing the message in the telegram
    
    





if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=True)