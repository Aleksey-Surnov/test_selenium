import os, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
opts = Options()
opts.add_argument('user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; rv:25.0) Gecko/20100101 Firefox/25.0')
#Меняем агента. Chrome открывает вид страницы в котором сразу можно вводить логин (адрес электронной почты) и пароль.

class Gotoyamail():
    def __init__(self, file_chromedriver, url: str):
        self.driver = webdriver.Chrome(file_chromedriver, chrome_options=opts)
        self.driver.get(url=url)

    def auth_yandex_mail(self, mylogin='', mypassword=''):                          # Заходим в яндекс-почту.
        time.sleep(3)                                                               # Пауза для загрузки страницы.
        driver = self.driver
        user = driver.find_element(by=By.NAME, value='login').send_keys(mylogin)
        time.sleep(2)
        password = driver.find_element(by=By.NAME, value='passwd').send_keys(mypassword)
        account = driver.find_element(By.CSS_SELECTOR, value='body > table > tbody > tr.row.rows__row.rows__row_first > td > table > tbody > tr > td.col.headline__item.headline__bar > table > tbody > tr > td.col.headline__bar-item.headline__domik > div > div.domik2__dropdown-wrapper.domik2__dropdown-wrapper_clickable_yes > div > div > div > form > div > table > tbody > tr > td.domik2__submit > button')
        time.sleep(3)
        account.click()

    def search_address(self, address=''):                                           # Считаем сколько пришло писем от отправителя.
        time.sleep(2)
        try:
            find_enter = self.driver.find_elements(By.LINK_TEXT, value=address)
            return len(find_enter)
        except NoSuchElementException:
            return 0

    def get_address(self, address=''):                                              # Получаем адрес почты.
        try:
            find_enter = self.driver.find_element(By.LINK_TEXT, value=address).click()
            time.sleep(2.1)                                                         # Пауза для загрузки страницы.
            find_address = self.driver.find_element(By.XPATH, value='/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/span/a').text
            return find_address
        except NoSuchElementException:
            return ''

    def click_mail(self, value='Входящие'):                                         # Заходим в папку почты.
        time.sleep(2)
        outer_mail = self.driver.find_element(By.LINK_TEXT, value=value).click()

    def send_message(self, count_response='', address='', tema='Тестовое задание'): # Отправляем письмо.
        time.sleep(1.8)
        go_button = self.driver.find_element(By.LINK_TEXT, value='Написать').click()
        time.sleep(3.1)
        input_address = self.driver.find_element(By.NAME, value='to').send_keys(address)
        time.sleep(0.7)
        input_tema = self.driver.find_element(By.NAME, value='subj').send_keys(tema)
        time.sleep(1.4)
        input_text = self.driver.find_element(By.NAME, value='send').send_keys(count_response)
        time.sleep(2.3)
        self.driver.find_element(By.NAME, value='doit').click()

    def go_next(self):                                                              # Пролистываем страницы.
        time.sleep(2)
        try:                                                                        # На случай если очень много писем и отправитель находится в конце.
            if self.driver.find_element(By.XPATH, value='/html/body/div[1]/div[2]/div[2]/form/div[4]/span[2]/span[2]/a/span/i').text == '→':
                self.driver.find_element(By.XPATH,
                                         value='/html/body/div[1]/div[2]/div[2]/form/div[4]/span[2]/span[2]/a/span/i').click()
            else:
                return False
        except NoSuchElementException:                                              # Все на одной странице. Обрабатываем исключение: "элемент пагинации не найден".
            return False
        return True


