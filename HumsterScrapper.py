import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import pickle
import requests
from selenium.webdriver.common.by import By
from typing import List, Dict
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

options = webdriver.ChromeOptions()
options.add_extension('Violentmonkey.crx')
options.add_argument(r"--user-data-dir=User Data") #e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
options.add_argument(r'--profile-directory=Profile 2') #e.g. Profile 3
options.add_argument('--window-size=1920,1080')
options.add_argument('--remote-debugging-port=9222')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-web-security')
options.add_argument("--disable-gpu")  # Отключение GPU
options.add_argument("--disable-software-rasterizer")   
options.add_argument("--force-device-scale-factor=1") 
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_argument("--disable-web-security")
options.add_argument('--headless')

options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)

# driver = webdriver.Chrome(options=options)

driver = webdriver.Chrome(options=options)

# # включить расширение
# driver.get('https://github.com/mudachyo/Hamster-Kombat/raw/main/hamster-kombat.user.js')
# WebDriverWait(driver, 10).until(lambda d: d.execute_script('return document.readyState') == 'complete')
# driver.save_screenshot("screenshot.png")
# wait = WebDriverWait(driver, 10)
# aut = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[1]/div[2]/div[2]/button[1]")))
# aut.click()

url = 'https://github.com/mudachyo/Hamster-Kombat/raw/main/hamster-kombat.user.js'
response = requests.get(url)

with open('hamster-kombat.user.js', 'wb') as file:
    file.write(response.content)
with open('hamster-kombat.user.js', 'r', encoding='utf-8') as script:
    driver.execute_script(script.read())

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



# собрать ежедневную награду если есть
try:
    aut = driver.find_element(By.CLASS_NAME,"daily-reward-bottom-button").click()
    driver.implicitly_wait(5)

except:
    pass

# собрать доход
try:
    aut = driver.find_element(By.CSS_SELECTOR,"#__nuxt > div > div.bottom-sheet.open > div.bottom-sheet-inner > div.bottom-sheet-scroll > div > button").click()
    driver.implicitly_wait(5)
except:
    pass

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

# перейти на вкладку со специальными карточками 
aut = driver.find_element(By.XPATH,"/html/body/div[1]/div/main/div[2]/div[3]/div[1]/div[5]").click()
driver.implicitly_wait(5)    
aut = driver.find_element(By.CSS_SELECTOR,"#__nuxt > div > main > div.content.is-main.has-glow > div.tabs > div.tabs-inner > div.tabs-special > div:nth-child(2)").click()
driver.implicitly_wait(5) 

cards = driver.find_elements(By.CSS_SELECTOR,"div.tabs-special-inner > div.upgrade-list > div.upgrade-special")
for card in cards:
        card_name = card.find_element(By.CLASS_NAME,"upgrade-special-title").text
        try:
            hour_profit = card.find_element(By.CSS_SELECTOR,"div.upgrade-special-profit-price > div > div.price-value").text
        except: 
            hour_profit = 'бесценна'   

        try:
            hour_profit = card.find_element(By.CSS_SELECTOR,"div.upgrade-special-profit-price > div > div.price-value").text
        except: 
            hour_profit = 'бесценна'  

        card_upgrade_price = card.find_element(By.CSS_SELECTOR,".upgrade-special-bottom > .upgrade-special-detail").text  
        try:
            card_lvl = card.find_element(By.CSS_SELECTOR,".upgrade-special-bottom > .upgrade-special-level").text   
        except: '0 lvl'   
        if card_name!='':
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

# проверить и собрать большую карточку со специальным предложением
try:
    cards = driver.find_elements(By.CSS_SELECTOR,"#__nuxt > div > main > div.content.is-main.has-glow > div.tabs > div.tabs-inner > div:nth-child(3) > div > div.upgrade-sport.is-border > div.upgrade-sport-inner")
    for card in cards:
            card_name = card.find_element(By.CLASS_NAME,"upgrade-sport-title").text
            if card_name!='':
                print(card_name) 
            try:
                hour_profit = card.find_element(By.CSS_SELECTOR,"#__nuxt > div > main > div.content.is-main.has-glow > div.tabs > div.tabs-inner > div:nth-child(3) > div > div.upgrade-sport.is-border > div.upgrade-sport-inner > div.upgrade-sport-bottom > div:nth-child(3) > div > div.upgrade-sport-profit-price > div > div.price-value").text
            except: 
                hour_profit = 'бесценна'   

            try:
                hour_profit = card.find_element(By.CSS_SELECTOR,"#__nuxt > div > main > div.content.is-main.has-glow > div.tabs > div.tabs-inner > div:nth-child(3) > div > div.upgrade-sport.is-border > div.upgrade-sport-inner > div.upgrade-sport-bottom > div:nth-child(3) > div > div.upgrade-sport-profit-price > div > div.price-value").text
            except: 
                hour_profit = 'бесценна'  

            card_upgrade_price = card.find_element(By.CSS_SELECTOR,"#__nuxt > div > main > div.content.is-main.has-glow > div.tabs > div.tabs-inner > div:nth-child(3) > div > div.upgrade-sport.is-border > div.upgrade-sport-inner > div.upgrade-sport-bottom > div:nth-child(5) > div > div.price-value").text  
            try:
                card_lvl = card.find_element(By.CSS_SELECTOR,"#__nuxt > div > main > div.content.is-main.has-glow > div.tabs > div.tabs-inner > div:nth-child(3) > div > div.upgrade-sport.is-border > div.upgrade-sport-inner > div.upgrade-sport-bottom > div.upgrade-special-level.text-white40").text   
            except: '0 lvl'   

            try:  
                supercard_path = card.find_element(By.CSS_SELECTOR,"#__nuxt > div > main > div.content.is-main.has-glow > div.tabs > div.tabs-inner > div:nth-child(3) > div > div.upgrade-sport.is-border > picture > img")  
                supercard_src = supercard_path.get_attribute("src")                                            
                card_img_value = 'https://hamsterkombatgame.io/'+supercard_src
            except:
            
                # если вместо картинки svg
                card_img_value = "https://pic.rutubelist.ru/video/2d/ed/2dedaea8149558b798972c66bc1eda9b.jpg"   

            # https://hamsterkombatgame.io/images/upgrade/adv/bg_1509.jpg



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
except:
    pass

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
   
