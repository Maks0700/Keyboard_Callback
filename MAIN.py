#Welcome to aiogram 3.10 YEEEEEEEEEEEEEEAAAAAAAAAAAAAAAHHHHHHHHHHHHHHHHHHHHH
import asyncio
from aiogram import Bot,Dispatcher,F #Magic F (filter) for simply checking text
from aiogram.types import Message,CallbackQuery
from dotenv import load_dotenv
import os
from pprint import pprint
from aiogram.filters import Command,CommandObject,CommandStart
from random import randint
from aiogram.enums.dice_emoji import DiceEmoji #emoji
from KEYBOARDS import CallButtons,Property,ProductCallbackData,ProductCallDescription
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
from aiogram.enums import ContentType
from KEYBOARDS import keyboard_start,list_products,product_details_kb,keyboard_update
from aiogram.utils import markdown

load_dotenv(".env")







bot=Bot(os.getenv("api"),parse_mode="Markdown")
dp=Dispatcher()





@dp.message(CommandStart())
async def process_cmd(message:Message):
    await message.answer("Info",reply_markup=keyboard_start())
    
    

@dp.callback_query(CallButtons.filter(F.action==Property.products))
async def process(call:CallbackQuery):
    
        await call.message.answer(text="Available products",reply_markup=list_products())
    


@dp.callback_query(CallButtons.filter(F.action==Property.root))
async def process(call:CallbackQuery):
    
        await call.message.answer(text="Available products",reply_markup=keyboard_start())
    
@dp.callback_query(ProductCallbackData.filter(F.action==ProductCallDescription.details))
async def process(call:CallbackQuery,callback_data:ProductCallbackData):
    message_text=(f"*Product № {callback_data.id}\nTitle {callback_data.title}\nPrice {callback_data.price}*")
    
        
    
    await call.message.edit_text(text=message_text,reply_markup=product_details_kb(callback_data))
    


@dp.callback_query(ProductCallbackData.filter(F.action==ProductCallDescription.delete))
async def handle_product_delete(call:CallbackQuery,callback_data:ProductCallbackData):
    message_text="Delete is progress!!"
    
        
    
    await call.answer(text=message_text,reply_markup=product_details_kb(callback_data))




@dp.callback_query(ProductCallbackData.filter(F.action==ProductCallDescription.update))
async def handle_product_update(call:CallbackQuery,callback_data:ProductCallbackData):
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=keyboard_update(callback_data))
    
    
    
    
async def main():
    try:
        await bot.delete_webhook(drop_pending_updates=True)# for skip all update
        pprint("Bot is success!!")
        await dp.start_polling(bot)
    except Exception:
        return -1


    
    

if __name__=="__main__":
    asyncio.run(main())