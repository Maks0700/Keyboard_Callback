from aiogram.types import(
    ReplyKeyboardMarkup,KeyboardButton,
    InlineKeyboardMarkup,InlineKeyboardButton,
    KeyboardButtonPollType # This is class for poll user
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder,InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from random import randint
from enum import Enum,auto,IntEnum
from aiogram.enums.dice_emoji import DiceEmoji


class Property(IntEnum):
    products=auto()
    address=auto()
    root=auto()
    
    
    
class CallButtons(CallbackData,prefix="callback_update "):
    action:int
    

class ProductCallDescription(IntEnum):
    details=auto()
    update=auto()
    delete=auto()
    
class ProductCallbackData(CallbackData,prefix="products_call_data"):
    action:ProductCallDescription
    id:int
    title:str
    price:int   


def keyboard_start():
    keyboard=InlineKeyboardBuilder()
    
    keyboard.button(
        text="Click on address",callback_data=CallButtons(action=Property.address).pack()
        
    )
    keyboard.button(
        text="Click on products",callback_data=CallButtons(action=Property.products).pack()
    )
    keyboard.adjust(1)
    return keyboard.as_markup()

def list_products():
    keyboard=InlineKeyboardBuilder()
    keyboard.button(text="Back to menu",
                    callback_data=CallButtons(action=Property.root).pack()
                    )
    for index, (name,value) in enumerate([
        ("Sneakers",1000),
        ("Computers",2000),
        ("Books",2500)
    ],start=1):
        keyboard.button(text=name,
                        callback_data=ProductCallbackData(action=ProductCallDescription.details,
                                                          id=index,
                                                          title=name,
                                                          price=value)
                        )
        
    keyboard.adjust(1)
    
    return keyboard.as_markup()


def product_details_kb(product_cb_data:ProductCallbackData):
    keyboard=InlineKeyboardBuilder()
    keyboard.button(
        text="Back to menu",
        callback_data=CallButtons(action=Property.products)
    )
    for label,act in [("Update",ProductCallDescription.update),
                          ("Delete",ProductCallDescription.delete)]:
        keyboard.button(
            text=label,
            callback_data=ProductCallbackData(action=act,**product_cb_data.model_dump(include={"id","title","price"})).pack()
        )      
        
    
    keyboard.adjust(1,2)
    return keyboard.as_markup()

def keyboard_update(update_callback_data:ProductCallbackData)->InlineKeyboardBuilder:
    keyboard=InlineKeyboardBuilder()
    keyboard.button(
        text=f"Back to {update_callback_data.title}",
        callback_data=ProductCallbackData(action=ProductCallDescription.details,**update_callback_data.model_dump(include={"id","title","price"}))
    )
    keyboard.button(
        text="🔄Update",
        callback_data="..."
    )   
    keyboard.adjust(1)
    
    return keyboard.as_markup()





    
    
    

    
    