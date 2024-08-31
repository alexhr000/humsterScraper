import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import pickle
import requests
from selenium.webdriver.common.by import By
from typing import List, Dict

options = webdriver.ChromeOptions()
options.add_extension('Violentmonkey.crx')
options.add_argument(r"--user-data-dir=C:\Users\Sergich\AppData\Local\Google\Chrome\User Data") #e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
options.add_argument(r'--profile-directory=Default') #e.g. Profile 3
driver = webdriver.Chrome(options=options)
driver.get('https://github.com/mudachyo/Hamster-Kombat/raw/main/hamster-kombat.user.js')
driver.implicitly_wait(5)
aut = driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div[2]/div[2]/button[1]").click()
driver.implicitly_wait(5)
driver.get('https://web.telegram.org/a/#7018368922')

result = []
old_card_list = []
new_card_list = []
new_card_item_list = []
break_out_flag = False

# запустить миниап
aut = driver.find_element(By.XPATH,"/html/body/div[2]/div/div[2]/div[4]/div[2]/div/div[1]/div/div[4]/div[3]/div[3]/div[2]/div[1]/button/div").click()
driver.implicitly_wait(5)

# подождать загрузку 
time.sleep(5)

# выбрать фрейм миниапа
iframe = driver.find_elements(By.TAG_NAME,'iframe')[0]
driver.switch_to.frame(iframe)
driver.implicitly_wait(5)

# собрать доход
aut = driver.find_element(By.CSS_SELECTOR,"#__nuxt > div > div.bottom-sheet.open > div.bottom-sheet-inner > div.bottom-sheet-scroll > div > button").click()
driver.implicitly_wait(5)


# перейти на вкладку с карточками 
aut = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/nav/a[2]").click()
driver.implicitly_wait(5)           

                           
 # собрать все обычные карточки
i=1
while i<=4:

    aut = driver.find_element(By.XPATH,"/html/body/div[1]/div/main/div[2]/div[3]/div[1]/div["+str(i)+"]").click()
    driver.implicitly_wait(5) 

    
    cards = driver.find_elements(By.CLASS_NAME,"upgrade-item")

    for card in cards:
        card_name = card.find_element(By.CLASS_NAME,"upgrade-item-title").text
        try:
            hour_profit = card.find_element(By.CSS_SELECTOR,".upgrade-buy-stats-info > .price > .price-value").text
        except: 
            hour_profit = 'бесценна'   

        card_upgrade_price = card.find_element(By.CSS_SELECTOR,".upgrade-item-detail").text  
        try:
            card_lvl = card.find_element(By.CSS_SELECTOR,".upgrade-item-level > span").text   
        except: '0 lvl' 
   
        card_name_lower = card_name.lower().replace(" ", "_")  
        print(card_name_lower)   
        try:                                 
            card_img = card.find_element(By.CSS_SELECTOR,"img[alt=" + card_name_lower +"]")
            card_img_value = card_img.get_attribute("src")
        except:
            
            # если вместо картинки svg
            card_img_value = "https://pic.rutubelist.ru/video/2d/ed/2dedaea8149558b798972c66bc1eda9b.jpg"   

        if card_name!='':
            result.append(
                    {
                        'card_name': card_name,
                        'hour_profit': hour_profit,
                        'card_upgrade_price': card_upgrade_price,
                        'card_lvl' :card_lvl,
                        'card_img_value' :card_img_value

                    }
                ) 

    i=i+1


print('закончил парсинг, перехожу к сравнению')

# сравнение новой информации с имеющиеся 
# записать названия бандлов в словари, новую информацию берет из результатов парсинга, старую с json

with open(r'card.json', encoding="utf-8") as file:
    data  = json.load(file)      
    for item in data:          
        old_card_list.append(item)
    number_of_old_item = len(old_card_list)
for item in result:        
    new_card_list.append(item)                
number_of_new_item = len(new_card_list)

# если появились новые бандлы, обновить информацию в json + записать информацию в json для новых бандлов
if (number_of_old_item == number_of_new_item):
    print('новых карт нет')  
else:
    print('вышли новые карты!') 

     # запись новых карт в отдельный json

    for new_item in new_card_list:
        if new_item not in old_card_list:   
            print('найдена новая карта!')
            print(new_item['card_name'])       

            new_card_item_list.append(new_item)
            with open(r"card_info_new.json", 'w', encoding='utf-8') as file:
                json.dump(new_card_item_list, file, ensure_ascii=False, indent=2)
            break_out_flag = True

        
           
    # обновить данные в главном json 
    with open(r"card.json", 'w', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False, indent=2)

driver.close()
driver.quit()                
   
