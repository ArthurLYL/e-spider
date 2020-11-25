# E-spider

## Environment

IDE: PyCharm

Python: 3.7.4

requests: 2.23.0

os

BeautifulSoup4: 4.9.1

## About running

`download.py`: Download comic using given URL (eg. https://e-hentai.org/g/xxxxxx/xxxxxx/). The function is not complete, and I will not update it in the future. 

`spider.py`: It can search comics according to user's will, and it will download all searched comics.  Using https://e-hentai.org/lofi, because it  is easier to design crawler code and find elements in html/xml basing on 'lofi'.

## TODO list

1. Catch exception (solving SSLEroor)
2. Request timeout processing(timeout threshold and maximum number of re-requests)
3. Augmenting robustness
4. Using IPProxyPool to cope with IP detection

