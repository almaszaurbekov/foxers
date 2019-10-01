from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import csv
import json
from random import uniform
from time import sleep
from random import choice
import os
import glob
from itertools import islice

class Parser():
    def __init__(self):
        # Инициализация фейковых прокси серверов
        self.__proxies = self.__proxyInit()
        # Путь к папке с разделами
        self.pathLinks = os.path.abspath("bookcityLinks/")
        # Расширение файлов
        self.extension = 'csv'
        # A complete path of directory to be changed to new directory path.
        os.chdir(self.pathLinks)

    def AppGeneralRun(self):
        """ Главный запуск приложения """
        self.AppGetLinksRun()
        self.AppGetBooksRun()

    def AppGetLinksRun(self):
        """ Запуск парсера ссылок на книги """
        # Получаю все ссылки на разделы книг
        data = self.getJson()
        # Пробегаюсь по каждой ссылке и парсим у них ссылки на книги
        for key in list(data.keys()):
            section = f"{self.getUrl()}{data[key]['id']}"
            self.__getLinks(section, key)

    def AppGetBookRun(self, name):
        """
        Запуск парсера информации о книге
        :param name: запрашиваемый раздел для парсера (имя файла)
        """
        # Получаем запрашиваемый файл
        section = "".join([x for x in
            glob.glob('*.{}'.format(self.extension)) if x == name])
        fieldnames = self.__getFieldNames()
        # Проверяем существует ли она
        if not self.__isEmpty(section):
            print(section)
            # Пробегаемся по каждому файлу
            with open(section, encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                # Для того, чтобы начать итерацию с 1,
                # т.к. row[0] это fieldnames
                with open('../bookcityBooks/{}'.format(section), 'w', newline='', encoding='utf-8') as csvfile:
                    spamwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    spamwriter.writeheader()
                    for row in islice(csv_reader, 1, None):
                        if (self.__isInt(row[0]) and not self.__isEmpty(row[1])):
                            book = self.__getBook(row[1])
                            self.__printReport(book)
                            self.__writeBookToCsv(spamwriter, fieldnames, book)

    def AppGetBooksRun(self, sectionName=None, stoppedIndex=None):
        """ Запуск парсера информации о книгах """
        # Получаем весь список созданных файлов
        sections = glob.glob('*.{}'.format(self.extension))
        fieldnames = self.__getFieldNames()
        if(sectionName is not None and stoppedIndex is not None):
            self.__getBooksFromStoppedIndex(sections, fieldnames, sectionName, stoppedIndex)
        else:
            # Пробегаемся по каждому файлу
            for section in sections:
                print(section)
                with open(section, encoding='utf-8') as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    # Для того, чтобы начать итерацию с 1,
                    # т.к. row[0] это fieldnames
                    with open('../bookcityBooks/{}'.format(section), 'w', newline='', encoding='utf-8') as csvfile:
                        spamwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        spamwriter.writeheader()
                        for row in islice(csv_reader, 1, None):
                            if (self.__isInt(row[0]) and not self.__isEmpty(row[1])):
                                book = self.__getBook(row[1])
                                self.__printReport(book)
                                self.__writeBookToCsv(spamwriter, fieldnames, book)

    def __getBooksFromStoppedIndex(self, sections, fieldnames, sectionName, stoppedIndex):
        startSectionIndex = sections.index(f"{sectionName}.csv")
        startRowIndex = stoppedIndex - 1
        hasBeginEnd = False
        writeMode = 'a'
        for section in islice(sections, startSectionIndex, None):
            print(section)
            with open(section, encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                if (hasBeginEnd is True):
                    writeMode = 'w'
                    startRowIndex = 1
                with open('../bookcityBooks/{}'.format(section), writeMode, newline='', encoding='utf-8') as csvfile:
                    spamwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    for row in islice(csv_reader, startRowIndex, None):
                        if (self.__isInt(row[0]) and not self.__isEmpty(row[1])):
                            book = self.__getBook(row[1])
                            self.__printReport(book)
                            self.__writeBookToCsv(spamwriter, fieldnames, book)
                hasBeginEnd = True

    def __writeBookToCsv(self, spamwriter, fieldnames, book):
        spamwriter.writerow({
            fieldnames[0]: book['title'],
            fieldnames[1]: book['author'],
            fieldnames[2]: book['description'],
            fieldnames[3]: book['price'],
            fieldnames[4]: book['rating'],
            fieldnames[5]: book['publisher'],
            fieldnames[6]: book['publishYear'],
            fieldnames[7]: book['barCode'],
            fieldnames[8]: book['pageCount'],
            fieldnames[9]: book['cover'],
            fieldnames[10]: book['size'],
            fieldnames[11]: book['thickness'],
            fieldnames[12]: book['weight'],
            fieldnames[13]: book['image'],
        })

    # Оформление CSV файла
    def __getFieldNames(self):
        return ['Название',
                'Автор',
                'Описание',
                'Цена',
                'Рейтинг',
                'Издательство',
                'Год издания',
                'Штрих-код',
                'Количество страниц',
                'Переплет',
                'Размер',
                'Толщина',
                'Вес',
                'Картина']

    def __getLinks(self, url, genre):
        """
        Возвращает все полученные ссылки из этого раздела
        :param url: ссылка на раздел
        :param genre: название раздела
        :return: list of links
        """
        # Первая страница парсинга
        firstPage = 1
        # Последняя страница парсинга
        lastPage = self.__getLastPage(url) + 1
        # В каком виде записывать данные
        fieldNames = ["Страница", "Ссылка"]
        # Данные записываем в СSV файл с названием раздела
        with open('../bookcityLinks/{}.csv'.format(genre), 'w', newline='', encoding='utf-8') as csvfile:
            print(genre)
            # Записываем что означают эти два поля
            spamwriter = csv.DictWriter(csvfile, fieldnames=fieldNames)
            spamwriter.writeheader()
            # Парсим ссылки на каждую страницу
            for page in range(firstPage, lastPage):
                # Имитация человеческого просмотра
                sleep(uniform(3, 6))
                # Вывести на консоль что мы сейчас парсим
                print("--------------------")
                URL = f"{url}?pagenumber={page}"
                print(f"Parsing '{URL}'...")
                # Получить доступ к странице
                response = requests.get(url=URL,
                    headers=self.__getUserAgent(), proxies=self.__getProxy())
                html = response.content
                soup = BeautifulSoup(html, 'html.parser')
                # Получаем все ссылки
                links = self.__getPageLinks(soup)
                # Если страница существовала и в ней были ссылки,
                # тогда записываем данные в CSV фалй
                if(len(links) > 0):
                    for link in links:
                        print(f"{fieldNames[0]}:{page}")
                        print(f"{fieldNames[1]}:{link}")
                        spamwriter.writerow({
                            fieldNames[0] : page,
                            fieldNames[1] : link
                        })
                    print("Success")

    # Получить последнюю страницу раздела
    def __getLastPage(self, url):
        try:
            response = requests.get(url=url,
                headers=self.__getUserAgent(), proxies=self.__getProxy())
            html = response.content
            soup = BeautifulSoup(html, 'html.parser')
            li = soup.find('li', attrs={'class': 'last-page'}).find('a')['href']
            return int(li.split('=')[-1])
        except:
            return -1

    def __getBook(self, url):
        sleep(uniform(1, 3))
        print("--------------------")
        print(f"Parsing '{url}'...")

        response = requests.get(url=url,
            headers=self.__getUserAgent(), proxies=self.__getProxy())
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')

        title = self.__getTitle(soup)
        author = self.__getAuthor(soup)
        description = self.__getDescription(soup)
        price = self.__getPrice(soup)
        rating = self.__getRating(soup)
        image = self.__getImage(soup)
        obj = None
        try:
            obj = soup.find('div', attrs={'id': 'add-info-text'}) \
                .find('table').findAll('tr')
        except: pass
        publisher = self.__getPublisher(obj)
        publishYear = self.__getPublishYear(obj)
        barCode = self.__getBarCode(obj)
        pageCount = self.__getPageCount(obj)
        cover = self.__getBookCover(obj)
        size = self.__getBookSize(obj)
        thickness = self.__getBookThickness(obj)
        weight = self.__getBookWeight(obj)

        return {
            "title" : title, "author" : author, "description" : description, "price" : price, "rating" : rating,
            "publisher": publisher, "publishYear": publishYear, "barCode": barCode, "pageCount": pageCount,
            "cover": cover, "size": size, "thickness": thickness, "weight": weight, 'image' : image
        }

    def __getTitle(self, soup):
        obj = soup.find('h1', attrs={'class': 'no-mobile'})
        if(obj == None):
            return "Неизвестно"
        return obj.text.strip()

    def __getAuthor(self, soup):
        try:
            obj = soup.find('div', attrs={'class': 'authorCardPage'}).find('a')
            return obj.text
        except:
            return "Неизвестно"

    def __getPrice(self, soup):
        try:
            obj = soup.find('div', attrs={'class': 'product-price'}).find('span')
            return obj.text.strip()
        except:
            return "Неизвестно"

    def __getRating(self, soup):
        try:
            obj = soup.find('div', attrs={'class': 'ratingBc'}).find('span')
            return obj.text.strip()
        except:
            return "Неизвестно"

    def __getImage(self, soup):
        try:
            obj = soup.find('div', attrs={'class': 'picture'}).find('a')
            return obj['href']
        except:
            return "Неизвестно"

    # Получить описание книги
    def __getDescription(self, soup):
        obj = soup.find('div', attrs={'class': 'short-description'})
        if (obj == None):
            return "Неизвестно"
        return obj.text.strip()

    def __getPublisher(self, soup):
        try:
            obj = soup[0].findAll('td')[1].text
            return obj
        except:
            return "Неизвестно"

    def __getPublishYear(self, soup):
        try:
            obj = soup[1].findAll('td')[1].text
            return obj
        except:
            return "Неизвестно"

    def __getBarCode(self, soup):
        try:
            obj = soup[2].findAll('td')[1].text
            return obj
        except:
            return "Неизвестно"

    def __getPageCount(self, soup):
        try:
            obj = soup[3].findAll('td')[1].text
            return obj
        except:
            return "Неизвестно"

    def __getBookCover(self, soup):
        try:
            obj = soup[4].findAll('td')[1].text
            return obj
        except:
            return "Неизвестно"

    def __getBookSize(self, soup):
        try:
            obj = soup[5].findAll('td')[1].text
            return obj
        except:
            return "Неизвестно"

    def __getBookThickness(self, soup):
        try:
            obj = soup[6].findAll('td')[1].text
            return obj
        except:
            return "Неизвестно"

    def __getBookWeight(self, soup):
        try:
            obj = soup[7].findAll('td')[1].text
            return obj
        except:
            return "Неизвестно"

    # Проверить существует ли страница
    def __checkPage(self, soup, index):
        if(index == 0):
            obj = len(soup.findAll('div', attrs={'class': 'product-title'}))
            return obj > 0
        else:
            pass

    # Получить все ссылки на книги в текущей странице
    def __getPageLinks(self, soup):
        list = []
        obj = soup.findAll('div', attrs={'class': 'fdw-background'})
        if(obj != None):
            for div in obj:
                list.append(f"http://www.bookcity.kz{div.find('a')['href']}")
        return list

    # Получить главную ссылку на сайт
    def getUrl(self):
        return "http://www.bookcity.kz/"

    # Получить ссылки на разделы книг
    def getJson(self):
        with open('../config.json', encoding="utf8") as f:
            data = json.load(f)
        return data

    # Инициализировать прокси сервера
    def __proxyInit(self):
        proxies = []
        # Прокси файл, где хранятся IP адреса
        proxyFile = open("proxies.content.txt", "r")
        soup = BeautifulSoup(proxyFile.read(), 'html.parser')
        tr = soup.findAll('td', attrs={'class' : 'tdl'})
        for td in tr:
            proxies.append(td.text)
        proxyFile.close()
        return proxies

    # Получить один из проинициализированных прокси серверов
    def __getProxy(self):
        return {'http//': choice(self.__proxies)}

    # Получить фейковое пользовательское приложение
    def __getUserAgent(self):
        return {'User-Agent': UserAgent().chrome}

    def __isInt(self, value):
        """
        Проверяет можно ли конвертировать строку в число
        :param value: строка
        :return: true or false
        """
        try:
            int(value)
            return True
        except ValueError:
            return False

    # Проверка на пустое значение
    def __isEmpty(self, value):
        return value.strip() == ""

    # Напечатать в консоли результаты парсинга
    def __printReport(self, obj):
        for key in list(obj.keys()):
            print(f"{key}: {obj[key]}")