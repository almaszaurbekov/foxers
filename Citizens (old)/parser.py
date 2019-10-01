from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import csv


def parse(start, end):
    fieldnames = ['ФИО', 'Телефон', 'Регион', 'Домашний адрес']
    with open('citizens.csv', 'w', newline='', encoding='utf-8') as csvfile:
        spamwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        spamwriter.writeheader()
        for i in range(start, end):
            url = 'http://spra.vkaru.net/peoples/7/727/{}/'.format(i)
            response = requests.get(url, headers={'User-Agent': UserAgent().chrome})
            html = response.content
            soup = BeautifulSoup(html, 'html.parser')
            # looking for necessary blocks
            obj = soup.find('div', attrs={'class': 'main-block1'})
            obj = obj.find('div', attrs={'class': 'row'})
            obj = obj.find('div', attrs={'class': 'col-xs-10'})
            obj = obj.findAll('div')

            name = obj[1].find('h4').text
            tel = obj[3].findAll('a')[0].text + '(' + obj[3].findAll('a')[1].text + ')' + obj[3].find('span').text
            region = obj[5].findAll('a')[0].text + ',' + obj[5].findAll('a')[1].text + ',' + obj[5].findAll('a')[2].text

            # Converting home address into something readable
            homeAddress = ''
            for j in range(len(obj[7].findAll())):
                if(j == len(obj[7].findAll())-1):
                    homeAddress += obj[7].findAll()[j].text
                else:
                    homeAddress += obj[7].findAll()[j].text + ', '

            # Writing a row into CSV File
            spamwriter.writerow({
                'ФИО' : name,
                'Телефон' : tel,
                'Регион' : region,
                'Домашний адрес' : homeAddress
            })
            print("Info about {} is hacked success. #{}".format(name, i))

if __name__ == '__main__':
    # startId = 2450751
    # endId =    12756444
    parse(2450751, 2450851)