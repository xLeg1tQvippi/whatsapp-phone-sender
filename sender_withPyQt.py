import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import ph_numbers
import time
import text as txt
from urllib.parse import quote
import sqlite3, copy, importlib, subprocess, os
import menu_PyQt
class Sender_Message():
    def __init__(self, num_amount):
        self.num_amount = num_amount
        self.chrome_options()
        send = self.mainInstruction()
        if send == 'complete':
            print('Отправка сообщений на номера завершена.')
    def chrome_options(self):
        try:
            print('Options Status:', end='')
            self.chrome_options = Options()
            profile_path = r'C:\Users\User\AppData\Local\Google\Chrome\User Data'
            profile_directory = 'Default'  # Имя профиля
            self.chrome_options.add_argument('--headless')
            self.chrome_options.add_argument('--disable-gpu')
            self.chrome_options.add_argument('--no-sandbox')
            self.chrome_options.add_argument(f"user-data-dir={profile_path}")
            self.chrome_options.add_argument(f"profile-directory={profile_directory}")
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)
            print('Complete')
        except Exception as error:
            print(error)

    def mainInstruction(self):
        language_dictionary = {
            'Russian': ['russian', 'russian1', 'russian2'],
            'English': ['english', 'english1', 'english2'],
            'Turkish': ['turkish', 'turkish1', 'turkish2'],
            'Doitch': ['doitch', 'doitch1', 'doitch2'],
            'Special': ['special', 'special1', 'special2']
        }
        self.numbers = ph_numbers.phone_numbers  # [['number', 'language']]
        for cn in self.numbers:  # ['number', 'language']
            print(f'Номеров осталось: {self.num_amount}')
            print('Отправка на номер:', cn[0])
            try:
                for text_key in language_dictionary[cn[1]]:
                    text = getattr(txt, text_key, None)
                    if text is None:
                        print(f'Text for key "{text_key}" not found in text module.')
                        continue
                    encoding_text = quote(text)
                    url = self.url_creater(cn[0], encoding_text)  # number & text to send.
                    send_message = self.get_to_site(url, text)
                    if send_message == 0:
                        print(f'У данного номера {cn[0]} нету WhatsApp аккаунта.')
                        self.delete_and_save()
                        break
            except Exception as error:
                print('error occured\n', error)
            else:
                if send_message != 0:
                    print('Сообщения успешно отправлены на номер.')
                    number = cn[0] #supposed to be a number.
                    save = self.save_to_db(number)
                    if save == True:
                        #Функция удаления номера по индексу из ph_numbers.py
                        status = self.delete_and_save()
                        if status == True:
                            print('Номер удален из активного списка')
                        if status == False:
                            print('Произошла ошибка при сохранении и удалении номера.')
                    if save != True:
                        print('error in saving number.')
            self.num_amount -= 1
        self.driver.quit()
        return 'complete'

    def url_creater(self, number, url_text):
        try:
            url = f'https://web.whatsapp.com/send?phone={number}&text={url_text}'
        except Exception as error:
            print(f'URL creation error: {error}')
        else:
            return url

    def get_to_site(self, url, message_text):
        self.driver.set_window_size(130, 800)
        self.driver.get(url)
        try:
            wait = WebDriverWait(self.driver, 20)
            # message_box_xpath = '//div[@contenteditable="true"][@data-tab="10"]'
            # wait.until(EC.element_to_be_clickable((By.XPATH, message_box_xpath)))
            send_button_tag = 'data-icon'
            send_button_class = "x1c4vz4f x2lah0s xdl72j9 xfect85 x1iy03kw x1lfpgzf"
            send_button_xpath = '//span[@data-icon="send"]'
            wait.until(EC.element_to_be_clickable((By.XPATH, send_button_xpath)))
        
        # Нажатие на кнопку отправки сообщения
            send_button = self.driver.find_element(By.XPATH, send_button_xpath)
            send_button.click()
        except TimeoutException as err:
            return 0
        finally:
                if self.driver:
                    time.sleep(1)
                    
    def save_to_db(self, number):
        try:
            # Открываем соединение с базой данных
            with sqlite3.connect('old_number.db') as con:
                cur = con.cursor()
                
                # Убедитесь, что таблица существует
                cur.execute('CREATE TABLE IF NOT EXISTS numbers (old TEXT)')
                
                # Вставляем номер в таблицу
                cur.execute('INSERT INTO numbers (old) VALUES (?)', (number,))
                
                # Сохраняем изменения
                con.commit()
                print('Номер сохранен в базу данных')
                return True

        except sqlite3.Error as e:
            print(f"Ошибка при работе с базой данных: {e}")
            return False
        
    def delete_and_save(self):
        try:
            # Получаем список номеров и создаем его глубокую копию
            numlist = ph_numbers.phone_numbers
            copy_list = copy.deepcopy(numlist)
            
            # Изменяем копию списка
            copy_list = copy_list[::-1]  # Инвертируем список
            copy_list.pop(-1)            # Удаляем последний элемент
            copy_list = copy_list[::-1]  # Восстанавливаем исходный порядок, за исключением удаленного элемента
            
            # Сохраняем измененный список в файл
            with open('ph_numbers.py', 'w') as file:
                file.write(f'phone_numbers = {copy_list}')
                print('file saved!')
            importlib.reload(ph_numbers)
            return True
        except Exception as e:
            print(f"Ошибка: {e}")
            return False
if __name__ == '__main__':
    win = Sender_Message(num_value=len(ph_numbers.phone_numbers))