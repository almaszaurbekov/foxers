from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import csv

def parserFlowers(lastPage,
                  url='https://rus-buket.ru/catalog?page={}',
                  pages=True,
                  file='file',
                  category=None):
    links = []
    mini_descriptions = []
    images = []
    info = []

    if(pages):
        for i in range(1, lastPage):
            page_link = url.format(i)
            response = requests.get(page_link, headers={'User-Agent': UserAgent().chrome})
            html = response.content
            soup = BeautifulSoup(html, 'html.parser')

            # find all mini descriptions
            obj = soup.findAll('div', attrs={'class': 'catalog-consist-inner'})
            for desc in obj:
                mini_descriptions.append(desc.text)

            # find all links
            obj = soup.findAll('a', attrs={'class': 'catalog-img-link'})
            for link in obj:
                links.append(link['href'])

            # find all images
            obj = soup.findAll('a', attrs={'class': 'catalog-img-link'})
            for image in obj:
                images.append("https://rus-buket.ru"+image.img['data-src'])
    else:
        page_link = url
        response = requests.get(page_link, headers={'User-Agent': UserAgent().chrome})
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')

        # find all mini descriptions
        obj = soup.findAll('div', attrs={'class': 'catalog-consist-inner'})
        for desc in obj:
            mini_descriptions.append(desc.text)

        # find all links
        obj = soup.findAll('a', attrs={'class': 'catalog-img-link'})
        for link in obj:
            links.append(link['href'])

        # find all images
        obj = soup.findAll('a', attrs={'class': 'catalog-img-link'})
        for image in obj:
            images.append("https://rus-buket.ru" + image.img['data-src'])

    index = 0
    for page in links:
        page_link = page
        response = requests.get(page_link, headers={'User-Agent': UserAgent().chrome})
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')

        # find name of object
        obj = soup.find('div', attrs={'class': 'item'})
        name = obj.h1.text

        # find price of object
        obj = soup.find('div', attrs={'class':'total_in_product'})
        price = int(obj.span.text.replace(' ',''))

        # find full description of object
        obj = soup.find('div', attrs={'class':'acc-content', 'itemprop':'description'})
        full_descprition = obj.text

        obj = soup.find('div', attrs={'class' : 'product-guarantee'})
        obj = obj.find('div', attrs={'class' : 'product-guarantee-img'})
        img = obj.find('img', attrs={'class' : 'img-responsive'})
        print(img['src'])


        if(category==None):
            info.append({"Изображения":images[index],
                         "Имя":name,
                         "Базовая цена":price*5.5,
                         "Описание":full_descprition,
                         "Короткое описание":mini_descriptions[index],
                         "Категории":"Цветы, Букет"})
        else:
            info.append({"Изображения": images[index],
                         "Имя": name,
                         "Базовая цена": price * 5.5,
                         "Описание": full_descprition,
                         "Короткое описание": mini_descriptions[index],
                         "Категории": "Цветы, Букет, {}".format(category)})
        index+=1

    fieldnames = ['Изображения', 'Имя', 'Базовая цена', 'Описание', 'Короткое описание', 'Категории']
    with open(file+'.csv', 'w', newline='', encoding='utf-8') as csvfile:
        spamwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        spamwriter.writeheader()
        for val in info:
            spamwriter.writerow(val)
