import requests
from bs4 import BeautifulSoup
from random import choice
from fake_useragent import UserAgent
import csv
import lxml
from lxml.etree import fromstring
from random import uniform
from urllib.request import urlopen
from time import sleep

def get_html(url, useragent=None, proxy=None):
    r = requests.get(url, headers=useragent, proxies=proxy)
    return r.text

def get_information(html):
    soup = BeautifulSoup(html, 'lxml')
    # print(soup)


    # FINDING INFORMATION

        # URL-PICTURE

    try:
        obj = soup.find('img', attrs={'id' : 'imgBlkFront'})
        img = obj['data-a-dynamic-image'].split('"')[1]
    except:
        img = None
    print("IMG: ", img)

        # TITLE
    try:
        obj = soup.find('span', attrs={'id' : 'productTitle'})
        title = str(obj.text)
    except:
        title = None
    print("TITLE: ", title)

        # AUTHOR
    try:
        obj = soup.find('a', attrs={'class' : 'contributorNameID'})
        temp = str(obj)
        t = temp.split('>')
        author = t[len(t) - 2].split('<')[0]
    except:
        author = None
    print("AUTHOR: ", author)

        # CONTENT
    try:
        content = soup.find('div', attrs={'class': 'content'})
        ul = content.find('ul')
        li = ul.findAll('li')
    except:
        pass

        # COUNT OF PAGES
    try:
        HardcoverSpiral = li[0].text
    except:
        HardcoverSpiral = None
    print(HardcoverSpiral)

        # PUBLISHED

    try:
        Publisher = li[1].text
    except:
        Publisher = None
    print(Publisher)

        # LANGUAGE

    try:
        Language = li[2].text
    except:
        Language = None
    print(Language)

        # BOOK'S CODE

    try:
        ISBN_10 = li[3].text
    except:
        ISBN_10 = None
    print(ISBN_10)

        # DESCRIPTION

    # obj = soup.findAll('div', attrs={'id' : 'bookDesc_iframe_wrapper'})
    # print(obj)
    #
    # iframexx = soup.find('iframe', attrs={'id' : 'bookDesc_iframe'})
    # print(iframexx)

    informations = {"Изображение" : img,
                    'Название' : title,
                    'Автор' : author,
                    'Количество страниц' : HardcoverSpiral,
                    'Издательство' : Publisher,
                    'Язык' : Language,
                    'ISBN-10' : ISBN_10}

    return informations




def main():
    # FROM 3 TO 75

    # FILTER LIST FROM GARBAGES
    f = open("links.txt", mode="r")
    links = f.read().splitlines()
    for i in range(len(links)):
        if (links[i][1] == "s" and links[i][2] == "?" and links[i][3] == "i"):
            links[i] = "garbage"

    links = [x for x in links if x != 'garbage']
    data = []
    n = 0

    for link in links:

        # BAN PROTECTION
        sleep(uniform(3,6))
        url = 'https://www.amazon.com' + link
        print("PAGE: ", url)
        print("N: ", n)
        n+=1


        # KEYS
        useragent = {'User-Agent' : 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36 Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10'}
        proxy = {'http//' : '93.156.177.91:53281'}

        # EXCEPTION
        try:
            html = get_html(url, useragent, proxy)
        except:
            return

        # TO CHECK WHICH PROXY AND USERAGENT IS WORKING
        print("--------------------------")
        print("PROXY: ", proxy)
        print("USERAGENT: ", useragent)
        print("--------------------------")


        data.append(get_information(html))

        # WRITING TO CSV FILE

        file = "books"
        fieldnames = ['Изображение',
                      'Название',
                      'Автор',
                      'Количество страниц',
                      'Издательство',
                      'Язык',
                      'ISBN-10'
                      ]

        with open(file + '.csv', 'w', newline='', encoding='utf-8') as csvfile:
            spamwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            spamwriter.writeheader()
            for val in data:
                spamwriter.writerow(val)




if __name__ == '__main__':
    main()