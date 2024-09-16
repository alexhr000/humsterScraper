import json
from aiogram import Bot, Dispatcher, executor, types

# from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
import os
import time
import asyncio
from dotenv import load_dotenv

load_dotenv()
bot_token = os.getenv("BOT_TOKEN")
bot = Bot(token=(bot_token), parse_mode=types.ParseMode.HTML)
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
            await asyncio.sleep(5) 
            with open(r'card_info_new.json', 'r', encoding='utf-8') as file:
                content = file.read().strip()
                if content:
                    try:
                        file.seek(0)  # Возвращаемся в начало файла
                        data1  = json.load(file)    
                        for item in data1:                   
                            bundle = f'{hbold("Название: ")}{item.get("card_name")}\n{hbold("Прибыль в час: ")}{item.get("hour_profit")}\n{hbold("Стоимость улучшения: ")}{item.get("card_upgrade_price")}\n\n'
                            new_bundle_alert = new_bundle_alert + bundle 
                            await bot.send_photo(message.chat.id, photo=item.get("card_img_value"), caption=new_bundle_alert)  
                    except json.JSONDecodeError as e:
                        print(f"Ошибка декодирования JSON: {e}")
                        await asyncio.sleep(5) 

                        with open(r'card_info_new.json', 'r', encoding='utf-8') as file:
                            content = file.read().strip()
                            if content:
                                try:
                                    file.seek(0)
                                    data1  = json.load(file)    
                                    for item in data1:                   
                                        bundle = f'{hbold("Название: ")}{item.get("card_name")}\n{hbold("Прибыль в час: ")}{item.get("hour_profit")}\n{hbold("Стоимость улучшения: ")}{item.get("card_upgrade_price")}\n\n'
                                        new_bundle_alert = new_bundle_alert + bundle 
                                   
                                        await bot.send_photo(message.chat.id, photo=item.get("card_img_value"), caption=new_bundle_alert)  
                                except json.JSONDecodeError as e:
                                    print(f"Ошибка декодирования JSON: {e}")



                else:
                    print("Файл пуст!")
        await asyncio.sleep(3)                   

def main():
        executor.start_polling(dp, skip_updates=True)



if __name__=='__main__':
    main()
