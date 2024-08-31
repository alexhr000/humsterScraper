import json
from aiogram import Bot, Dispatcher, executor, types

# from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
import os
import time
import asyncio


bot = Bot(token=('6418166216:AAGKaYlY-BxPxNpwXKgihOG7y7sNjt1zxTk'), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)



@dp.message_handler(commands='start')
async def start(message: types.Message):
  
    # получить стартовое время обновления json карточки  
    startTimejson = os.path.getmtime(r"card_info_new.json.")


    while(True):
        lastModify = os.path.getmtime(r"card_info_new.json")
        if(lastModify!=startTimejson):
            startTimejson = lastModify  
            new_bundle_alert = "Вышла новая карточка! 🐹 \n \n"

            with open(r'card_info_new.json',) as file:
                data1  = json.load(file)    
                for item in data1:                   
                    bundle = f'{hbold("Название: ")}{item.get("card_name")}\n{hbold("Прибыль в час: ")}{item.get("hour_profit")}\n{hbold("Стоимость улучшения: ")}{item.get("card_upgrade_price")}\n\n'
                    new_bundle_alert = new_bundle_alert + bundle 
                    # await message.answer(new_bundle_alert)  
                    await bot.send_photo(message.chat.id, photo=item.get("card_img_value"), caption=new_bundle_alert)  
        await asyncio.sleep(3)                   

def main():
        executor.start_polling(dp, skip_updates=True)



if __name__=='__main__':
    main()
