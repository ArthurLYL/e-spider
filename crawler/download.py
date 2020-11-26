import requests
import os
from bs4 import BeautifulSoup
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}


def save_file(url, path):
    response = requests.get(url, headers=headers)
    with open(path, 'wb') as f:
        f.write(response.content)
        f.flush()


def get_pic_url(url):
    site = requests.get(url, headers=headers)
    content = site.text
    soup = BeautifulSoup(content, 'lxml')
    imgs = soup.find_all(id='img')
    for img in imgs:
        pic_src = img['src']
        return pic_src


def get_website(url):
    site = requests.get(url, headers=headers)
    content = site.text
    soup = BeautifulSoup(content, 'lxml')
    divs = soup.find_all(class_='gdtm')
    title = soup.h1.get_text()
    page = 0
    i = 0
    for div in divs:
        pic_url = div.a.get('href')
        page += 1
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