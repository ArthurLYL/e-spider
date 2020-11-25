import requests
import os
from bs4 import BeautifulSoup
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36', 'Connection': 'close'}
proxies = {'http': 'http://127.0.0.1:25378', 'https': 'http://127.0.0.1:25378'}  # setting proxy
path = 'E:/comic/'  # saving path


def get_content(url):
    """
    standard handle using BeautifulSoup
    :param url: url
    :return: BeautifulSoup in lxml
    """
    site = requests.get(url, headers=headers, proxies=proxies)
    content = site.text
    soup = BeautifulSoup(content, 'lxml')
    return soup


def next_page(url):
    """
    check whether there is next page
    :param url:
    :return: next page exists => 1 else => 0
    """
    soup = get_content(url)
    if soup.find('Next Page') != -1:
        return 1
    else:
        return 0


def dic_url(url):
    """
    download all comics in research result
    :param url: url of research result
    :return:
    """
    soup = get_content(url)
    dic = soup.find_all(class_='b')
    order = 0
    for x in range(1, len(dic) - 1):
        # print(dic[order]['href'])
        print('The comic name is ' + dic[order].text + ', start downloading')
        print(dic[order]['href'])
        get_images(dic[order]['href'], dic[order].text)
        order += 1
    return


def image_download(url, page, name):
    """
    download a page of searched comic
    :param url:url of the picture page
    :param page:page number
    :param name:comic name
    :return:
    """
    soup = get_content(url)
    img_url = soup.find_all('img', id='sm')[0]['src']
    # print(img_url[0]['src'])
    response = requests.get(img_url, headers=headers, proxies=proxies)
    with open(path + name + '/' + str(page) + '.jpg', 'wb') as f:
        f.write(response.content)
        f.flush()


def get_images(url, name):
    """
    download one of comics
    :param url: url of a searched comic
    :param name: name of a comic
    :return:
    """
    if os.path.exists(path + name) is False:
        os.mkdir(path + name)
    soup = get_content(url)
    all_img = soup.find_all(rel='nofollow')
    i = 1
    cur_url = url
    page = 1
    for img in all_img:
        if os.path.exists(path + name + '/' + str(page) + '.jpg'):
            page += 1
            continue
        print('Saving file ' + name + str(page) + '.jpg')
        image_download(img['href'], page, name)
        page += 1
    while next_page(cur_url) != 0:
        cur_url = url + "%d"%i
        i += 1
        soup = get_content(cur_url)
        all_img = soup.find_all(rel='nofollow')
        # all_img += all_img_new
        for img in all_img:
            if os.path.exists(path + name + '/' + str(page) + '.jpg'):
                page += 1
                continue
            print('Saving file ' + name + str(page) + '.jpg')
            image_download(img['href'], page, name)
            page += 1
    # page = 1
    # for img in all_img:
    #     print('Saving file ' + name + str(page) + '.jpg')
    #     image_download(img['href'], page, name)
    #     page += 1


page_link = 'https://e-hentai.org/lofi/?f_search=shindol+chinese'  # search

if __name__ == '__main__':
    dic_url(page_link)
# example of a url of a comic 'https://e-hentai.org/lofi/g/531176/a5b2fa21f0/'
# example of the first page url of a comic "https://e-hentai.org/lofi/s/7f9e010977/531176-1"