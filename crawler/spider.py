import requests
import os
from bs4 import BeautifulSoup
import re
import math
import time
import random

headers = [{
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'Connection': 'Keep-Alive'}, {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36 Edg/87.0.664.41',
    'Connection': 'Keep-Alive'}]
proxies = {'http': 'http://127.0.0.1:25378', 'https': 'http://127.0.0.1:25378'}  # setting proxy
path = 'E:/comic/'  # saving path
max_try = 3  # maximum number of trying to download a page of the comic
rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |' filter invalid symbols in comic name
host = 'https://e-hentai.org/?page='  # search


def get_content(url):
    """
    standard handle using BeautifulSoup
    :param url: url
    :return: BeautifulSoup in lxml
    """
    site = requests.get(url, headers=headers[random.randint(0, 1)], proxies=proxies)
    time.sleep(random.randint(1, 10))
    content = site.text
    soup = BeautifulSoup(content, 'lxml')
    return soup


def turned_exist(url):
    """
    check whether turned page exists
    :param url:
    :return: this page exists => 1 else => 0
    """
    # not used
    soup = get_content(url)
    soup.find_all(class_='itg gltc')
    if soup.find_all(class_='itg gltc')[0].td.text != 'No unfiltered results in this page range. You either requested an invalid page or used too aggressive filters.':
        return 1
    else:
        return 0


def search_exist(url):
    """
    check whether search content is valid
    :param url:
    :return: 1 => valid, 0=> invalid
    """
    soup = get_content(url)
    if soup.find('p', style='text-align:center; font-style:italic; margin-bottom:10px') is None:
        return 1
    else:
        return 0


def dic_url(link, search):
    """
    download all comics in research result
    :param link:
    :param search: search content
    :return:
    """
    url = link + str(0) + search
    if search_exist(url):
        soup = get_content(url)
        text = soup.find_all('p', class_='ip')[0].text
        pattern = re.compile('[0-9]+')
        # Using regular expression to fetch the number of comic books
        urls = re.search(pattern, text).group()
        print('There are ' + str(urls) + ' comic books in all')
        url_number = math.ceil(math.ceil(int(urls) / 25))
        for i in range(0, url_number):
            cur_url = link + str(i) + search
            soup = get_content(cur_url)
            links = soup.find_all('td', class_='gl3c glname')
            for dic in links:
                print('*' * 3 + 'Start downloading ' + dic.div.text + '*' * 3)
                print('Gallery URL: ' + dic.a.get('href'))
                get_gallery(dic.a.get('href'), dic.div.text)
                print('*' * 50 + 'complete' + '*' * 50)
    else:
        print('Search error!')
    print('Done')


def image_download(url, page, name):
    """
    download a page of searched comic
    :param url:url of the picture page
    :param page:page number
    :param name:comic name
    :return:
    """
    soup = get_content(url)
    img_url = soup.find('img', id='img')['src']
    # print(img_url[0]['src'])
    for i in range(1, max_try + 1):
        try:
            response = requests.get(img_url, headers=headers[random.randint(0, 1)], proxies=proxies, timeout=61)
            time.sleep(random.randint(1, 10))
        except Exception as e:
            print(str(i) + ' time download try failed')
            if max_try == i:
                print(e)
                print('Failed URL: ' + img_url)
                raise e
        else:
            print(str(i) + ' time download try succeed')
            with open(path + name + '/' + str(page) + '.jpg', 'wb') as f:
                f.write(response.content)
                f.flush()
            return


def get_gallery(url, name):
    """
    download one of searched comics
    :param url: url of a searched comic
    :param name: name of a comic
    :return:
    """
    name = re.sub(rstr, '', name)
    if os.path.exists(path + name) is False:
        os.mkdir(path + name)
    soup_g = get_content(url)
    text = soup_g.find('p', class_='gpc').text
    pattern = re.compile('[0-9]+')
    urls = re.findall(pattern, text)
    url_number = math.ceil(math.ceil(int(urls[2]) / int(urls[1])))
    page = 1
    fail = 0
    for _url in range(0, url_number):
        cur_url = url + '?p=' + str(_url)
        soup = get_content(cur_url)
        all_imgs = soup.find_all(class_='gdtm')  # all sheet urls of a comic
        for img in all_imgs:
            if os.path.exists(path + name + '/' + str(page) + '.jpg'):
                page += 1
                continue
            print('Saving file ' + name + str(page) + '.jpg')
            try:
                image_download(img.a.get('href'), page, name)
            except:
                print('The ' + str(page) + ' page of ' + name + '.jpg download failed')
                fail += 1
            page += 1
    print('download complete, ' + str(fail) + ' pages download fail overall')


search_content = '&f_search=shindol+chinese'

if __name__ == '__main__':
    dic_url(host, search_content)
