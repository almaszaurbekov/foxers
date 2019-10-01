import requests
from bs4 import BeautifulSoup
from random import choice
from fake_useragent import UserAgent
import time
import csv
from selenium import webdriver

def main():
    # parse(True)
    test()

def parse(areLinksParsed=False):
    if not areLinksParsed:
        file = open("links.txt", "a")
        links = []
        start = 1
        pages = 17
        for page in range(start, pages+1):
            url = f"https://www.rmj.ru/archive/?PAGEN_1={page}"
            print(f"parsing...{url} :", end=" ")
            response = requests.get(url=url,
                headers=getUserAgent(), proxies=getProxy())
            html = response.content
            soup = BeautifulSoup(html, 'html.parser')
            for link in get_links(soup):
                file.write(link + "\n")
                print("Success!")
                file.close()
    # test()
    files = open("links.txt", "r")
    with open('data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        spamwriter = csv.DictWriter(csvfile, fieldnames=["Title", "PDF"])
        spamwriter.writeheader()
        for url in files.readlines():
            print(f"parsing...{url} :", end=" ")
            try:
                data = get_data(url)
                spamwriter.writerow({
                    "Title" : data["title"],
                    "PDF" : data["pdf"]
                })
                print("Success!", end=" ")
            except Exception as e:
                print("Failed!")
                print(f"Exception: {e}")
            break

def getProxy():
    proxies = []
    proxyFile = open("proxies.content.txt", "r")
    soup = BeautifulSoup(proxyFile.read(), 'html.parser')
    tr = soup.findAll('td', attrs={'class': 'tdl'})
    for td in tr:
        proxies.append(td.text)
        proxyFile.close()
    return {'http//': choice(proxies)}

def getUserAgent():
    return { 'User-Agent': UserAgent().chrome }

def get_links(html):
    links = []
    try:
        blocks = html.findAll('div', attrs={'class': 'block'})
        for block in blocks:
            images = block.findAll('div', attrs={'class': 'image'})
            for img in images:
                links.append("https://www.rmj.ru" + img.find('a')["href"])
    except:
        print("Error")
    return links

def get_data(url):
    response = requests.get(url=url,
    headers=getUserAgent(), proxies=getProxy())
    html = BeautifulSoup(response.content, 'html.parser')
    title = html.find('h1').text
    pdf = html.find('a', attrs={ 'class' : 'icon_pdf'})["href"]

    return {
    "title" : title,
    "pdf" : "https://www.rmj.ru" + pdf
    }

def test():
    driver = webdriver.Chrome()
    driver.get("https://www.youtube.com/results?search_query=selenium+python")
    time.sleep(12)
    driver.close()


if __name__ == "__main__":
    main()