def parserGifts():

    links = []
    mini_descriptions = []
    images = []
    info = []

    page_link = 'https://rus-buket.ru/gifts'
    response = requests.get(page_link, headers={'User-Agent': UserAgent().chrome})
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')

    # find all mini descriptions
    obj = soup.findAll('div', attrs={'class': 'catalog-consist-inner'})
    for desc in obj:
        mini_descriptions.append(desc.text)

    # find all links
    obj = soup.findAll('a', attrs={'class': 'catalog-img-link'})
    for link in obj:
        links.append(link['href'])

    # find all images
    obj = soup.findAll('a', attrs={'class': 'catalog-img-link'})
    for image in obj:
        images.append("https://rus-buket.ru" + image.img['data-src'])

    index = 0
    for page in links:
        response = requests.get(page, headers={'User-Agent': UserAgent().chrome})
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')

        # find name of object
        obj = soup.find('div', attrs={'class': 'item'})
        name = obj.h1.text

        # find price of object
        obj = soup.find('div', attrs={'class': 'total_in_product'})
        price = int(obj.span.text.replace(' ', ''))

        # find full description of object
        obj = soup.find('div', attrs={'class': 'acc-content', 'itemprop': 'description'})
        full_descprition = obj.text


        info.append({"Изображения": images[index],
                     "Имя": name,
                     "Базовая цена": price * 5.5,
                     "Описание": full_descprition,
                     "Короткое описание": mini_descriptions[index],
                     "Категории":"Подарок"})
        index += 1

    fieldnames = ['Изображения', 'Имя', 'Базовая цена', 'Описание', 'Короткое описание', 'Категории']
    with open('gifts.csv', 'w', newline='', encoding='utf-8') as csvfile:
        spamwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        spamwriter.writeheader()
        for val in info:
            spamwriter.writerow(val)
def parserByCategory():

    dictOfCategory = {  'роза':['https://rus-buket.ru/catalog/rozy',6,[]],
                        'гортензии':['https://rus-buket.ru/catalog/gortenzii',1,[]],
                        'пионы':['https://rus-buket.ru/catalog/piony',1,[]],
                        'орхидеи':['https://rus-buket.ru/catalog/orhidei',1,[]],
                        'гвоздика':['https://rus-buket.ru/catalog/gvozdika',1,[]],
                        'тюльпаны':['https://rus-buket.ru/catalog/tyulpany',1,[]],
                        'ирисы':['https://rus-buket.ru/catalog/irisy',1,[]],
                        'лилии':['https://rus-buket.ru/catalog/liliy',1,[]],
                        'ромашки':['https://rus-buket.ru/catalog/romashki',1,[]],
                        'хризантемы':['https://rus-buket.ru/catalog/hrizantemy',1,[]],
                        'калии':['https://rus-buket.ru/catalog/kally',1,[]],
                        'альстромерии':['https://rus-buket.ru/catalog/alstromeriy',1,[]],
                        'герберы':['https://rus-buket.ru/catalog/gerbery',1,[]],
                        'подсолнухи':['https://rus-buket.ru/catalog/podsolnuhy',1,[]],
                        'лизиантусы':['https://rus-buket.ru/catalog/liziantusy',1,[]],
                        'экзотические':['https://rus-buket.ru/catalog/ekzoticheskie',2,[]]}
    keys = list(dictOfCategory.keys())
    for key in keys:
        # if count of pages less than 1
        if dictOfCategory[key][1] <= 1:

            names = []
            page_link = str(dictOfCategory[key][0])
            response = requests.get(page_link, headers={'User-Agent': UserAgent().chrome})
            html = response.content
            soup = BeautifulSoup(html, 'html.parser')

            # find all links
            obj = soup.findAll('div', attrs={'class': 'fn title_price'})
            for div in obj:
                names.append(div.a.text)

            for name in names:
                dictOfCategory[key][2].append(name)
        else:
            names = []
            for i in range(dictOfCategory[key][1]):
                if i == 0:
                    page_link = str(dictOfCategory[key][0])
                else:
                    page_link = dictOfCategory[key][0]+'?page={}'.format(i)
                response = requests.get(page_link, headers={'User-Agent': UserAgent().chrome})
                html = response.content
                soup = BeautifulSoup(html, 'html.parser')

                # find all links
                obj = soup.findAll('div', attrs={'class': 'fn title_price'})
                for div in obj:
                    names.append(div.a.text)

                for name in names:
                    dictOfCategory[key][2].append(name)

    for i in range(len(keys)):
        print(keys[i],dictOfCategory[keys[i]][2])

if __name__ == '__main__':
    parserFlowers(10)