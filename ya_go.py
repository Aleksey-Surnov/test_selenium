import os, json
from Yamailenter import yandexmail


def init_conf():
    with open(os.path.abspath('config/config.json'), encoding='UTF-8') as f:
        return json.load(f)


def get_message_count(bot, count_response=0, go=True):
    count_response = bot.search_address(address=config["FROM_HUMAN"])
    go = bot.go_next()
    while go == True:
        count_response = count_response + bot.search_address(address=config["FROM_HUMAN"])
        go = bot.go_next()
    return count_response


def get_email(bot, go=True):
    count_response = bot.search_address(address=config["FROM_HUMAN"])
    if count_response != 0:
        email = bot.get_address(address=config["FROM_HUMAN"])
        return email
    go = bot.go_next()
    while go == True:
        email = bot.get_address(address=config["FROM_HUMAN"])
        if email != '': return email
        go = bot.go_next()
        return email


if __name__=='__main__':

    try:
        file_chromedriver = os.path.abspath('./chromedrivermodul/chromedriver')
        config = init_conf()["DEFAULT"]
        bot = yandexmail.Gotoyamail(file_chromedriver, url=config["URL"])

        # Авторизация.
        bot.auth_yandex_mail(mylogin=config["MYLOGIN"], mypassword=config["MYPASSWORD"])

        # Сначала проверяем все страницы в папке "Входящие". Если нет проверяем папку "Спам".
        for element in ['Входящие', 'Спам']:
            bot.click_mail(value=element)
            email = get_email(bot)
            if email != '':
                bot.click_mail(value=element)
                count_response = get_message_count(bot)
                break
            else:
                continue

        if email == '':
            print('Письма от ' + config["FROM_HUMAN"] + ' не отправлялись')
        else:
            bot.send_message(count_response=count_response, address=email,
                             tema='Тестовое задание Сурнов')

    except FileNotFoundError:
        print('Отсутствуют необходимые файлы: Проверьте наличие файла "config.json" или "chromedriver.exe"')
        print('"config.json" должен быть в папке config')
        print('"chromedriver.exe" должен быть в папке chromedrivermodul')








