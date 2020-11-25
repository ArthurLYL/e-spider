import requests
import os
from bs4 import BeautifulSoup
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}  # http请求头


def save_file(url, path):
    response = requests.get(url, headers=headers)
    with open(path, 'wb') as f:
        f.write(response.content)
        f.flush()


def get_pic_url(url):
    # 识别页面图片url
    site = requests.get(url, headers=headers)
    content = site.text
    soup = BeautifulSoup(content, 'lxml')
    # 获得页面
    imgs = soup.find_all(id='img')
    # 查找'img'标签
    for img in imgs:
        # 遍历标签找到src的值
        pic_src = img['src']
        return pic_src


def get_website(url):
    site = requests.get(url, headers=headers)
    content = site.text
    # 保存页面
    soup = BeautifulSoup(content, 'lxml')
    divs = soup.find_all(class_='gdtm')
    # 找出class为‘gdtm'的标签
    title = soup.h1.get_text()
    # 在<h1>标题中获取值
    page = 0
    i = 0
    for div in divs:
        pic_url = div.a.get('href')
        # 在<a>和</a>之间找到'href'的值，即图片真实链接
        page += 1
        # 计算总页数
        print('Saving file ' + title + str(page) + '.jpg')
        try:
            save_file(get_pic_url(pic_url), 'E:/comic/' + title + '/' + title + str(page) + '.jpg')
        except:
            print('Cannot download ' + title + str(page) + '.jpg')
        else:
            print('Succeed')
            i += 1
    print('Finished downloading '+str(page)+' files,'+str(i)+' of them are successful')
    menu()


def menu():
    url = input('Please enter the url\n')
    if url.find('https://e-hentai.org/g/') != -1:
        print('--OK,getting information--')
        try:
            site = requests.get(url, headers=headers)
            content = site.text
            soup = BeautifulSoup(content, 'lxml')
            divs = soup.find_all(class_='gdtm')
            title = str(soup.h1.get_text())
            # 获取标题和页面
            page = 0
            for div in divs:
                page = page + 1
        except:
            print('Wrong!Please try again!!!')
            menu()
        else:
            print('The comic name is ' + title + ',it has ' + str(page) + ' page,start downloading!!!')
            if os.path.exists('E:/comic/' + title):
                get_website(url)
            else:
                os.mkdir('E:/comic/' + title)
                get_website(url)
    else:
        print('Oh,it is not an e-hentai comic url,please enter again\n')
        menu()
menu()