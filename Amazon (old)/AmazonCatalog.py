import requests
from bs4 import BeautifulSoup
from random import choice
from fake_useragent import UserAgent
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
from random import uniform
from time import sleep

def get_html(url, useragent=None, proxy=None):
    r = requests.get(url, headers=useragent, proxies=proxy)
    return r.text

def get_links(html):
    soup = BeautifulSoup(html, 'lxml')
    print(soup)

    # FINDING ALL LINKS

    # garbage = ['']
    links = soup.findAll('a', attrs={'class': 'a-link-normal a-text-normal'})
    links = [str(link.attrs['href']) for link in links]
    # links = [x for x in links if x not in garbage]

    print("LINKS:")
    for val in links:
        print(val)

    # WRITING TO TXT FILE

    a = open("links.txt", mode="a")
    for val in links:
        a.write(val)
        a.write("\n")
    a.close()



def main():
    # FROM 3 TO 75
    for page in range(3,75):
        # BAN PROTECTION
        sleep(uniform(3,6))
        print("PAGE: ", page)
        url = 'https://www.amazon.com/s?rh=n%3A283155%2Cn%3A%211000%2Cn%3A5&page={}&qid=1552735508&ref=lp_5_pg_{}'.format(page,page)

        # PROXY SERVER

        proxies = []
        r = requests.get('https://www.ip-adress.com/proxy-list')
        soup = BeautifulSoup(r.content, 'html.parser')
        for tr in soup.findAll('tr'):
            td = tr.find('td')
            if td:
                proxies.append(td.text)



        for i in range(10):

        # BAN PROTECTION
            sleep(uniform(3,6))


            # KEYS
            useragent = {'User-Agent': UserAgent().chrome}
            # useragent = {'User-Agent' : 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36 Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10'}
            proxy = {'http//': choice(proxies)}
            # proxy = {'http//' : '93.156.177.91:53281'}

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


            get_links(html)



if __name__ == '__main__':
    main()