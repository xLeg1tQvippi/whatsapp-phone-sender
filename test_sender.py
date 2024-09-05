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

class Sender_Message:
    def __init__(self):
        self.chrome_options()
        self.mainInstruction()

    def chrome_options(self):
        self.chrome_options = Options()
        profile_path = r'C:\Users\User\AppData\Local\Google\Chrome\User Data'
        profile_directory = 'Default'  # Имя профиля
        self.chrome_options.add_argument('--headless')  # Включаем режим headless
        self.chrome_options.add_argument('--disable-gpu')  # Отключаем GPU
        self.chrome_options.add_argument('--no-sandbox')  # Не использовать песочницу
        self.chrome_options.add_argument('--disable-dev-shm-usage')  # Разрешить использование кеша
        self.chrome_options.add_argument('--window-size=1920,1080')  # Устанавливаем размер окна
        self.chrome_options.add_argument(f"user-data-dir={profile_path}")
        self.chrome_options.add_argument(f"profile-directory={profile_directory}")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)

    def mainInstruction(self):
        language_dictionary = {
            'Russian': ['russian', 'russian1', 'russian2'],
            'English': ['english', 'english1', 'english2'],
            'Turkish': ['turkish', 'turkish1', 'turkish2'],
            'Doitch': ['doitch', 'doitch1', 'doitch2']
        }
        self.numbers = ph_numbers.phone_numbers  # [['number', 'language']]
        for cn in self.numbers:  # ['number', 'language']
            try:
                for text_key in language_dictionary[cn[1]]:
                    text = getattr(txt, text_key, None)
                    if text is None:
                        print(f'Text for key "{text_key}" not found in text module.')
                        continue
                    encoding_text = quote(text)
                    url = self.url_creater(cn[0], encoding_text)  # number & text to send.
                    result = self.get_to_site(url, text)
                    if result == 0:
                        print('Error occurred, moving to next number.')
                        break
            except Exception as error:
                print(f'MainInstruction Error: {error}')
            
    def url_creater(self, number, url_text):
        try:
            url = f'https://web.whatsapp.com/send?phone={number}&text={url_text}'
        except Exception as e:
            print(f'URL creation error: {e}')
        else:
            return url

    def get_to_site(self, url, message_text):
        self.driver.get(url)
        try:
            wait = WebDriverWait(self.driver, 30)  # Увеличение времени ожидания
            # Проверка на наличие сообщения об ошибке
            error_message_xpath = '//div[contains(text(), "Номер телефона, отправленный по ссылке, недействительный")]'
            if self.check_element_exists(error_message_xpath):
                print(f'Error: Phone number invalid for URL')
                return 0

            # Дождитесь загрузки поля ввода сообщения
            message_box_xpath = '//div[@contenteditable="true"][@data-tab="10"]'
            wait.until(EC.visibility_of_element_located((By.XPATH, message_box_xpath)))
            message_box = self.driver.find_element(By.XPATH, message_box_xpath)
            message_box.click()
            message_box.send_keys(message_text)

            # Дождитесь загрузки и нажмите кнопку отправки сообщения
            send_button_xpath = '//span[@data-icon="send"]'
            wait.until(EC.element_to_be_clickable((By.XPATH, send_button_xpath)))
            send_button = self.driver.find_element(By.XPATH, send_button_xpath)
            send_button.click()
            print('Message sent successfully')
            return 1
        except TimeoutException as err:
            print('Timeout: Unable to locate the input field or send button.')
            return 0
        except NoSuchElementException as e:
            print(f'Element not found: {e}')
            return 0
        finally:
            if self.driver:
                time.sleep(3)  # Дайте время для завершения отправки, если нужно

    def check_element_exists(self, xpath):
        try:
            self.driver.find_element(By.XPATH, xpath)
            return True
        except NoSuchElementException:
            return False

if __name__ == '__main__':
    win = Sender_Message()
