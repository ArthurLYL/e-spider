import requests
import os
from bs4 import BeautifulSoup
import re
import math
import time
import random
from requests.adapters import HTTPAdapter
import gc
import datetime


# TODO: Using Redis to re-try unsuccessful download. Creating database to write down unsuccessful connections to
#  search/gallery/image at last. Using IPProxyPool to build proxy pool
headers = [{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/86.0.4240.198 Safari/537.36'},
           {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/87.0.4280.66 Safari/537.36 Edg/87.0.664.41'}]
proxies = {'http': 'http://127.0.0.1:25378', 'https': 'http://127.0.0.1:25378'}  # setting proxy
default_path = 'E:/comic/Mizuryu Kei/'  # saving path
max_try = 3  # maximum number of re-trying to download a page of the comic
r_str = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |' filter invalid symbols in comic name
host = 'https://e-hentai.org/?page='  # host
search_content = '&f_search='
default_search = search_content + 'Mizuryu Kei+chinese'


def get_content(url):
    """
    standard handle using BeautifulSoup
    :param url: url
    :return: Connection failed => False, succeed => soup
    """
    try:
        site = s.get(url, headers=headers[random.randint(0, 1)], proxies=proxies, timeout=21)
        time.sleep(random.randint(0, 3))
    except Exception as e:
        print(e)
        return False
    else:
        content = site.text
        soup = BeautifulSoup(content, 'lxml')
        return soup


def image_download(url, page, name, path):
    """
    download a page of searched comic
    :param url:url of the picture page
    :param page:page number
    :param name:comic name
    :param path:file path
    :return: False => Download fail
                True => Download succeed
    """
    soup = get_content(url)
    if soup is False:
        print('Connection to the ' + str(page) + 'nd failed')
        return False
    img_url = soup.find('img', id='img')['src']  # download url
    # print(img_url[0]['src'])
    try:
        response = s.get(img_url, headers=headers[random.randint(0, 1)], proxies=proxies, timeout=21)
        time.sleep(random.randint(0, 3))
    except Exception as e:
        print(e)
        print('JPG download failed')
        return False
    else:
        print('JPG download succeed')
        with open(path + name + '/' + str(page) + '.jpg', 'wb') as f:
            f.write(response.content)
            f.flush()
        return True
    # for i in range(1, max_try + 1):
    #     try:
    #         response = requests.get(img_url, headers=headers[random.randint(0, 1)], proxies=proxies, timeout=61)
    #         time.sleep(random.randint(1, 10))
    #     except Exception as e:
    #         print(str(i) + ' time download try failed')
    #         if max_try == i:
    #             print(e)
    #             print('Failed URL: ' + img_url)
    #             return False
    #     else:
    #         print(str(i) + ' time download try succeed')
    #         with open(path + name + '/' + str(page) + '.jpg', 'wb') as f:
    #             f.write(response.content)
    #             f.flush()
    #         return True


def get_gallery(url, name, path):
    """
    download one of searched comics
    :param url: url of a searched comic
    :param name: name of a comic
    :param path: file path
    :return:False => Connection to gallery fail
            True => gallery has been downloaded before
    """
    name = re.sub(r_str, '', name)
    if os.path.exists(path + name) is False:
        os.mkdir(path + name)
    soup_g = get_content(url)
    if soup_g is False:
        print('Connection to gallery failed')
        return False
    text = soup_g.find('p', class_='gpc').text
    pattern = re.compile('[0-9]+')
    urls = re.findall(pattern, text)
    url_number = math.ceil(math.ceil(int(urls[2]) / int(urls[1])))  # The page number of a gallery
    print('Number of pages: ' + urls[2])
    count = 0
    for root, dirs, files in os.walk(path + name):  # Counting the number of files
        for each in files:
            count += 1
    if count == int(urls[2]):
        # TODO: Use hashtable to record books that have been downloaded
        print('This book has been downloaded')
        return True
    page = 1
    fail = 0
    for _url in range(0, url_number):
        cur_url = url + '?p=' + str(_url)
        soup = get_content(cur_url)
        if soup is False:
            print('Connection to the' + str(_url) + 'nd page of gallery failed')
            continue
        all_imgs = soup.find_all(class_='gdtm')  # all sheet urls in a page of gallery
        for img in all_imgs:
            if os.path.exists(path + name + '/' + str(page) + '.jpg'):
                # Judge whether the file has been downloaded before
                page += 1
                continue
            print('Saving file ' + name + str(page) + '.jpg')
            if image_download(img.a.get('href'), page, name, path) is False:
                print('The ' + str(page) + 'nd page of ' + name + '.jpg download failed')
                fail += 1
            page += 1
    print('Download complete, ' + str(fail) + ' pages download fail in all')
    del each, root, dirs, files, page, fail, count
    gc.collect()


def dic_url(search, path):
    """
    download all comics in research result
    :param search: search content
    :param path: file path
    :return:
    """
    url = host + str(0) + search
    soup = get_content(url)
    if soup is False:
        print('Connection to web-site failed')
        return
    elif soup.find('p', style='text-align:center; font-style:italic; margin-bottom:10px') is not None:
        print('Search error')
        return
    else:
        text = soup.find_all('p', class_='ip')[0].text
        pattern = re.compile('[0-9]+')
        # Using regular expression to fetch the number of comics
        urls = re.search(pattern, text).group()  # the number of comics
        # print('There are ' + str(urls) + ' comic books in all')
        print('There are ' + str(math.ceil(math.ceil(int(urls) / 25))) + ' pages in all')
        dl_number = input('There are ' + str(urls) + ' comic books in all, input the number of books to download: ')
        dl_number = int(dl_number)
        url_number = min(math.ceil(math.ceil(dl_number / 25)), math.ceil(math.ceil(int(urls) / 25)))
        # the number of needed pages
        count = 1
        start_time = datetime.datetime.now()
        print('Start time: ' + str(start_time))
        for i in range(0, url_number):
            cur_url = host + str(i) + search  # url of each search web page
            soup = get_content(cur_url)
            if soup is False:
                print('Connection to ' + str(i + 1) + ' search page failed')
                continue
            links = soup.find_all('td', class_='gl3c glname')
            for dic in links[:min(dl_number, len(links))]:
                # handled each gallery
                title = dic.div.text
                print('*' * 5 + 'Start downloading the ' + str(count) + 'nd comic: ' + title + '*' * 5)
                print('Gallery URL: ' + dic.a.get('href'))
                if get_gallery(dic.a.get('href'), title, path) is False:
                    print('Connection to gallery' + title + ' failed')
                print('*' * 50 + 'complete' + '*' * 50)
                count += 1
            dl_number -= 25
        end_time = datetime.datetime.now()
        print('End time: ' + str(start_time-end_time))
        del dl_number, count
        gc.collect()


def menu():
    content = input('Input the keyword to search: ')
    content = search_content + content.replace(' ', '+')
    path = input('Input the file path to save comic(eg.E:/comic/Mizuryu Kei): ')
    if os.path.exists(path) is False:
        os.mkdir(path)
    path = path + '/'
    dic_url(content, path)
    print('Done')


if __name__ == '__main__':
    s = requests.Session()
    a = HTTPAdapter(max_retries=max_try)
    s.mount('http://', a)
    s.mount('https://', a)
    cookie_dict = {'cookie': 'nw=1'}
    s.cookies.update(cookie_dict)
    # s.keep_alive = False
    menu()
    s.close()
